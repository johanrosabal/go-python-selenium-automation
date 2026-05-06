from core.api.actions.base_api_action import BaseAPIAction
from core.api.common.api_response import APIResponse

class DELETEActions(BaseAPIAction):
    """
    Specialized DELETE actions.
    """
    def call(self, url, headers=None, **kwargs):
        """Generic DELETE call."""
        self._log_request("DELETE", url, headers=headers, **kwargs)
        response = self.session.delete(url, headers=headers, **kwargs)
        self._log_response(response)
        return APIResponse(response)

    def with_params(self, url, params, headers=None, **kwargs):
        """DELETE with query parameters."""
        self._log_request("DELETE (PARAMS)", url, params=params, headers=headers, **kwargs)
        response = self.session.delete(url, params=params, headers=headers, **kwargs)
        self._log_response(response)
        return APIResponse(response)
