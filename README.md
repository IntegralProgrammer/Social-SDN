# Social SDN
Building a Software Defined Network (SDN) over social connections

## Utilities

### connect_container_to_pipe.sh

Redirects STDIO to a network interface (eth1) within a Docker container.
This in-container network interface is assigned the IPv4
address **192.168.1.1/24**.

```bash
sudo connect_container_to_pipe.sh <DOCKER-CONTAINER-ID>
```

## Examples

### Connecting to a Dockerized HTTP Service Over Socat

- Start the container

```bash
docker run --rm --name gitlab -it gitlab/gitlab-ce
```

- Get its *Container ID*

```bash
docker ps | grep gitlab
```

- Connect a *Socat* relay to the container

```bash
mkfifo netpipe
cat netpipe | sudo ./connect_container_to_pipe.sh <DOCKER-CONTAINER-ID> | sudo socat -d -d STDIO TUN:192.168.1.2/24,up > netpipe
```

- Open the web browser to **http://192.168.1.1/** to access the Dockerized service.
