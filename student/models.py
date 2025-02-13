from django.db import models
from instructor.models import Course,User
# Create your models here.

class Order(models.Model):
    course_objects=models.ManyToManyField(Course,related_name="enrollment")
    student=models.ForeignKey(User,on_delete=models.CASCADE,related_name="purchase")
    is_paid=models.BooleanField(default=False)
    rsp_order_id=models.CharField(max_length=100,null=True)
    created_date=models.DateTimeField(auto_now_add=True)
    total=models.DecimalField(decimal_places=2, max_digits=12)