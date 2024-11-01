# sinAPI

[![Publish to PyPI on Release](https://github.com/sheptalo/my_sin_api/actions/workflows/release.yml/badge.svg)](https://github.com/sheptalo/my_sin_api/actions/workflows/release.yml)
[![pypi](https://img.shields.io/pypi/status/sinAPI.svg?style=flat-square)](https://pypi.org/project/sinAPI/#description)
![python versions](https://img.shields.io/pypi/pyversions/aiogram.svg?style=flat-square)

## Install

```Bash
$ pip install sinAPI
```

## RU

класс интерфейс для связи с апи REST,

На данный момент иидеально работает только с ботами семьи Tegtory


## EN

class interface to act with REST API's

for now only work with Tegtory bots.

To get know how to create class open ```_models.py```

## Examples

[![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=sheptalo&repo=Tegtory&theme=dark)](https://github.com/sheptalo/Tegtory)

## Usage

```python
from my_sin_api import SinApi

api = SinApi('YOUR API TOKEN', 'http://API.URL/')

item = api.any('NAME OF NEEDED ITEM', 'ID OF NEEDED ITEM')
print(item.name)
# eq
# requests.get('http://API.URL/NAME OF NEEDED ITEM/ID OF NEEDED ITEM',
#              headers={'Authorization': "YOUR API TOKEN"})
```
