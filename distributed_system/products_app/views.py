from django.shortcuts import render
from django.http import JsonResponse
from .models import Product
from django.core.exceptions import ValidationError
from concurrent.futures import ThreadPoolExecutor


def insert_product(data):
    try:
        product = Product(
            name=data['name'],
            price=data['price']
        )
        product.full_clean()
        product.save(using='products_db')
        return {
            'status': 'success',
            'message': f"Product created: {data['name']}",
            'data': {'id': product.id, 'name': product.name, 'price': float(product.price)}
        }
    except ValidationError as e:
        return {
            'status': 'error',
            'message': f"Validation error: {str(e)}",
            'data': data
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f"Error: {str(e)}",
            'data': data
        }


def bulk_insert_products(request):
    products_data = [
        {'name': 'Laptop', 'price': 1000.00},
        {'name': 'Smartphone', 'price': 700.00},
        {'name': 'Headphones', 'price': 150.00},
        {'name': 'Monitor', 'price': 300.00},
        {'name': 'Keyboard', 'price': 50.00},
        {'name': 'Mouse', 'price': 30.00},
        {'name': 'Laptop', 'price': 1000.00},
        {'name': 'Smartwatch', 'price': 250.00},
        {'name': 'Gaming Chair', 'price': 500.00},
        {'name': 'Earbuds', 'price': -50.00},
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

