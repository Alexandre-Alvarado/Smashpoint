from django.shortcuts import redirect
from django.urls import resolve

PUBLIC_NAMES = {
    'login', 'logout', 'ranking_public', 'scoreboard_public', 'jugador_public', 'offline'
}

class JugadoresRestriccionMiddleware:
    """Restringe el acceso de usuarios del grupo 'Jugadores' a solo vistas públicas.
    Si intenta acceder a una vista no pública, se le redirige al ranking público.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                if request.user.groups.filter(name='Jugadores').exists():
                    match = resolve(request.path_info)
                    if match.url_name not in PUBLIC_NAMES and not request.path_info.startswith('/public/'):
                        return redirect('ranking_public')
            except Exception:
                # En caso de error de resolución, continuar normalmente
                pass
        response = self.get_response(request)
        return response
