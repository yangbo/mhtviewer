#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from extract import Extract

RID="PRComment"
RID_TOC=f'{RID}_TOC'
RID_PARENT='caUSsX'

def tadd(p,t): 
    p.contents.append(t)
    return p

def relink(ex, review_tag):
    def mktg(name): return ex.soup.new_tag(name)

    links = ex.soup.new_tag('ul')
    rtags = ex.get_all(review_tag)
    for i, tag in enumerate(rtags):
        rid = f'{RID}_{(i+2):03}'
        tag['id'] = rid
        tag.string = f'{rid}. {tag.string}'

        link = mktg('a')
        link['href'] = f'#{tag["id"]}'
        link.string = tag.string

        item = tadd(mktg('li'), link)
        tadd(links, item)

    toc = mktg('div')
    toc['id'] = RID_TOC
    toc.string = f"List of {RID}s"
    sibling = ex.get(class_=RID_PARENT)
    assert sibling
    sibling.insert_before(tadd(toc, links))
    # NOTE: searching tags after the insertion point FAILS
    return ex

def main():
    args = sys.argv
    if len(args) != 3:
        print("Usage: ./relink.py <mht file> <review_tag>")
        return
    mht = sys.argv[1]
    reviewer = sys.argv[2]
    print(f'Extract multi-part from "{mht}" ...')
    ex = Extract(mht)
    print('Adding links to "{reviewer}" ...')
    relink(ex, reviewer)
    ex.save()

if __name__ == '__main__':
    main()
