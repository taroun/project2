from django.urls import path

from animateapp.views import AnimateCreateView, AnimateDetailView, FileDownloadView

app_name = 'animateapp'

urlpatterns = [
    path('create/', AnimateCreateView.as_view(), name='create'),
    path('detail/<int:pk>', AnimateDetailView.as_view(), name='detail'),
    #path('document/<int:pk>', FileDownloadView.as_view(), name="download"),
    #path('download/<id>', views.download, name='download'),
]