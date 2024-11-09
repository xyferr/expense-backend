from django.urls import path
from . import views
#import csrf exempt
from django.views.decorators.csrf import csrf_exempt




urlpatterns = [
    path('', views.index, name='expenses'),
    path('add_expense', views.add_expense, name='add_expense'),
    path('edit_expense/<int:id>', views.edit_expense, name='edit-expense'),
    path('delete_expense/<int:id>', views.delete_expense, name='delete-expense'),
    path('search-expenses', csrf_exempt(views.search_expenses), name='search-expenses'),
]
