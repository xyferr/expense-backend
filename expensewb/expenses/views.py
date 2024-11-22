from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import urllib
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


import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from django.db.models import Sum
from django.shortcuts import render
from .models import Expense  # Adjust based on your app's structure


def summary_expense(request):
    # Get all the expenses of this user and calculate the total for each category
    expenses = Expense.objects.filter(owner=request.user)
    expense_list = expenses.values('category').annotate(total_amount=Sum('amount'))

    # Prepare data for the pie chart
    categories = [expense['category'] for expense in expense_list]
    amounts = [expense['total_amount'] for expense in expense_list]  # Use 'total_amount'


    #debug
    # print(expense_list)
    # print(expenses)
    # print(amounts)
    # print(categories)
    
    
    # Generate the pie chart
    fig, ax = plt.subplots()
    ax.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle.

    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read()).decode('utf-8')  # Decode to string
    buf.close()
    plt.close(fig)  # Close the figure to free memory

    # Prepare the URI for embedding in HTML
    uri = 'data:image/png;base64,' + string
    
    
    #now making bar plot of categories and their amount
    # Generate the bar plot
    fig, ax = plt.subplots()
    ax.bar(categories, amounts, color='skyblue')  # Adding color for clarity
    ax.set_xlabel('Categories')
    ax.set_ylabel('Amount')
    ax.set_title('Expenses by Category')
    bars = ax.bar(categories, amounts, color='skyblue')  # Adding color for clarity

    # Rotate and align category labels
    plt.xticks(rotation=45, ha='right')  # Rotate labels for better readability
    plt.tight_layout()  # Adjust layout to prevent clipping
    # Annotate each bar with the amount
    for bar, amount in zip(bars, amounts):
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,  # X-coordinate (center of the bar)
            height,                             # Y-coordinate (top of the bar)
            f'{amount:.2f}',                    # Text to display (formatted amount)
            ha='center',                        # Horizontal alignment
            va='bottom',                        # Vertical alignment
            fontsize=10                         # Font size
        )
        
    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string2 = base64.b64encode(buf.read()).decode('utf-8')  # Decode binary to string
    buf.close()
    plt.close(fig)  # Close the figure to release memory

    # Prepare the URI for embedding in HTML
    uri2 = 'data:image/png;base64,' + string2

    return render(request, 'expenses/summary.html', {'graph': uri , 'graph2': uri2})
   