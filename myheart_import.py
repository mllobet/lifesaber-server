#!/usr/bin/env python2.7

import argparse

from pymongo import MongoClient

def run(infile):
    client = MongoClient()
    db = client.lifesaber
    c = db.aed
    with open(infile, 'r') as f:
        aeds = eval(f.read()) # top kek
        in_aeds = []
        for aed in aeds['results']:
            aed['loc'] = {'type':'Point', 'coordinates':[aed['loc'][1], aed['loc'][0]]}
            c.insert(aed)

        c.ensure_index([('loc', '2dsphere')])

    c = db.watches
    c.ensure_index([('loc', '2dsphere')])


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="imports db dump from myheart");
    parser.add_argument('-i', '--in-file', default='./pretty_dump.json')

    args = parser.parse_args()
    run(args.in_file)
