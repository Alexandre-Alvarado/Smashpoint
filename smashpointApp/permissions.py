from rest_framework.permissions import BasePermission, SAFE_METHODS

class WritePermissionByModelPerm(BasePermission):
    """Permite lectura pública y escritura solo si el usuario tiene permisos del modelo correspondiente."""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        model = getattr(view, 'queryset', None).model if getattr(view, 'queryset', None) else None
        if not model:
            return False
        opts = model._meta
        perms_needed = []
        if request.method == 'POST':
            perms_needed.append(f"{opts.app_label}.add_{opts.model_name}")
        elif request.method in ['PUT','PATCH']:
            perms_needed.append(f"{opts.app_label}.change_{opts.model_name}")
        elif request.method == 'DELETE':
            perms_needed.append(f"{opts.app_label}.delete_{opts.model_name}")
        return all(request.user.has_perm(p) for p in perms_needed)
