from django.shortcuts import render,redirect
from django.views.generic import View, FormView, CreateView, TemplateView
from student.forms import StudentCreateForm, StudentSignInForm

from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login

from instructor.models import Course
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

        return render(request,"index.html",{"courses":allcourses})



class CourseDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        course_instance=Course.objects.get(id=id)
        return render(request,"course_detail.html",{"course":course_instance})