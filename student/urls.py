from django.urls import path
from student import views
urlpatterns=[
    path("register/",views.StudentRegisterView.as_view(),name="student-register"),
    path("signin/",views.StudentSignInView.as_view(),name="signin"),
    path("index/",views.IndexView.as_view(),name='index'),
    path("coursedetail/<int:pk>/",views.CourseDetailView.as_view(),name='course-detail'),
    path("courses/<int:pk>/add-to-cart/",views.AddToCartView.as_view(),name="add-to-cart"),
    path("cart/summary/",views.CartSummaryView.as_view(),name="cart-summary"),
    path("cart/remove/<int:pk>/",views.CartDeleteView.as_view(),name="cart-remove"),
    path('checkout/',views.CheckOutView.as_view(),name="check-out"),
    path("mycourses/",views.MyCoursesView.as_view(),name="mycourses"),
    
]