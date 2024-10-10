from django.http import JsonResponse
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from .utils import identify_role


class CreateRoleBasedRedirectMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        target_urls = [reverse('create_user'), reverse('team'), reverse('task'), reverse('add_task'),
                       reverse('add_team')]
        if request.path in target_urls:
            role = identify_role(request.headers.get('Authorization'))

            if role in [1]:
                return view_func(request, *view_args, **view_kwargs)
            return JsonResponse(data={"message": "Permission denied", "ok": False}, status=403)
        return None
