from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('product/', views.product, name='product'),
    path('company/', views.company, name='company'),
    path('company/message/', views.company_message, name='company_message'),
    path('company/profile/', views.company_profile, name='company_profile'),
    path('company/history/', views.company_history, name='company_history'),
    path('company/organization/', views.company_organization, name='company_organization'),
    path('recruit/', views.recruit, name='recruit'),
    path('recruit/apply/', views.recruit_apply, name='recruit_apply'),
    path('news/', views.news, name='news'),
    path('contact/', views.contact, name='contact'),
]
