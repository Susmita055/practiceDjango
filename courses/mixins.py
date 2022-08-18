from django.contrib.auth.mixins import AccessMixin
from courses.models import Course
from django.shortcuts import redirect


class IsCreatorMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if Course.objects.get(id=kwargs["pk"]).created_by == self.request.user:
            return super().dispatch(request, *args, **kwargs)
        return redirect("courses:course_list")
