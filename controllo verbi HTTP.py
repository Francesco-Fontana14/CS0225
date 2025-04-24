import requests
import time
from typing import Optional, Dict, Any


class HTTPTester:
    def __init__(self, base_url: str, timeout: int = 5):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()

    def send_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        start_time = time.time()
        try:
            response = self.session.request(
                method,
                url,
                params=params,
                data=data,
                json=json,
                headers=headers,
                timeout=self.timeout
            )
            elapsed = round(time.time() - start_time, 3)
            result = {
                "success": True,
                "status_code": response.status_code,
                "response_time": elapsed,
                "headers": dict(response.headers),
                "data": response.json() if "application/json" in response.headers.get("Content-Type", "") else response.text,
            }
        except requests.exceptions.RequestException as e:
            result = {
                "success": False,
                "error": str(e),
                "status_code": getattr(e.response, "status_code", None)
            }
        return result

    def test_endpoint(self, method: str, endpoint: str, expected_status: int = 200, **kwargs) -> bool:
        print(f"\n🔍 Testing {method.upper()} {endpoint}...")
        result = self.send_request(method, endpoint, **kwargs)

        if not result["success"]:
            print(f"❌ Error: {result['error']}")
            return False

        print(f"✅ Status: {result['status_code']} (Expected: {expected_status})")
        print(f"⏱️ Time: {result['response_time']}s")

        data_preview = result.get("data", "")
        if isinstance(data_preview, str) and len(data_preview) > 100:
            data_preview = "[Large Payload]"
        print(f"📦 Data: {data_preview}")
        return result["status_code"] == expected_status


if __name__ == "__main__":
    #  Come funziona?
    BASE_URL = input("Inserisci l'URL da testare: ")
    tester = HTTPTester(BASE_URL)

    # Test GET
    tester.test_endpoint("GET", "/posts/1")

    # Test POST
    tester.test_endpoint(
        "POST",
        "/posts",
        expected_status=201,
        json={"title": "foo", "body": "bar", "userId": 1}
    )

    # Test PUT
    tester.test_endpoint(
        "PUT",
        "/posts/1",
        expected_status=200,
        json={"id": 1, "title": "updated", "body": "updated", "userId": 1}
    )

    # Test DELETE
    tester.test_endpoint("DELETE", "/posts/1", expected_status=200)