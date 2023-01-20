from extract import * 
from pathlib import Path
from pytest import fixture
from tempfile import TemporaryDirectory

TEST_MHT='sample.mhtml'
TEST_URI='cid:css-e7ca07c8-72d8-4000-b7d9-618b43ee95de@mhtml.blink'

def filename():
	file_path = Path(TEST_URI.split(':')[1])
	assert MAGIC_EXT in str(file_path)
	file_name = extract_filename(file_path, ['text', 'css'])
	return file_name

@fixture
def ex():
	ex = Extract(TEST_MHT)
	return ex

@fixture
def tmp():
    with TemporaryDirectory() as tmpdirname:
        yield tmpdirname

def test_ex_html(ex):
	assert ex
	assert ex.html
	assert 'User F' in str(ex)

def test_ex_save(ex, tmp):
	assert ex.folder =='reportgen'
	root = ex.save('/tmp')
	assert root
	assert root.exists()
	assert (root / 'index.html').exists()
	assert (root / filename()).exists()

def test_filename(ex):
	file_name = filename()
	local_file = f'./{file_name}'
	assert '618b43ee95de.css' in local_file
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
