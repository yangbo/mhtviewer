# mht-unarchive
Python program to extract from `mht` (Microsoft HTML archive) to html and image files.

Inspired by [yangbo/mhtviewer](https://github.com/yangbo/mhtviewer)
Rewritten using `email.message_from_file`

## Usage
```
curl -sSL https://install.python-poetry.org | python3 - # install poetry
poetry install
poetry run ./extract.py <file.mht>
poetry run ./relink.py <mht file> <review_tag>
```
Output is written to a folder with the same name as the original HTML file.

## Testing
```
poetry install
poetry run ptw
```


