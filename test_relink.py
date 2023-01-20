from extract import Extract
from relink import *

from pathlib import Path
from pytest import fixture

TEST_MHT='sample.mht'

@fixture
def soup():
	ex = Extract(TEST_MHT)
	rel = relink(ex, REVIEWER)
	return rel.soup

def test_rel(soup):
	assert soup

def test_toc(soup):
	toc = soup.body.div
	assert toc
	assert 'List' in str(toc)
	assert RID in toc['id']
	assert len(toc.contents) > 1
	olist = toc.contents[1]
	item = olist.contents[0]
	anchor = item.contents[0]
	assert anchor
	assert RID in anchor['href']



