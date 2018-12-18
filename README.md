        ____ ____ _  _ _    ____ ____ _  _ _  _ ___
        |__| [__  |\ | |    |  | |  | |_/  |  | |__]
        |  | ___] | \| |___ |__| |__| | \_ |__| |

          Author: Yassine Aboukir (@yassineaboukir)
   
 ## Description
>An autonomous system number (ASN) is a unique number assigned to an autonomous system (AS) by the Internet Assigned Numbers Authority (IANA).
An AS consists of blocks of IP addresses which have a distinctly defined policy for accessing external networks and are administered by a single organization

This tool will search an updated database for a specific organization's ASN then use the latter to look up all IP addresses (IPv4 and IPv6) registered and owned by the organization.

## Objective
This script should be used during reconnaissance phase to identify properties owned by the company, and run a port scan on it to identify open ports and publicly exposed services.

## Usage
Tested on Python >= 2.7.
```
$ git clone https://github.com/yassineaboukir/Asnlookup && cd Asnlookup
$ pip install -r requirements.txt
$ python asnlookup.py -o <Organization>
```

## Port Scanning
The tool exports the list of IP addresses as a text file which you can use with other tools such as Masscan. On the other hand, the tool supports Nmap port scanning but it requires you to already have Nmap installed on your machine. How to?

```
- On CentOS

yum install nmap

- On Debian

apt-get install nmap

- On Ubuntu

sudo apt-get install nmap

- Mac OS

brew install nmap
```

To scan the IP addresses, add `-s` arugment to the command:

```
$ python asnlookup.py -s -o <Organization>
```

You can also pass your own Nmap arguments `(Default: -p 1-65535 -T4 -A -v)`.

```
$ python asnlookup.py -s "<Nmap arguments>" -o <Organization>
```

E.g:

```
$ python asnlookup.py -s "--top-ports 65535" -o twitter
```

It will export the result to a text file in the same directory as the script `(E.g: ./twitter.txt)` then run Nmap as follows:

<img src="https://yassineaboukir.com/asnlookup2.png" width="400" height="300" />

## Limitation
For smaller organizations the ASN will usually be that of their ISP whereas the hostname might not. One example of this is 207.97.227.245, a GitHub IP address. The ASN is AS27357 (Rackspace Hosting), but the hostname is pages.github.com.
