from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Users

def index(request):
    return render(request, 'first_app/index.html')

def registration(request):
    data={
    'f_name':request.POST['f_name'],
    'l_name':request.POST['l_name'],
    'email':request.POST['email'],
    'password':request.POST['password'],
    'confemail':request.POST['confirm_pw']
    }

    result= Users.objects.register(data)
    if result['errors'] == None:
        request.session['user']= result['user'].id
        return redirect('/profile')
    else:
        for error in result['errors']:
            print error
            messages.add_message(request, messages.ERROR, error)
            return redirect('/')

    # for error in result['errors']:
    #         message.add_message(request messages.ERROR, errors)
    #         return redirect('/')

    return render(request, "first_app/registration")

def login(request):
    print request.POST
    data={
    'email': request.POST['logemail'],
    'password':request.POST['password']
    }
    result= Users.objects.login(data)
    if result['loginerrors']==None:
        request.session['user']=result['user'].id
        return redirect('/profile')
    else:
        for loginerror in result['loginerrors']:

            messages.add_message(request, messages.ERROR, loginerror)
            return redirect('/')



def profile(request):
    id=request.session['user']
    user = Users.objects.get(id=int(id))
    # print user
    # print Users.objects.filter(id=id).values('name')

    context={
    'first':user.f_name,
    'last':user.l_name,
    'email':user.email
    }
    return render(request, "first_app/profile.html", context)
