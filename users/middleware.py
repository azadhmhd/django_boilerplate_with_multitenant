import logging
from threading import local

from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_multitenant.utils import set_current_tenant, unset_current_tenant, unset_current_tenant_user, \
    set_current_tenant_user

from users.models import TenantUser

_thread_locals = local()
logger = logging.getLogger(__name__)


class MultiTenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.authenticator = JWTAuthentication()

    def __call__(self, request):
        response = self.get_response(request)
        unset_current_tenant()
        unset_current_tenant_user()
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.method == 'PUT':
            return JsonResponse({'error': 'Method not allowed'}, status=405)
        try:
            user, _ = self.authenticator.authenticate(request)
            tenant_id = view_kwargs.get('org', None)
            if tenant_id:
                try:
                    tenant_user = TenantUser.objects.select_related('account').get(account_id=tenant_id,
                                                                                   user_id=user.id)
                    set_current_tenant_user(tenant_user)
                    set_current_tenant(tenant_user.account)
                except Exception as ee:
                    logger.info("Error access", ee)
                    return JsonResponse({'error': 'Not Authorized'}, status=401)
        except Exception as e:
            logger.info("AccessUnsecured page")
