from django.shortcuts import render, HttpResponse, redirect
import bcrypt
from .models import *
from django.contrib import messages


# Create your views here.
def index(request):
    return render(request,'belt_exam_app/index.html')

def process(request):
    
    errors = User.objects.reg_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        if 'fname' not in request.session:
            request.session['fname'] = ""
        if 'id' not in request.session:
            request.session['id'] = 0
        input_pass = request.POST['pass']
        hash1 = bcrypt.hashpw(input_pass.encode(), bcrypt.gensalt())
        print "password is.....{}....{}".format(input_pass,hash1)
        u = User.objects.create(name = request.POST['name'], alias = request.POST['alias'], email = request.POST['email'], password = hash1, dob = request.POST['bday'])
        request.session['fname'] = request.POST['name']
        request.session['id'] = u.id
        return redirect('/quotes')
def login_process(request):
    errors1 = User.objects.login_validator(request.POST)
    if len(errors1):
        for tag, error in errors1.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        if 'fname' not in request.session:
            request.session['fname'] = ""
        
        u = []
        u = User.objects.filter(email = request.POST['login_email'])
        request.session['fname'] = u[0].name
        request.session['id'] = u[0].id
        return redirect('/quotes')
    # return redirect('/')

def quotes(request):
    print "session id is------{}".format(request.session['id'])
    context = {}
    c = User.objects.get(id = request.session['id'])
    a = c.favorite_quotes.all()
    b = Quote.objects.all()

    context = {
        'quotes': Quote.objects.exclude(favorite = c),
        'favorites' : c.favorite_quotes.all()
    }

    return render(request,'belt_exam_app/success.html',context)

def add_quote(request):
    errors2 = Quote.objects.quote_validator(request.POST)
    if len(errors2):
        for tag, error in errors2.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/quotes')
    else:
        Quote.objects.create(quote = request.POST['message'],quoted_by = request.POST['quoted_by'],user_id = request.session['id'])
    return redirect('/quotes')

def add_favorite(request , id):
    
    this_quote = Quote.objects.get(id = id)
    this_user = User.objects.get(id = request.session['id'])
    this_quote.favorite.add(this_user)
    return redirect('/quotes')

def remove_favorite(request, id):
    this_user = User.objects.get(id = request.session['id'])
    this_quote = Quote.objects.get(id = id)
    this_quote.favorite.remove(this_user)
    
    return redirect('/quotes')

def show_user(request, id):
    context = {}
    context = {
        'user' : User.objects.filter(id = id),
        'quotes' : Quote.objects.filter(user_id = id),
        'count' : Quote.objects.filter(user_id = id).count()
    }
    return render(request,'belt_exam_app/show_user.html',context)

def logout(request):
    request.session['id'] = 0,
    request.session['fname'] = ""
    return redirect('/')


