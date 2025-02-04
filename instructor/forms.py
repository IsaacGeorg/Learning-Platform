
from django.contrib.auth.forms import UserCreationForm

from instructor.models import User

class InstructorCreate(UserCreationForm):

    class Meta:
        model=User
        fields=["username","email","password1","password2","first_name"]