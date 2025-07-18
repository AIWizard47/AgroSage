from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Check, MarketItems, Cart, Feedback, Category, FarmerHistory
from .forms import ContactForm
from .groq_ai import ask_ai
import requests
from .formatter import format_ai_response_to_html
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO
from .models import Cart
from django.views.decorators.http import require_POST
from .search_index import InvertedIndex
from .autocomplete import AutocompleteTrie
import qrcode
from io import BytesIO
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
            messages.success(request, "Login successful!")
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

        messages.success(request, "Registration complete! You can now log in.")
        user = User.objects.create_user(username=email, email=email, password=password,
                                        first_name=first_name, last_name=last_name)
        check = Check(user=user)
        if user_type == "farmer":
            check.is_farmer = True
        elif user_type == "vendor":
            check.is_vendor = True
        check.phone_number = phone
        check.save()

        login(request, user)
        return redirect('index')

    return render(request, 'register/login.html')


def log_out(request):
    logout(request)  # Pass the request, not the user
    return redirect('index')  # Redirect to your homepage or login page

@login_required
def market(request):
    user = request.user
    cart_items = Cart.objects.filter(user=request.user)
    total_count = cart_items.count()
    if user.is_authenticated:
        items = MarketItems.objects.all()
        context = {
            "market_items": items,
            "total_count" : total_count
        }
        return render(request, "marketplace/market.html", context)
    else:
        return redirect("login")  # replace "login" with your login URL name


