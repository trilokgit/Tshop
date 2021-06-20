from django.urls import path
from store import views

urlpatterns = [
    path('',views.home,name="home"),
    path('signup',views.signup,name="signup"),
    path('login',views.login,name="login"),
    path('cart',views.cart,name="cart"),
    path('order',views.order,name="order"),
    path('logout',views.logout,name="logout"),
    path('checkout',views.checkout,name="checkout"),
    path('product/<str:slug>',views.product,name="product"), 
    path('addtocart/<str:slug>/<str:size>',views.addtocart,name="addtocart"),
    path('validate_payment',views.validatePayment,name="validate_payment"),


]
