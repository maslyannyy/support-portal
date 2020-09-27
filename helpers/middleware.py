import logging

_logger = logging.getLogger(__name__)


class ErrorMiddleware:
    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request):
        response = self._get_response(request)
        return response

    @staticmethod
    def process_exception(request, exception):
        _logger.error(request)
        _logger.error(exception)
