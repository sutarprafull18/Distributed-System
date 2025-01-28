from django.shortcuts import render
from django.http import JsonResponse
from users_app.models import User
from products_app.models import Product
from orders_app.models import Order
import threading


def dashboard(request):
    users = User.objects.using('users_db').all()
    products = Product.objects.using('products_db').all()
    orders = Order.objects.using('orders_db').all()

    return render(request, 'main_app/dashboard.html', {
        'users': users,
        'products': products,
        'orders': orders
    })


def run_all_insertions(request):
    from users_app.views import bulk_insert_users
    from products_app.views import bulk_insert_products
    from orders_app.views import bulk_insert_orders

    # Create threads for each bulk insertion
    threads = [
        threading.Thread(target=lambda: bulk_insert_users(request)),
        threading.Thread(target=lambda: bulk_insert_products(request)),
        threading.Thread(target=lambda: bulk_insert_orders(request))
    ]

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    return JsonResponse({
        'status': 'success',
        'message': 'All insertions completed'
    })

