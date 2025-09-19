from django.http import HttpResponseForbidden
from .models import Visitor, BlockedIP

class IPBlockerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        if ip and BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Your IP has been blocked.")

        response = self.get_response(request)
        return response

class VisitorIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        # Səhifəyə hər daxil olanda bir qeyd yaratmaq üçün
        if request.method == 'GET' and ip:
            Visitor.objects.create(
                ip_address=ip,
                user=request.user if request.user.is_authenticated else None
            )
        
        response = self.get_response(request)
        return response