# -*- coding: utf-8 -*-
import logging
import urllib.parse as uparse
from base64 import b64encode
from dataclasses import dataclass
from typing import Any, Callable, Dict, Literal, Optional, Tuple

import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(category=InsecureRequestWarning)

__version__ = '0.2.2'
__author__ = 'Sergey M'
__email__ = 'tz4678@gmail.com'
__copyright__ = 'Copyright 2020, Sergey M'
__license__ = 'MIT'
__url__ = 'https://github.com/tz4678/cpanel-api'

DEFAULT_USER_AGENT = (
    'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


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


ApiVersion = Literal['cpanel2', 'uapi']


class Api:
    def __init__(self, version: ApiVersion, client: 'CPanelApi') -> None:
        self.version = version
        self.client = client

    def __getattr__(self, attr: str) -> 'Scope':
        return Scope(attr, self)


class Scope:
    def __init__(self, name: str, api: Api) -> None:
        self.name = name
        self.api = api

    def __getattr__(
        self, attr: str
    ) -> Callable[[Tuple[str, ...], Dict[str, Any]], Result]:
        function_name = attr

        def func(*args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> Result:
            return self.api.client.call_api(
                self.api.version, self.name, function_name, *args, **kwargs
            )

        func.__name__ = function_name
        return func


class CPanelApi:
    def __init__(
        self,
        hostname: str,
        username: str,
        password: str,
        port: int = 2083,
        *,
        auth_type: Literal['hash', 'password', 'token', 'utoken'] = 'password',
        session: Optional[requests.Session] = None,
        ssl: bool = True,
        timeout: float = 10.0,
        verify: bool = False,
    ) -> None:
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.auth_type = auth_type
        if session is None:
            session = requests.session()
            session.headers.update({'User-Agent': DEFAULT_USER_AGENT})
        self.session = session
        self.ssl = ssl
        self.timeout = timeout
        self.verify = verify

    @property
    def auth(self) -> str:
        credentials: str = f'{self.username}:{self.password}'
        if self.auth_type == 'password':
            enc = b64encode(credentials.encode()).decode()
            auth = f'Basic {enc}'
        elif self.auth_type == 'hash':
            auth = f'WHM {credentials}'
        elif self.auth_type == 'token':
            auth = f'whm {credentials}'
        elif self.auth_type == 'utoken':
            auth = f'cpanel {credentials}'
        else:
            raise ValueError(f'unknown auth type: {self.auth_type!r}')
        return auth

    @property
    def base_url(self) -> str:
        return '{}://{}:{}'.format(
            'https' if self.ssl else 'http', self.hostname, self.port
        )

    def call_api(
        self,
        v: ApiVersion,
        module: str,
        function: str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs: Dict[str, Any],
    ) -> Result:
        params = dict(params or {})
        params.update(kwargs)
        if v == 'cpanel2':
            path: str = '/json-api/cpanel'
            params = {
                'cpanel_jsonapi_user': self.username,
                'cpanel_jsonapi_apiversion': '2',
                'cpanel_jsonapi_module': module,
                'cpanel_jsonapi_func': function,
                **params,
            }
        elif v == 'uapi':
            path: str = f'/execute/{module}/{function}'
        else:
            raise ValueError(f'unknown version: {v}')
        logger.debug('reqparams: %s', ','.join(params))
        url = uparse.urljoin(self.base_url, path)
        headers = {'Authorization': self.auth}
        r: requests.Response = self.session.post(
            url,
            params,
            allow_redirects=False,
            headers=headers,
            timeout=self.timeout,
            verify=self.verify,
        )
        if r.status_code == 401:
            raise Unauthorized()
        try:
            return r.json(object_hook=Result)
        except ValueError:
            raise BadResponse()

    def __getattr__(self, attr: str) -> Api:
        return Api(attr, self)
