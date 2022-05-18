from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import PermissionDenied
from random import random
from datetime import datetime


class FilterRequestsMiddleware(MiddlewareMixin):

    def process_request(self, request):

        # print("Inside process request of custom middleware ")
        #
        # allowed_ips = ['192.168.1.1', '123.123.123.1', ]
        #
        # print(request.META.get('HTTP_USER_AGENT'))
        #
        # ip = request.META.get('REMOTE_ADDR')
        #
        # if ip not in allowed_ips:
        #     raise PermissionDenied
        #
        # return None

        # allowed_app_versions = ['1.2.4', '1.2.5']
        #
        # app_version = request.META.get('HTTP_APP_VERSION')
        #
        # if app_version not in allowed_app_versions:
        #     raise PermissionDenied

        return None

    def process_response(self, request, response):
        # Check response for any sensitive middleware
        # keys_to_check = ['password', 'date_of_birth', 'email', ]
        #print("Inside response ---- > " , response.content)

        return response


class PerformanceLoggerMiddleware(MiddlewareMixin):

    def process_request(self, request):


        request_id = random()

        #print("Going to set request id as -> ", request_id)

        setattr(request, 'request_id', request_id)

        request_time = datetime.now()

        # Save the request id along with other info about the
        # request  endpoint, user token, current time

        return None

    def process_response(self, request, response):

        response_time = datetime.now()

        request_id = request.request_id

        # TODO: query the db for the request log object (saved in process_request method above)
        # TODO: Store the response time

        #print("Inside response ---> ", request_id)

        return response