def farmer_guidance(request):
    ai_response = None
    formatted_response = None

    if request.method == 'POST':
        question = request.POST.get('question')
        if question:
            ai_response = ask_ai(question)
            formatted_response = format_ai_response_to_html(ai_response)

    return render(request, 'home/farmer_guidance.html', {
        'ai_response': formatted_response or ai_response
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
    # if weight<=item.items_weight:
    #     item.min_weight = weight
    #     item.save()
    return redirect('market')

@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_count = cart_items.count()
    total_price = 0
    
    for price in cart_items:
        total_price += price.items.item_price  * price.items.items_weight*100
    context = {
        'cart_items': cart_items,
        'total_count' : total_count,
        'total_price' : total_price,
        
    }
    return render(request, 'marketplace/cart.html', context)

@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    return redirect('view_cart')

@login_required
def list_item(request):
    user = request.user
    try:
        check = Check.objects.get(user=user)
        if not check.is_farmer:
            messages.error(request, "Only farmers can list items.")
            return redirect("index")
    except Check.DoesNotExist:
        messages.error(request, "Access denied. Farmer status not verified.")
        return redirect("index")

    categories = Category.objects.all()

    if request.method == 'POST':
        name = request.POST.get('items_name')
        description = request.POST.get('items_description')
        category_id = request.POST.get('category')
        price = request.POST.get('item_price')
        weight = request.POST.get('items_weight')
        image = request.FILES.get('item_image')
        location = request.POST.get('location')

        if name and description and category_id and price and weight and image:
            try:
                category = Category.objects.get(id=category_id)
                MarketItems.objects.create(
                    farmer = user,
                    items_name=name,
                    items_description=description,
                    category=category,
                    item_price=price,
                    items_weight=weight,
                    item_image=image,
                    location = location
                )
                messages.success(request, "Item listed successfully!")
                return redirect('market')
            except Category.DoesNotExist:
                messages.error(request, "Invalid category selected.")
        else:
            messages.error(request, "All fields are required.")

    return render(request, "marketplace/list_items.html", {"categories": categories})

@login_required
def farmer_dashboard(request):
    user = request.user
    history = FarmerHistory.objects.filter(farmer=user)
    market_items = MarketItems.objects.filter(farmer=request.user)
    total_amount = 0
    for item in history:
        total_amount += item.item_price*100*item.items_weight
    print(market_items)
    print(history)
    context = {
        "name" : user.first_name,
        "history":history,
        "total_amount" : total_amount,
        "market_items" : market_items
    }
    return render(request,"home/farmer_dashboard.html",context)


TREFLE_API_TOKEN = 'OhBkdYoPLnwI-HstvgN1ZTnevZfho_C3morAMbbiLSc'

def plant_search(request):
    query = request.GET.get('q', '')
    plants = []

    if query:
        url = f'https://trefle.io/api/v1/plants?token=${TREFLE_API_TOKEN}'
        response = requests.get(url, params={
            'token': TREFLE_API_TOKEN,
            'q': query
        })
        if response.status_code == 200:
            data = response.json()
            plants = data.get('data', [])

    return render(request, 'home/plant_search.html', {
        'plants': plants,
        'query': query
    })
@login_required
def generate_invoice(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    context = {
        "user": user,
        "cart_items": cart_items,
        "total": sum(item.items.item_price*100 * item.items.items_weight for item in cart_items),
    }
    html = render_to_string("home/invoice_template.html", context)

    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type="application/pdf")
        response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
        return response
    return HttpResponse("Error generating PDF", status=500)

# from weasyprint import HTML

# def generate_invoice(request):
#     html_string = render_to_string("invoice_template.html", {...})
#     html = HTML(string=html_string)
#     pdf = html.write_pdf()

#     response = HttpResponse(pdf, content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
#     return response

@login_required
def payment_success(request):
    # Generate invoice
    response = generate_invoice(request)
    if request.user.is_authenticated:
        # Get all cart items for the user
        cart_items = Cart.objects.filter(user=request.user)
        
        for cart_item in cart_items:
            item = cart_item.items  # assuming Cart has a ForeignKey to item as `item`
            # Save to FarmerHistory
            FarmerHistory.objects.create(
                farmer=item.farmer,
                items_name=item.items_name,
                items_description=item.items_description,
                category=item.category,
                item_price=item.item_price,
                item_image=item.item_image,
                items_weight=item.items_weight,
                item_rating=item.item_rating,
                location=item.location,
                item_list_date=item.item_list_date  # Use original listing date
            )
            # Remove item from market (optional)
            item.delete()
        # Clear the cart
        cart_items.delete()
    return response


@require_POST
def feedback(request):
    email = request.POST.get("email")
    description = request.POST.get("message")

    if email and description:
        # Optionally save to the database
        Feedback.objects.create(email=email, description=description)
        
        # Optional: success message
        messages.success(request, "Thank you for your feedback!")
    else:
        messages.error(request, "Please fill in both fields.")

    return redirect('index')


def guidance(request):
    return render(request,"home/guidance.html")

# ideally, these live in a singleton service
inverted_index = InvertedIndex()
autocomplete_trie = AutocompleteTrie()

_loaded = False

def load_indices():
    global _loaded
    if _loaded:
        return
    for p in MarketItems.objects.all():
        inverted_index.add_product(p)
        autocomplete_trie.insert(p)
        print(p,inverted_index)
    _loaded = True

# call load_indices() once on startup (e.g. in AppConfig.ready)
@login_required
def search_products(request):
    q = request.GET.get('q', '').strip().lower()
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort_by = request.GET.get('sort', 'item_price')  # change 'item_price'
    load_indices()
    ids = set()
    if q:
        terms = q.split()
        ids = inverted_index.lookup(terms)
    else:
        ids = set(MarketItems.objects.values_list('id', flat=True))

    qs = MarketItems.objects.filter(id__in=ids)

    # filter with correct field name
    if min_price: qs = qs.filter(item_price__gte=min_price)
    if max_price: qs = qs.filter(item_price__lte=max_price)

    # sort with correct field name
    valid_sorts = ['item_price', '-item_price', 'item_rating', '-item_rating']
    if sort_by in valid_sorts:
        qs = qs.order_by(sort_by)

    return render(request, "home/search_results.html", {"products": qs})


# views.py
def page_not_found(request, exception=None):  # Include `exception` argument
    return render(request, 'home/page_not_found.html', status=404)

def about_us(request):
    form = ContactForm()
    success = False

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
            form = ContactForm()  # reset form

    return render(request, 'home/about_us.html', {'form': form, 'success': success})

# views.py
@login_required
def payment_qr(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Calculate total
    cart_items = Cart.objects.filter(user=request.user)
    total_amount = sum(item.items.item_price *100* item.items.items_weight for item in cart_items)

    return render(request, 'marketplace/payment_qr.html', {
        'total_amount': total_amount,
    })

@login_required
def product_card(request, product_id):
    # Get the main product
    product = get_object_or_404(MarketItems, id=product_id)
    related_products = MarketItems.objects.filter(category=product.category).exclude(id=product.id)
    check = Check.objects.filter(user=product.farmer).first()
    phone_number = check.phone_number
    total_price = product.item_price*100*product.items_weight
    print(product.item_image)
    context = {
        "product": product,
        "related_products": related_products,
        "phone_number" : phone_number,
        "total_price" : total_price,
    }
    return render(request, 'marketplace/product_card.html', context)


def restore(request):
    if request.user.is_authenticated:
        # Get all cart items for the user
        history = FarmerHistory.objects.all()
        
        for item in history:
            # Save to FarmerHistory
            MarketItems.objects.create(
                farmer=item.farmer,
                items_name=item.items_name,
                items_description=item.items_description,
                category=item.category,
                item_price=item.item_price,
                item_image=item.item_image,
                items_weight=item.items_weight,
                item_rating=item.item_rating,
                location=item.location
            )
            # MarketItems.save()
        