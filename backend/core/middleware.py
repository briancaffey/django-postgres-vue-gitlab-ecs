class SubdomainMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        return self.get_response(request)

    def process_request(self, request):
        """
        Attach the subdomain to the request
        """
        if 'HTTP_HOST' in request.META:
            request.subdomain = request.META.get('HTTP_HOST').split('.')[0]
        else:
            request.subomain = 'test'
        return request
