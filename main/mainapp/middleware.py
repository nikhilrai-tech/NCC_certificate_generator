# mainapp/middleware.py
from django.utils.deprecation import MiddlewareMixin

class CustomXFrameOptionsMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response['X-Frame-Options'] = 'ALLOWALL'  # Allow all origins
        return response
