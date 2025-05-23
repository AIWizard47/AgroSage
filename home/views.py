from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Check, MarketItems, Cart
from .groq_ai import ask_ai

# Create your views here.
def index(request):
    is_farmer = False
    is_vendor = False

    if request.user.is_authenticated:
        check = Check.objects.filter(user=request.user).first()
        if check:
            is_farmer = check.is_farmer
            is_vendor = check.is_vendor

    context = {
        "is_farmer": is_farmer,
        "is_vendor": is_vendor,
    }
    return render(request, "home/index.html", context)

def login_view(request):
    
    user = request.user
    if user.is_authenticated:
            return redirect('index')
    
    if request.method == 'POST':
        username = request.POST.get('username')  # or email, if you customized auth
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')  # change to your desired redirect URL
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'register/login.html')

def register_view(request):
    user = request.user
    if user.is_authenticated:
            return redirect('index')
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        user_type = request.POST.get('user_type')

        
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already in use.")
            return redirect('register')

        user = User.objects.create_user(username=email, email=email, password=password,
                                        first_name=first_name, last_name=last_name)
        check = Check(user=user)
        if user_type == "farmer":
            check.is_farmer = True
        elif user_type == "vendor":
            check.is_vendor = True
        check.save()

        login(request, user)
        return redirect('index')

    return render(request, 'register/login.html')


def log_out(request):
    logout(request)  # Pass the request, not the user
    return redirect('index')  # Redirect to your homepage or login page

def market(request):
    user = request.user
    if user.is_authenticated:
        items = MarketItems.objects.all()
        context = {
            "market_items": items
        }
        return render(request, "marketplace/market.html", context)
    else:
        return redirect("login")  # replace "login" with your login URL name

def farmer_guidance(request):
    ai_response = None
    if request.method == 'POST':
        question = request.POST.get('question')
        if question:
            ai_response = ask_ai(question)

    return render(request, 'home/farmer_guidance.html', {
        'ai_response': ai_response
    })
    
@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(MarketItems, id=item_id)
    
    # Check if item is already in the cart
    if Cart.objects.filter(user=request.user, items=item).exists():
        # Optionally show a message or redirect with warning
        return redirect('view_cart')

    # Add item to cart
    Cart.objects.create(user=request.user, items=item)
    return redirect('view_cart')

@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    return render(request, 'marketplace/cart.html', {'cart_items': cart_items})

@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    return redirect('view_cart')