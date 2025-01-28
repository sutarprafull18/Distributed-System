from django.shortcuts import render
from django.http import JsonResponse
from .models import Product
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal


def insert_product(data):
    try:
        product = Product(
            id=data['id'],
            name=data['name'],
            price=Decimal(str(data['price']))
        )
        result = product.save(using='products_db')

        if result is None:
            return {
                'status': 'skipped',
                'message': f"Product not created: Negative price or duplicate name",
                'data': data
            }

        return {
            'status': 'success',
            'message': f"Product created: {data['name']}",
            'data': data
        }
    except Exception as e:
        return {
            'status': 'skipped',
            'message': str(e),
            'data': data
        }


def bulk_insert_products(request):
    products_data = [
        {'id': 1, 'name': 'Laptop', 'price': '1000.00'},
        {'id': 2, 'name': 'Smartphone', 'price': '700.00'},
        {'id': 3, 'name': 'Headphones', 'price': '150.00'},
        {'id': 4, 'name': 'Monitor', 'price': '300.00'},
        {'id': 5, 'name': 'Keyboard', 'price': '50.00'},
        {'id': 6, 'name': 'Mouse', 'price': '30.00'},
        {'id': 7, 'name': 'Laptop', 'price': '1000.00'},  # Should fail - duplicate name
        {'id': 8, 'name': 'Smartwatch', 'price': '250.00'},
        {'id': 9, 'name': 'Gaming Chair', 'price': '500.00'},
        {'id': 10, 'name': 'Earbuds', 'price': '-50.00'}  # Should fail - negative price
    ]

    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_product = {executor.submit(insert_product, product_data): product_data
                             for product_data in products_data}
        for future in future_to_product:
            results.append(future.result())

    return JsonResponse({'results': results})


def list_products(request):
    products = Product.objects.using('products_db').all()
    return render(request, 'products_app/products_list.html', {'products': products})