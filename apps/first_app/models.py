from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register(self, data):
        errors=[]
        if data['f_name']== "":
            errors.append("first name may not be blank")
        elif len(data['f_name'])<2:
            errors.append("first name must be at least 2 charactors long")
        elif not EMAIL_REGEX.match(data['email']):
            errors.append("email is not in the right format!")
        if not data['f_name'].isalpha():
            errors.append("first name may only be letters")
        if data['password']!= data['confemail']:
            errors.append("passwords do not match")
        if data['l_name'] == "":
            errors.append("Last name cannot be empty")
        try:
            Users.objects.get(email=data['email'])
            errors.append("you already have an account!!")
        except:
            pass
        if len(errors) == 0:
            user = Users.objects.create(f_name=data['f_name'], l_name=data['l_name'],email=data['email'],password=data['password'])
            return {'user':user, 'errors': None}
        else:
            return {'user':None, 'errors': errors}
        pass

    def login(self,data):
        loginerrors=[]
        # user=Users.objects.get(email = data['email'])
        try:
            user= Users.objects.get(email=data['email'])
            pass
        except:
            loginerrors.append("You do not have an account!  Please register")
            return {'users':None, 'loginerrors': loginerrors}

        print user

        if user.password == data['password']:
            pass
        else:
            loginerrors.append("Password is incorrect!")
        if len(loginerrors) == 0:
            return {'users':user, 'loginerrors':None}
        else:
            return {'users':None, 'loginerrors': loginerrors}

# Create your models here.

class Users(models.Model):
    f_name= models.CharField(max_length=50)
    l_name= models.CharField(max_length=50)
    email= models.CharField(max_length=30)
    password= models.CharField(max_length=10)
    objects= UserManager()
