#!/usr/bin/python
# Tested on Python 2.7 and 3.5

import csv
import sys
import argparse
import requests
import re
import os
from termcolor import colored
from bs4 import BeautifulSoup
from config import *
requests.packages.urllib3.disable_warnings()

download_link = 'https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-ASN-CSV&license_key={}&suffix=zip'.format(license_key)

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

def check_licensekey():
    if not license_key:
        print (colored('[!] Please enter a valid Maxmind user license key in config.py.', 'red'))
        sys.exit(1)
    else:
        try:
            r = requests.head('{}'.format(download_link))
            if r.status_code == requests.codes.ok:
                print (colored("[*] User's license key is valid!\n", 'green'))
            else:
                print (colored("[!] Please enter a valid Maxmind user license key in config.py.", 'red'))
                sys.exit(1)
        except requests.exceptions.RequestException as e:
            print (e)
            sys.exit(1)

def download_db():
    global input
    useragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:64.0) Gecko/20100101 Firefox/64.0'
    # Download a local copy of ASN database from maxmind.com
    if (os.path.isfile('./GeoLite2-ASN-Blocks-IPv4.csv')) == False:
        print(colored("[*] Downloading ASN database ...\n", "red"))
        os.system("wget -O GeoLite2-ASN-CSV.zip '{}' && unzip GeoLite2-ASN-CSV.zip && rm -f GeoLite2-ASN-CSV.zip && mv GeoLite*/* . && rm -f GeoLite2-ASN-Blocks-IPv6.csv && rm -f COPYRIGHT.txt LICENSE.txt && rm -rf GeoLite*/".format(download_link))
        print(colored("\nDone!\n", "red"))

        # Extracting and saving database file size locally
        try:
            response = requests.head("{}".format(download_link), headers={'User-Agent': useragent}, timeout = 10)
        except:
            print(colored("[*] Timed out while trying to connect to the database server, please run the tool again.", "red"))
            sys.exit(1)

        with open("filesize.txt", "w") as filesize:
            filesize.write(response.headers['Content-Length'])
    else:
        # Checking if there is a new database change and download a new copy if applicable
        try:
            response = requests.head("{}".format(download_link), headers={'User-Agent': useragent}, timeout = 10)
        except:
            print(colored("[*] Timed out while trying to the database server, please run the tool again.", "red"))
            sys.exit(1)
        with open("filesize.txt", "r") as filesize:
            for line in filesize:
                if line == response.headers['Content-Length']:
                    pass
                else:
                    print(colored("[*] It seems like you have not updated the database.","red"))
                    try: input = raw_input #fixes python 2.x and 3.x input keyword
                    except NameError: pass
                    choice = input(colored("[?] Do you want to update now? [Y]es [N]o, default: [N] ", "red"))
                    if choice.upper() == "Y":
                        os.system("rm -rf GeoLite2*")
                        print(colored("[*] Downloading a new copy of the database ...\n","red"))
                        os.system("wget -O GeoLite2-ASN-CSV.zip '{} && unzip GeoLite2-ASN-CSV.zip && rm -f GeoLite2-ASN-CSV.zip && mv GeoLite*/* . && rm -f GeoLite2-ASN-Blocks-IPv6.csv  && rm -f COPYRIGHT.txt LICENSE.txt && rm -rf GeoLite*/".format(download_link))

                        try:
                            response = requests.get("{}".format(download_link), headers={'User-Agent': useragent}, timeout = 10)
                        except:
                            print(colored("[*] Timed out while trying to the database server, please run the tool again.", "red"))
                            sys.exit(1)
                        print("\nDone!\n")
                        with open("filesize.txt", "w") as filesize:
                            filesize.write(response.headers['Content-Length'])
                    else: pass

