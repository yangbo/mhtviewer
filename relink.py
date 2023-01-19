#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from extract import Extract

RID="PRComment"
REVIEWER="User F"

def tadd(p,t): 
    p.contents.append(t)
    return p

def relink(ex, reviewer):
    def mktg(name): return ex.soup.new_tag(name)

    links = ex.soup.new_tag('ol')
    rtags = ex.get_all('b', string=reviewer)
    for i, tag in enumerate(rtags):
        n = i+1
        tag['id'] = f'{RID}_{n:03}'
        tag.string = f'{RID} #{n:03}. {tag.string}'

        link = mktg('a')
        link['href'] = f'#{tag["id"]}'
        link.string = tag.string

        item = tadd(mktg('li'), link)
        tadd(links, item)

    toc = mktg('div')
    toc['id'] = f'{RID}_TOC'
    toc.string = "List of {RID}s"
    body = ex.get('body')
    body.contents.insert(0, tadd(toc, links))
    return ex

def main():
    args = sys.argv
    if len(args) != 2:
        print("Usage: ./relink.py <mht file>")
        return
    mht = sys.argv[1]
    log('Extract multi-part of "%s" ...' % mht)
    parsed = Extract(mht)
    relink(ex, REVIEWER)

if __name__ == '__main__':
    main()
