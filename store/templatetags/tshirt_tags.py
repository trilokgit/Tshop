from django import template
register = template.Library()

@register.filter
def rupee(number):
    return f'₹{number}'


@register.filter
def cal_total_price(cart):
    total = 0
    for c in cart:
        discount = c.get('tshirt').discount
        price = c.get('size').price
        sale_price = clc_sale_price(price, discount)
        price_of_single_product = sale_price * c.get('quantity')
        total = total + price_of_single_product
    
    return total;

@register.filter
def pay_amount(oi):
    total = 0
    for c in oi:
       total = total + multiply(c.price,c.quantity)
    return total;
         



@register.simple_tag
def min_price(tshirt):
    size = tshirt.sizevariant_set.all().order_by('price').first()
    return size.price

@register.simple_tag
def sale_price(tshirt):
    price = min_price(tshirt)
    discount = tshirt.discount
    return int(price - (price*(discount/100)))


@register.simple_tag
def get_active_size_btn(active_size,size):
   if active_size==size:
       return "dark"
   return "light"


@register.simple_tag
def multiply(a,b):
   return a*b

@register.simple_tag
def clc_sale_price(price,discount):
   return int(price - (price*(discount/100)))

@register.simple_tag
def save(price,sale_price,qty):
   return (price-sale_price)*qty


@register.simple_tag
def total_save(cart):
    total = 0
    
    for c in cart:
        tshirt_price = c.get('size').price
        dis_price = clc_sale_price(tshirt_price,c.get('tshirt').discount)
        total = total + save(tshirt_price,dis_price,c.get('quantity'))
    return total
    
  





