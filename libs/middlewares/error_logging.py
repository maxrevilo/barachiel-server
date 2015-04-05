"""
    Put this file in a directory called, eg, 'middleware,' inside your django
    project. Make sure to create an __init__.py file in the directory so it can
    be included as a module.

    In settings.py. Then include
        'import.path.to.error_logging.ErrorLoggingMiddleware'
    in MIDDLEWARE_CLASSES in settings.py.

    Based on http://stackoverflow.com/a/24807721/1024693
"""
import logging

request_logger = logging.getLogger('api.request.logger')


class ErrorLoggingMiddleware(object):
    """
    Logs the request's body if the response is 5xx
    """
    request_body = None

    def process_request(self, request):
        # This is required because for some reasons there is no way to access
        # request.body in the 'process_response' method.
        self.request_body = request.body

    def process_response(self, request, response):
        is5XX = int(response.status_code / 100) == 5
        if is5XX:
            request_logger.log(
                logging.ERROR,
                "STATUS={}\nQuery Args: {}.\nBody: {}\nContent: {}"
                .format(
                    response.status_code,
                    request.GET,
                    self.request_body,
                    response.content[:1024]
                ),
                extra={
                    'tags': {
                        'url': request.build_absolute_uri()
                    }
                }
            )
        return response
