from django.http import JsonResponse
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from .utils import identify_role
from .views import Authentication, TeamAndTaskAPIView


class CreateRoleBasedRedirectMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        target_urls = [reverse('create_user')]
        if request.path in target_urls:
            role = identify_role(request.headers.get('Authorization'))

            if role in [1]:
                print(role)
                return Authentication.as_view({'post': 'create_user'})(request, *view_args, **view_kwargs)
            return JsonResponse(data={"message": "Permission denied", "ok": False}, status=403)
        return None


class CreateTeamBasedRedirectMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        target_urls = [reverse('team')]
        if request.path in target_urls:
            role = identify_role(request.headers.get('Authorization'))
            if role in [1]:
                return TeamAndTaskAPIView.as_view({'post': 'create'})(request, *view_args, **view_kwargs)
            return JsonResponse(data={"message": "Permission denied", "ok": False}, status=403)
        return None
