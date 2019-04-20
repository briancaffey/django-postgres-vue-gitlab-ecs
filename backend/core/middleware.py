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
        request.subdomain = request.META.get('HTTP_HOST').split('.')[0]
        return request
