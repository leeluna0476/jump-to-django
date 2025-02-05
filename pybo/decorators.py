from django.http import JsonResponse

def require_http_methods(methods):
    def decorator(f):
        def wrapper(request, *args, **kwargs):
            if request not in methods:
                return JsonResponse({"error": "Method not allowed"}, status=405)
            return f(request)
        return wrapper
    return decorator

@require_http_methods(['GET', 'POST'])
def func(request):
    return 'yes'

#request = 'PUT'
#print(func(request))
