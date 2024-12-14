import copy
import json

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class LogRequestResponseMiddleware(MiddlewareMixin):

    body: bytes

    def process_request(self, request):
        if settings.DEBUG:
            self.body = copy.deepcopy(request.body)
        return None

    def process_response(self, request, response):
        if settings.DEBUG:
            self.log_response(request, response)
        return response

    def log_request(self, request):
        print("----- Request -----")
        print(f"Method: {request.method}")
        print(f"Path: {request.get_full_path()}")
        print(f"Headers: {self.format_headers(request.headers)}")
        if self.body:
            try:
                print(f"Body: {json.dumps(json.loads(self.body), indent=4)}")
            except json.JSONDecodeError:
                print(f"Body: {request.body.decode('utf-8')}")
        print("-------------------")

    def log_response(self, request, response):
        if response.status_code < 400 or response.status_code > 500:
            return
        self.log_request(request)
        print("----- Response -----")
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {self.format_headers(response.headers)}")
        if 'application/json' in response['Content-Type']:
            try:
                content = json.loads(response.content)
                print(f"Content: {json.dumps(content, indent=4)}")
            except json.JSONDecodeError:
                print(f"Content: {response.content.decode('utf-8')}")
        # else:
        #     print(f"Content: {response.content.decode('utf-8')}")
        print("--------------------")

    def format_headers(self, headers):
        return json.dumps(dict(headers), indent=4)
