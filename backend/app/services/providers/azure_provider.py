from app.services.providers.openai_provider import OpenAIProvider
from app.services.providers.base import NormalizedRequest


class AzureProvider(OpenAIProvider):
    """
    Azure OpenAI uses the same request/response shape as OpenAI.
    The caller must supply api_endpoint as the full Azure deployment URL:
      https://<resource>.openai.azure.com/openai/deployments/<deployment>/chat/completions?api-version=2024-02-01
    """

    def __init__(self, api_endpoint: str):
        self._api_endpoint = api_endpoint

    def get_api_url(self, model: str) -> str:
        return self._api_endpoint

    def get_headers(self, api_key: str) -> dict:
        return {
            "api-key": api_key,
            "Content-Type": "application/json",
        }

    def build_request_payload(self, req: NormalizedRequest) -> dict:
        payload = super().build_request_payload(req)
        # Azure ignores the model field in the body (deployment is in the URL)
        payload.pop("model", None)
        return payload
