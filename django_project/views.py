from django.http import HttpResponse
from django.db import connection
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

def my_custom_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check for SQL injection pattern
        if any(injection_pattern in username for injection_pattern in ["'", "--", ";", "OR", "AND"]):
            # Vulnerable SQL Query for SQL injection demonstration
            sql = f"SELECT * FROM auth_user WHERE username = '{username}'"
            
            with connection.cursor() as cursor:
                print(sql)  # For debugging purposes
                cursor.execute(sql)
                user_row = cursor.fetchone()

            if user_row:
                # Manually authenticate and log in the user
                user_id = user_row[0]
                user = User.objects.get(pk=user_id)
                login(request, user)  # Manually log in the user
                return redirect('home')  # Redirect to home after login
            else:
                return HttpResponse("Login failed due to SQL injection attempt.")
        else:
            # Handle normal login attempts using Django's authentication system
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return HttpResponse("Login failed. Incorrect username or password.")

    return render(request, 'registration/login.html')
