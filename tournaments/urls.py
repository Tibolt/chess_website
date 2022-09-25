from django.urls import path
from . import views

app_name = 'tournaments'
urlpatterns = [
    path('', views.index, name='index'),
    path('brackets/', views.brackets_list, name='brackets'),
    # /brackets/table/1
    path('brackets/table/<int:id>', views.bracket, name='bracket'),
    path('brackets/add', views.add_bracket, name='add_bracket'),
    path('brackets/table/<int:id>/add', views.add_players, name='add_players'),
    path('brackets/table/<int:id>/edit', views.edit_players, name='edit_players'),
    path('brackets/table/<int:id>/rounds/<int:round>', views.rounds, name='rounds'),
    path('brackets/table/<int:id>/rounds/<int:round>/edit', views.edit_rounds, name='edit_rounds'),
]
