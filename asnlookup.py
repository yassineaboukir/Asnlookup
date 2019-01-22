#!/usr/bin/python

import csv
import sys
import argparse
import requests
import re
import os
from termcolor import colored
from bs4 import BeautifulSoup
requests.packages.urllib3.disable_warnings()

def banner():
        print('''
        ____ ____ _  _ _    ____ ____ _  _ _  _ ___
        |__| [__  |\ | |    |  | |  | |_/  |  | |__]
        |  | ___] | \| |___ |__| |__| | \_ |__| |

         Author: Yassine Aboukir (@yassineaboukir)\n''')

def parse_args():
    # parse the argument
    parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' + sys.argv[0] + " -o twitter")
    org = parser.add_argument('-o', '--org', help="Organization to look up", required=True)
    nmapscan = parser.add_argument('-n', '--nmapscan', help="Run Nmap", required=False, action="store", nargs='?', const="-p 1-65535 -T4 -A -v")
    masscan = parser.add_argument('-m', '--masscan', help="Run Masscan", required=False, action="store", nargs='?', const="-p0-65535 --rate 200")
    return parser.parse_args()

org = parse_args().org
nmapscan = parse_args().nmapscan
masscan = parse_args().masscan

def download_db():
    # Download a local copy of ASN database from maxmind.com
    if (os.path.isfile('./GeoLite2-ASN-Blocks-IPv4.csv') and os.path.isfile('./GeoLite2-ASN-Blocks-IPv6.csv')) == False:
        print(colored("Downloading ASN database ...\n", "red"))
        os.system("wget https://geolite.maxmind.com/download/geoip/database/GeoLite2-ASN-CSV.zip && unzip GeoLite2-ASN-CSV.zip && rm -f GeoLite2-ASN-CSV.zip && mv GeoLite*/* . && rm -f COPYRIGHT.txt LICENSE.txt && rm -rf GeoLite*/")
        print(colored("\nDone!\n", "red"))

        # Extracting and saving database file size locally
        try:
            response = requests.get("https://geolite.maxmind.com/download/geoip/database/GeoLite2-ASN-CSV.zip")
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)

        with open("filesize.txt", "w") as filesize:
            filesize.write(response.headers['Content-Length'])
    else:
        # Checking if there is a new database change and download a new copy if applicable
        response = requests.get("https://geolite.maxmind.com/download/geoip/database/GeoLite2-ASN-CSV.zip")
        with open("filesize.txt", "r") as filesize:
            for line in filesize:
                if line == response.headers['Content-Length']:
                    pass
                else:
                    print(colored("[i] It seems like you have not updated the database.","red"))
                    choice = raw_input(colored("[?] Do you want to update now? [Y]es [N]o, default: [N] ", "red"))
                    if choice.upper() == "Y":
                        os.system("rm -rf GeoLite2*")
                        print(colored("Downloading a new copy of the database ...\n","red"))
                        os.system("wget -O GeoLite2-ASN-CSV.zip https://geolite.maxmind.com/download/geoip/database/GeoLite2-ASN-CSV.zip && unzip GeoLite2-ASN-CSV.zip && rm -f GeoLite2-ASN-CSV.zip && mv GeoLite*/* . && rm -f COPYRIGHT.txt LICENSE.txt && rm -rf GeoLite*/")

                        try:
                            response = requests.get("https://geolite.maxmind.com/download/geoip/database/GeoLite2-ASN-CSV.zip")
                        except requests.exceptions.RequestException as e:
                            print(e)
                            sys.exit(1)
                        print("\nDone!\n")
                        with open("filesize.txt", "w") as filesize:
                            filesize.write(response.headers['Content-Length'])
                    else: pass

def extract(organization):
    #read csv, and split on "," the line
    ips = []

    ipv4 = csv.reader(open('GeoLite2-ASN-Blocks-IPv4.csv', "r"), delimiter=",")
    #loop through csv list
    for row in ipv4:
        #if current rows 2nd value is equal to input, print that row
        if organization.upper() in row[2].upper():
            ips.append(row[0])

    ipv6 = csv.reader(open('GeoLite2-ASN-Blocks-IPv6.csv', "r"), delimiter=",")
    for row in ipv6:
        #if current rows 2nd value is equal to input, print that row
        if organization.upper() in row[2].upper():
            ips.append(row[0])

    print(colored("IP addresses owned by {} are the following:\n".format(organization),"red"))
    if ips is not None:
        if os.path.isfile('./' + organization + '.txt') == True:
            os.system('rm -f ' + organization + '.txt')
        else:
            pass

        for ip in ips:
            with open(organization + ".txt", "a") as export:
                export.write(ip + "\n") # Exporting the result to a txt file
            print(colored(ip, "yellow"))
    else:
        print(colored("Sorry! We couldn't find the organization's ASN and IP addresses.", "red"))

# Due to Maxmind structural change, below function is useless Windows

# def extract_ip(asn, organization):
#     if asn is not None:
#         for num in asn:
#             ipinfo = "https://ipinfo.io/"
#             try:
#                 response = requests.get(ipinfo + num)
#             except requests.exceptions.RequestException as e:
#                 print(e)
#                 sys.exit(1)
#             html = response.content
#             soup = BeautifulSoup(html, 'html.parser')
#             ip_addresses = []
#             for link in soup.find_all('a'):
#                 if num in link.get('href'):
#                     lookfor = '/'+num+'/'
#                     ip = re.sub(lookfor, '', link.get('href'))
#                     ip_addresses.append(ip)
#             print(colored("IP addresses owned by {} are the following:\n".format(organization),"red"))
#             for i in ip_addresses:
#                 # Exporting the result to a txt file
#                 with open(organization + ".txt", "a") as export:
#                     export.write(i + "\n")
#                 print(colored(i, "yellow"))
#             print("\n")
#     else:
#         print(colored("Sorry! We couldn't find the organization's ASN and IP addresses.", "red"))

def scanning(n, m, organization):
    # Only allow one scanner choice
    if n and m is not None:
    	print(colored("\nPlease only select one port scanner: -m --> Masscan or -n --> Nmap.", "red"))
    # Run Nmap on the IP addresses if -m argument is set
    elif n is not None:
        if os.path.isfile(organization + '.txt') == True:
            print(colored("\nRunning port scanning using Nmap ...\n", "red"))
            os.system("nmap {} -iL {}".format(n, organization + ".txt"))
    # Run Masscan on the IP addresses if -m argument is set
    elif m is not None:
    	if os.path.isfile(organization + '.txt') == True:
        	print(colored("\nRunning port scanning using Masscan ...\n", "red"))
        	os.system("masscan {} -iL {}".format(m, organization + ".txt"))
    else: pass

if __name__ == '__main__':
    banner()
    download_db()
    extract(org)
    scanning(nmapscan, masscan, org)