def extract_asn(organization):
    #read csv, and split on "," the line
    asn_ipv4 = csv.reader(open('GeoLite2-ASN-Blocks-IPv4.csv', "r"), delimiter=",")
    #loop through csv list
    for row in asn_ipv4:
        #if current rows 2nd value is equal to input, print that row
        if organization.upper().replace('_', ' ') in row[2].upper():
            return(row[1])


def extract_ip(asn, organization):

    path_ipv6 = os.path.dirname(os.path.realpath(__file__)) + "/output/" + organization + "_ipv6.txt"
    path_ipv4 = os.path.dirname(os.path.realpath(__file__)) + "/output/" + organization + "_ipv4.txt"

    if asn:
        if not os.path.exists("output"):
            os.makedirs("output")
        elif os.path.isfile('./output/' + organization + '.txt') == True:
            os.system('cd ./output/ && rm -f ' + organization + '.txt')
        else:
            pass

        ipinfo = "https://ipinfo.io/"

        try:
            response = requests.get(ipinfo + "AS" + asn)
        except:
            print(colored("[*] Timed out while trying to the ASN lookup server, please run the tool again.", "red"))
            sys.exit(1)

        html = response.content
        soup = BeautifulSoup(html, 'html.parser')
        ipv6 = []
        ipv4 = []
        for link in soup.find_all('a'):
            if asn in link.get('href'):
                search_criteria = '/' + "AS" + asn + '/'
                ip = re.sub(search_criteria, '', link.get('href'))
                if "robtex" not in ip:
                    if ":" in ip:
                        ipv6.append(ip)
                    else: ipv4.append(ip)
                else: pass

        print(colored("[*] IP addresses owned by {} are the following (IPv4 or IPv6):".format(organization),"green"))

        if ipv4:
            print(colored("\n[*] IPv4 addresses saved to: ", "green"))
            print(colored("{}\n".format(path_ipv4), "yellow"))
            with open("./output/" + organization + "_ipv4.txt", "w") as dump:
                for i in ipv4:
                    dump.write(i + "\n")
                    print(colored(i, "yellow"))

        if ipv6:
            print(colored("\n[*] IPv6 addresses saved to: ", "green"))
            print(colored("{}\n".format(path_ipv6), "yellow"))
            with open("./output/" + organization + "_ipv6.txt", "w") as dump:
                for i in ipv6:
                    dump.write(i + "\n")
                    print(colored(i, "yellow"))
    else:
        print(colored("[*] Sorry! We couldn't find the organization's ASN and IP addresses.", "red"))

def scanning(n, m, organization):
    # Only allow one scanner choice
    if n and m:
    	print(colored("\n[*] Please only select one port scanner: -m --> Masscan or -n --> Nmap.", "red"))

    # Run Nmap on the IP addresses if -m argument is set
    elif n:
        if os.path.isfile("./output/" + organization + '_ipv4.txt') == True:
            print(colored("\n[*] Running port scanning using Nmap on IPV4 ...", "red"))
            os.system("nmap {} -iL {}".format(n, "./output/" + organization + "_ipv4.txt"))

            if os.path.isfile("./output/" + organization + '_ipv6.txt') == True:
                print(colored("\n[*] Running port scanning using Nmap on IPV6 ...\n", "red"))
                os.system("nmap {} -iL {}".format(n, "./output/" + organization + "_ipv6.txt"))
        else: pass

    # Run Masscan on the IP addresses if -m argument is set
    elif m:
    	if os.path.isfile("./output/" + organization + '_ipv4.txt') == True:
        	print(colored("\n[*] Running port scanning using Masscan (Warning: supports only IPV4)...", "red"))
        	os.system("masscan {} -iL {}".format(m, "./output/" + organization + "_ipv4.txt"))
    else: pass

if __name__ == '__main__':
    banner()
    nmapscan = parse_args().nmapscan
    masscan = parse_args().masscan
    org = parse_args().org \
                        .replace(' ', '_')
    check_licensekey()
    download_db()
    extract_ip(extract_asn(org), org)
    scanning(nmapscan, masscan, org)
