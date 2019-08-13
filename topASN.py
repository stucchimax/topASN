#!/usr/bin/env python3

import requests
import argparse
from pprint import pprint

parser = argparse.ArgumentParser(description='A script to generate statistics about the ASNs with the highest number of downstream customers in a given country')

parser.add_argument("country", help="the country (in ISO 2-letter format)")

args = parser.parse_args()

url = "https://stat.ripe.net/data/country-asns/data.json?resource=" + args.country + "&lod=1"

r = requests.get(url)

resources = r.json()

#pprint(resources)

neighbour_count = {}

q = requests.Session()

for asn in resources['data']['countries'][0]['routed']:

    url = "https://stat.ripe.net/data/asn-neighbours/data.json?resource=" + asn

    r2 = q.get(url)

    neighbours = r2.json()

    neighbour_count[asn] = neighbours['data']['neighbour_counts']['right']

hello = sorted(neighbour_count.items(), key=lambda item: item[1], reverse=True)

i = 0
while i < 5 :
    
    asn = hello[i]

    url = "https://stat.ripe.net/data/as-overview/data.json?resource=" + asn[0]

    r3 = q.get(url)

    asn_details = r3.json()

    print("AS{} - {}, with {} downstream neighbours".format(asn[0], asn_details['data']['holder'], asn[1]))

    i +=1
