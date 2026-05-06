from core.api.actions.base_api_action import BaseAPIAction
from core.api.common.api_response import APIResponse

class PUTActions(BaseAPIAction):
    """
    Specialized PUT actions.
    """
    def call(self, url, body=None, json=None, headers=None, **kwargs):
        """Generic PUT call."""
        self._log_request("PUT", url, json=json or body, headers=headers, **kwargs)
        response = self.session.put(url, data=body, json=json, headers=headers, **kwargs)
        self._log_response(response)
        return APIResponse(response)

    def with_json(self, url, payload, headers=None, **kwargs):
        """PUT with JSON body."""
        self._log_request("PUT (JSON)", url, json=payload, headers=headers, **kwargs)
        response = self.session.put(url, json=payload, headers=headers, **kwargs)
        self._log_response(response)
        return APIResponse(response)

    def with_form(self, url, data, headers=None, **kwargs):
        """PUT with Form Data."""
        self._log_request("PUT (FORM)", url, data=data, headers=headers, **kwargs)
        response = self.session.put(url, data=data, headers=headers, **kwargs)
        self._log_response(response)
        return APIResponse(response)

    def with_files(self, url, files, data=None, headers=None, **kwargs):
        """PUT with Files."""
        self._log_request("PUT (MULTIPART)", url, data=data, headers=headers, files=files, **kwargs)
        response = self.session.put(url, files=files, data=data, headers=headers, **kwargs)
        self._log_response(response)
        return APIResponse(response)
