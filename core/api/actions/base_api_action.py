import json
import allure
from core.utils.logger_config import setup_logger
from requests import Session

class BaseAPIAction:
    """
    Base class for all API action components (GET, POST, etc.).
    Provides shared logging and session management.
    """
    def __init__(self, session: Session):
        self.session = session
        self._logger = None

    @property
    def logger(self):
        if not self._logger:
            self._logger = setup_logger(self.__class__.__name__)
        return self._logger

    def builder(self, method=None):
        """Returns a fluent RequestBuilder for this action."""
        from core.api.common.request_builder import RequestBuilder
        # Infer method from class name if not provided (e.g., GETActions -> GET)
        if not method:
            method = self.__class__.__name__.replace("Actions", "").replace("Action", "").upper()
        return RequestBuilder(self.session, method, self)

    # --- Fluent Builder Shortcuts (Legacy Style Compatibility) ---
    
    def set_url(self, url):
        return self.builder().set_url(url)

    def set_endpoint(self, endpoint):
        return self.builder().set_endpoint(endpoint)

    def set_json(self, json_data):
        return self.builder().set_json(json_data)

    def set_data(self, data):
        return self.builder().set_data(data)

    def set_params(self, params):
        return self.builder().set_params(params)

    def set_auth(self, username, password):
        return self.builder().set_auth(username, password)

    def add_header(self, key, value):
        return self.builder().add_header(key, value)

    def set_files(self, files):
        return self.builder().set_files(files)

    def set_timeout(self, timeout):
        return self.builder().set_timeout(timeout)

    def set_verify(self, verify):
        return self.builder().set_verify(verify)

    def set_allow_redirects(self, allow):
        return self.builder().set_allow_redirects(allow)

    def set_cookies(self, cookies):
        return self.builder().set_cookies(cookies)

    def set_proxies(self, proxies):
        return self.builder().set_proxies(proxies)

    def set_stream(self, stream):
        return self.builder().set_stream(stream)

    def set_cert(self, cert):
        return self.builder().set_cert(cert)

    def build_url(self, **kwargs):
        return self.builder().build_url(**kwargs)

    def _log_request(self, method, url, **kwargs):
        """Logs the request details to the console and Allure."""
        self.logger.info(f"🌐 {method} request to: {url}")
        
        if kwargs.get('json'):
            self.logger.info(f"📦 Body: {json.dumps(kwargs.get('json'))}")
        elif kwargs.get('data'):
            # If data is a dict (Form), log as JSON-like, else as raw string
            data = kwargs.get('data')
            if isinstance(data, dict):
                self.logger.info(f"📦 Form Data: {json.dumps(data)}")
            else:
                self.logger.info(f"📦 Raw Body: {str(data)[:1000]}")
        
        if kwargs.get('files'):
            file_names = [f"{k}: {getattr(v, 'name', 'binary')}" for k, v in kwargs.get('files').items()]
            self.logger.info(f"📁 Files: {', '.join(file_names)}")
            
        if kwargs.get('params'):
            self.logger.info(f"🔍 Params: {json.dumps(kwargs.get('params'))}")
        
        # Log headers for the Inspector
        if kwargs.get('headers'):
            self.logger.info(f"📋 Request Headers: {json.dumps(kwargs.get('headers'))}")

        # Log CURL equivalent
        curl_cmd = self._to_curl(method, url, **kwargs)
        self.logger.info(f"💻 CURL: {curl_cmd}")

        # Allure attachment
        allure.attach(
            f"Method: {method}\nURL: {url}\nHeaders: {kwargs.get('headers')}\nBody: {kwargs.get('json') or kwargs.get('data')}\nParams: {kwargs.get('params')}\n\nCURL:\n{curl_cmd}",
            name=f"Request: {method} {url}",
            attachment_type=allure.attachment_type.TEXT
        )

    def _log_response(self, response):
        """Logs the response details."""
        status_icon = "✅" if response.status_code < 400 else "❌"
        self.logger.info(f"{status_icon} Status: {response.status_code} {response.reason}")
        
        try:
            body = response.json()
            self.logger.info(f"📥 Response Body: {json.dumps(body)}")
            self.logger.info(f"📋 Response Headers: {json.dumps(dict(response.headers))}")
            allure.attach(
                json.dumps(body, indent=2),
                name="Response Body",
                attachment_type=allure.attachment_type.JSON
            )
        except Exception:
            self.logger.info(f"📥 Response Body: {response.text}")
            allure.attach(
                response.text,
                name="Response Body",
                attachment_type=allure.attachment_type.TEXT
            )

    def _to_curl(self, method, url, **kwargs):
        """Generates a curl command equivalent to the request."""
        parts = [f"curl -X {method} '{url}'"]
        
        headers = kwargs.get('headers', {})
        for k, v in headers.items():
            parts.append(f"-H '{k}: {v}'")
            
        params = kwargs.get('params')
        if params:
            import urllib.parse
            query = urllib.parse.urlencode(params)
            # Replace the URL in the first part if it doesn't already have params
            if '?' not in parts[0]:
                parts[0] = parts[0].replace(f"'{url}'", f"'{url}?{query}'")
            else:
                parts[0] = parts[0].replace(f"'{url}'", f"'{url}&{query}'")

        json_data = kwargs.get('json')
        if json_data:
            parts.append(f"-d '{json.dumps(json_data)}'")
            
        data = kwargs.get('data')
        if data:
            if isinstance(data, dict):
                parts.append(f"-d '{json.dumps(data)}'")
            else:
                parts.append(f"-d '{data}'")
                
        return " ".join(parts)
