# -*- coding: utf-8 -*-
import urllib.parse as uparse
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Optional

import requests
import urllib3
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(category=InsecureRequestWarning)

__version__ = '0.1.0'
__author__ = 'Sergey M'
__email__ = 'tz4678@gmail.com'
__copyright__ = 'Copyright 2020, Sergey M'
__license__ = 'MIT'
__url__ = 'https://github.com/tz4678/cpanel-api'

DEFAULT_USER_AGENT = (
    'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'
)


class AttrDict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class ClientError(Exception):
    message: str = None

    def __init__(self, message: Optional[str] = None) -> None:
        self.message = message or self.message
        super().__init__(self.message)


class BadResponse(ClientError):
    message = 'Bad response'


class CPanelAPI:
    username: str = None
    password: str = None
    security_token: str = None

    def __init__(
        self,
        hostname: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        *,
        port: int = 2083,
        security_token: Optional[str] = None,
        session: Optional[requests.Session] = None,
        ssl: bool = True,
        verify: bool = False,
    ) -> None:
        self.hostname = hostname
        self.port = port
        self.security_token = security_token or self.security_token
        if session is None:
            session = requests.session()
            session.headers.update({'User-Agent': DEFAULT_USER_AGENT})
        self.session = session
        self.ssl = ssl
        self.verify = verify
        if username is not None or password is not None:
            self.login(username, password)

    @property
    def base_url(self) -> str:
        return '{}://{}:{}'.format(
            'https' if self.ssl else 'http', self.hostname, self.port
        )

    def request(
        self,
        method: str,
        path: str,
        use_token: bool = True,
        **kwargs: Dict[str, Any],
    ) -> Any:
        url = self.base_url
        if use_token:
            url = uparse.urljoin(url, self.security_token.rstrip('/') + '/')
        url = uparse.urljoin(url, path.lstrip('/'))
        r = self.session.request(method, url, verify=self.verify, **kwargs)
        try:
            return r.json(object_hook=AttrDict)
        except ValueError:
            raise BadResponse()

    def get(
        self,
        path: str,
        params: Optional[Dict[str, str]] = None,
        **kwargs: Dict[str, Any],
    ) -> Any:
        return self.request('GET', path, params=params, **kwargs)

    def post(
        self,
        path: str,
        data: Optional[Dict[str, str]] = None,
        **kwargs: Dict[str, Any],
    ) -> Any:
        return self.request('POST', path, data=data, **kwargs)

    def login(
        self, username: Optional[str] = None, password: Optional[str] = None
    ) -> None:
        if username is not None:
            self.username = username
        if password is not None:
            self.password = password
        if self.username is None or self.password is None:
            raise ClientError('username and password are required')
        postdata = {
            'user': username,
            'pass': password,
        }
        result = self.post('/login/?login_only=1', postdata, use_token=False)
        if result.status == 0:
            raise ClientError('invalid username or password')
        self.security_token = result.security_token
