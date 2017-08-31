#!/usr/bin/python

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Hack an Amazon Dash Button to trigger IFTTT actions via webhook.  #
# There are hundreds of actions available on IFTTT to choose from.  #
#                                                                   #
# Created by Wesley Archer (aka. @raspberrycoulis)                  #
# Web: https://www.raspberrycoulis.co.uk                            #
# Git: https://github.com/raspberrycoulis                           #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import requests
import logging
import urllib
import httplib
  
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

def button_pressed_dash():
    # Replace TRIGGER and YOUR_UNIQUE_KEY in the URL below - this is found the documentation for Webhooks on IFTTT.com
    requests.post("https://maker.ifttt.com/trigger/TRIGGER/with/key/YOUR_UNIQUE_KEY")

def udp_filter(pkt):
    options = pkt[DHCP].options
    for option in options:
        if isinstance(option, tuple):
            if 'requested_addr' in option:
                mac_to_action[pkt.src]()
                break
  
mac_to_action = {'xx:xx:xx:xx:xx:xx' : button_pressed_dash} # Add your Amazon Dash Button's MAC address in lowercase
mac_id_list = list(mac_to_action.keys())
sniff(prn=udp_filter, store=0, filter="udp", lfilter=lambda d: d.src in mac_id_list)
  
if __name__ == "__main__":
    main()
