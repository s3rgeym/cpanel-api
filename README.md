# CPanel API Client for Python

Supports cPanel API 2 and UAPI.

```zsh
$ pip install cpanel-api
```

Basic usage:

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import sys

from cpanel_api import *

logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)

hostname = 'HOSTNAME_OR_IPADRESS'
username = 'USERNAME'
password = 'PASSWORD'

client = CPanelApi(hostname, username, password)
```

Domain list:

```ipython
In [10]: client.uapi.DomainInfo.list_domains()
Out [10]:
{'messages': None,
 'status': 1,
 'data': {'main_domain': 'site.info',
  'sub_domains': ['cabinet.site.info',
   'news.site.info',
   'shop.site.info'],
  'parked_domains': [],
  'addon_domains': []},
 'errors': None,
 'metadata': {},
 'warnings': None}
```

SSH kyes:

```ipython
In [20]: client.cpanel2.SSH.listkeys()
Out [20]:
{'cpanelresult': {'postevent': {'result': 1},
  'apiversion': 2,
  'preevent': {'result': 1},
  'module': 'SSH',
  'func': 'listkeys',
  'data': [],
  'event': {'result': 1}}}
```

Function call syntax:

```python
client.api_version.ModuleName.function_name({'param': 'value'})
client.api_version.ModuleName.function_name(param='value')
client.api_version.ModuleName.function_name({'param': 'value'}, param='value')
client.api_cal('version', 'ModuleName', 'function_name', {'param': 'value'}, param='value')
```

Links:

- [Official documentation](https://documentation.cpanel.net/display/DD/Developer+Documentation+Home).
