# -*- coding: utf-8 -*-
import datetime as dt
import locale
import re

__all__ = ['Clipping', 'parse_loc_bounds']


def convert_to_chinese_time(t):
    locale.setlocale(locale.LC_TIME, "zh_CN")
    fmt = u"%Y年%m月%d日星期%a %p%I:%M:%S"
    return t.strftime(fmt.encode('utf-8'))


class Clipping(object):
    def __init__(self, title, author, page, loc, time, highlight, note):
        self.title = title
        self.author = author
        self.page = page
        self.loc = loc
        self.time = convert_to_chinese_time(time)
        self.highlight = highlight
        self.note = note

    @classmethod
    def create_clipping_from_marvin(cls, csv_row, loc_bounds=None):
        if loc_bounds:
            loc = cls.find_nearest_loc(csv_row.Date, loc_bounds)
            page, loc = loc['page'], loc['locs']
        else:
            page, loc = 0, (0, 0)
        clipping = cls(
            title=csv_row.Title,
            author=csv_row.Author,
            time=csv_row.Date,
            highlight=csv_row.HighlightText,
            note=csv_row.EntryText,
            page=page,
            loc=loc,
        )
        return clipping

    @classmethod
    def find_nearest_loc(cls, _time, loc_bounds):
        loc_bound = min(loc_bounds,
                        key=lambda x: abs(x['time'] - _time))
        return loc_bound

    def __repr__(self):
        # todo support en_US template
        template = """{Title} ({Author})
- 您在第 {Page} 页（位置 #{Loc}）的标注 | 添加于 {Time}

{HighlightText}
==========
"""
        return template.format(
            Title=self.title,
            Author=self.author,
            Page=self.page,
            Loc='%s-%s' % self.loc,
            Time=self.time,
            HighlightText=self.highlight
        )


def parse_kindle_time(meta_line):
    # local timezone
    time_str = meta_line.split('|')[-1]
    is_en = time_str.find('Added on') >= 0
    if is_en:
        locale.setlocale(locale.LC_TIME, "en_US")
        t = dt.datetime.strptime(time_str.strip(), 'Added on %A, %B %d, %Y %I:%M:%S %p')
        pos = re.findall(r"(?:page (\d+) .*?)?(\d+)-(\d+)", meta_line)[0]
    else:
        locale.setlocale(locale.LC_TIME, "zh_CN")
        t = dt.datetime.strptime(time_str.strip(), '添加于 %Y年%b月%d日%A %p%I:%M:%S')
        pos = re.findall(r"您在(?:第 (\d+) 页（)?位置 #(\d+)(?:-(\d+))?(）)?的(?:笔记|标注)", meta_line)[0]

    page, locs = pos[0], pos[1:]
    return page, locs, t


def parse_loc_bounds(kindle_f, title, author):
    key = '%s (%s)' % (title, author)
    with open(kindle_f) as f:
        lines = iter(f.readlines())

    items = []
    for line in lines:
        if line.find(key) >= 0:
            page, locs, t = parse_kindle_time(next(lines))
            items.append({'time': t, 'locs': locs, 'page': page})
    items.sort(key=lambda x: x['time'])
    return items
