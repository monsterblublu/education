from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView
from .forms import UserCreateForm, UserChangeForm, LoginForm
from django.utils.text import slugify
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage,send_mail
from django.contrib.auth import get_user_model
User = get_user_model()
#local
from .tokens import account_activation_token


class RegisterView(CreateView):
    form_class = UserCreateForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self,form):
        self.user = form.save(commit=False)
        self.user.username = slugify(self.user.first_name + self.user.last_name,
        allow_unicode=True)
        self.user.is_active = False
        self.user.save()
        current_site = get_current_site(self.request)
        mail_subject = "Activate Your Account"
        messages = render_to_string("accounts/account_activate.html",{
            'user' : self.user,
            'domain' : current_site.domain,
            'uid' : urlsafe_base64_encode(force_bytes(self.user.pk)),
            'token' : account_activation_token.make_token(self.user),
        })
        to_email = form.cleaned_data.get('email')
        send_mail(mail_subject, messages, 'azrielsebastianpam@gmail.com', [to_email])
        return super(RegisterView, self).form_valid(form)

    


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name='accounts/login.html'

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse("Thank You for your email confirm")
    else:
        return HttpResponse("Activation Link Is invalid")



