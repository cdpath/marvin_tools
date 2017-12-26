# -*- coding: utf-8 -*-
import argparse
import csv
import datetime as dt
import locale
from collections import namedtuple

from marvin_tools.kindle import *
from . import __version__


def clean_bom(lines):
    encodings = ('utf-8-sig', 'gb2312', 'gbk', 'big5')
    for l in lines:
        for i, c in enumerate(encodings):
            try:
                s = l.decode(c)
                break
            except UnicodeDecodeError:
                if i == (len(encodings) - 1):
                    raise
        yield s.encode('utf-8')


def parse_marvin_time(t):
    locale.setlocale(locale.LC_TIME, "zh_CN")
    # todo support other timezone
    return dt.datetime.strptime(t, "%Y-%m-%dT%H:%M:%SZ") + dt.timedelta(hours=8)


def parse_marvin(f_name):
    with open(f_name) as f:
        f_csv = csv.reader(clean_bom(f))
        headers = next(f_csv)
        Journal = namedtuple('Journal', headers)
        for r in f_csv:
            idx = headers.index('Date')
            r[idx] = parse_marvin_time(r[idx])
            yield Journal(*r)


def convert(marvin_f, kindle_f, output_f):
    if kindle_f:
        meta = next(parse_marvin(marvin_f))
        loc_bounds = parse_loc_bounds(kindle_f, meta.Title, meta.Author)
    else:
        loc_bounds = None

    with open(output_f, 'w') as f:
        clippings = [str(Clipping.create_clipping_from_marvin(row, loc_bounds))
                     for row in parse_marvin(marvin_f)]
        f.writelines(clippings)


def get_parser():
    parser = argparse.ArgumentParser(description="Convert Marvin CSV to My Clippings.txt")
    parser.add_argument('-m', '--marvin', help='Journal.csv exported via Marvin', dest='marvin', action='store')
    parser.add_argument('-k', '--kindle', help='My Clippings.txt found in Kindle', dest='kindle', action='store')
    parser.add_argument('-o', '--output', dest='output', default='./My Clippings.txt', action='store')
    parser.add_argument('-v', '--version', help='displays the current version of Marvin tools', action='store_true')
    return parser


def command_line_runner():
    parser = get_parser()
    args = vars(parser.parse_args())

    if args['version']:
        print(__version__)
        return

    if not args['marvin']:
        parser.print_help()
        return

    if not args['marvin'].endswith('csv'):
        print('Error: re-export journal in csv')
        return

    convert(args['marvin'], args['kindle'], args['output'])
    print("Saved to %s" % args['output'])


if __name__ == '__main__':
    command_line_runner()
