#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from extract import Extract

RID="PRComment"
RID_TOC=f'{RID}_TOC'

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
    toc['id'] = RID_TOC
    toc.string = f"List of {RID}s"
    sibling = ex.get("div", {"data-test": "review__header"})
    assert sibling
    sibling.insert_before(tadd(toc, links))
    return ex

def main():
    args = sys.argv
    if len(args) != 3:
        print("Usage: ./relink.py <mht file> <reviewer>")
        return
    mht = sys.argv[1]
    reviewer = sys.argv[2]
    print('Extract multi-part of "%s" ...' % mht)
    ex = Extract(mht)
    print('Adding links for "%s" ...' % reviewer)
    relink(ex, reviewer)
    ex.save()

if __name__ == '__main__':
    main()
