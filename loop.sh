#automate running of various tools on a line separated file of IP addresses
#uncomment what youd like to run for now because i suck at bash scripting
#based on https://unix.stackexchange.com/questions/7011/how-to-loop-over-the-lines-of-a-file
#usage is ./sslscan.sh <inputfile>
#for text output use > outputfile.txt etc

#useful command:
#expand cidr with nmap
#nmap -sL -n -iL $file | grep 'Nmap scan report for' | cut -f 5 -d ' '

#!/bin/bash
IFS=$'\n'       # make newlines the only separator
set -f          # disable globbing

while IFS= read -r line; do

    
    # asa file disclosures 
    # https://$line/+CSCOT+/translationtable?type=mst&textdomain=/%2bCSCOE%2b/portal_inc.lua&default-language&lang=../
    #need to work on this one wrt filenames
    # https://$line/+CSCOT+/oem-customization?app=AnyConnect&type=oem&platform=..&resource-type=..&name=%2bCSCOE%2b/[LOCAL-FILE]

    #sslscan an ip
    #sslscan "$line"

    #curl an ip (or list of urls) and intercept with a local proxy like burp
    #curl --get --insecure --proxy 127.0.0.1:8080 $line

    #run enum4linux
    #enum4linux $line

    #test for tcp timestamps, edit the port number you are attempting
    #hping3 -S -c 2 $line -p 443 --tcp-timestamp

    #Responder's RunFinger.py with greppable output. must be in your path or in the tools dir
    #python3 RunFinger.py -g -i $line

    #chromium web screenshot with ip as filename
    #chromium --headless --disable-gpu --screenshot https://$line --screenshot=$line.png

    #ike aggressive mode check
    #sudo ike-scan -M -A -n foo $line -P
    wait
done < "$1"
