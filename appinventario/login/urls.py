from login.views import *
from django.urls.conf import path


urlpatterns = [
    path('', LoginFormView.as_view(), name='login'),
    #path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('logout/', LogoutRedirectView.as_view(), name='logout'),
    #path('logout/', LogoutView.as_view(), name='logout'), #Otra manera
]
