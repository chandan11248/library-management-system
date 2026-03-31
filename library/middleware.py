import time
import logging

from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden

logger = logging.getLogger('library')


class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware for Logging - logs every request/response cycle.
    Demonstrates: Middleware concepts, request/response interception.
    """

    def process_request(self, request):
        request._start_time = time.time()
        user = request.user.username if request.user.is_authenticated else 'Anonymous'
        logger.info(f"[REQUEST] {request.method} {request.path} - User: {user} - IP: {request.META.get('REMOTE_ADDR')}")

    def process_response(self, request, response):
        duration = time.time() - getattr(request, '_start_time', time.time())
        duration_ms = round(duration * 1000, 2)
        logger.info(f"[RESPONSE] {request.method} {request.path} - Status: {response.status_code} - Time: {duration_ms}ms")

        # Store activity log in database (lazy import to avoid circular imports)
        try:
            from .models import ActivityLog
            ActivityLog.objects.create(
                method=request.method,
                path=request.path,
                user=request.user.username if request.user.is_authenticated else 'Anonymous',
                ip_address=request.META.get('REMOTE_ADDR'),
                status_code=response.status_code,
                response_time_ms=duration_ms,
            )
        except Exception:
            pass  # Don't break the response if logging fails

        return response


class SecurityMiddleware(MiddlewareMixin):
    """
    Custom Security Middleware - adds security headers and blocks suspicious requests.
    Demonstrates: Security middleware concepts.
    """

    BLOCKED_USER_AGENTS = ['sqlmap', 'nikto', 'nmap']

    def process_request(self, request):
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        for blocked in self.BLOCKED_USER_AGENTS:
            if blocked in user_agent:
                logger.warning(f"[SECURITY] Blocked suspicious user agent: {user_agent}")
                return HttpResponseForbidden("Access Denied")

        # Block requests with SQL injection patterns in query strings
        query_string = request.META.get('QUERY_STRING', '').lower()
        sql_patterns = ['union select', 'drop table', '--', ';--']
        for pattern in sql_patterns:
            if pattern in query_string:
                logger.warning(f"[SECURITY] Blocked SQL injection attempt: {query_string}")
                return HttpResponseForbidden("Access Denied")

    def process_response(self, request, response):
        # Add security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        return response


class ErrorHandlingMiddleware(MiddlewareMixin):
    """
    Error Handling Middleware - catches exceptions and logs them.
    Demonstrates: Error handling middleware concepts.
    """

    def process_exception(self, request, exception):
        logger.error(
            f"[ERROR] {type(exception).__name__}: {str(exception)} "
            f"- Path: {request.path} - User: {request.user}"
        )
        return None  # Let Django's default error handling take over


class VisitCounterMiddleware(MiddlewareMixin):
    """
    Session-based visit counter middleware.
    Demonstrates: Session handling in middleware, cookies.
    """

    def process_request(self, request):
        if not request.session.get('visit_count'):
            request.session['visit_count'] = 0
        request.session['visit_count'] += 1
        request.session['last_visit'] = time.strftime('%Y-%m-%d %H:%M:%S')
