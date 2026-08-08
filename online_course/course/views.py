from http.client import HTTPResponse
from idlelib import query
from multiprocessing import context

from django.db.models import Model
from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

import course
from course.forms import CourseForm,RegisterForm,LoginForm
from course.models import Course,Payment


# Create your views here.

class Index(View):
    def get(self,request):
        return render(request,'index.html')



class Home(View):
    def get(self, request):
        return render(request,'home.html')


class About(View):
    def get(self, request):
        return render(request,'about.html')


class Courses(View):
    def get(self,request):
        c=Course.objects.all()
        context={'course':c}
        return render(request,'course.html', context)



class CourseDetail(View):

    def get(self, request,i ):

        detail = get_object_or_404(Course, id=i)

        has_paid = False

        if request.user.is_authenticated:
            has_paid = Payment.objects.filter(
                user=request.user,
                payment_status='Success'
            ).exists()

        return render(
            request,
            'coursedetail.html',
            {
                'detail': detail,
                'has_paid': has_paid
            }
        )





# Authentications

class UserLogin(View):
    def get(self, request):
        form_instance = LoginForm()
        context = {'form': form_instance}

        return render(request, 'login.html', context)

    def post(self, request):
        form_instance = LoginForm(request.POST)
        if form_instance.is_valid():

            data = form_instance.cleaned_data

            u = data['username']
            p = data['password']

            # authenticate(username,password)
            #

            user = authenticate(username=u, password=p)

            if user and user.is_superuser == True:
                login(request, user)  # adds the user into current session
                u = request.user
                print(u)
                return redirect('home')

            elif user and user.is_superuser == False:
                login(request, user)
                b=request.i=user
                print(b)
                return redirect('home')
            else:
                messages.error(request, 'Incorrect Username and Password')
                return redirect('userlogin')


from django.contrib.auth.models import User

class UserRegister(View):
    def get(self,request):
        return render(request,'Register.html')

    def post(self,request):
        username=request.POST.get('username')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        email = request.POST.get('email')

        if password == confirm_password:
            user=User.objects.create_user(username=username,password=password,email=email)
            user.save()
            return redirect('userlogin')
        else:
            pass


class UserLogout(View):
    def get(self,request):
        logout(request)
        return redirect('userlogin')







# Add Category and Course




class AddCourse(View):
    def get(self,request):
        form_instance=CourseForm()
        context={'form':form_instance}
        return render(request,'addcourse.html',context)

    def post(self,request):
        name=request.POST.get('name')
        description=request.POST.get('description')
        duration=request.POST.get('duration')
        price = request.POST.get('price')
        modules = request.POST.get('modules')
        image = request.FILES.get('image')
        Course.objects.create(name=name,description=description,duration=duration,price=price,
                                      modules=modules,image=image)

        return redirect('courses')





import razorpay







class PaymentView(View):

    def get(self, request):
        courses = Course.objects.all()

        return render(
            request,
            'payment.html',
            {'courses': courses}
        )

    def post(self, request):

        # Prevent duplicate application
        if Payment.objects.filter(
            user=request.user,
            payment_status='Success'
        ).exists():

            messages.warning(
                request,
                "You have already applied for a course."
            )

            return redirect('payment-history')

        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        whatsapp = request.POST.get('whatsapp')

        course_id = request.POST.get('course')
        learning_mode = request.POST.get('learning_mode')

        course = get_object_or_404(
            Course,
            id=course_id
        )

        # Create Payment record first
        payment = Payment.objects.create(
            user=request.user,
            name=name,
            email=email,
            phone=phone,
            whatsapp=whatsapp,
            course=course,
            learning_mode=learning_mode,
            amount=1000,
            payment_status='Pending'
        )

        # Store Payment ID
        request.session['payment_id'] = payment.id

        print("CREATED PAYMENT:", payment.id)

        return redirect('razorpay-payment')








class PaymentSuccessView(View):

    def get(self, request):

        payment_id = request.GET.get('payment_id')
        order_id = request.GET.get('order_id')



        payment = get_object_or_404(
            Payment,
            razorpay_order_id=order_id,
            user=request.user
        )

        payment.razorpay_payment_id = payment_id
        payment.payment_status = "Success"
        payment.save()

        return render(
            request,
            'payment_success.html',
            {
                'payment': payment
            }
        )


    import razorpay

class RazorpayPaymentView(View):

    def get(self, request):

        amount = 1000

        client = razorpay.Client(
            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET
            )
        )

        order = client.order.create({
            'amount': 100000,
            'currency': 'INR',
            'payment_capture': True
        })

        print("RAZORPAY ORDER:", order)

        # Get Payment object
        payment_id = request.session.get('payment_id')

        print("PAYMENT ID:", payment_id)

        payment = get_object_or_404(
            Payment,
            id=payment_id,
            user=request.user
        )

        # SAVE ORDER ID
        payment.razorpay_order_id = order['id']
        payment.save()

        print("SAVED ORDER ID:", payment.razorpay_order_id)

        return render(
            request,
            'razorpay_payment.html',
            {
                'order': order,
                'amount': amount,
                'razorpay_key': settings.RAZORPAY_KEY_ID
            }
        )



class PaymentHistoryView(View):

    def get(self, request):

        payments = Payment.objects.filter(user=request.user).order_by('-id')

        return render(request,'payment_history.html',{'payments': payments})




from django.db.models import Q

class Search(View):
    def get(self,request):

        query=request.GET['q']

        c=Course.objects.filter(Q(name__icontains=query)|
                                Q(price__icontains=query)|
                                Q(description__icontains=query))
        context={'search':c}
        return render(request,'search.html',context)


from django.conf import settings

class Contact(View):
    def get(self, request):
        courses = Course.objects.all()
        context = {'course': courses}
        return render(request, 'contact.html', context)




class EditView(View):
    def get(self,request,i):
        b = Course.objects.get(id=i)
        form_instance = CourseForm(instance = b)
        context = {'form':form_instance}
        return render(request,'edit.html',context)


    def post(self,request,i):
        b = Course.objects.get(id=i)
        form_instance = CourseForm(request.POST,request.FILES,instance = b)
        if form_instance.is_valid():
            form_instance.save()

        return redirect('courses')


class DeleteView(View):
    def get(self,request,i):
        m = Course.objects.get(id=i)
        m.delete()
        return  redirect('courses')


class PaymentDetail(View):
    def get(self,request):
        c=Payment.objects.all()
        context = {'detail':c}
        return render(request,'paymentdetail.html',context)




from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Payment


class PaymentUser(View):

    def get(self, request, i):

        # Only superuser can access
        if not request.user.is_authenticated or not request.user.is_superuser:
            return redirect('home')

        payment = get_object_or_404(
            Payment,
            id=i
        )

        return render(
            request,
            'payment_user.html',
            {
                'payment': payment
            }
        )