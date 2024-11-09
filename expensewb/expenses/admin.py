from django.contrib import admin
from .models import Expense, Category

# Register your models here.

#Admin panel me aur attributes display karne ke liye
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['amount', 'description', 'category', 'owner', 'date']
    search_fields = ['amount', 'date', 'category', 'owner']
    list_filter = ['date', 'category', 'owner']
    
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Category, CategoryAdmin)
