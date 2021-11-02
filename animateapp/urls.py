from django.urls import path

from animateapp.views import AnimateCreateView

app_name = 'animateapp'

urlpatterns = [
    path('create/', AnimateCreateView.as_view(), name='create'),
]