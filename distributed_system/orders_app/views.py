from django.shortcuts import render
from django.http import JsonResponse
from .models import Order
from concurrent.futures import ThreadPoolExecutor


def insert_order(data):
    try:
        order = Order(
            id=data['id'],
            user_id=data['user_id'],
            product_id=data['product_id'],
            quantity=data['quantity']
        )
        result = order.save(using='orders_db')

        if result is None:
            return {
                'status': 'skipped',
                'message': f"Order not created: Invalid quantity or invalid user/product ID",
                'data': data
            }

        return {
            'status': 'success',
            'message': f"Order created for user {data['user_id']}",
            'data': data
        }
    except Exception as e:
        return {
            'status': 'skipped',
            'message': str(e),
            'data': data
        }


def bulk_insert_orders(request):
    orders_data = [
        {'id': 1, 'user_id': 1, 'product_id': 1, 'quantity': 2},
        {'id': 2, 'user_id': 2, 'product_id': 2, 'quantity': 1},
        {'id': 3, 'user_id': 3, 'product_id': 3, 'quantity': 5},
        {'id': 4, 'user_id': 4, 'product_id': 4, 'quantity': 1},
        {'id': 5, 'user_id': 5, 'product_id': 5, 'quantity': 3},
        {'id': 6, 'user_id': 6, 'product_id': 6, 'quantity': 4},
        {'id': 7, 'user_id': 7, 'product_id': 7, 'quantity': 2},
        {'id': 8, 'user_id': 8, 'product_id': 8, 'quantity': 0},  # Should fail - zero quantity
        {'id': 9, 'user_id': 9, 'product_id': 1, 'quantity': -1},  # Should fail - negative quantity
        {'id': 10, 'user_id': 10, 'product_id': 11, 'quantity': 2}  # Should fail - invalid product_id
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