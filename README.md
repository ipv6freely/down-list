# DOWN-LIST

Grabs list of currently down devices from Statseeker

# Usage

Grab Docker image from Docker Hub:

```docker pull ipv6freely/down-list```

Start up the container. The script expects `STATSEEKER_USERNAME` and `STATSEEKER_PASSWORD` to be in the environment variables. Pass these as either command line arguments using `--env STATSEEKER_USERNAME=username --env STATSEEKER_PASSWORD=password` or put the ENV variables into a file and use the `--env-file` option.

Examples:

```
docker run -d --env-file ~/.envfile --name=down-list -p 80:80 -t ipv6freely/down-list
```
OR

```
docker run -d --env STATSEEKER_USERNAME=username --env STATSEEKER_PASSWORD=password --name=down-list -p 80:80 -t ipv6freely/down-list
```

# Docker Hub Repo
The Docker image can be found at my public repo:
https://hub.docker.com/r/ipv6freely/down-list/

# TODO
* Error handling++

# Credits
This application uses the `tiangolo/uwsgi-nginx-flask:flask-python3.5` Docker image created by Sebastian Ramirez. 
https://hub.docker.com/r/tiangolo/uwsgi-nginx-flask/