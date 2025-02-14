from django.shortcuts import render,redirect
from django.views.generic import View, FormView, CreateView, TemplateView
from student.forms import StudentCreateForm, StudentSignInForm
from instructor.models import Cart, Module, Lesson

from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login

from instructor.models import Course

from django.db.models import Sum

from student.models import Order
# Create your views here.
class StudentRegisterView(CreateView):

    template_name="studentreg.html"
    form_class=StudentCreateForm
    success_url=reverse_lazy("signin")

    # def get(self,request,*args,**kwargs):
    #     form_instance=StudentCreateForm()
    #     return render(request,"studentreg.html",{"form":form_instance})
    



# Template View
# Form View
# Create View

class StudentSignInView(FormView):
    template_name="studentreg.html"
    form_class=StudentSignInForm

    def post(self, request, *args, **kwargs):
        form_data=request.POST
        form_instance=StudentSignInForm(form_data)

        if form_instance.is_valid():
            data=form_instance.cleaned_data
            
            uname=data.get("username")
            pwd=data.get("password")

            user_instance=authenticate(request,username=uname,password=pwd)

            if user_instance:
                login(request,user_instance)
                return redirect("index")
        
        else:

            return render(request,"studentreg.html",{"form":form_instance})
        

class IndexView(View):
    def get(self,request,*args,**kwargs):
        allcourses=Course.objects.all()
        purchased_courses=Order.objects.filter(student=request.user).values_list("course_objects",flat=True)
        print(purchased_courses)

        return render(request,"index.html",{"courses":allcourses,"purchased_courses":purchased_courses})



class CourseDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        course_instance=Course.objects.get(id=id)
        return render(request,"course_detail.html",{"course":course_instance})
    

class AddToCartView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        course_instance=Course.objects.get(id=id)
        user_instance=request.user
        cart_instance,created=Cart.objects.get_or_create(course_object=course_instance,user=user_instance)
        print(created,"===============")
        return redirect("index")


class CartSummaryView(View):
    def get(self,request,*args,**kwargs):
        qs=request.user.basket.all()

        # or 
        # qs= Cart.objects.filter(user=request.user)

        cart_total=qs.values("course_object__price").aggregate(total=Sum("course_object__price")).get("total")
        print("cart_total =",cart_total)

        return render(request,"cart_summary.html",{"carts":qs,"basket_total":cart_total})
    


class CartDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Cart.objects.get(id=id).delete()
        return redirect("cart-summary")
    


class CheckOutView(View):
    def get(self,request,*args,**kwargs):
        cart_items=request.user.basket.all()
        order_total=sum([ci.course_object.price for ci in cart_items])
        order_instance=Order.objects.create(student=request.user,total=order_total)

        for ci in cart_items:
            order_instance.course_objects.add(ci.course_object)
            ci.delete()

        order_instance.save()
        return redirect("index")
    


class MyCoursesView(View):
    def get(self,request,*args,**kwargs):
        qs=request.user.purchase.all()
        return render(request,"mycourses.html",{"orders":qs})
    





class LessonDetailView(View):
    def get(self,request,*args,**kwargs):


# localhost:8000//student/courses/1/watch?module=1&lesson=5/  (requried url)

        course_id=kwargs.get("pk")
        course_instance=Lesson.objects.get(id=course_id)
        
        # request.GET = {"module":1,"lesson":5}

        module_id= request.GET.get("module") if "module" in request.GET else 1
        lesson_id= request.GET.get("lesson") if "lesson" in request.GET else 1

        print(module_id,"&&&&&&&&&&&&&&&&&&&&")
        print(lesson_id,"$$$$$$$$$")

        module_instance = Module.objects.get(id=module_id,course_object=course_instance)
        lesson_instance=Lesson.objects.get(id=lesson_id,module_object=module_instance)

        return render(request,"lesson_detail.html",{"course":course_instance,"lesson":lesson_instance})