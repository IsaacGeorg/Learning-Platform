from django.shortcuts import render,redirect

# Create your views here.
from django.views.generic import View
from instructor.forms import InstructorCreate

from instructor.models import User


class InstructorCreateView(View):

    def get(self,request,*args,**kwargs):
        form_instance=InstructorCreate()
        return render(request,"instructor_register.html",{"form":form_instance})

    def post(self,request,*args,**kwargs):
        form_data=request.POST
        form_instance=InstructorCreate(form_data)

        if form_instance.is_valid():

            form_instance.instance.role="instructor"
            form_instance.instance.is_superuser=True
            form_instance.instance.is_staff=True
            form_instance.save()

            return redirect("instructor-register")
        
        else:

            return render(request,"instructor_register.html",{"form":form_instance})
