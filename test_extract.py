from extract import * 
from pathlib import Path
from pytest import fixture

TEST_FILE='sample.mht'
TEST_URI='cid:css-8e135dc7-1298-4278-b82b-9168ec675a37@mhtml.blink'

@fixture
def ex():
	ex = Extract(TEST_FILE)
	return ex

def test_ex_html(ex):
	assert ex
	assert ex.html
	assert 'User F' in str(ex)

def test_filename(ex):
	file_path = Path(TEST_URI.split(':')[1])
	assert MAGIC_EXT in str(file_path)
	file_name = extract_filename(file_path, ['text', 'css'])
	local_file = f'./{file_name}'
	assert '9168ec675a37.css' in local_file
	assert TEST_URI not in str(ex)
	assert file_name in str(ex)

def test_ex_get(ex):
	PREFIX="PRComment"
	result = ex.get_all('b', string='User F')
	assert result
	assert len(result) == 41
	tag = result[0]
	n = 1
	tag['id'] = f'{PREFIX}_{n:03}'
	tag.string = f'{PREFIX} #{n:03}. {tag.string}'
	assert 'Comment_001' in str(tag)
	assert 'Comment_001' in str(ex)

def test_ex_attrs(ex):
	assert ex.attrs
	keys = ex.files()
	file_name = keys[0]
	assert 'css' in file_name

	attrs = ex.attrs.get(file_name)
	assert attrs
	assert MAGIC_EXT in attrs['uri']
	assert MAGIC_EXT not in file_name
	assert '.css' in file_name

def test_ex_suffix(ex):
	"""every filename has a suffix"""
	for key in ex.files():
		suffix = Path(key).suffix
		assert suffix 

def test_ex_update_link(ex):
	keys = ex.files()
	file_name = keys[0]
	attrs = ex.attrs.get(file_name)
	uri = attrs['uri']
	assert uri not in str(ex)

def test_unquote(ex):
	assert '=3D"' in ex.raw_html
	assert '=3D"' not in ex.html
