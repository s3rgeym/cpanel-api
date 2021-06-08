# CPanel API Client for Python

[![Downloads](https://pepy.tech/badge/cpanelapi)](https://pepy.tech/project/cpanelapi)
[![Downloads](https://pepy.tech/badge/cpanelapi/month)](https://pepy.tech/project/cpanelapi)
[![Downloads](https://pepy.tech/badge/cpanelapi/week)](https://pepy.tech/project/cpanelapi)

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

from cpanel_api import CPanelApi

logging.basicConfig(level=logging.WARNING, stream=sys.stderr)

hostname = 'HOSTNAME_OR_IPADRESS'
username = 'USERNAME'
password = 'PASSWORD'

client = CPanelApi(hostname, username, password)

# Alternatively, to authenticate using a UAPI or cPanel API 2 token, use:
# client = CPanelApi(hostname, username, '<TOKEN>', auth_type = 'utoken')

# {'warnings': None, 'errors': None, 'data': {'port': '1243'}, 'metadata': {}, 'status': 1, 'messages': None}
r = client.uapi.SSH.get_port()
print('SSH port:', r.data.port)
# get all public ssh keys
# {'cpanelresult': {'postevent': {'result': 1}, 'apiversion': 2, 'data': [...], 'func': 'listkeys', 'event': {'result': 1}, 'module': 'SSH', 'preevent': {'result': 1}}}
r = client.cpanel2.SSH.listkeys()
pprint(r.cpanelresult.data)
# retrieve key
r = client.cpanel2.SSH.fetchkey(name='id_rsa')
# {"name": "id_rsa", "key": "ssh-rsa XXX"}
print(r.cpanelresult.data[0].key)
r = client.cpanel2.SSH.importkey(name='new_rsa.pub', key='*data*')
pprint(r)
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
