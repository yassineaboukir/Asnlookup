                                ____ ____ _  _ _    ____ ____ _  _ _  _ ___
                                |__| [__  |\ | |    |  | |  | |_/  |  | |__]
                                |  | ___] | \| |___ |__| |__| | \_ |__| |

                                         Author: Yassine Aboukir
 
 <p align="center"><a target="_blank" href="https://twitter.com/yassineaboukir"><img src="https://img.shields.io/twitter/follow/yassineaboukir.svg?logo=twitter"></a></p>

 ## Description
>An autonomous system number (ASN) is a unique number assigned to an autonomous system (AS) by the Internet Assigned Numbers Authority (IANA).
An AS consists of blocks of IP addresses which have a distinctly defined policy for accessing external networks and are administered by a single organization

This tool will search an updated database for a specific organization's ASN then use the latter to look up all IP addresses (IPv4 and IPv6) registered and owned by the organization.

A web application version of this tool which was built with Flask is live on http://asnlookup.com/

## Objective
This script should be used during reconnaissance phase to identify properties owned by the company, and run a port scan on it to identify open ports and publicly exposed services.

## Usage
- Tested on Python >= 2.7 and Python 3.5. Execute the following:
```
$ git clone https://github.com/yassineaboukir/Asnlookup && cd Asnlookup
$ pip install -r requirements.txt (or pip3 install -r requirements.txt if you're using Python3)
```

- Sign up for a free account on Maxmind: `https://www.maxmind.com/en/geolite2/signup`
- Sign in and browse to `https://www.maxmind.com/en/accounts/1` > `My License Key` > `Generate new license key` > Check `No` for `Will this key be used for GeoIP Update?`.
- Open `config.py` with a text editor, and replace `key_here` placeholder with the license key you generated.

To use, execute: 

```
$ python asnlookup.py -o <Organization>`
```

## Port Scanning
The tool exports the list of IP addresses as a text file which you can use with other tools such as Masscan. On the other hand, the tool supports Nmap and Masscan port scanning but it requires you to already have both installed on your machine. How to?

- For Nmap:

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

- For Masscan: **NOTE THAT MASSCAN DOESN'T SUPPORT IPV6 PORT SCANNING**

Please refer to https://github.com/robertdavidgraham/masscan/

To scan the IP addresses, append to the command `-m` arugment for Masscan or `-n` for Nmap:

```
$ python asnlookup.py -m -o <Organization>
```

You can also pass your own Nmap/Masscan arguments (Default for nmap: `-p 1-65535 -T4 -A -v`; default for Masscan: `-p0-65535 --rate 200`).

```
$ python asnlookup.py -m="<Masscan arguments>" -o <Organization>
```

Example using Nmap with custom arguments:

```
$ python asnlookup.py -n="--top-ports 65535" -o twitter
```

It will export the result to a text file in the output directory `(E.g: ./output/salesforce.txt)` then run Nmap.

## Limitation
For smaller organizations the ASN will usually be that of their ISP whereas the hostname might not. One example of this is 207.97.227.245, a GitHub IP address. The ASN is AS27357 (Rackspace Hosting), but the hostname is pages.github.com.

## Support
If you appreciate my work and wish to support it, feel free to: <a href="http://buymeacoffee.com/yassineaboukir"><img src="https://cdn-images-1.medium.com/max/738/1*G95uyokAH4JC5Ppvx4LmoQ@2x.png" width="150"></a>

