from multiprocessing import context
from datetime import date, datetime
import calendar
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.db.models import Sum
from .models import Budget, Expense, Income
from django.contrib.auth.decorators import login_required
from django.db.models.functions import TruncWeek, ExtractWeek

def auth_view(request):
    if request.method == "POST":

        #  SIGN UP
        if "name" in request.POST:
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")

            if User.objects.filter(username=username).exists():
                return render(request, "sign_in_up.html", {
                        "error": "Invalid credentials",
                        "form_type": "signin"
                    })

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )

            return redirect("auth")

        #  SIGN IN
        else:
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("dashboard") 
            else:
                return render(request, "sign_in_up.html", {
                        "error": "Invalid credentials",
                        "form_type": "signin"
                })

    return render(request, "sign_in_up.html")

def logout_view(request):
    logout(request)
    return redirect('auth')
    


@login_required
def dashboard(request):
    
    incomes = Income.objects.filter(user=request.user)
    total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
    
    expenses = Expense.objects.filter(user=request.user)
    total_spent = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    savings = total_income * 0.20
    
    budget, created = Budget.objects.get_or_create(user=request.user)
    progress_percentage = (total_spent / budget.amount) * 100 if budget.amount > 0 else 0
    remaining_budget = budget.amount - total_spent
    budget_amount = budget.amount
    
    # Chart1
    
    today = datetime.today()
    current_month = today.month
    current_year = today.year
    
    month_expenses = expenses.filter(
                                    date__year=current_year, 
                                    date__month=current_month
                                    )
    
    week_ranges = [
        (1, 7),
        (8, 14),
        (15, 21),
        (22, 31),
       
    ]
    weeks=[]
    weekly_totals = []
    
    for i, (start_day, end_day) in enumerate(week_ranges,start=1):
        total = month_expenses.filter(
                                    date__day__gte=start_day, 
                                    date__day__lte=end_day
                                    ).aggregate(Sum('amount'))['amount__sum'] or 0
        weeks.append(f"Week {i}")
        weekly_totals.append(float(total))
        
        
    # Chart2
    budget, created = Budget.objects.get_or_create(user=request.user)
    active_weeks = len([w for w in weekly_totals if w > 0])
    savings_rate = budget.savings_rate 
    savings = total_income * (savings_rate / 100)
    savings_score = min((savings / total_income * 100) / savings_rate * 100, 100
                        ) if total_income > 0 and savings_rate > 0 else 0
    budget_score = progress_percentage
    
    consistency_score = (active_weeks / 4) * 100
    health_score = round((savings_score * 0.20) + (budget_score * 0.40) + (consistency_score * 0.40))
    
    if health_score >= 80:
        health_status = "Excellent"
    elif health_score >= 60:
        health_status = "Good"
    elif health_score >= 40:
        health_status = "Fair"
    else:
        health_status = "Poor"            
    
    # chart3
    category_data = []
    categories = expenses.values('category').annotate(total=Sum('amount'))
    
    for item in categories:
        percentage=0
        
        if total_spent>0:
            percentage = round((item['total'] / total_spent) * 100)
            
            color_map = {
                "Bills": "red",
                "Rent": "rgb(221, 73, 80)",
                "Entertainment": "purple",
                "Food": "teal",
                "Shopping": "orange",
                "Transport": "blue",
                "Health": "green",
                "Other" : "maroon"
            }
        
        category_data.append({
            "category":item['category'],
            "total":item['total'],
            "percentage":percentage,
            "color": color_map.get(item['category'], "gray"),
            
        })
    
    context ={
        "total_spent": total_spent,
        "total_income": total_income,
        "total_savings": savings,
        "progress_percentage": progress_percentage,
        "remaining_budget": remaining_budget,
        "budget_amount": budget_amount,
        "category_data": category_data,
        "weeks": weeks,
        "weekly_totals": weekly_totals,
        "health_score": health_score,
        "health_status": health_status,
        "savings_score": savings_score,
        "budget_score": budget_score,
        "consistency_score": consistency_score
        
    }
    return render(request, 'dashboard.html', context)

@login_required
def expenses(request):
    
    if request.method == "POST":
        
        amount = request.POST.get("amount")
        category = request.POST.get("category")
        date = request.POST.get("date")
        description = request.POST.get("description")
        
        Expense.objects.create(
            user=request.user,
            amount=amount,
            category=category,
            date=date,
            description=description
        )

        return redirect('expenses')
    
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    
    selected_category = request.GET.get("category")
    if selected_category:
        expenses = expenses.filter(
            category=selected_category
        )
    
    search = request.GET.get("search")
    if search:
        expenses = expenses.filter(
            description__icontains=search
        )   
        
    
    total_spent = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    total_transactions = expenses.count()
    
    
    
    context = {
        "expenses": expenses,
        "total_spent": total_spent,
        "total_transactions": total_transactions,
        "selected_category": selected_category or "All"
    }
    return render(request, 'expenses.html', context)

def delete_expense(request,id):
    expense = Expense.objects.get(
        id=id,
        user=request.user
    )
    expense.delete()
    return redirect('expenses')

def income(request):
    
    budget, _ = Budget.objects.get_or_create(user=request.user)
    
    if request.method == "POST":
        
        if "savings_rate" in request.POST:
            rate = float(request.POST.get("savings_rate"))
            budget.savings_rate = rate
            budget.save()
            return redirect('income')
        
        amount = request.POST.get("amount")
        source = request.POST.get("source")
        date = request.POST.get("date")

        Income.objects.create(
            user=request.user,
            amount=amount,
            source=source,
            date=date
        )
        return redirect('income')
    
    incomes = Income.objects.filter(user=request.user).order_by('-date')
    total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
    amount = Income.objects.filter(user=request.user)
    savings_rate = budget.savings_rate 
    sources = incomes.count()
    
    for inc in incomes:
        inc.percentage = round((inc.amount / total_income) * 100) if total_income > 0 else 0
           

    
    context = {
        "incomes": incomes,
        "total_income": total_income,
        "sources": sources,
        "savings_rate": savings_rate
    }
    
    return render(request, 'income.html', context)

