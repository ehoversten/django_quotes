from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages

# Create your views here.
def index(request):
    # User.objects.all().delete()
    # Quote.objects.all().delete()
    return render(request, 'belt_quotes/index.html')

def dashboard(request):
    
    my_quotes = User.objects.get(id=request.session['id']).added_fav.all()
    others_quotes = Quote.objects.exclude(users_favs=request.session['id'])

    context = {
        'my_favs' : my_quotes,
        'others_quotes' : others_quotes,
    }
    return render(request, 'belt_quotes/dashboard.html', context)

def register(request):
    results = User.objects.reg_validator(request.POST)
    print("*"*25)
    print('Results OBJECT: ', results)
    print("*"*25)

    if results[0]:
        request.session['id'] = results[1].id
        request.session['name'] = results[1].name
        return redirect('/dashboard')
    else:
        for error in results[1]:
            messages.add_message(request, messages.ERROR, error, extra_tags='register')
        return redirect('/main')

def login(request):
    results = User.objects.loginValidator(request.POST)

    if results[0]:
        request.session['id'] = results[1].id
        request.session['name'] = results[1].name
        return redirect('/dashboard')
    else:
        for error in results[1]:
            messages.add_message(request, messages.ERROR, error, extra_tags='login')
        return redirect('/main')

    return redirect('/main')

def create_quote(request):
    results = Quote.objects.quote_validator(request.POST, request.session['id'])
    print("*"*25)
    print('Create Quote OBJECT: ', results)
    print("*"*25)

    if results[0]:
        return redirect('/dashboard')
    else:
        for error in results[1]:
            messages.add_message(request, messages.ERROR, error, extra_tags='login')
        return redirect('/dashboard')

def join(request, quote_id):
    user = User.objects.get(id=request.session['id'])
    this_quote = Quote.objects.get(id=quote_id)

    user.added_fav.add(this_quote)
    return redirect('/dashboard')

def take_off(request, quote_id):
    user = User.objects.get(id=request.session['id'])
    this_quote = Quote.objects.get(id=quote_id)

    user.added_fav.remove(this_quote)
    return redirect('/dashboard')

def show(request, user_id):

    user = User.objects.get(id=user_id)
# --- TEST ---

    # print("*"*25)
    # print('this user OBJECT: ', user)
    # print("*"*25)

    in_quote = user.quoted.all()
# --- TEST ---
    # print("*"*25)
    # print('User has... ', in_quote)
    # print("*"*25)

    count = len(in_quote)
# --- TEST ---

    # print("-"*25)
    # print('count OBJECT: ', count)
    # print("-"*25)
    context = {
        'all_my_quotes' : in_quote,
        'this_user' : user,
        'count' : count,
    }
    return render(request, 'belt_quotes/show.html', context)


def logout(request):
    request.session.clear()
    return redirect('/main')
