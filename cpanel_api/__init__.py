# -*- coding: utf-8 -*-
import urllib.parse as uparse
from base64 import b64encode
from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, Optional, Tuple

import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(category=InsecureRequestWarning)

__version__ = '0.1.0'
__author__ = 'Sergey M'
__email__ = 'tz4678@gmail.com'
__copyright__ = 'Copyright 2020, Sergey M'
__license__ = 'MIT'
__url__ = 'https://github.com/tz4678/cpanel_api'

DEFAULT_USER_AGENT = (
    'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'
)

__all__ = (
    'ClientError',
    'Unauthorized',
    'BadResponse',
    'Result',
    'CPanelClient',
)


class ClientError(Exception):
    message: str = None

    def __init__(self, message: Optional[str] = None) -> None:
        self.message = message or self.message
        super().__init__(self.message)


class Unauthorized(ClientError):
    message = 'Unauthorized'


class BadResponse(ClientError):
    message = 'Bad response'


class AttrDict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class Result(AttrDict):
    pass


class Call:
    def __init__(self, client: 'CPanelClient', module: str) -> None:
        self.client = client
        self.module = module

    def __getattr__(self, name: str) -> Callable[..., Result]:
        def f(*args: Tuple[Any], **kw: Dict[str, Any]) -> Any:
            return self.client.api(self.module, name, *args, **kw)

        f.__name__ = name
        return f


class CPanelClient:
    def __init__(
        self,
        hostname: str,
        username: str,
        password: Optional[str] = None,
        *,
        hash: Optional[str] = None,
        port: int = 2083,
        session: Optional[requests.Session] = None,
        ssl: bool = True,
        timeout: float = 10.0,
        verify: bool = False,
    ) -> None:
        self.hostname = hostname
        self.username = username
        self.password = password
        self.hash = hash
        self.port = port
        if session is None:
            session = requests.session()
            session.headers.update({'User-Agent': DEFAULT_USER_AGENT})
        self.session = session
        self.ssl = ssl
        self.timeout = timeout
        self.verify = verify

    @property
    def auth(self) -> str:
        if self.hash:
            return f'WHM {self.username}:{self.hash}'
        encoded = b64encode(
            f'{self.username}:{self.password}'.encode()
        ).decode()
        return f'Basic {encoded}'

    @property
    def base_url(self) -> str:
        return '{}://{}:{}'.format(
            'https' if self.ssl else 'http', self.hostname, self.port
        )

    def api(
        self,
        module: str,
        function: str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Dict[str, Any],
    ) -> Result:
        url = uparse.urljoin(self.base_url, f'/execute/{module}/{function}')
        params = dict(params or {})
        params.update(kwargs)
        headers = {'Authorization': self.auth}
        r = self.session.post(
            url,
            params,
            headers=headers,
            timeout=self.timeout,
            verify=self.verify,
        )
        if r.status_code == 401:
            raise Unauthorized()
        try:
            return r.json(object_hook=AttrDict)
        except ValueError:
            raise BadResponse()

    def __getattr__(self, name: str) -> Call:
        return Call(self, name)