def delete_income(request,id):
    income = Income.objects.get(
        id=id,
        user=request.user
    )
    income.delete()
    return redirect('income')

def budget(request):
    
    budget, created = Budget.objects.get_or_create(user=request.user)
        
    
    if request.method == "POST":
        new_budget = request.POST.get("new_budget")
        budget.amount = new_budget
        budget.save()
        
        return redirect('budget')
    
    total_spent = Expense.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
    remaining_budget = budget.amount - total_spent
    progress_percentage = (total_spent / budget.amount) * 100 if budget.amount > 0 else 0
    
    today = datetime.now().day
    avg_daily_spent = (total_spent / today )if today > 0 else 0
    
    now = datetime.now()
    total_days = calendar.monthrange(now.year, now.month)[1]
    remaining_days = total_days - today
    
    daily_limit=0
    
    if remaining_days > 0:
        daily_limit = (remaining_budget / remaining_days)
    else:
        daily_limit = 0

    category_data = Expense.objects.filter(user=request.user).values('category').annotate(total=Sum('amount'))
    for item in category_data:
        item['percentage'] = (item['total'] / total_spent) * 100 if total_spent > 0 else 0
        
    
    context = {
        "budget": budget,
        "total_spent": total_spent,
        "remaining_budget": remaining_budget,
        "progress_percentage": progress_percentage,
        "avg_daily_spent": avg_daily_spent,
        "daily_limit": daily_limit,
        "remaining_days": remaining_days,
        "today": today,
        "category_data": category_data
        
        
    }
    return render(request, 'budget.html', context)

@login_required
def insights(request):
    
    today = date.today()
    expenses = Expense.objects.filter(user=request.user)
    
    # weekly overspending
    
    weekend_expenses = []
    weekday_expenses = []
    
    for expense in expenses:
        day = expense.date.weekday()
        if day >= 5:  
            weekend_expenses.append(expense.amount)
        else:
            weekday_expenses.append(expense.amount)
            
    avg_weekend = sum(weekend_expenses) / len(weekend_expenses) if weekend_expenses else 0
    avg_weekday = sum(weekday_expenses) / len(weekday_expenses) if weekday_expenses else 0
    
    if avg_weekday > 0:
        weekend_jump = ((avg_weekend - avg_weekday) / avg_weekday) * 100
    else:
        weekend_jump = 0
        
     # Rising Entertainment
     
    last_month = today.month - 1 
    last_year = today.year 
    
    if last_month == 0:
        last_month = 12
        last_year -= 1
        
    this_month_entertainment = expenses.filter(
        category="Entertainment",
        date__year=today.year,
        date__month=today.month
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    last_month_entertainment = expenses.filter(
        category="Entertainment",
        date__year=last_year,
        date__month=last_month
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    if last_month_entertainment > 0:
        entertainment_jump = ((this_month_entertainment - last_month_entertainment) / last_month_entertainment) * 100
    else:
        entertainment_jump = 0
        
    # Frequent small Expenses
    
    small_expenses = expenses.filter(
        date__year=today.year,
        date__month=today.month,
        amount__lte=500
    )
    small_count = small_expenses.count()
    small_total = small_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    
    day_totals = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    day_counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    
    for expense in expenses:
        day = expense.date.weekday()
        day_totals[day] += expense.amount
        day_counts[day] += 1
    
    # Chart Data
      
    day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    daily_pattern = []
    for i in range(7):
        avg = round(day_totals[i] / day_counts[i]) if day_counts[i] > 0 else 0
        daily_pattern.append(avg)
        
    # Latte Factor
    
    annual_impact = small_total * 12
    ten_year_impact = annual_impact * 10
    
    rate= 0.07
    years = 10
    future_value = annual_impact * (((1 + rate) ** years - 1) / rate)  
    future_value = round(future_value)
    
    # Expense Prediction
    budget, created = Budget.objects.get_or_create(user=request.user)
    today = datetime.now().day  
    total_spent = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    avg_daily_spent = (total_spent / today) if today > 0 else 0
    now = datetime.now()
    
    total_days = calendar.monthrange(now.year, now.month)[1]
    remaining_days = total_days - today
    predicted_spend = avg_daily_spent * total_days
    prediction_percentage = min((predicted_spend / budget.amount) * 100, 100) if budget.amount > 0 else 0
    if predicted_spend <= budget.amount:
        status = "Within Budget"
    else:
        status = "Over Budget"
        
    last_month = now.month - 1
    last_year = now.year

    if last_month == 0:
        last_month = 12
        last_year -= 1

    last_month_total = expenses.filter(
        date__year=last_year,
        date__month=last_month
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    

    return render(request, 'insights.html', {
        'avg_weekend': avg_weekend,
        'avg_weekday': avg_weekday,
        'weekend_jump': weekend_jump,
        'this_month_entertainment': this_month_entertainment,
        'last_month_entertainment': last_month_entertainment,
        'entertainment_jump': entertainment_jump,
        'small_count': small_count,
        'small_total': small_total,
        'day_names': day_names,
        'daily_pattern': daily_pattern,
        'annual_impact': annual_impact,
        'ten_year_impact': ten_year_impact,
        'future_value': future_value,
        'avg_daily_spent': avg_daily_spent,
        'predicted_spend': predicted_spend,
        'prediction_percentage': prediction_percentage,
        'status': status,
        'budget_amount': budget.amount,
        'last_month_total': last_month_total
        
        
        
    })