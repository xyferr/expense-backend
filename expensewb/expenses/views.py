from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Expense, Category
from django.shortcuts import redirect

from userpreferences.models import UserPreference
from django.core.paginator import Paginator
import json
from django.http import JsonResponse

#import messages
from django.contrib import messages

# Create your views here.

def search_expenses(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        
        expenses = Expense.objects.filter(
            amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
            description__icontains=search_str, owner=request.user) | Expense.objects.filter(
            category__icontains=search_str, owner=request.user)
        
        data = expenses.values()
        return JsonResponse(list(data), safe=False)




@login_required(login_url='/auth/login')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    try:
        currency = UserPreference.objects.get(user=request.user).currency
    except UserPreference.DoesNotExist:
        currency = 'USD'  # Default currency if UserPreference does not exist
    
    context={
        'categories': categories,
        'expenses': expenses,
        'currency': currency,
        'page_obj': page_obj
    }
    return render(request, 'expenses/index.html', context)

def add_expense(request):
    categories = Category.objects.all()
    context={
        'categories': categories,
        'values': request.POST  
    }
    
    if request.method == 'GET':
        
        return render(request, 'expenses/add_expenses.html',context)
    
    elif request.method == 'POST':
        amount = request.POST['amount']
        category = request.POST['category']
        #check if user added date or not , and set date to current date and time
        
        
        description = request.POST['description']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expenses.html',context)
        if not category:
            messages.error(request, 'Category is required')
            return render(request, 'expenses/add_expenses.html',context)
        if request.POST['date']:
            date = request.POST['date']
            Expense.objects.create(amount=amount, category=category, date=date, description=description, owner=request.user)
        else:
            Expense.objects.create(amount=amount, category=category, description=description, owner=request.user)
        messages.success(request, 'Expense added successfully')
        return redirect('expenses')
    
def edit_expense(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context={
        'values': expense,
        'categories': categories,
    }
    
    if request.method == 'GET':
        
        return render(request, 'expenses/edit-expense.html', context)
    else:
        amount = request.POST['amount']
        category = request.POST['category']
        description = request.POST['description']
        date = request.POST['date']
        
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit-expense.html', context)
        if not category:
            messages.error(request, 'Category is required')
            return render(request, 'expenses/edit-expense.html', context)
        
        expense.amount = amount
        expense.category = category
        expense.description = description
        if not date:
            expense.save()
        else:
            expense.date = date
            expense.save()  
            
            
        messages.success(request, 'Expense updated successfully')
        return redirect('expenses')
    
def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense removed')
    return redirect('expenses')