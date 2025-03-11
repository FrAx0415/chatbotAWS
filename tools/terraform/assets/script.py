#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This is a helper tool
   to generate `terraformer` plan files on per-zone basis
   for AWS Route53 service.
   Follow these instructions to generate the global plan file
   and then feed it to the script to create separate plans:
   https://github.com/GoogleCloudPlatform/terraformer#planning
"""

import os
import sys
import json
import collections

def makeZoneMap(plan):
    zoneMap = {}
    print("Creating map of Route53 zone...")
    for res in plan['ImportedResource']['route53']:
        if res['InstanceInfo']['Type'] == 'aws_route53_zone':
            zoneName = res['InstanceState']['attributes']['name']
            zoneId = res['InstanceState']['attributes']['zone_id']
            zoneMap[zoneId] = zoneName
    return zoneMap

def makeZoneFiles(plan, zoneMap):
    zoneRecordsMap = collections.defaultdict(list)
    print("Parsing Route53 records...")
    for res in plan['ImportedResource']['route53']:
        recordZoneId = res['InstanceState']['attributes']['zone_id']
        zoneRecordsMap[recordZoneId].append(res)
    print("Generating resulting per-zone plan files...")
    for zone in zoneMap.keys():
        zoneFilesMap = dict(plan)
        zoneFilesMap['ImportedResource']['route53'] = zoneRecordsMap[zone]
        with open('{}.plan.json'.format(zoneMap[zone].translate({ ord(c): '_' for c in ".-" })), 'w') as outFile:
            outFile.write(json.dumps(zoneFilesMap, indent=2))

def main():
    if not (os.path.exists('plan.json')):
        print("No plan.json file found in current directory!")
        sys.exit(1)
    else:
        print("Parsing plan.json ...")
        with open('plan.json', 'r') as planFile:
            plan = json.load(planFile)
    zoneMap = makeZoneMap(plan)
    makeZoneFiles(plan, zoneMap)

if __name__ == "__main__":
    main()
