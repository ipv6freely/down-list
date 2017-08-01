from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/")
def down():
    import requests
    import datetime
    import os
    from ipaddress import IPv4Address, IPv4Network
    from operator import itemgetter

    statseeker_username = os.getenv("STATSEEKER_USERNAME")
    statseeker_password = os.getenv("STATSEEKER_PASSWORD")
    statseeker_url = os.getenv("STATSEEKER_URL")

    requests.packages.urllib3.disable_warnings()

    headers = {'Accept':'application/json', 'Content-Type':'application/json'}
    down_events_url = statseeker_url + '/api/latest/event/?fields=device,description,status&status_formats=time,state&description_filter==\u0027ping_state\u0027&status_filter==\u0027down\u0027&status_filter_format=state&links=none&limit=0&indent=3'
    down_events = requests.get(down_events_url, headers=headers, auth=(statseeker_username, statseeker_password), verify=False).json()

    all_devices_url = statseeker_url + '/api/latest/cdt_device/?fields=name,.ipaddress,SNMPv2-MIB.sysDescr,SNMPv2-MIB.sysContact,SNMPv2-MIB.sysLocation,.ping_poll,.snmp_poll&.snmp_poll_filter=IS(\u0027on\u0027)&.ping_poll_filter=IS(\u0027on\u0027)&links=none&limit=0'
    all_devices = requests.get(all_devices_url, headers=headers, auth=(statseeker_username, statseeker_password), verify=False).json()

    include_net_list = [
                        '128.0.0.0/8', 
                        '161.0.0.0/8', 
                        '192.168.0.0/16', 
                        '172.16.0.0/12', 
                        '10.0.0.0/8'
                        ]

    exclude_net_list = [
                        '172.31.240.0/23',
                        '172.30.0.0/21'   
                        ]

    device_list = list(filter(lambda foo: 
                            any(IPv4Address(foo['.ipaddress']) in IPv4Network(x) for x in include_net_list)
                            and not any(IPv4Address(foo['.ipaddress']) in IPv4Network(x) for x in exclude_net_list)
                            , all_devices['data']['objects'][0]['data']))

    results = []
    for event in down_events['data']['objects'][0]['data']:
        tempdict = {}
        for device in device_list:
            if event['device'] == device['name']:
                tempdict['name'] = device['name']
                tempdict['ipaddress'] = device['.ipaddress']
                tempdict['location'] = device['SNMPv2-MIB.sysLocation']
                tempdict['contact'] = device['SNMPv2-MIB.sysContact']
                tempdict['status'] = event['status']['state']
                downtime = datetime.datetime.fromtimestamp(event['status']['time']).strftime('%Y-%m-%d %H:%M:%S')
                tempdict['downtime'] = downtime
                delta = datetime.datetime.now() - datetime.datetime.fromtimestamp(event['status']['time'])
                hours, seconds = divmod(delta.seconds, 3600)
                tempdict['elapsed'] = '%d days %d hours %d minutes\n' % (delta.days, hours, seconds/60)
                results.append(tempdict)

    results = sorted(results, key=itemgetter('downtime'), reverse=True)

    return render_template('down.html', title='Down Devices', downdevices=results)