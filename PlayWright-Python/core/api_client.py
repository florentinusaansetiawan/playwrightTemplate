import time

from playwright.sync_api import APIRequestContext


class APIClient:

    def __init__(self, request: APIRequestContext):
        self.request = request

    def request_api(
        self,
        method: str,
        url: str,
        headers: dict | None = None,
        body: dict | None = None,
        params: dict | None = None
    ):
        start_time = time.perf_counter()

        response = self.request.fetch(
            url,
            method=method.upper(),
            headers=headers,
            data=body,
            params=params
        )

        duration = time.perf_counter() - start_time

        try:
            response_body = response.json()
        except Exception:
            response_body = response.text()

        return {
            "status_code": response.status,
            "headers": dict(response.headers),
            "body": response_body,
            "duration": round(duration * 1000, 2),

            "request": {
                "method": method.upper(),
                "url": url,
                "headers": headers or {},
                "body": body,
                "params": params or {}
            }
        }

    def get(
        self,
        url: str,
        headers: dict | None = None,
        params: dict | None = None
    ):
        return self.request_api(
            method="GET",
            url=url,
            headers=headers,
            params=params
        )

    def post(
        self,
        url: str,
        headers: dict | None = None,
        body: dict | None = None,
        params: dict | None = None
    ):
        return self.request_api(
            method="POST",
            url=url,
            headers=headers,
            body=body,
            params=params
        )

    def put(
        self,
        url: str,
        headers: dict | None = None,
        body: dict | None = None,
        params: dict | None = None
    ):
        return self.request_api(
            method="PUT",
            url=url,
            headers=headers,
            body=body,
            params=params
        )

    def patch(
        self,
        url: str,
        headers: dict | None = None,
        body: dict | None = None,
        params: dict | None = None
    ):
        return self.request_api(
            method="PATCH",
            url=url,
            headers=headers,
            body=body,
            params=params
        )

    def delete(
        self,
        url: str,
        headers: dict | None = None,
        body: dict | None = None,
        params: dict | None = None
    ):
        return self.request_api(
            method="DELETE",
            url=url,
            headers=headers,
            body=body,
            params=params
        )