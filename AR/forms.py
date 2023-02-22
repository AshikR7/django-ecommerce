from django import forms

class registerform(forms.Form):
    name = forms.CharField(max_length=20)
    place = forms.CharField(max_length=20)
    shop_id = forms.IntegerField()
    email = forms.EmailField()
    password = forms.CharField(max_length=20)
    conpassword = forms.CharField(max_length=20)

class loginform(forms.Form):
    name = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20)

#
# class user_registerform(forms.Form):
#     name = forms.CharField(max_length=20)
#     place = forms.CharField(max_length=20)
#     email = forms.EmailField()
#     password = forms.CharField(max_length=20)
#     conpassword = forms.CharField(max_length=20)


class product_upload_form(forms.Form):
    name = forms.CharField(max_length=20)
    price = forms.IntegerField()
    imgfile = forms.ImageField()

class customercardform(forms.Form):
    cardname = forms.CharField(max_length=30)
    cardnumber = forms.CharField(max_length=30)
    cardexpiry = forms.CharField(max_length=30)
    code = forms.CharField(max_length=30)