import sys
import json
import os
from kit import utils
from os.path import dirname, join


def format_csv(timestamp):

    data_json = '../data/{}.subject.json'.format(timestamp)
    data_dir = '../data/{}'.format(timestamp)
    out_csv = '../data/{}.csv'.format(timestamp)
    data = utils.load_json(data_json, verbose=True)
    url_with_subj = dict()
    for subj in data:
        for url in data[subj]:
            url_with_subj[url] = subj

    utils.qprint('writing ' + out_csv)
    fout = open(out_csv, 'w')
    for fname in os.listdir(data_dir):
        journal = fname.split('/')[-1].replace('.html', '').lower()
        fname = join(data_dir, fname)
        jdata = utils.load_json(fname, verbose=False)
        if jdata['url'] in url_with_subj:
            subj = url_with_subj[jdata['url']]
        else:
            subj = 'unknown'
        print(subj, journal,
              jdata['title'].replace(',',''),
              jdata['impact']['2016/2017']['ifact'],
              jdata['impact']['2015']['ifact'],
              jdata['impact']['2014']['ifact'],
              jdata['impact']['2016/2017']['npub'],
              jdata['impact']['2015']['npub'],
              jdata['impact']['2014']['npub'],
              jdata['title_abbrev'].replace(',',''),
              jdata['issn'].replace(',',''),
              jdata['url'], sep=',', file=fout)

    for subj in sorted(data):
        for url in sorted(data[subj]):
            journal = url.split('/')[-1].replace('.html', '').lower()
            fname = '{}/{}.json'.format(data_dir, journal)
    fout.close()

if __name__ == '__main__':

    timestamp = sys.argv[1]
    format_csv(timestamp)
