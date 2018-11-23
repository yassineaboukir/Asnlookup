#!/usr/bin/python

import csv, sys, argparse, requests, re, os
from termcolor import colored
from bs4 import BeautifulSoup

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
    scan = parser.add_argument('-s', '--scan', help="Run Nmap", required=False, action="store", nargs='?', const="-p 1-65535 -T4 -A -v")
    return parser.parse_args()

def download_db():
    # Download a local copy of ASN database from maxmind.com
    if os.path.isfile('./GeoIPASNum2.csv') == False:
        print(colored("Downloading ASN database ...\n", "red"))
        os.system("wget http://download.maxmind.com/download/geoip/database/asnum/GeoIPASNum2.zip && unzip GeoIPASNum2.zip && rm -f GeoIPASNum2.zip")
        print(colored("\nDone!\n", "red"))

        # Extracting and saving database file size locally
        try:
            response = requests.get("http://download.maxmind.com/download/geoip/database/asnum/GeoIPASNum2.zip")
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)

        with open("filesize.txt", "w") as filesize:
            filesize.write(response.headers['Content-Length'])
    else:
        # Checking if there is a new database change and download a new copy if applicable
        response = requests.get("http://download.maxmind.com/download/geoip/database/asnum/GeoIPASNum2.zip")
        with open("filesize.txt", "r") as filesize:
            for line in filesize:
                if line == response.headers['Content-Length']:
                    pass
                else:
                    print(colored("[i] It seems like you have not updated the database.","red"))
                    choice = input(colored("[?] Do you want to update now? [Y]es [N]o, default: [N]", "red"))
                    if choice.upper() == "Y":
                        print(colored("Downloading a new copy of the database ...\n","red"))
                        os.system("wget -O GeoIPASNum2.zip http://download.maxmind.com/download/geoip/database/asnum/GeoIPASNum2.zip && unzip GeoIPASNum2.zip && rm -f GeoIPASNum2.zip")

                        try:
                            response = requests.get("http://download.maxmind.com/download/geoip/database/asnum/GeoIPASNum2.zip")
                        except requests.exceptions.RequestException as e:
                            print(e)
                            sys.exit(1)

                        print("\nDone!\n")
                        with open("filesize.txt", "w") as filesize:
                            filesize.write(response.headers['Content-Length'])
                    else: pass

def extract_asn(organization):
    #read csv, and split on "," the line
    csv_file = csv.reader(open('GeoIPASNum2.csv', "r"), delimiter=",")
    #loop through csv list
    for row in csv_file:
        #if current rows 2nd value is equal to input, print that row
        if organization in row[2] or organization.title() in row[2]:
            asn = row[2].split(' ', 1)[0]
            return(asn)

def extract_ip(asn, organization):
    if asn is not None:
        ipinfo = "https://ipinfo.io/"
        try:
            response = requests.get(ipinfo + asn)
        except requests.exceptions.RequestException as e:
            print(e)
            sys.exit(1)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')
        ip_addresses = []
        for link in soup.find_all('a'):
            if asn in link.get('href'):
                lookfor = '/'+asn+'/'
                ip = re.sub(lookfor, '', link.get('href'))
                ip_addresses.append(ip)
        print(colored("IP addresses owned by {} are the following:\n".format(organization),"red"))
        for i in ip_addresses:
            # Exporting the result to a txt file
            with open(organization + ".txt", "a") as export:
                export.write(i + "\n")
            print(colored(i, "yellow"))
        print("\n")
    else:
        print(colored("Sorry! We couldn't find the organization's ASN and IP addresses.", "red"))

def nmap(scan, organization):
    # Run Nmap on the IP addresses if -s argument is set
    if scan is not None:
        print(colored("Running port scanning using Nmap ...\n", "red"))
        os.system("nmap {} -iL {}".format(scan, organization + ".txt"))
    else: pass

if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings()
    banner()
    org = parse_args().org
    scan = parse_args().scan
    download_db()
    extract_ip(extract_asn(org), org)
    nmap(scan, org)
