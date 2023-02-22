import datetime
import uuid

from django.core.mail import send_mail
from myapp.settings import EMAIL_HOST_USER
from django.contrib import messages
from django.shortcuts import render,redirect
from django.http import HttpResponse


from .forms import *
from .models import *
import os
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import datetime
from datetime import timedelta


# Create your views here.

def index(request):
    return render(request,'index.html')

def register(request):
    if request.method=='POST':
        a=registerform(request.POST)
        if a.is_valid():
            us=a.cleaned_data["name"]
            pl=a.cleaned_data["place"]
            sp=a.cleaned_data["shop_id"]
            em=a.cleaned_data["email"]
            ps=a.cleaned_data["password"]
            cp=a.cleaned_data["conpassword"]
            if ps==cp:
                b=registermodel(name=us,place=pl,shop_id=sp,email=em,password=ps)
                b.save()
                return redirect(login)
            else:
                return HttpResponse("password doesn't match")
        else:
            return HttpResponse("fail")
    return render(request,'shop_regi.html')



def login(request):
    if request.method=='POST':
        a=loginform(request.POST)
        if a.is_valid():
            us=a.cleaned_data["name"]
            ps=a.cleaned_data["password"]
            b=registermodel.objects.all()
            for i in b:
                if us==i.name and ps==i.password:
                    return redirect(shop_profile)
            else:
                return HttpResponse("login Failed")
    return render(request,'shop_login.html')


def shop_profile(request):
    return render(request,'profile.html')



def product_upload(request):
    if request.method=='POST':
        a=product_upload_form(request.POST,request.FILES)
        if a.is_valid():
            pn=a.cleaned_data['name']
            pp=a.cleaned_data['price']
            fl=a.cleaned_data['imgfile']
            b=product_upload_model(name=pn,price=pp,imgfile=fl)
            b.save()
            return HttpResponse("Upload success")
        else:
            return HttpResponse("Upload failed")
    return render(request,'product_upload.html')

def product_display(request):
    a=product_upload_model.objects.all()
    name=[]
    price=[]
    img=[]
    id=[]
    for i in a:
        id1=i.id
        id.append(id1)
        nm=i.name
        name.append(nm)
        pr=i.price
        price.append(pr)
        im=i.imgfile
        img.append(str(im).split('/')[-1])
    mylist=zip(name,price,img,id)
    return render(request,'product_display.html',{'mylist':mylist})


def product_del(request,id):
    a=product_upload_model.objects.get(id=id)
    a.delete()
    return redirect(product_display)
def product_edit(request,id):
    a=product_upload_model.objects.get(id=id)
    im=str(a.imgfile).split('/')[-1]
    if request.method=='POST':
        if len(request.FILES): #new file has come or not
            if len(a.image)>0: #old file
                os.remove(a.image.path)
            a.image=request.FILES['imgfile']
        a.name=request.POST.get('name')
        a.price = request.POST.get('price')
        a.save()
        return redirect(product_display)
    return render(request,'edit.html',{'a':a,'im':im})


def regis(request):
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        password=request.POST.get('password')

        #checking whether the username exists

        if User.objects.filter(username=username).first():
            # it will get 1st object from filter query
            messages.success(request,'username is already taken')
            #message is a framework allow to store msgs in one request and retrive them in the request page

            return redirect(regis)

        if User.objects.filter(email=email).first():
            messages.success(request, 'email is already taken')
            return redirect(regis)
        user_obj=User(username=username,email=email,first_name=first_name,last_name=last_name)
        user_obj.set_password(password)
        user_obj.save()
        #import uuid
        auth_token=str(uuid.uuid4())
        #new model is created
        profile_obj=profile.objects.create(user=user_obj,auth_token=auth_token)
        profile_obj.save()
        send_mail_regis(email,auth_token)
        return  render(request,'success.html')
    return render(request,'user_pro.html')

def send_mail_regis(email,auth_token):
    subject="your account has been varified"
    message=f'click the link to verify your account http://127.0.0.1:8000/AR/verify/{auth_token}'
    email_from=EMAIL_HOST_USER
    recipient=[email]
    send_mail(subject,message,email_from,recipient)

def verify(request,auth_token):
    profile_obj=profile.objects.filter(auth_token=auth_token).first()
    if profile_obj:
        if profile_obj.is_verified:
            messages.success(request,'your account is already verified')
            return redirect(user_login)
        profile_obj.is_verified=True
        profile_obj.save()
        messages.success(request,'your account has been verified')
        return redirect(user_login)
    else:
        messages.success(request,'user not found')
        return redirect(user_login)
