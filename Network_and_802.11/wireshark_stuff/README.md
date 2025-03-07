# Wireshark Guide


[Wireshark](https://www.wireshark.org/) is an open source **network packet analyzer** that allows live  traffic analysis, with support to several  protocols.

Wireshark also allows **network forensic**, being very useful for CTFs for example (check my writeups for the  [D-CTF Quals 2014](http://https://singularity-sh.vercel.app/exploring-d-ctf-quals-2014s-exploits.html) and for the CSAW Quals 2014 in [Networking](http://https://singularity-sh.vercel.app/csaw-ctf-2014-networking-100-big-data.html) and [Forensics](http://https://singularity-sh.vercel.app/csaw-ctf-2014-forensics-200-why-not-sftp.html)).



------------------------------------------------------
# The Network Architecture

Before we are able to understand and analyze network traffic packets, we must have an insight of how the network stack works.


## The OSI Model

The [Open Systems Interconnection](http://en.wikipedia.org/wiki/OSI_model) (OSI) model  was published in 1983 and is a conceptual model that characterizes and standardizes the internal functions of a communication system by partitioning it into abstraction layers.

![](http://i.imgur.com/dZyiOTX.png)

Protocols are separated according to their function and the hierarchy makes it easier to understand network communication:



### Layer 1: Physical Layer

Represents the physical and electrical medium through which the network data is transferred.

It comprehends all hardware, hubs, network adapters, cable, etc.

### Layer 2: Data Link Layer

Provides the means of *transporting data* across a physical network. Bridges and switches are the physical devices in this layer.

It is responsible for providing an addressing scheme that can be used to identify physical devices: the [MAC address](http://en.wikipedia.org/wiki/MAC_address).

Examples of protocols in this layer are: [Ethernet](http://en.wikipedia.org/wiki/Ethernet), [Token Ring](http://en.wikipedia.org/wiki/Token_ring), [AppleTalk](http://en.wikipedia.org/wiki/AppleTalk),  and [Fiber Distributed Data Interface](http://en.wikipedia.org/wiki/Fiber_Distributed_Data_Interface) (FDDI).

### Layer 3: Network Layer

Responsible for routing data between physical networks, assigning the *logical addressing* of network hosts. It also handles *packet fragmentation* and *error detection*.

Routers and its *routing tables* belong to this layer. Examples of protocols are: [Internet Protocol](http://en.wikipedia.org/wiki/Internet_Protocol) (IP), [Internetwork Packet Exchange](http://en.wikipedia.org/wiki/Internetwork_Packet_Exchange), and the [Internet Control Message Protocol](http://en.wikipedia.org/wiki/Internet_Control_Message_Protocol) (ICMP).


### Layer 4: Transport Layer

Provides the *flow control* of data between two hosts.  Many firewalls and proxy servers operate at this layer.

Examples of protocol are: [UDP](http://en.wikipedia.org/wiki/User_Datagram_Protocol) and [TCP](http://en.wikipedia.org/wiki/Transmission_Control_Protocol).

### Layer 5: Session Layer
Responsible for the *session* between two computers, managing operations such as gracefully terminating  connections. It can also  establish whether a connection is [duplex or half-duplex](http://en.wikipedia.org/wiki/Duplex_%28telecommunications%29).

Examples of Protocols are: [NetBIOS](http://en.wikipedia.org/wiki/NetBIOS) and [NWLink](http://en.wikipedia.org/wiki/NWLink).

### Layer 6: Presentation Layer

Transforms the received data into a format that can be read by the application layer, such as enconding/decoding and several forms of encryption/decryption for securing the data.

Examples of protocols are: [ASCII](http://en.wikipedia.org/wiki/ASCII), [MPEG](http://en.wikipedia.org/wiki/Moving_Picture_Experts_Group), [JPEG](http://en.wikipedia.org/wiki/JPEG), and [MIDI](http://en.wikipedia.org/wiki/MIDI).

### Layer 7: Application Layer

Provides the details for end users to access network resources.

Examples of protocols are: [HTTP](http://en.wikipedia.org/wiki/Hypertext_Transfer_Protocol), [SMTP](http://en.wikipedia.org/wiki/Simple_Mail_Transfer_Protocol), [FTP](http://en.wikipedia.org/wiki/File_Transfer_Protocol), and [Telnet](http://en.wikipedia.org/wiki/Telnet).

---

## Data Encapsulation

The way the protocols on different layers of the OSI model communicate is by the *data encapsulation*, where each layer in the stack adds a header or footer to the packet.

The encapsulation protocol creates a [protocol data unit](http://en.wikipedia.org/wiki/Protocol_data_unit) (PDU),  including the data with all header and footer information added to it. What we call *packet* is the complete PDU.

For instance, in Wireshark we can track the sequence number where a higher layer PDU starts and stops. This allows us to  measure how long it took to transfer a PDU (the *display filter* is **tcp.pdu.time**).


---


## Switches and Routers
There are four primary ways to capture traffic from a target device on a
**switched** network: using a **hub**, using a **tap**, by port mirroring, or by ARP spoofing/cache poisoning. The first two obviously require a hub or a tap. Port mirroring requires forwarding capability from the switch. A great way to decide which method to use was borrowed by the reference [1]:

![](http://i.imgur.com/aRUfmsp.png)


All of the techniques for switched network are available on **routed** networks as well. However, for routers the sniffer placement becomes more relevant since a device's broadcast domain extends only until it reaches a
router.

---
## Types of Traffic Packets

There are three types of traffic packets within a network:

* **Broadcast packet**: sent to all ports on the network segment. Broadcast MAC address is  *ff:ff:ff:ff:ff:ff* (layer 2) or the highest possible IP address (layer 3).

* **Multicast packet**: sent from a single source to multiple destinations, to simplify the process using as little as bandwidth as possible.

* **Unicast packet**: transmitted from one computer to another.


---
## Common Protocols by Layer

### The Address Resolution Protocol   (Layer 2)

Both **logical** and **physical addresses** are used for communication on a network. Logical addresses allows communication between multiple networks (indirectly connected devices). Physical addresses allows communication on a single network (devices that are  connected to each other with a switch for example).


[ARP](http://en.wikipedia.org/wiki/Address_Resolution_Protocol) is the protocol used to determine which [MAC address](http://en.wikipedia.org/wiki/MAC_address) (physical address such as 00:09:5B:01:02:03 and belonging to layer 2) corresponds to a particular IP address (logical addresses such as 10.100.20.1, belonging to layer 3).

The ARP resolution process uses two packets (*ARP request* and  *ARP response*) to find the matching MAC address, sending a **broadcast** packet to every device in the domain, and waiting for the response of the  correct client. This works because  a switch uses a MAC table to know through which port to send the traffic.

In Wireshark, ARP is easily spotted with sentences such as **"Who has 192.168.11/ Tell 192.168.1.1"**. Additionally, you can see the ARP table in your device with:

```
$ arp -a
```

### The Internet Protocol (Layer 3)

Every interface on an Internet must have a unique Internet address. An IP has the task of delivering packets between hosts based on the IP addresses in the packet headers.

[IPv4](http://en.wikipedia.org/wiki/IPv4) addresses are 32-bit addresses used to uniquely identify devices connected in a network. They are represented by the dotted-quad notation with four sets of 8 bits, represented by  decimal numbers between 0 and 255.

In addition, an IP address consists of two parts: a **network address** and a **host address**. The network address identifies the *local area network* (LAN), and the host address identifies the device on that network.

The determination of these two parts is given by another set of addressing information, the **network mask** (netmask or subnet mask), which is also 32 bit longs. In the netmask, every bit set to 1 identifies the portion of the IP address that belongs to the network address. Remaining bits set to 0 identify the host address:

![](http://i.imgur.com/a7Evq9z.png)

Additionally, the IP packet header contain informations such as:

* **Version**: version of IP used.

* **Header Length**:  length of the IP header.

* **Type of Service**: flag used by routers to prioritize traffic.

* **Total length**:  length of the IP header and the data in the packet.

* **Identification**: identification of a packet or sequence of fragmented packets.

* **Fragment offset**:  identification of whether a packet is a fragment.

* **Time to Live**: definition of the lifetime of the packet, measured in hops/seconds through routers. A TTL is defined when a packet is created, and generally is decremented by 1 every time the packet is forwarded by a router.

* **Protocol**: identification of the type of packet coming next in the sequence.

* **Header checksum**: error-detection mechanism.

* **Source IP Address**.

* **Destination IP address**.

* **Options**: for routing and timestamps.

* **Data**.



### The Internet Control Message Protocol (Layer 3)

ICMP is the utility protocol of TCP/IP responsible for providing information about the availability of devices, services, or routes on a network.

Examples of services that use ICMP are  **ping**:

```
$ ping www.google.com
PING www.google.com (74.125.228.210) 56(84) bytes of data.
64 bytes from iad23s23-in-f18.1e100.net (74.125.228.210): icmp_seq=1 ttl=53 time=21.5 ms
64 bytes from iad23s23-in-f18.1e100.net (74.125.228.210): icmp_seq=2 ttl=53 time=22.5 ms
64 bytes from iad23s23-in-f18.1e100.net (74.125.228.210): icmp_seq=3 ttl=53 time=21.4 ms
```


and **traceroute** (Windows sends ICMP packets,  Linux sends UDP):

```
$ traceroute www.google.com
traceroute to www.google.com (173.194.46.84), 30 hops max, 60 byte packets
 1  * * *
 2  67.59.254.85 (67.59.254.85)  30.078 ms  30.452 ms  30.766 ms
 3  67.59.255.137 (67.59.255.137)  33.889 ms 67.59.255.129 (67.59.255.129)  33.426 ms 67.59.255.137 (67.59.255.137)  34.007 ms
 4  rtr101.wan.hcvlny.cv.net (65.19.107.109)  34.004 ms 451be075.cst.lightpath.net (65.19.107.117)  32.743 ms rtr102.wan.hcvlny.cv.net (65.19.107.125)  33.951 ms
 5  64.15.3.222 (64.15.3.222)  34.972 ms 64.15.0.218 (64.15.0.218)  35.187 ms  35.120 ms
 6  * 72.14.215.203 (72.14.215.203)  29.225 ms  29.646 ms
 7  209.85.248.242 (209.85.248.242)  29.361 ms 209.85.245.116 (209.85.245.116)  39.780 ms  42.108 ms
 8  209.85.249.212 (209.85.249.212)  33.220 ms 209.85.252.242 (209.85.252.242)  33.500 ms  33.786 ms
 9  216.239.50.248 (216.239.50.248)  53.231 ms  57.314 ms 216.239.46.215 (216.239.46.215)  52.140 ms
10  216.239.50.237 (216.239.50.237)  52.022 ms 209.85.254.241 (209.85.254.241)  48.517 ms  48.075 ms
11  209.85.243.55 (209.85.243.55)  56.220 ms  45.359 ms  44.934 ms
12  ord08s11-in-f20.1e100.net (173.194.46.84)  43.184 ms  39.770 ms  45.095 ms
```

The way traceroute works is by sending an echo request that has a particular feature in the IP header: **the TTL is 1**. This means that the packet will be dropped at the first hop. The second packet goes through the first hop and then is dropped in the second hop (TTL is 2), and so on.

To make this work, the router replies response with a *double-headed packet*, containing a copy of the IP header and the data that was sent in the original echo request.

PS: Check out  this post from Julia Evans on how to create a simple [*Traceroute in 15 lines of code using Python's Scapy*](http://jvns.ca/blog/2013/10/31/day-20-scapy-and-traceroute/).


### The Transmission Control Protocol (Layer 4)

Provides a reliable flow of data between two hosts with a **three-way handshake**. The purpose is to allow the transmitting host to ensure that the destination host is up, and let the transmitting host check the availability of the port as well.

This handshake works as the follow:

1. Host A sends an initial packet with no data but with the synchronize (SYN) flag and the initial sequence number and [maximum segment size](http://en.wikipedia.org/wiki/Maximum_segment_size) (MSS) for the communication process.
2. Host B responds with a synchronize and acknowledge (SYN + ACK) flag, with its initial sequence number.
3. Host A sends an acknowledge (ACK) packet.

When the communication is done, a **TCP teardown** process is used to gracefully end a connection between two devices. The process involves four packets:

1. Host A sends a packet with FIN and ACK flags.
2. Host B sends an ACK packet and then a FIN/ACK packet.
4. Host A sends an ACK packet.


Sometimes, however, connections can end abruptly (for example due to a potential attacker issuing a port scan or due a misconfigured host). In these cases, TCP resets packets with a RST flag are used. This indicate that a connection was closed abruptly or a connection attempt was refused.

Furthermore, when communicating with TCP, 65,535 ports are available. We typically divide them into two groups:

* **standard port group**: from 1 to 1023, used by specific services.

* **ephemeral port group**: from 1024 through 65535, randomly chosen by services.

Finally, the TCP header contains information such as:

* **Source Port**.
* **Destination Port**.
* **Sequence number**: identify a TCP segment.
* **Acknowledgment Number**: sequence number to be expected in the next packet from the other device.
* **Flags**: URG, ACK, PSH, RST, SYN, FIN flags for identifying the type of TCP packet being transmitted.
* **Windows size**:  size of the TCP receiver buffer in bytes.
* **Checksum**: ensure the contents of the TCP header.
* **Urgent Pointer**:  examined for additional instructions where the CPU should be reading the data within the packet.
* **Options**: optional fields.


### The User Datagram Protocol (Layer 4)

While TCP is designed for reliable data delivery, UDP focus on speed. UDP sends packets of data called **datagrams** from one host to another, with no guarantee that they reach the other end.

Unlike TCP, UDP does not formally establish and terminate a connection between hosts. For this reason, it usually relies on built-in reliability services (for example protocols such as DNS and DHCP).

The UDP header  has fewer fields than TCP:

* **Source Port**.
* **Destination Port**.
* **Packet Length**.
* **Checksum**.


###  The Dynamic Host Configuration Protocol (Layer 7)


In the beginning of the Internet, when a device needed to communicate over
a network, it would be assigned an address by hand.

As the Internet grown, the **Bootstrap Protocol** (BOOTP) was created,   automatically assigning addresses to  devices. Later, BOOTP was replaced by DHCP.


### The Hypertext Transfer Protocol (Layer 7)

HTTP is the mechanism that allows browsers to connect to web servers to view web pages.  HTTP packets are built on the top of TCP and they are identified by one of the eight different request methods.


------------------------------------------------------


#  Analyzing Packets in Wireshark

In Wireshark, the entire process of network sniffing can be divided into three steps:

1.  **Collection**:   transferring the selected network interface into promiscuous mode so it can capture raw binary data.

2.  **Conversion**:  chunks of collected binary are converted into readable form.

3. **Analysis**: processing of the protocol type, communication channel, port number, protocol headers, etc.

## Collecting Packets
Network traffic sniffing is only possible if the ** network interface** (NIC) is transfered to **promiscuous mode**. This allows the transfer of all received traffic  to the CPU (instead of processing frames that the interface was intended to receive). If the NIC is not set to promiscuous mode, packets that are not destined to that controller are discarded.

##  Wireshark main's GUI
The Wireshark main's GUI is composed of four parts:

* **Capture's options**.
* **Packet List**: list all packets in the capture file. It can be edited to display packet number, relative time, source, destination, protocol, etc.
* **Packet details**: hierarchal display of information about a single packet.
* **Packet Bytes**: a packet in its raw, unprocessed form.

To start capturing packets, all you need to do is to choose the network interface. You may also edit a *capture filter* prior to the packet collection.



## Color Scheme

The packet list panel displays  several type of traffic by (configurable) colors. For instance:

* green is TCP (and consequently HTTP),
* dark blue is DNS,
* light blue is UDP,
* light yellow is for ARP,
* black identifies TCP packets with problems.

##  Packet Visualization and Statistics

Wireshark has several tools to learn about packets and networks:

* **Statistics -> IO Graphs**: Allows to graph throughput of data. For instance, you can use graphs to find peaks in the data, discover performance bottlenecks in individual protocols, and compare data streams. Filtering is available in this interface (for example, to show ARP and DHCP traffic).

* **Statistics -> TCP -> Stream Graph -> Round Trip Time Graph**:  Allows to  plot **round-trip times** (RTT) for a given capture file. This is the time it takes for an acknowledgment to be received from a sent packet.

* **Statistics -> Flow Graph**: Timeline-based representation of communication statistics (based on time intervals). It allows the visualization of connections and the flow of data over time.  A flow graph contains a column-based view of a connection between hosts and organizes the traffic. This analysis can show slow points or bottlenecks and determine if there is any latency.

* **Statistics -> Summary**: Returns a report about the entire process by features such as interface, capture duration and number, and size of packets.

* **Statistics -> Protocol Hierarchy**: Shows statistical information of different protocols  in a *nodal form*.  It arranges the protocols according to its layers, presenting them in percentage form. For example, if you know that your network usually gets 15%  ARP traffic, if you see a value such as 50%, you know something is wrong.

* **Statistics -> Conversations**: Shows the address of the endpoints involved in the conversation.

* **Statistics -> Endpoints**: Similar to conversations, reflecting the statistics of traffic to and from an IP address. For example, for TCP, it can look like  **SYN, SYN/ACK, SYN**.

* **Edit-> Finding Packet or CTRL-F**: Finds packets that match to some criteria. There are three options:
    * *Display filter*:  expression-based filter (for example **not ip**, **ip addr==192.168.0.10**,  or **arp**).
    * *Hex value*: packets with a hexadecimal (for example 00:ff, ff:ff).
    * *String*:  packets with a text string (for example admin or workstation).

* **Right click -> Follow TCP Stream**: Reassembles TCP streams into an  readable format (instead of having the data being in small chunks). The text displayed in *red* to signifies traffic from the source to the destination, and in  *blue* identifies traffic in the opposite direction. If you know the stream number (value to be followed to get various data packets), you can also use the following filter for the same purpose:

```
tcp.stream eq <number>
```

* **Right click -> Mark Packet or CTRL+M**: Helps to organization of relevant packets.




---
##  Filters

### The Berkeley Packet Filter Syntax
Wireshark's filtering is a very powerful feature. It uses the [Berkeley Packet Filter](http://en.wikipedia.org/wiki/Berkeley_Packet_Filter) (BFP) syntax.  The syntax corresponds to an **expression** which is made of one more **primitives**. These primitives can have  one or more **qualifier**, which are defined below:

* **Type**:  ID name or number (for example: **host**, **net**, **port**).
* **Dir**: transfer direction to or from the ID name or number (for example: **src** and **dst**).
* **Proto**: restricts the match to a particular protocol (for example: **ether**, **ip**, **tcp**, **udp**, or **http**)

A example of primitive is:
```
dst host 192.168.0.10
```
where **dst host** is the qualifier, and the IP address is the ID.

### Types of Filters
Packages can be filtering in two ways:

* **Capture filters**: specified when packets are being captured. This method is good for performance of large captures.
* **Display filters**: applied to an existing set of collected packets. This method gives more versatility since you have the entire data available.

In the following sessions I  show several examples of capture and display  filters.

### Capture Filters by Host Address and Name

* Traffic associated with a host's IPV4 address (also works for a IPv6 network).

```
host 172.16.16.150
```

* Traffic to or from a range of IP addresses:

```
net 192.168.0.0/24
```

* Device's hostname with the host qualifier:

```
host testserver
```

* If you are concerned that the IP address for a host changed, you can filter based on MAC address:

```
ether host ff-ff-ff-ff-ff-aa
```

* Only traffic coming from a particular host (host is an optional qualifier):

```
src host 172.16.16.150
```

* All the traffic leaving a host:

```
dst host 172.16.16.150
```

* Only  traffic to or from IP address 173.15.2.1

```
host 173.15.2.1
```

* Traffic from a range of IP addresses:

```
src net 192.168.0.0/24
```


### Capture Filters by Ports

* Only traffic on port 8000:

```
port 8000
```

* All traffic except on port 443:

```
!port 443
```

* Traffic going to a host listening on 80:

```
dst port 80
```

* Traffic within a range of port:

```
tcp portrange 1501-1549
```

* Both inbound and outbound traffic on port 80 and 21:

```
port 80 || port == 21
```

* Only non-http and non-SMTP traffic (equivalent):

```
host www.example.com and not (port 80 or port 25)
```

### Capture Filters by  Protocols

* Capture only unicast traffic (useful to get rid of noise on the network):

```
not broadcast and not multicast
```

*  ICMP traffic only:

```
icmp
```


* Drop ARP packets:

```
!arp
```

* Drop IPv6 traffic:

```
!ipv6
```

* DNS traffic:

```
dns
```

* Clear text email traffic:

```
smtp || pop || imap
```

### Capture Filters  by Packet's  Properties

* TCP packets with SYN flag set:

```
tcp[13]&2==2
```

* ICMP packets with destination unreachable (type 3):

```
icmp[0]==3
```

*  HTTP GET requests (bytes 'G','E','T' are hex values 47, 45, 54):

```
port 80 and tcp[((tcp[12:1] & 0xf0 ) >> 2  ):4 ] = 0x47455420
```

---
### Display Filters by Host Address and Name


* Filter by IP address:

```
ip.addr == 10.0.0.1
```

* IP source address field:

```
ip.src == 192.168.1.114
```

* IP address src/dst for a network range:

```
ip.addr== 192.168.1.0/24
```

### Display Filters by Ports

* Any TCP packet with 4000 as a source or destination port:

```
tcp.port == 4000
```

* Source port:

```
tcp.srcport == 31337
```

### Display Filters by  Protocols

* Drops  arp, icmp, dns, or whatever other protocols may be background noise:

```
!(arp or icmp or dns)
```

* Displays all re-transmissions in the trace (helps when tracking down slow application performance and packet loss):

```
tcp.analysis.retransmission
```

* ICMP Type field to find all PING packets:

```
icmp.type== 8
```

### Display Filters  by Packet's  Properties

* Displays all HTTP GET requests:

```
http.request
```

* Display all POST requests:

```
http.request.method == "POST"
```

* Filter for the HEX values:

```
udp contains 33:27:58
```

* Sequence number field in a TCP header:

```
tcp.seq == 52703261
```


* Packets that are less than 128 bytes in length:

```
frame.len <= 128
```

* TCP packets with SYN flag set:

```
tcp.flags.syn == 1
```

* TCP packets with RST flag set:

```
tcp.flags.rst == 1
```

* Displays all TCP resets:

```
tcp.flags.reset == 1
```

* IP flags where fragment bit is not set (see if someone is trying ping):

```
ip.flags.df == 0
```


--------------------------------------
#  Using Wireshak for Security


## Some Reconnaissance Tips

### Network Scan with SYN

A  TCP SYN scan is fast and reliable  method to scan ports and services in a network. It is also less noisy than other scanning techniques.

Basically, it relies on the three-way handshake process to determine which ports are open on a target host:

1. The attacker sends a TCP SYN packet to a range of ports on the victim.

2. Once this packet is received by the victim, the follow response will be observed:

    * **Open ports**: replies with a TCP SYN/ACK packet (three times). Then the attacker knows that port is open and a service is listening on it.

    * **Closed ports, not filtered**: the attacker receives a RST response.

    * **Filtered ports** (by a firewall, for example): the attacker does not receive any response.


### Operating System Fingerprint

Technique to determine the operating system on a system without have access to it.

In a **Passive Fingerprinting**, an attacker can use certain fields within packets sent from the target to craft a stealthy fingerprinting.

This is possible due the lack of specificity by protocol's [RFCs](http://en.wikipedia.org/wiki/Request_for_Comments): although the various fields contained in the TCP, UDP and IP headers are very specific, no default values are defined for these fields.

For instance, the following header values can help one to distinguish between several operating systems:

* **IP, Initial Time to Live**:
    - 64 for Linux, Mac OS
    - 128 for Windows
    - 255 for Cisco IOS
* **IP, Don't Fragment Flag**:
    - Set for Linux, Mac OS, Windows
    - Not set for Cisco IOS
* **TCP, Max Segment Size**:
    - 1440 for Windows
    - 1460 for Mac OS 10, Linux
* **TCP, Window Size**:
    - 2920-5840 for Linux
    - 4128 for Cisco  IOS
    - 65535 for for Mac OS 10
    - variable for Windows
* **TCP, StackOK**:
    - Set for Linux, Windowns
    - Not set for Cisco IOS, Mac OS 10

Note: A nice tool using operating system fingerprinting techniques is [p0f](http://lcamtuf.coredump.cx/p0f3/).



In **Active Fingerprinting**, the attacker actively sends crafted packets to the victim whose replies reveal the OS. This can be done with [Nmap](http://nmap.org/).

---


## Some Forensics Tips

### DNS Queries

Look at different DNS queries that are made while the user was online. A possible filter is:

```
dsn
```
This will give a view of any malicious DNS request done without the knowledge of the user. An example is a case where a  visited website has a hidden **iframe** with some malicious script inside.

### HTTP GET Headers

Look for different HTTP streams that have flown during the network activity:  HTML, JavaScript,  image traffic, 302 redirections, non-HTTP streams, Java Archive downloads, etc. A possible filter is:

```
http
```
You can also look at different GET requests  with:

```
tcp contains "GET"
```

### Checking for DNS Leaks with VMs

In a virtual machine look at **statistics --> Endponts**. There should be only one public IP address: the VPN server that the virtual machine is connected to.

---
## ARP Cache Poisoning

### Sniffing

ARP cache poisoning  allows tapping into the wire with Wireshark. This can be used for good or for evil.

The way this works is the following: all devices on a network communicate with each other on layer 3 using IP addresses. Because switches operate on layer 2 they only see MAC addresses, which are usually cached.

When a MAC address is not in the cache list, ARP broadcasts a packet asking which IP address owns some MAC address. The destination machine replies to the packet with its MAC address via an ARP reply (as we have learned above). So,  at this point, the transmitting computer has the data link layer addressing the information it needs to communicate with the remote computer. This information is then stored into the ARP cache.

An attacker can spoof this process by  sending ARP messages to an Ethernet switch or router with fake MAC  addresses in order to intercept the traffic of another computer.

In Linux, ARP spoofing can be done with [arpspoof or Ettercap](http://www.irongeek.com/i.php?page=security/arpspoof). For instance, if  your wlan0 is at 192.168.0.10 and the router is at 192.168.0.1, you can run:

```
$ arpspoof -i wlan0 -t 192.168.0.10 192.168.0.1
```

If you are in Windows, ARP cache poising can be crafted using [Cain & Abel](http://www.oxid.it/cain.html).


### Denial-of-Service

In  networks with very high demand, when you reroute traffic, everything  transmitted and received by the target system must first go through your analyzer system. This makes  your analyzer the bottleneck in the communication process and being suitable to cause [DoS](http://en.wikipedia.org/wiki/Denial-of-service_attack).

You might be able avoid all the traffic going through your analyzer system by using a feature called [asymmetric routing](http://www.cisco.com/web/services/news/ts_newsletter/tech/chalktalk/archives/200903.html).

---
## Wireless Sniffing

### The 802.11 Spectrum
The unique difference when capturing traffic from a **wireless local area network** (WLAN) is that the wireless spectrum is a **shared medium** (unlike wired networks, where each client has it own cable to the switch).

A single WLAN occupy a portion of the [802.11 spectrum](http://en.wikipedia.org/wiki/IEEE_802.11), allowing multiple systems to operate in the same physical medium. In the US, 11 channels are available and a WLAN can operate only one channel at time (and so the sniffing).

However, a technique called **channel hopping** allows quick change between channels to collect data. A tool to perform this is [kismet](https://www.kismetwireless.net/), which can hop up to 10 channels/second.



### Wireless NIC  modes

Wireless network cards can have four modes:

* **Managed**: when the wireless client connects directly to a wireless access point (WAP).

* **ad hoc mode**:   devices connect directly to each other, sharing the responsibility of  a WAP.

* **Master mode**: the NIC works with specialized software to allow the computer act as a WAP for other devices.

* **Monitor**: used to stop transmitting and receiving data, and start listening to the packets flying in the air.

To access the wireless extensions in Linux you can type:

```
$ iwconfig
```

To change the interface (for example eth1) to monitor mode, you type:
```
$ iwconfig eth1 mode monitor
$ iwconfig eth1 up
```

To change the channel of the interface:

```
$ iwconfig eth` channel 4
```





-------
## Further References:

- [Wireshark wiki](http://wiki.wireshark.org/)
- [Practical Packet Analysis, ](http://wiki.wireshark.org/)
- [Wireshark plugin  for writing dissectors in Python](https://github.com/ashdnazg/pyreshark)
- [Using Wireshark ti check for DNS Leaks](https://lilithlela.cyberguerrilla.org/?p=76081)
- [Publicly available PCAP files](http://www.netresec.com/?page=PcapFiles)
- [Malware PCAP files](http://contagiodump.blogspot.se/2013/08/deepend-research-list-of-malware-pcaps.html)