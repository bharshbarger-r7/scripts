#!/usr/bin/env python3

import sys, os, hashlib, binascii, argparse, signal

class ReverseHashLookup(object):

    def __init__(self, args, parser):

        #import args and parser objects from argparse
        self.args = args
        self.parser = parser

    #https://www.trustedsec.com/2010/03/generate-an-ntlm-hash-in-3-lines-of-python/
    def password_to_nthash(self):
        ntpass = ''.join(self.args.password)
        nt_hash = hashlib.new('md4', ntpass.encode('utf-16le')).digest()
        print ('NTLM: %s' % (binascii.hexlify(nt_hash).decode()))

    #https://docs.python.org/3/library/hashlib.html    
    def password_to_sha1(self):
        shapass = ''.join(self.args.password).encode()
        print('SHA1: %s' % (hashlib.sha1(shapass).hexdigest()))
        

def main():
    #https://docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', help = 'specify a mode (e.g. 100 or 1000)', nargs = "*")
    parser.add_argument('-p', '--password', help = 'specify a password to hash', nargs = 1)
    #parser.add_argument('-r', '--rawhash', help = 'specify a hash', nargs = "*")
    parser.add_argument('-v', '--verbose', help = 'Verbose', action = 'store_true')

    args = parser.parse_args()

    run = ReverseHashLookup(args,parser)

    if args.mode is None:
        print('please select the hashcat mode(s) of the passwords you want to check, e.g. FilterHash.py -m 1000 5500')
        sys.exit(0)

    for m in args.mode:

        if m == '1000':
            run.password_to_nthash()
        if m == '100':
            run.password_to_sha1()


if __name__ == '__main__':

    main()
