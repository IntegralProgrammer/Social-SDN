# Social SDN
Building a Software Defined Network (SDN) over social connections

## Dependencies

Install the following Python packages:

- PyNaCl
- Scapy3k
- u-msgpack-python

For using the graphical user interface (GUI), install the following Python packages:

- easygui
- pyperclip
- zenity

Install the *SocatAdapter3* Python module

```bash
git clone https://github.com/IntegralProgrammer/scapy-pipeline
cd scapy-pipeline
sudo make install3
```

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

### connect_executable_to_pipe.sh

Runs a program in a new network namespace and uses STDIN to create
inbound IPv4 traffic and outbound IPv4 traffic is sent over STDOUT.

```bash
#This example runs an instance of the Droopy quick file sharing server

mkfifo netpipe
cat netpipe | sudo socat -d -d STDIO TUN:192.168.1.1/24,up | unshare -n -r ./connect_executable_to_pipe.sh droopy 192.168.1.48/24 > netpipe
```

#### Connecting two VoIP devices together (unencrypted)

```bash
# (Assume this device has an IP of 10.115.210.1)
mkfifo netpipe
cat netpipe | nc -l -p 9500 -q 0 | unshare -n -r ./connect_executable_to_pipe.sh linphone 192.168.1.36/24 > netpipe
```

```bash
# (Assume this device has an IP of 10.115.210.2)
mkfifo netpipe
cat netpipe | nc 10.115.210.1 9500 -q 0 | unshare -n -r ./connect_executable_to_pipe.sh linphone 192.168.1.26/24 > netpipe
```

Now, the device with the IP address **10.115.210.1** can call the device
with the IP address **10.115.210.2** at **192.168.1.26**. The device
with the IP address **10.115.210.2** can call the device with the IP
address **10.115.210.1** at **192.168.1.36**.

#### Connecting two VoIP devices together (encrypted)

```bash
# (Assume this device has an IP of 10.115.210.1)
cd Linphone_Example/Machine_B
cp ../../connect_executable_to_pipe.sh .
cp ../../outbound_gatekeeper.py .
cp ../../inbound_gatekeeper.py .
cp ../../SocatAdapter3.py .
mkfifo netpipe
cat netpipe | nc -l -p 9500 -q 0 | python3 inbound_gatekeeper.py | unshare -n -r ./connect_executable_to_pipe.sh linphone 192.168.1.2/24 | python3 outbound_gatekeeper.py > netpipe
```

```bash
# (Assume this device has an IP of 10.115.210.2)
cd Linphone_Example/Machine_A
cp ../../connect_executable_to_pipe.sh .
cp ../../outbound_gatekeeper.py .
cp ../../inbound_gatekeeper.py .
cp ../../SocatAdapter3.py .
mkfifo netpipe
cat netpipe | nc 10.115.210.1 9500 -q 0 | python3 inbound_gatekeeper.py | unshare -n -r ./connect_executable_to_pipe.sh linphone 192.168.1.1/24 | python3 outbound_gatekeeper.py > netpipe
```

The device with the IP address **10.115.210.1** can make encrypted calls
to the device **10.115.210.2** at **192.168.1.1**. The device with the
IP address **10.115.210.2** can make encrypted calls to the device
**10.115.210.1** at **192.168.1.2**.

#### Connecting two VoIP devices together (encrypted, automated)

```bash
# (Assume this device has an IP of 10.20.112.30

# Install the framework onto this device
cd Setup
chmod +x install.sh
sudo ./install.sh

# Setup this device's identity
setup_socialsdn_identity.sh

# Create a working directory for this example
cd ~
mkdir tmp
cd tmp
initialize_socialsdn_directory.sh

# (Copy the file test_create_initiator.py from the repository into this directory)

# Configure this device as connection initiator
python3 test_create_initiator.py
Enter the transport mechanism name: netcat
Enter a value for (Hostname): 10.20.112.30
Enter a value for (TCP Port): 9005
Enter the remote peer ID: #Obtain this value by reading the file ~/.socialsdn/pubkey.hex on the 10.49.22.178 machine
Enter the IP address for this side: 192.168.1.1
Enter the IP address for the remote side: 192.168.1.2
Enter the app name: linphone

# (Now transfer the generated request link to 10.49.22.178)

#Start the pipeline
./run_pipeline.sh
```

```bash
# (Assume this device has an IP of 10.49.22.178

# Install the framework onto this device
cd Setup
chmod +x install.sh
sudo ./install.sh

# Setup this device's identity
setup_socialsdn_identity.sh

# Create a working directory for this example
cd ~
mkdir tmp
cd tmp
initialize_socialsdn_directory.sh

# (Copy the file test_create_connector.py from the repository into this directory)

# Respond to the request
python3 test_create_connector.py
Enter the request link: #Enter the value generated by 10.20.112.30
# (Accept the connection)

#Start the pipeline
./run_pipeline.sh
```

#### Traffic Tagging/Shaping

By default, running `initialize_socialsdn_directory.sh` will copy
`inbound_sidechannel_passthrough.py` as `inbound_sidechannel_shaper.py`
and `outbound_sidechannel_passthrough.py` as
`outbound_sidechannel_shaper.py`. This will cause network traffic to be
passed through without tagging or shaping.

For an example which tags each outbound packet with a 64 bit number
representing milliseconds since the Epoch and then prints to *STDERR*
the *average*, *minimum*, and *maximum* packet delays of the last *250*
IP packets, copy the file `inbound_sidechannel_timedebug.py` as
`inbound_sidechannel_shaper.py` and `outbound_sidechannel_timedebug.py`
as `outbound_sidechannel_shaper.py`.

#### Connecting two VoIP devices together (encrypted, automated, side-channel protected)

Copy the files `outbound_sidechannel_voipmodel.py` and
`inbound_sidechannel_voipmodel.py` as `outbound_sidechannel_shaper.py`
and `inbound_sidechannel_shaper.py`, respectively, into the working
directories on both machines. Then start both pipelines by following the
instructions given in the subsection **Connecting two VoIP devices
together (encrypted, automated)**.

### Time Synchronization

For network data transport that must satisfy real-time constraints, the
value (plus or minus three seconds) of the UNIX time on the remote host
must be known on the local host. To obtain the delta in UTC clock
readings between the local host and the remote host, run the following:

On the remote host, run `test_create_initiator.py` connecting to the
local host. Choose the value *192.168.1.1* for *IP address for this side*
and *192.168.1.2* for *IP address for the remote side*. The *app name*
should be *TIMESYNC*.

On the local host, run `test_create_connector.py` and accept the request
link from the remote host.

After starting the network pipelines on both sides, the local host will
record the time delta between its UNIX time and the remote host's UNIX
time under `~/.socialsdn/timediffs/<peer ID of remote host>.json`.
