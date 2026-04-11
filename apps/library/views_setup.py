from django.http import HttpResponse
from django.contrib.auth.models import User

def setup_admin_quick(request):
    try:
        user, created = User.objects.get_or_create(username='Mouiezuddin')
        user.set_password('Mouiez1234!!')
        user.is_superuser = True
        user.is_staff = True
        user.save()
        
        status = "Created" if created else "Updated password for existing"
        
        html = f"""
        <h3>Superuser Account Ready! ({status})</h3>
        <p><strong>Username:</strong> Mouiezuddin<br>
        <strong>Password:</strong> Mouiez1234!!</p>
        <p>You can now log in to the admin panel using these credentials.</p>
        <br>
        <p><a href='/admin/' style='padding: 10px 20px; background: #007bff; color: white; text-decoration: none; border-radius: 5px;'>Go to Admin Login</a></p>
        <br>
        <p><em>Note: You can change this password inside the admin panel later!</em></p>
        """
        return HttpResponse(html)
    except Exception as e:
        return HttpResponse(f"Error: {e}")
