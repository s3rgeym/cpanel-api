# CPanel API Client for Python

Supports only UAPI.

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

client = CPanelClient(hostname, username, password)

r = client.SSH.get_port()
print('SSH port:', r.data.port)

from pprint import pprint
r = client.DomainInfo.list_domains()
pprint(r.data)
```

Function call syntax:

```python
client.ModuleName.function_name({'param': 'value'})
client.ModuleName.function_name(param='value')
client.ModuleName.function_name({'param': 'value'}, param='value')
client.api('ModuleName', 'function_name', {'param': 'value'}, param='value')
```

Pagination:

```python
client.ModuleName.function_name({'api.paginate': 1, 'api.paginate_size': 10, 'api.paginate_page': 2})
```

Links:

- [Official documentation](https://documentation.cpanel.net/display/DD/Guide+to+UAPI).