def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user_obj= User.objects.filter(username=username).first()
        if user_obj is None:
            messages.success(request,'user not found')
            return redirect(user_login)
        profile_obj=profile.objects.filter(user=user_obj).first()
        if not profile_obj.is_verified:
            messages.success(request,'profile not verified check your email')
            return redirect(user_login)
        user=authenticate(username=username,password=password)
        if user is None:
            messages.success(request,'wrong password or username')
            return redirect(user_login)
        return redirect(user_profile)
    return render(request,'user_login.html')


def user_profile(request):
    return render(request,'user_profile.html')


def user_product_all(request):
    a = product_upload_model.objects.all()
    name = []
    price = []
    img = []
    id = []
    for i in a:
        id1 = i.id
        id.append(id1)
        nm = i.name
        name.append(nm)
        pr = i.price
        price.append(pr)
        im = i.imgfile
        img.append(str(im).split('/')[-1])
    mylist = zip(name, price, img, id)
    return render(request, 'user_product.html', {'mylist': mylist})


def addcart(request,id):
    a=product_upload_model.objects.get(id=id)
    if cart.objects.filter(name=a.name):
        messages.success(request,'already added')
        return redirect(cart_al_ready)
    b=cart(name=a.name,price=a.price,imgfile=a.imgfile)
    b.save()
    return redirect(cartdis)

def cart_al_ready(request):
    return render(request,'cart_already_added.html')

def wishlist1(request,id):
    a=product_upload_model.objects.get(id=id)
    if wishlist.objects.filter(name=a.name):
        messages.success(request,'already added')
        return redirect(wish_al_ready)
    b=wishlist(name=a.name,price=a.price,imgfile=a.imgfile)
    b.save()
    return redirect(wishlistdis)

def wish_al_ready(request):
    return render(request,'wish_already_added.html')





def wishlistdis(request):
    a=wishlist.objects.all()
    name=[]
    price=[]
    img=[]
    id=[]
    for i in a:
        id1=i.id
        id.append(id1)
        nm=i.name
        name.append(nm)
        pr=i.price
        price.append(pr)
        im=i.imgfile
        img.append(str(im).split('/')[-1])
    mylist=zip(name,price,img,id)
    print(name)
    return render(request,'wishlist.html',{'mylist':mylist})


def cartdis(request):
    a=cart.objects.all()
    name=[]
    price=[]
    img=[]
    id=[]
    for i in a:
        id1=i.id
        id.append(id1)
        nm=i.name
        name.append(nm)
        pr=i.price
        price.append(pr)
        im=i.imgfile
        img.append(str(im).split('/')[-1])
    mylist=zip(name,price,img,id)

    return render(request,'cart.html',{'mylist':mylist})



def cart_del(request,id):
    a=cart.objects.get(id=id)
    a.delete()
    return redirect(cartdis)

def wish_del(request,id):
    a=wishlist.objects.get(id=id)
    a.delete()
    return redirect(wishlistdis)

def wishcart(request,id):
    a=wishlist.objects.get(id=id)
    if cart.objects.filter(name=a.name):
        messages.success(request,'already added')
        return redirect(wishcart_al_ready)
    b = cart(name=a.name, price=a.price, imgfile=a.imgfile)
    b.save()
    return redirect(wishlistdis)

def wishcart_al_ready(request):
    return render(request,'wish_cart_already.html')



def cart_buy(request,id):
    a=cart.objects.get(id=id)
    im=str(a.imgfile).split('/')[-1]
    if request.method=='POST':
        name=request.POST.get('name')
        price=request.POST.get('price')
        quantity=request.POST.get('quantity')
        b=buy(name=name,price=price,quantity=quantity)
        b.save()
        total=int(price)*int(quantity)
        return render(request,'final_bill.html',{'b':b,'tt':total})
    return render(request,'buyproduct.html',{'a':a ,'im':im})




def card_pay(request):
    if request.method=='POST':
        cardname=request.POST.get('cardname')
        cardnumber=request.POST.get('cardnumber')
        cardexpiry=request.POST.get('cardexpiry')
        code=request.POST.get('code')
        user_obj=customercard(cardname=cardnumber,cardnumber=cardnumber,cardexpiry=cardexpiry,code=code)
        user_obj.save()
        today=datetime.date.today()
        today+=timedelta(days=10)
        return render(request,"success.html")
    return render(request,'card_payment.html')