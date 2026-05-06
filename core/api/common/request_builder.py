import json
import allure
from core.api.common.api_response import APIResponse

class RequestBuilder:
    """
    Fluent Request Builder to construct complex API calls step-by-step.
    Inspired by high-level automation patterns.
    """
    
    def __init__(self, session, method, action_instance):
        self.session = session
        self.method = method.upper()
        self.action = action_instance # Reference to GETActions/POSTActions for logging
        
        # State
        self.url = ""
        self.headers = {}
        self.params = {}
        self.data = None
        self.json_data = None
        self.files = None
        self.auth = None
        self.cookies = None
        self.timeout = None
        self.verify = True
        self.allow_redirects = True
        self.stream = False

    def set_url(self, url):
        self.url = url
        return self

    def set_endpoint(self, endpoint):
        """Set the API endpoint (relative path)."""
        # Ensure base URL ends with / and endpoint doesn't start with /
        if self.url and not self.url.endswith('/'):
            self.url += '/'
        self.url += endpoint.lstrip('/')
        return self

    def build_url(self, **kwargs):
        """Insert dynamic values into the URL (e.g. /users/{id} -> /users/1)."""
        self.url = self.url.format(**kwargs)
        return self

    def add_header(self, key, value):
        self.headers[key] = value
        return self

    def set_headers(self, headers: dict):
        self.headers.update(headers)
        return self

    def set_params(self, params: dict):
        self.params.update(params)
        return self

    def set_json(self, json_data):
        self.json_data = json_data
        return self

    def set_data(self, data):
        self.data = data
        return self

    def set_files(self, files: dict):
        self.files = files
        return self

    def set_auth(self, username, password):
        self.auth = (username, password)
        return self

    def set_timeout(self, timeout):
        self.timeout = timeout
        return self

    def set_verify(self, verify: bool):
        self.verify = verify
        return self

    def set_cookies(self, cookies: dict):
        self.cookies = cookies
        return self

    def set_allow_redirects(self, allow: bool):
        self.allow_redirects = allow
        return self

    def set_proxies(self, proxies: dict):
        self.proxies = proxies
        return self

    def set_stream(self, stream: bool):
        self.stream = stream
        return self

    def set_cert(self, cert):
        self.cert = cert
        return self

    def send(self):
        """Executes the request with the built state."""
        kwargs = {
            "params": self.params,
            "headers": self.headers,
            "data": self.data,
            "json": self.json_data,
            "files": self.files,
            "auth": self.auth,
            "cookies": self.cookies,
            "timeout": self.timeout,
            "verify": self.verify,
            "allow_redirects": self.allow_redirects,
            "proxies": getattr(self, 'proxies', None),
            "stream": getattr(self, 'stream', False),
            "cert": getattr(self, 'cert', None)
        }
        
        # Log via the action instance to keep consistent formatting
        self.action._log_request(self.method, self.url, **kwargs)
        
        # Execute via requests session
        response = self.session.request(self.method, self.url, **kwargs)
        
        self.action._log_response(response)
        return APIResponse(response)
