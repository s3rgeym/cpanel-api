# CPanel API Client for Python

Supports only UAPI.

```zsh
$ pip install cpanel_api
```

Examples:

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import sys

from cpanel_api import *

logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)

hostname = 'HOSTNAME_OR_IP_ADRESS'
username = 'USERNAME'
password = 'PASSWORD'

client = CPanelClient(hostname, username, password)

client.Module.function({'param': 'value'}, param='value')
client.api('Module', 'function', {'param': 'value'}, param='value')

res = client.SSH.get_port()
# {
#     'data': {'port': '1243'},
#     'errors': None,
#     'metadata': {},
#     'warnings': None,
#     'messages': None,
#     'status': 1,
# }
print(res.data.port)
```

Links:

- [Official documentation](https://documentation.cpanel.net/display/DD/Guide+to+UAPI).
