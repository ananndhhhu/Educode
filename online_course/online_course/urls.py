"""
URL configuration for online_course project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views import View

from course import views


app_name = 'course'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.Index.as_view(),name='index'),
    path('home',views.Home.as_view(),name='home'),
    path('about',views.About.as_view(),name='about'),

    path('coursedetail<int:i>/',views.CourseDetail.as_view(),name='coursedetail'),

    path('userlogin',views.UserLogin.as_view(),name='userlogin'),
    path('register/',views.UserRegister.as_view(),name='register'),
    path('userlogout',views.UserLogout.as_view(),name='userlogout'),
    path('addcourse',views.AddCourse.as_view(),name='addcourse'),
    path('courses',views.Courses.as_view(),name='courses'),
    path('payment',views.PaymentView.as_view(),name='payment'),
    path('search',views.Search.as_view(),name='search'),
    path('contact',views.Contact.as_view(),name='contact'),
    path('edit<int:i>/',views.EditView.as_view(),name='edit'),
    path('delete<int:i>/',views.DeleteView.as_view(),name='delete'),
    path('paymentdetail',views.PaymentDetail.as_view(),name='paymentdetail'),
    path('payment-success/',views.PaymentSuccessView.as_view(),name='payment-success'),
    path('payment-history/',views.PaymentHistoryView.as_view(),name='payment-history'),
    path('razorpay-payment/',views.RazorpayPaymentView.as_view(),name='razorpay-payment'),
    path('paymentuser<int:i>/',views.PaymentUser.as_view(),name='paymentuser')
]



from django.conf.urls.static import static
from django.conf import settings

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)



