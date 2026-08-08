from django.http import HttpResponse
from django.contrib import messages


def admin_required(fun):
    def wrapper(request):
        if request.user.is_superuser == False:
            messages.error(request,"You are not autherized to view this page.")
            return HttpResponse('Admin User Only')
        else:
            return fun(request)
    return wrapper