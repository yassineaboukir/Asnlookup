        ____ ____ _  _ _    ____ ____ _  _ _  _ ___
        |__| [__  |\ | |    |  | |  | |_/  |  | |__]
        |  | ___] | \| |___ |__| |__| | \_ |__| |

          Author: Yassine Aboukir (@yassineaboukir)
   
 ## Description
>An autonomous system number (ASN) is a unique number assigned to an autonomous system (AS) by the Internet Assigned Numbers Authority (IANA).
An AS consists of blocks of IP addresses which have a distinctly defined policy for accessing external networks and are administered by a single organization

This tool will search an updated database for a specific organization's ASN then use the latter to look up all IP addresses (IPv4) registered and owned by the organization.

## Objective
This script should be used during reconnaissance phase to identify properties owned by the company and later use Nmap, Masscan or any other tool to scan for all open TCP ports. For what it's worth, integrating Nmap in the script to automatically scan the IP address block is in the roadmap but any help is highly appreciated.

## Usage
```
$ git clone https://github.com/yassineaboukir/asnlookup && cd asnlookup
$ pip install -r requirements.txt
$ python asnlookup.py -o <Organization>
```

E.g:

```
$ python asnlookup.py -o Twitter
```

Should return:

<img src="https://yassineaboukir.com/asnlookup.png" width="400" height="200" />

## Limitation
For smaller organizations the ASN will usually be that of their ISP whereas the hostname might not. One example of this is 207.97.227.245, a GitHub IP address. The ASN is AS27357 (Rackspace Hosting), but the hostname is pages.github.com.
