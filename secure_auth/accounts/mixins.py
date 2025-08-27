from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from .models import Document


class OwnerRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        document = get_object_or_404(Document, pk=kwargs['pk'])
        if document.owner != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

class GroupRequiredMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        required_groups = kwargs.get('groups', [])
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not any(request.user.groups.filter(name=group).exists() for group in required_groups):
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)