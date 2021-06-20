from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from store.forms.authforms import CustomerCreationForm, CustomerAuthForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as Login, logout as Logout
from store.models import Tshirt, SizeVariant, Cart, Order, OrderItem, Payment, Occasion, Brand, Color, IdealFor, NackType, Sleeve
from urllib.parse import urlencode

from django.contrib.auth.decorators import login_required
from store.forms.checkout_form import CheckForm
from instamojo_wrapper import Instamojo
from Tshop.settings import API_KEY, AUTH_TOKEN
api = Instamojo(api_key=API_KEY, auth_token=AUTH_TOKEN)


# Create your views here.


def home(request):

    query = request.GET

    tshirts = []
    tshirts = Tshirt.objects.all()
    brand = query.get('brand')
    sleeve = query.get('sleeve')
    nacktype = query.get('nacktype')
    color = query.get('color')
    idealfor = query.get('idealfor')
    page = query.get("page")
    
    if(page is None or page == ''):
        page=1
       


    if brand != "" and brand is not None:
        tshirts = tshirts.filter(brand__slug=brand)
    if nacktype != "" and nacktype is not None:
        tshirts = tshirts.filter(nack_type__slug=nacktype)
    if color != "" and color is not None:
        tshirts = tshirts.filter(color__slug=color)
    if sleeve != "" and sleeve is not None:
        tshirts = tshirts.filter(sleeve__slug=sleeve)
    if idealfor != "" and idealfor is not None:
        tshirts = tshirts.filter(ideal_for__slug=idealfor)

    occasions = Occasion.objects.all()
    brands = Brand.objects.all()
    sleeves = Sleeve.objects.all()
    nacktypes = NackType.objects.all()
    colors = Color.objects.all()
    idealfors = IdealFor.objects.all()
    cart = request.session.get('cart')
    paginator = Paginator(tshirts , 3)
    page_obj = paginator.get_page(page)

    query = request.GET.copy()
    query['page'] = ''
    pageurl = urlencode(query)

    context = {
        'page_object': page_obj,
        "occasions": occasions,
        "brands": brands,
        "nacktypes": nacktypes,
        "colors": colors,
        "idealfors": idealfors,
        "sleeves": sleeves,
        "pageurl":pageurl
    }


    return render(request, 'store/home.html', context=context)


def signup(request):
    if request.method == 'GET':
        form = CustomerCreationForm()
        context = {
            "form": form
        }

        return render(request, 'store/signup.html', context=context)
    else:
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = user.username
            user.save()
            return redirect('login')
    context = {
        "form": form
    }

    return render(request, 'store/signup.html', context=context)


def login(request):

    if request.method == 'GET':
        form = CustomerAuthForm()
        next_page = request.GET.get('next')
        if next_page is not None:
            request.session['next_page'] = next_page

        context = {

            'form': form
        }
        return render(request, 'store/login.html', context=context)
    else:
        form = CustomerAuthForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                Login(request, user)
                session_cart = request.session.get('cart')
                if session_cart is None:
                    session_cart = []
                else:
                    for c in session_cart:
                        size = c.get('size')
                        tshirt_id = c.get('tshirt')
                        quantity = c.get('quantity')
                        cart_obj = Cart()
                        cart_obj.sizeVariant = SizeVariant.objects.get(
                            size=size, tshirt=tshirt_id)
                        cart_obj.quantity = quantity
                        cart_obj.user = user
                        cart_obj.save()

                # we store in session {tshirt_id,size_of_tshirt,quantity}
                carts = Cart.objects.filter(user=user)
                session_cart = []
                for c in carts:
                    obj = {
                        'size': c.sizeVariant.size,
                        'tshirt': c.sizeVariant.tshirt.id,
                        'quantity': c.quantity
                    }
                    session_cart.append(obj)

                request.session['cart'] = session_cart
                next_page = request.session.get('next_page')
                if next_page is None:
                    next_page = 'home'

                return redirect(next_page)

        else:
            return render(request, 'store/login.html', context={'form': form})


def cart(request):
    cart = request.session.get('cart')
    if cart is None:
        cart = []
    for c in cart:
        tshirt_id = c.get('tshirt')
        tshirt = Tshirt.objects.get(id=tshirt_id)
        c['size'] = SizeVariant.objects.get(tshirt=tshirt_id, size=c['size'])
        c['tshirt'] = tshirt
    return render(request, 'store/cart.html', {'cart': cart})


@login_required(login_url='/login')
def order(request):
    user = request.user
    orders = Order.objects.filter(user=user).order_by('-date').exclude(order_status="PENDING")
    context = {
        "orders": orders
    }

    return render(request, 'store/orders.html', context=context)


def logout(request):

    Logout(request)
    return redirect('login')


