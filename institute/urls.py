# urls.py
from django.urls import path
from .views import InstituteCreate,InstituteBatch
urlpatterns = [
    path('institutes/', InstituteCreate.as_view(), name='create-institute'),
    path('batch/', InstituteBatch.as_view(), name='create-institute'),
    path('batch/<int:institute_id>/', InstituteBatch.as_view(), name='institute-batches'),

]
