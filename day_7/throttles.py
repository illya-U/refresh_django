from rest_framework.throttling import SimpleRateThrottle

class PostGetThrottle(SimpleRateThrottle):
    scope = "login"

    def get_rate(self):
        return "5/hour"

    def get_cache_key(self, request, view):
        return self.get_ident(request)
