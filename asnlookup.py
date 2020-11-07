#!/usr/bin/python

import sys
import json
import argparse
import requests
import os
from termcolor import colored
requests.packages.urllib3.disable_warnings()

API = 'http://asnlookup.com/api/lookup?org='
headers = {
    'User-Agent': 'ASNLookup PY/Client'
    }

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
    nmapscan = parser.add_argument('-n', '--nmapscan', help='Run Nmap port scanning.', required=False, action='store', nargs='?', const='-p 1-65535 -T4 -A -v')
    masscan = parser.add_argument('-m', '--masscan', help='Run Masscan port scanning.', required=False, action='store', nargs='?', const='-p0-65535 --rate 200')
    return parser.parse_args()

def get_ip_space(organization):
    # retrieve ip space from asnlookup.com
    try:
        response = requests.get(API + organization.replace('_', ' '), headers = headers, timeout = 10)
        ip_space = json.loads(response.text)
    except:
        print(colored('[!] We couldn\'t connect to asnlookup.com API. Try again!', 'red'))
        sys.exit(1)

    if ip_space:
        path_ipv6 = os.path.dirname(os.path.realpath(__file__)) + '/output/' + organization + '_ipv6.txt'
        path_ipv4 = os.path.dirname(os.path.realpath(__file__)) + '/output/' + organization + '_ipv4.txt'
        ipv4_exist =  False
        ipv6_exist =  False

        if not os.path.exists('output'):
            os.makedirs('output')
        elif os.path.isfile('./output/' + organization + '.txt') == True:
            os.system('cd ./output/ && rm -f ' + organization + '.txt')

        for ip in ip_space:
            if ':' not in ip:
                with open('./output/' + organization + '_ipv4.txt', 'a') as dump:
                    dump.write(ip + '\n')
                    print(colored(ip, 'yellow'))
                    ipv4_exist =  True
            else:
                with open('./output/' + organization + '_ipv6.txt', 'a') as dump:
                    dump.write(ip + '\n')
                    print(colored(ip, 'yellow'))
                    ipv6_exist =  True

        if ipv4_exist is True:
            print(colored('\nIPv4: {}'.format(path_ipv4), 'green'))
        if ipv6_exist is True:
            print(colored('\nIPv6: {}'.format(path_ipv6), 'green'))

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
    banner()
    nmapscan = parse_args().nmapscan
    masscan = parse_args().masscan
    org = parse_args().org \
                            .replace(' ', '_')
    get_ip_space(org)
    scanning(nmapscan, masscan, org)
