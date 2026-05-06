from core.api.actions.base_api_action import BaseAPIAction
from core.api.common.api_response import APIResponse

class PatchAction(BaseAPIAction):
    """
    Specialized PATCH actions.
    """
    def call(self, url, json=None, data=None, headers=None, **kwargs):
        """Generic PATCH call."""
        self._log_request("PATCH", url, json=json, data=data, headers=headers, **kwargs)
        response = self.session.patch(url, json=json, data=data, headers=headers, **kwargs)
        self._log_response(response)
        return APIResponse(response)

    def with_json(self, url, payload, headers=None, **kwargs):
        """PATCH with JSON body."""
        self._log_request("PATCH (JSON)", url, json=payload, headers=headers, **kwargs)
        response = self.session.patch(url, json=payload, headers=headers, **kwargs)
        self._log_response(response)
        return APIResponse(response)

    def with_form(self, url, data, headers=None, **kwargs):
        """PATCH with Form Data."""
        self._log_request("PATCH (FORM)", url, data=data, headers=headers, **kwargs)
        response = self.session.patch(url, data=data, headers=headers, **kwargs)
        self._log_response(response)
        return APIResponse(response)

    def with_files(self, url, files, data=None, headers=None, **kwargs):
        """PATCH with Files."""
        self._log_request("PATCH (MULTIPART)", url, data=data, headers=headers, files=files, **kwargs)
        response = self.session.patch(url, files=files, data=data, headers=headers, **kwargs)
        self._log_response(response)
        return APIResponse(response)
