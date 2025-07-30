#!/usr/bin/python3

import os
import sys
import json
import argparse
import requests
from termcolor import colored

requests.packages.urllib3.disable_warnings()

def banner():
        print('''
        ____ ____ _  _ _    ____ ____ _  _ _  _ ___
        |__| [__  |\ | |    |  | |  | |_/  |  | |__]
        |  | ___] | \| |___ |__| |__| | \_ |__| |
                        asnlookup.com
         Author: Yassine Aboukir (@yassineaboukir)\n''')

def parse_args():
    # parse the argument
    parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' + sys.argv[0] + ' -o twitter')
    org = parser.add_argument('-o', '--org', help='Organization to look up.', required=True)
    apikey = parser.add_argument('-k', '--apikey', help='API key.', required=True)
    nmapscan = parser.add_argument('-n', '--nmapscan', help='Run Nmap port scanning.', required=False, action='store', nargs='?', const='-p 1-65535 -T4 -A -v')
    masscan = parser.add_argument('-m', '--masscan', help='Run Masscan port scanning.', required=False, action='store', nargs='?', const='-p0-65535 --rate 200')
    return parser.parse_args()

def get_ip_space(organization,apikey):
    # retrieve ip space from asnlookup.com
    API_URL = 'https://asn-lookup.p.rapidapi.com/api?orgname='

    headers = {
        'User-Agent': 'ASNLookup PY/Client',
        'X-Rapidapi-Key': apikey,
    }

    try:
        response = requests.get(API_URL + organization.replace('_', ' '), headers = headers, timeout = 10)
        # print(response)
        ip_space = json.loads(response.text)
        # print(ip_space)
    except:
        print(colored('[!] We couldn\'t connect to asnlookup.com API. Try again!', 'red'))
        sys.exit(1)

    if ip_space and len(ip_space):
        path_ipv6 = os.path.dirname(os.path.realpath(__file__)) + '/output/' + organization + '_ipv6.txt'
        path_ipv4 = os.path.dirname(os.path.realpath(__file__)) + '/output/' + organization + '_ipv4.txt'

        if not os.path.exists('output'):
            os.makedirs('output')
        elif os.path.isfile('./output/' + organization + '.txt') == True:
            os.system('cd ./output/ && rm -f ' + organization + '.txt')

        for item in ip_space:
            # print(item)
            # print(item['ipv4_prefix'])
            if item['ipv4_prefix'] and len(item['ipv4_prefix']):
                # print("\n".join(item['ipv4_prefix']))
                ipv4_str = "\n".join(item['ipv4_prefix'])
                print(ipv4_str)
                with open('./output/' + organization + '_ipv4.txt', 'a') as dump:
                    dump.write(ipv4_str+"\n")

            if item['ipv6_prefix'] and len(item['ipv6_prefix']):
                # print("\n".join(item['ipv6_prefix']))
                ipv6_str = "\n".join(item['ipv6_prefix'])
                print(ipv6_str)
                with open('./output/' + organization + '_ipv6.txt', 'a') as dump:
                    dump.write(ipv6_str+"\n")
    else:
        print(colored('[!] Sorry! We couldn\'t find the organization\'s ASN.', 'red'))

def scanning(n, m, organization):
    # Only allow one scanner choice
    if n and m:
    	print(colored('\n[*] Please only select one port scanner: -m --> Masscan or -n --> Nmap.', 'red'))

    # Run Nmap on the IP addresses if -m argument is set
    elif n:
        if os.path.isfile('./output/' + organization + '_ipv4.txt') == True:
            print(colored('\n[*] Running port scanning with Nmap on IPV4 ...', 'red'))
            os.system('nmap {} -iL {}'.format(n, './output/' + organization + '_ipv4.txt'))

            if os.path.isfile('./output/' + organization + '_ipv6.txt') == True:
                print(colored('\n[*] Running port scanning with Nmap on IPV6 ...\n', 'red'))
                os.system('nmap {} -iL {}'.format(n, './output/' + organization + '_ipv6.txt'))
        else: pass

    # Run Masscan on the IP addresses if -m argument is set
    elif m:
    	if os.path.isfile('./output/' + organization + '_ipv4.txt') == True:
        	print(colored('\n[*] Running port scanning with Masscan (Warning: only supports IPV4) ...', 'red'))
        	os.system('masscan {} -iL {}'.format(m, './output/' + organization + '_ipv4.txt'))
    else: pass

if __name__ == '__main__':
    # banner()
    parser = parse_args()
    nmapscan = parser.nmapscan
    masscan = parser.masscan
    org = parser.org.replace(' ', '_')
    apikey = parser.apikey
    get_ip_space(org,apikey)
    scanning(nmapscan, masscan, org)
