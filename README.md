# CPanel API Client for Python

Supports cPanel API 2 and UAPI.

## Install

```zsh
$ pip install cpanel-api
```

## Examples

Basic usage:

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import sys

from pprint import pprint

from cpanel_api import *

logging.basicConfig(level=logging.WARNING, stream=sys.stderr)

hostname = 'HOSTNAME_OR_IPADRESS'
username = 'USERNAME'
password = 'PASSWORD'

client = CPanelApi(hostname, username, password)
# {'warnings': None, 'errors': None, 'data': {'port': '1243'}, 'metadata': {}, 'status': 1, 'messages': None}
r = client.uapi.SSH.get_port()
print('SSH port:', r.data.port)
# {'cpanelresult': {'postevent': {'result': 1}, 'apiversion': 2, 'data': [], 'func': 'listkeys', 'event': {'result': 1}, 'module': 'SSH', 'preevent': {'result': 1}}}
r = client.cpanel2.SSH.listkeys()
pprint(r.data)
# ...
r = client.cpanel2.DomainLookup.getdocroot(domain='site.info')
print(r.cpanelresult.data[0].reldocroot)  # public_html
```

Function call syntax:

```python
client.api_version.ModuleName.function_name({'param': 'value'})
client.api_version.ModuleName.function_name(param='value')
client.api_version.ModuleName.function_name({'param': 'value'}, param='value')
client.api_cal('api_version', 'ModuleName', 'function_name', {'param': 'value'}, param='value')
```

Where `api_version` is `cpanel2` or `uapi`.

## Links:

- [Official documentation](https://documentation.cpanel.net/display/DD/Developer+Documentation+Home).
