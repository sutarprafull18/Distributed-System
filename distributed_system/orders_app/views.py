from django.shortcuts import render
from django.http import JsonResponse
from .models import Order
from django.core.exceptions import ValidationError
from concurrent.futures import ThreadPoolExecutor


def insert_order(data):
    try:
        order = Order(
            user_id=data['user_id'],
            product_id=data['product_id'],
            quantity=data['quantity']
        )
        order.full_clean()
        order.save(using='orders_db')
        return {
            'status': 'success',
            'message': f"Order created for user {data['user_id']}",
            'data': {
                'id': order.id,
                'user_id': order.user_id,
                'product_id': order.product_id,
                'quantity': order.quantity
            }
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


def bulk_insert_orders(request):
    orders_data = [
        {'user_id': 1, 'product_id': 1, 'quantity': 2},
        {'user_id': 2, 'product_id': 2, 'quantity': 1},
        {'user_id': 3, 'product_id': 3, 'quantity': 5},
        {'user_id': 4, 'product_id': 4, 'quantity': 1},
        {'user_id': 5, 'product_id': 5, 'quantity': 3},
        {'user_id': 6, 'product_id': 6, 'quantity': 4},
        {'user_id': 7, 'product_id': 7, 'quantity': 2},
        {'user_id': 8, 'product_id': 8, 'quantity': 0},
        {'user_id': 9, 'product_id': 1, 'quantity': -1},
        {'user_id': 10, 'product_id': 11, 'quantity': 2},
    ]

    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_order = {executor.submit(insert_order, order_data): order_data
                           for order_data in orders_data}
        for future in future_to_order:
            results.append(future.result())

    return JsonResponse({'results': results})


def list_orders(request):
    orders = Order.objects.using('orders_db').all()
    return render(request, 'orders_app/orders_list.html', {'orders': orders})

