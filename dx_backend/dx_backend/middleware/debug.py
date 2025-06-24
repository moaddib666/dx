import copy
import json

from django.conf import settings
from django.utils.deprecation import MiddlewareMixin


class LogRequestResponseMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # Don't access request.body for POST requests to avoid consuming the stream
        # The admin interface needs to access request.body later
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

        # For POST requests, log form data instead of body
        if request.method == 'POST':
            if request.POST:
                print(f"POST data: {dict(request.POST)}")
            if request.FILES:
                print(f"FILES: {dict(request.FILES)}")
        # Only try to access body for non-POST requests or if it's already been read
        elif hasattr(request, '_body'):
            try:
                print(f"Body: {json.dumps(json.loads(request._body), indent=4)}")
            except (json.JSONDecodeError, AttributeError):
                try:
                    print(f"Body: {request._body.decode('utf-8')}")
                except (AttributeError, UnicodeDecodeError):
                    pass
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
