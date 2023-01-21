from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_auth
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import NewUserForm


def base(request):
    return render(request, 'base.html')

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    return render(request, 'home.html')


def register_user(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login_auth(request, user)
            return redirect('login')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = NewUserForm()
    return render(request, 'register.html', {'register_form': form})


def login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login_auth(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'The username and/or password you specified are not correct.')
        else:
                messages.error(request,"Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'login_form': form})


from django.core.mail import BadHeaderError, send_mail

""" django.core.mail.BadHeaderError (a subclass of ValueError) and, hence, will not send the email. Its your responsibility to validate all data before passing it to the email functions """
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.db.models.query_utils import Q
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode



def password_reset_request(request):  # sourcery skip: hoist-statement-from-loop
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			mail_address = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=mail_address))
			if associated_users.exists():
				for user in associated_users:
					subject = "Someones trying to reset your password"
					email_template_name = "password_reset/reset_email.txt"
					email_component = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, email_component)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					string = f"We sent an email to {mail_address} with a link to recover your account."
				messages.success(request, string)
			else:
				messages.warning(request, "No account associated with the email address")
	password_reset_form = PasswordResetForm()
	return render(request,"password_reset/password_reset.html",{"password_reset_form":password_reset_form})
