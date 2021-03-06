# -*- coding: utf-8 -*-

import os, sys, json
import gzip, requests, time

# -------------------------------------------------------------------------

def write_text(text, text_name, verbose=True):

    if verbose:
        qprint('write ' + text_name)
    if text_name.endswith('.gz'):
        fout = gzip.open(text_name, 'wb')
        fout.write((text+'\n').encode('utf-8'))
    else:
        fout = open(text_name, 'w')
        fout.write(text+'\n')
    fout.close()

# -------------------------------------------------------------------------

def read_text(text_name, verbose=True):

    if verbose:
        qprint('read ' + text_name)
    if text_name.endswith('.gz'):
        text = gzip.open(text_name).read().decode('utf-8')
    else:
        text = open(text_name).read()
    return text

# -------------------------------------------------------------------------

def get_timestamp(fmt_str="%Y%m%d%H%M"):

    timestamp = datetime.datetime.now().strftime(fmt_str)
    return timestamp

# -------------------------------------------------------------------------

def qprint(msg, verbose=True):
    print(':: ' + msg, file=sys.stderr, flush=True)

# -------------------------------------------------------------------------

def qopen(fname, mode='r', verbose=True):

    if verbose:
        if mode == 'w':
            qprint('writing {}'.format(fname))
        else:
            qprint('reading {}'.format(fname))

    return open(fname, mode)

# -------------------------------------------------------------------------

def write_json(data, json_name, verbose=True):
    if verbose:
        qprint('write ' + json_name)
    if json_name.endswith('.gz'):
        fout = gzip.open(json_name, 'wb')
        fout.write((json.dumps(data, sort_keys=True) + '\n').encode('utf-8'))
    else:
        fout = open(json_name, 'w')
        fout.write(json.dumps(data, sort_keys=True) + '\n')
    fout.close()

# -------------------------------------------------------------------------

def read_json(json_name, verbose=True):
    if verbose:
        qprint('read ' + json_name)
    if json_name.endswith('.gz'):
        data = json.loads(gzip.open(json_name).read().decode('utf-8'))
    else:
        data = json.loads(open(json_name).read())
    return data


# -------------------------------------------------------------------------

def down_public(in_name, out_dir, sleep_time=0):

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    todo_set = set()
    for line in qopen(in_name):
        url = line.rstrip()
        todo_set.add(url)

    while len(todo_set):
        failed_set = set()
        qprint('todo: {} urls to extract'.format(len(todo_set)))
        for url in sorted(todo_set):
            out_name = '{}/{}.html'.format(out_dir, url.split('//')[1])
            if os.path.isfile(out_name + '.gz'):
                continue
            tmp_out_dir = os.path.dirname(out_name)
            os.makedirs(tmp_out_dir, exist_ok=True)

            try:
                r = requests.get(url, headers=headers)
                write_text(r.text, out_name + '.gz')
                time.sleep(sleep_time)

            except Exception as e:
                print('*ERROR* failed to retrieve {}'.format(url))
                failed_set.add(url)

        todo_set = failed_set


if __name__ == '__main__':

    article_list = sys.argv[1]
    down_public(article_list, '../data/html/public', sleep_time=0)


# end
