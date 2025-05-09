# TCP
Trans-Fem Communication Protocol (TCP)
## Description
TCP is exactly as the name inplies, it uses the tcp and udp protocol to send simple messages either directly to a host or on the entire broadcast domain as a form of group chat. The purpose is to instantly message somebody without any outside servers as many popular messaging platforms are restricted on my school's network and cell reception is terrible. By using the broadcast domain it allows groupchats without any of the commitment or constant spamming if you just want to share a few messages and nothing else.
## How to run / Setup
simply download the script, change the variable `alias = "default"` to whatever string you would like to be known as, install termcolor, and run. you will be greeted with the option to either message one on one by pressing 1 or to communicate by broadcast by pressing 2. Mode 1 uses tcp so you are given an indicator that will be green if the message is recieved, mode 2 uses udp so there is no verification.
