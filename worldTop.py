#!/usr/bin/env python3

import csv
import requests
import sys
from pprint import pprint

regions = {}

with open('data/countries.csv', newline='') as csvfile:
    
    has_header = csv.Sniffer().has_header(csvfile.read(1024))
    csvfile.seek(0)
    countries = csv.reader(csvfile)
    
    if has_header:
        next(countries)

    for country in countries:
        print("-------------")
        print("{}".format(country[0]))
        print("-------------")
        sys.stdout.flush()
        url = "https://stat.ripe.net/data/country-asns/data.json?resource=" + country[1] + "&lod=1"

        r = requests.get(url)

        resources = r.json()

        neighbour_count = {}

        q = requests.Session()

        for asn in resources['data']['countries'][0]['routed']:

            url = "https://stat.ripe.net/data/asn-neighbours/data.json?resource=" + asn

            r2 = q.get(url)

            neighbours = r2.json()

            neighbour_count[asn] = neighbours['data']['neighbour_counts']['right']

        sorted_asns = sorted(neighbour_count.items(), key=lambda item: item[1], reverse=True)

        i = 0
        while i < 5 :
    
            try:
                asn = sorted_asns[i]
                url = "https://stat.ripe.net/data/as-overview/data.json?resource=" + asn[0]
                r3 = q.get(url)

                asn_details = r3.json()

                print("AS{} - {}, with {} downstream neighbours".format(asn[0], asn_details['data']['holder'], asn[1]))
                region = country[6]
                as_number = asn[0]
                if region not in regions.keys():
                    regions[region] = {}

                regions[region][as_number] = asn[1]
            except:
                pass

            i +=1 

for region in regions:
    
    print(region)

    sorted_asns = sorted(region.items(), key=lambda item: item[1], reverse=True)

    while i < 5 :
    
            try:
                asn = sorted_asns[i]
                url = "https://stat.ripe.net/data/as-overview/data.json?resource=" + asn[0]
                r3 = q.get(url)

                asn_details = r3.json()

                print("AS{} - {}, with {} downstream neighbours".format(asn[0], asn_details['data']['holder'], asn[1]))
                region = country[6]
                as_number = asn[0]
                if region not in regions.keys():
                    regions[region] = {}

                regions[region][as_number] = asn[1]
            except:
                pass

            i +=1

pprint(regions)
