from django.urls import path
from .views import *



urlpatterns=[
    path('index/',index),
    path('register/',register),
    path('login/',login),
    # path('userregi/',user_register),
    path('shoppro',shop_profile),
    path('upload/',product_upload),
    path('prodis/',product_display),
    path('del/<int:id>',product_del),
    path('edit/<int:id>',product_edit),
    path('userreg/',regis),
    path('verify/<auth_token>',verify),
    path('userlog/',user_login),
    path('userprofile/',user_profile),
    path('userprodis/',user_product_all),
    path('cart/<int:id>',addcart),
    path('wish/<int:id>',wishlist1),
    path('cartdis/',cartdis),
    path('wishdis/',wishlistdis),
    path('cartdel/<int:id>',cart_del),
    path('wishdel/<int:id>',wish_del),
    path('wishcart/<int:id>',wishcart),
    path('cartbuy/<int:id>',cart_buy),
    path('cardpay/',card_pay),
    path('cartalready',cart_al_ready),
    path('wishalready',wish_al_ready),
    path('wishcartalready',wishcart_al_ready)


]