def product(request, slug):

    tshirt = Tshirt.objects.get(slug=slug)
    size = request.GET.get('size')

    if size is None:
        size = tshirt.sizevariant_set.all().order_by('price').first()
    else:
        size = tshirt.sizevariant_set.get(size=size)

    sell_price = int(size.price - (size.price*(tshirt.discount/100)))
    context = {
        'tshirt': tshirt, 'price': size.price, 'sell_price': sell_price, 'active_size': size
    }

    return render(request, 'store/product_details.html', context=context)


def addtocart(request, slug, size):
    user = None
    if request.user.is_authenticated:
        user = request.user

    cart = request.session.get('cart')
    if cart is None:
        cart = []

    tshirt = Tshirt.objects.get(slug=slug)
    size_temp = SizeVariant.objects.get(size=size, tshirt=tshirt)
    flag = True
    for cart_obj in cart:
        t_id = cart_obj.get('tshirt')
        size_short = cart_obj.get('size')
        if t_id == tshirt.id and size == size_short:
            flag = False
            cart_obj['quantity'] = cart_obj['quantity']+1
            break
    if flag:
        cart_obj = {
            'tshirt': tshirt.id,
            'size': size,
            'quantity': 1
        }
        cart.append(cart_obj)

    if user is not None:
        existing = Cart.objects.filter(user=user, sizeVariant=size_temp)

        if len(existing) > 0:
            obj = existing[0]
            obj.quantity = obj.quantity+1
            obj.save()

        else:
            c = Cart()
            c.user = user
            c.sizeVariant = size_temp
            c.quantity = 1
            c.save()

    request.session['cart'] = cart
    return_url = request.GET.get('return_url')

    return redirect(return_url)


def cal_total_price(cart):
    total = 0
    for c in cart:
        discount = c.get('tshirt').discount
        price = c.get('size').price
        sale_price = int(price - (price*(discount/100)))
        price_of_single_product = sale_price * c.get('quantity')
        total = total + price_of_single_product

    return total


@login_required(login_url='/login')
def checkout(request):
    if request.method == 'GET':
        form = CheckForm()
        cart = request.session.get('cart')
        if cart is None:
            cart = []
        for c in cart:
            size_str = c.get('size')
            tshirt_id = c.get('tshirt')
            size_obj = SizeVariant.objects.get(size=size_str, tshirt=tshirt_id)
            c['size'] = size_obj
            c['tshirt'] = size_obj.tshirt
        return render(request, 'store/checkout.html', {'form': form, 'cart': cart})
    else:
        form = CheckForm(request.POST)
        user = None
        if request.user.is_authenticated:
            user = request.user
        if form.is_valid():
            cart = request.session.get('cart')
            if cart is None:
                cart = []
            for c in cart:
                size_str = c.get('size')
                tshirt_id = c.get('tshirt')
                size_obj = SizeVariant.objects.get(
                    size=size_str, tshirt=tshirt_id)
                c['size'] = size_obj
                c['tshirt'] = size_obj.tshirt

            shipping_address = form.cleaned_data.get('shipping_address')
            phone = form.cleaned_data.get('phone')
            payment_method = form.cleaned_data.get('payment_method')
            total = cal_total_price(cart)
            order = Order()
            order.shipping_address = shipping_address
            order.phone = phone
            order.payment_method = payment_method
            order.total = total
            order.order_status = 'PENDING'
            order.user = user
            order.save()

            for c in cart:
                order_item = OrderItem()
                order_item.order = order
                order_item.price = int(
                    c.get('size').price-(c.get('size').price*(c.get('tshirt').discount/100)))
                order_item.quantity = c.get('quantity')
                order_item.size = c.get('size')
                order_item.tshirt = c.get('tshirt')
                order_item.save()

            response = api.payment_request_create(
                amount=order.total,
                purpose="Payment for E-shop shopping",
                send_email=True,
                buyer_name=f'{user.first_name} {user.last_name}',
                email=user.email,
                send_sms=True,
                phone=phone,
                redirect_url="http://localhost:8000/validate_payment"
            )

            payment = Payment()
            payment.order = order
            payment.payment_request_id = response['payment_request']['id']
            payment.save()

            return redirect(response['payment_request']['longurl'])
        else:
            return redirect('/checkout')


def validatePayment(request):
    user = None
    if request.user.is_authenticated:
        user = request.user

    payment_request_id = request.GET.get("payment_request_id")
    payment_id = request.GET.get("payment_id")
    response = api.payment_request_payment_status(
        payment_request_id, payment_id)
    status = response.get('payment_request').get('payment').get('status')

    if status != "Failed":
        print("payment success")
        try:
            payment = Payment.objects.get(
                payment_request_id=payment_request_id)
            payment.payment_id = payment_id
            payment.payment_status = status
            payment.save()
            order = payment.order
            order.order_status = "PLACED"
            order.save()
            cart = []
            request.session['cart'] = cart
            Cart.objects.filter(user=user).delete()
            return redirect('order')

        except:
            return render(request, 'store/payment_failed.html')
    else:
        return render(request, 'store/payment_failed.html')
