from django.shortcuts import render
from django.http import JsonResponse
from .models import User
from django.core.exceptions import ValidationError
from concurrent.futures import ThreadPoolExecutor


def insert_user(data):
    try:
        user = User(
            name=data['name'],
            email=data['email']
        )
        user.full_clean()
        user.save(using='users_db')
        return {
            'status': 'success',
            'message': f"User created: {data['name']}",
            'data': {'id': user.id, 'name': user.name, 'email': user.email}
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


def bulk_insert_users(request):
    users_data = [
        {'name': 'Alice', 'email': 'alice@example.com'},
        {'name': 'Bob', 'email': 'bob@example.com'},
        {'name': 'Charlie', 'email': 'charlie@example.com'},
        {'name': 'David', 'email': 'david@example.com'},
        {'name': 'Eve', 'email': 'eve@example.com'},
        {'name': 'Frank', 'email': 'frank@example.com'},
        {'name': 'Grace', 'email': 'grace@example.com'},
        {'name': 'Alice', 'email': 'alice2@example.com'},
        {'name': 'Henry', 'email': 'henry@example.com'},
        {'name': 'Jane', 'email': 'jane@example.com'},
    ]

    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_user = {executor.submit(insert_user, user_data): user_data
                          for user_data in users_data}
        for future in future_to_user:
            results.append(future.result())

    return JsonResponse({'results': results})


def list_users(request):
    users = User.objects.using('users_db').all()
    return render(request, 'users_app/users_list.html', {'users': users})

