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

### outbound_gatekeeper.py

Listens on STDIN for IPv4 packets. Once an IPv4 packet is recieved, a
new *NaCl protected* packet is created with *source* set by the file
`service_publickey.json` and *destination* set according to the rules
in `tx_ipmappings.json`. This *NaCl protected* packet is symmetrically
protected using the key defined in `tx_keymappings.json` for the given
*destination*. This *NaCl protected* packet is then sent over STDOUT.

### inbound_gatekeeper.py

Listens on STDIN for *NaCl protected* packets. Verifies the integrity
of the incoming *NaCl protected* packet. If it is accepted, based on
the keys provided in `rx_keymappings.json`, it is remapped to having a
*destination* IP address defined by the file `dst_ip.json` and the
source IP address is derived based on its *NaCl protected* source and
the rules in `rx_ipmappings.json`. This IPv4 packet is then sent out
over STDOUT.

### debugger_passthrough.py

Listens on STDIN for *NaCl protected* packets. For each packet, its
*source*, *destination*, *length*, and *cryptographic nonce* are printed
to STDERR. The *NaCl protected* packet is then passed along to STDOUT.

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

### test_unidirectional_pipe_debug.sh

Running this command will create a *tun0* interface with an IP address
of **192.168.3.10/24** and a *tun1* interface with an IP address of
**192.168.1.1/24**. IPv4 packets destined for **192.168.3.20** that are
passed into *tun0* will be piped into *tun1* and will appear as IPv4
packets sourced from **192.168.1.10** destined for **192.168.1.1**.

```bash
(Terminal 1) ./test_unidirectional_pipe_debug.sh
(Terminal 2) socat UDP-RECV:8700,bind=192.168.1.1 STDIO
(Terminal 3) socat UDP-SENDTO:192.168.3.20:8700 STDIO
```

Now, anything typed into *(Terminal 3)* will appear in *(Terminal 2)*.

### Pipeline_To_Docker

Connects a host interface, *tun0*, with the IP
address **192.168.4.1/24** to a running Docker container with an
internal IP address of **192.168.1.1**. Packets sent from the host side
to **192.168.4.16** will exit the internal Docker interface with a
destination of **192.168.1.1** and a source of **192.168.1.2**.

```bash
cd Pipeline_To_Docker/
./build.sh
docker run --rm --name gitlab -it gitlab/gitlab-ce

#...Get the id of the running gitlab container...

./connect_host_to_container.sh <GITLAB DOCKER CONTAINER ID>

#...now point your web browser to http://192.168.4.16/
```
