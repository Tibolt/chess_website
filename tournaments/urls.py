from django.urls import path
from . import views

app_name = 'tournaments'
urlpatterns = [
    path('', views.index, name='index'),
    path('brackets/', views.brackets_list, name='brackets'),
    # /brackets/table/1
    path('brackets/table/<int:id>', views.bracket, name='bracket'),
    path('brackets/add', views.add_bracket, name='add_bracket')
]
