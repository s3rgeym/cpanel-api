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

from cpanel_api import *

logging.basicConfig(level=logging.WARNING, stream=sys.stderr)

hostname = 'HOSTNAME_OR_IPADRESS'
username = 'USERNAME'
password = 'PASSWORD'

client = CPanelApi(hostname, username, password)
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
