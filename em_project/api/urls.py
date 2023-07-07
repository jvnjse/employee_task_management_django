
from django.urls import path
from .views import UserRegistrationView, UserLoginView,UserListView,JobView,AssignedJobsView,JobStatusView


urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path('api/users/', UserListView.as_view(), name='user-list'),
    path('api/jobs/', JobView.as_view(), name='job-create'),
    path('api/jobs/<int:pk>/', JobView.as_view(), name='job-detail'),
    path('api/assigned-jobs/', AssignedJobsView.as_view(), name='assigned-jobs'),
    path('api/jobs/<int:pk>/status/', JobStatusView.as_view(), name='job-status'),

]
