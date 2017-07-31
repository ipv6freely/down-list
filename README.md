# DOWN-LIST

Does stuff.

# Usage

Grab Docker image from Docker Hub:
`docker pull ipv6freely/down-list`

Start up the container. The script expects `STATSEEKER_USERNAME` and `STATSEEKER_PASSWORD` to be in the environment variables. Pass these as either command line arguments using `--env STATSEEKER_USERNAME=username --env STATSEEKER_PASSWORD=password` or put the ENV variables into a file and use the `--env-file` option.

Example:
`docker run -d --env-file ~/.envfile --name=down-devices -p 80:80 -t ipv6freely/down-devices`
