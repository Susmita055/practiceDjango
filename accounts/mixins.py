from django.contrib.auth.mixins import AccessMixin
from accounts.models import User
from django.shortcuts import redirect


class IsSelfMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if User.objects.get(id=kwargs["pk"]).first_name == request.user.first_name:
            return super().dispatch(request, *args, **kwargs)
        return redirect("courses:course_list")
