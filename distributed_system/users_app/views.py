from django.shortcuts import render
from django.http import JsonResponse
from .models import User
from concurrent.futures import ThreadPoolExecutor


def insert_user(data):
    try:
        user = User(
            id=data['id'],
            name=data.get('name', ''),
            email=data['email']
        )
        result = user.save(using='users_db')

        if result is None:
            return {
                'status': 'skipped',
                'message': f"User not created: Invalid data or duplicate email",
                'data': data
            }

        return {
            'status': 'success',
            'message': f"User created: {data['email']}",
            'data': data
        }
    except Exception as e:
        return {
            'status': 'skipped',
            'message': str(e),
            'data': data
        }


def bulk_insert_users(request):
    users_data = [
        {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
        {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'},
        {'id': 3, 'name': 'Charlie', 'email': 'charlie@example.com'},
        {'id': 4, 'name': 'David', 'email': 'david@example.com'},
        {'id': 5, 'name': 'Eve', 'email': 'eve@example.com'},
        {'id': 6, 'name': 'Frank', 'email': 'frank@example.com'},
        {'id': 7, 'name': 'Grace', 'email': 'grace@example.com'},
        {'id': 8, 'name': 'Alice', 'email': 'alice@example.com'},  # Should fail - duplicate email
        {'id': 9, 'name': 'Henry', 'email': 'henry@example.com'},
        {'id': 10, 'email': 'jane@example.com'}  # Should fail - no name
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