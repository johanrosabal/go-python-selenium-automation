from core.api.actions.base_api_action import BaseAPIAction
from core.api.common.api_response import APIResponse

class POSTActions(BaseAPIAction):
    """
    Specialized POST actions for different content types and scenarios.
    """
    
    def call(self, url, body=None, json=None, headers=None, **kwargs):
        """Generic POST call (Legacy/Fallback)."""
        self._log_request("POST", url, json=json or body, headers=headers, **kwargs)
        response = self.session.post(url, data=body, json=json, headers=headers, **kwargs)
        self._log_response(response)
        return APIResponse(response)

    def with_json(self, url, payload, headers=None, **kwargs):
        """
        POST with JSON body. 
        Automatically sets 'Content-Type: application/json'.
        """
        self._log_request("POST (JSON)", url, json=payload, headers=headers, **kwargs)
        response = self.session.post(url, json=payload, headers=headers, **kwargs)
        self._log_response(response)
        return APIResponse(response)

    def with_form(self, url, data, headers=None, **kwargs):
        """
        POST with Form Data (URL encoded).
        Automatically sets 'Content-Type: application/x-www-form-urlencoded'.
        """
        self._log_request("POST (FORM)", url, data=data, headers=headers, **kwargs)
        response = self.session.post(url, data=data, headers=headers, **kwargs)
        self._log_response(response)
        return APIResponse(response)

    def with_files(self, url, files, data=None, headers=None, **kwargs):
        """
        POST with Files (Multipart).
        Args:
            files: Dictionary like {'file': open('report.xls', 'rb')} 
                   or {'file': ('name.txt', 'content')}
        """
        self._log_request("POST (MULTIPART)", url, data=data, headers=headers, files=files, **kwargs)
        response = self.session.post(url, files=files, data=data, headers=headers, **kwargs)
        self._log_response(response)
        return APIResponse(response)

    def with_raw(self, url, data, content_type="text/plain", headers=None, **kwargs):
        """
        POST with raw body (Text, XML, Binary).
        """
        if headers is None: headers = {}
        headers["Content-Type"] = content_type
        
        self._log_request(f"POST ({content_type})", url, data=data, headers=headers, **kwargs)
        response = self.session.post(url, data=data, headers=headers, **kwargs)
        self._log_response(response)
        return APIResponse(response)
