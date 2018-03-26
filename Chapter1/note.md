# Goals

* Big Picture
    * basic terminology & concepts
    * hardware & software
* Delay, loss, and throughput
    * transmission
    * propagation
    * queuing
* architectural principles
* security

# What is the Internet?  Explore from two sides:

* Physical side: hardware & software
* Logical side: working infrastructure

## A Nuts-and Bolts Description Hardware: 
**communication links**(coaxial cable, copper wire, ...) and **packet 
switches**(routers and link-layer switches).

## A services Description 
Internet is an infrastructure that provides services
to applications.

## What is a protocol?  
A protocol is a specification, that defines certain
messages that can be exchanged, and certain actions should be performed upon
receiving a specific message. It's a logical specification which doesn't
physically exist. Implementations by engineers physically exist.

So, what is computer network? A computer network is a collection of hardware &
software, which implements a certain set of protocols, to provide transmission
services to applications. The Internet is a kind of computer network, with a
certain set of protocols.

# The Network Edge 
**end systems** = **host**, which refer to devices such as
mobile phone, computer, laptop, servers, etc that sitting at the edge of the
Internet. When we say hosts, it means this device run some application programs.
Depending on whether the running program receive messages or send messages, the
hosts can be further divided into **clients** and **servers**.

## Access Networks 
An access network is a type of telecommunications network
which connects subscribers to their immediate service provider.

# The Network Core 
## Packet Switching 
Application exchange messages. Messages
breaks into smaller chunks do data, known as packets. Then packets are
transferred within the network.

**Store and forward transmission**  
**Queuing Delays and Packet Loss**  
Packet switch has multiple links attached to it. **Each** attached link has an
associated output buffer. Arrived packets may suffer output buffer queuing
delays, if there are packets in front of it to be sent. If number of arrived
packets exceeds the capacity of the buffer, packet loss happens.  
**Forwarding Tables and Routing Protocols**  
When a packet arrives at a router in the network,
the router examines a **portion** of the packet’s destination address and
forwards the packet to an adjacent router. More specifically, each router has a
forwarding table that maps destination addresses (or portions of the destination
addresses) to that router’s outbound links.

## Circuit Switching 
There are two fundamental approaches to moving data through
a network of links and switches: circuit switching and packet switching. This
section is about circuit switching. Circuit switching reserves **all** the
resources along a communication path(buffers, link transmission rate) while
transferring data. Packet switching doesn't do reservation. As a consequence,
packet switching incurs waiting.

# Delay, Loss, and Throughput in Packet-Switched Networks 
Delay consists of four
types: nodal processing delay, queuing delay, transmission delay, and
propagation delay.

## Overview of Delay in Packet-Switched Networks
- **Processing Delay**  
  When a packet arrives at the router, the router examines
  the packet's header to find, which outbound link the packet should go. Also,
  it does some error check.
- **Queuing Delay**  
- **Transmission Delay**  
  Transmission Delay is the time spent by sending messages out of the router.
- **Propagation Delay**  
  Propagation delay is the time spent in the transmission media.

## Queuing Delay and Packet Loss 
Queuing delay is the most interesting component
of nodal delay. Since queuing delay varies from packet to packet, depending on
their arriving order at router, one typically uses statistical measures when
characterizing queuing delay.

Three facets affecting queuing delay: arriving traffic rate, transmission rate,
and arriving pattern of traffic. Suppose the traffic arriving rate is _a_
packets/second **on average**, and each packet contains _L_ bits. Assume the
transmission rate is _R_ bits/second. Then, the ratio _La/R_ is called **traffic
intensity**. The queuing delay depends on both the traffic intensity and the
traffic pattern. In reality, no specific traffic pattern exists. A general rule
is that, as the traffic intensity approaches 1, the **average** queue length
gets larger and larger. (Remember even the traffic intensity is an average
value)

Packet Loss happens because the capacity of queue in a router is finite.

## End-to-End Delay

