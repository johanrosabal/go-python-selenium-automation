from core.api.actions.base_api_action import BaseAPIAction
from core.api.common.api_response import APIResponse

class GETActions(BaseAPIAction):
    """
    Specialized GET actions.
    """
    def call(self, url, params=None, headers=None, **kwargs):
        """Generic GET call."""
        self._log_request("GET", url, params=params, headers=headers, **kwargs)
        response = self.session.get(url, params=params, headers=headers, **kwargs)
        self._log_response(response)
        return APIResponse(response)

    def with_params(self, url, params, headers=None, **kwargs):
        """GET with explicit query parameters."""
        self._log_request("GET (PARAMS)", url, params=params, headers=headers, **kwargs)
        response = self.session.get(url, params=params, headers=headers, **kwargs)
        self._log_response(response)
        return APIResponse(response)
