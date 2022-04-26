                                ____ ____ _  _ _    ____ ____ _  _ _  _ ___
                                |__| [__  |\ | |    |  | |  | |_/  |  | |__]
                                |  | ___] | \| |___ |__| |__| | \_ |__| |
                                              asnlookup.com
                                         Author: Yassine Aboukir
 
 <p align="center"><a target="_blank" href="https://twitter.com/yassineaboukir"><img src="https://img.shields.io/twitter/follow/yassineaboukir.svg?logo=twitter"></a></p>
 
## *Notice:* The python client is being refactored but you can use asnlookup.com web service or its free/paid API at the moment

 ## Description
>An autonomous system number (ASN) is a unique number assigned to an autonomous system (AS) by the Internet Assigned Numbers Authority (IANA).
An AS consists of blocks of IP addresses which have a distinctly defined policy for accessing external networks and are administered by a single organization

This is a python client which leverages our asnlookup.com [free API](http://asnlookup.com/api) to find the IP space (IPv4 and IPv6) registered and owned by a specific organization. 

ASNLookup searches for the organization ASNs and use the latter to find the IP space. You can also use asnlookup client to run port scanning on the IP space using `Nmap` or `Masscan`.

Check out http://asnlookup.com/ for easy use and for the API.

## Usage
```
$ git clone https://github.com/yassineaboukir/Asnlookup && cd Asnlookup
$ pip install -r requirements.txt (or pip3 install -r requirements.txt if you're using Python3)
```

```
$ python asnlookup.py -o <Organization>
```

_E.g: python asnlookup.py -o "Capital One"_

## Port Scanning
The tool supports port scanning using Nmap or Masscan but requires prior installation on your machine. How to?

- For Nmap:

```
On CentOS
$ yum install nmap

- On Debian
$ apt-get install nmap

- On Ubuntu
$ sudo apt-get install nmap

- Mac OS
$ brew install nmap
```

- For Masscan *(Doesn't support IPv6 scanning):* refer to https://github.com/robertdavidgraham/masscan/

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

It will export the results to a text file in the output directory `(E.g: ./output/salesforce.txt)` then run Nmap.

## Limitation
For smaller organizations the ASN will usually be that of their ISP whereas the hostname might not. One example of this is 207.97.227.245, a GitHub IP address. The ASN is AS27357 (Rackspace Hosting), but the hostname is pages.github.com.

## Support
If you appreciate my work and wish to support it, feel free to: <a href="http://buymeacoffee.com/yassineaboukir"><img src="https://cdn-images-1.medium.com/max/738/1*G95uyokAH4JC5Ppvx4LmoQ@2x.png" width="150"></a>

## Disclaimer
This project is made for educational and ethical testing purposes only. Usage of this tool for attacking targets without prior mutual consent is illegal. Developers assume no liability and are not responsible for any misuse or damage caused by this tool.
