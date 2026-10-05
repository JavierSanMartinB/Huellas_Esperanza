from functools import wraps
import bcrypt
from django.core import signing
from django.db import connection
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from adopcion.forms import AnimalForm
from .forms import UserForm
from .models import Refugio
from adopcion.models import Animal

# Create your views here.

USER_COOKIE_NAME = 'user_access'
USER_COOKIE_SALT = 'huellas.user_access'
USER_COOKIE_MAX_AGE = 60 * 60 * 8

def index(request):
    animales = list(
        Animal.objects.select_related('raza')
        .filter(fecha_salida__isnull=True)
        .order_by('id_animal')
    )
    especies = sorted({animal.especie for animal in animales})
    refugio = Refugio.objects.first()
    return render(request, 'index.html', {
        'animales': animales,
        'especies': especies,
        'refugio': refugio,
        'es_personal': usuario_es_personal(request),
        'usuario_autenticado': usuario_autenticado(request),
    })


def detalle_animal(request, animal_id):
    animal = get_object_or_404(
        Animal.objects.select_related('raza'),
        id_animal=animal_id,
        fecha_salida__isnull=True,
    )
    return render(request, 'animal_detalle.html', {'animal': animal})


def registrar(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('iniciar_sesion')
    else:
        form = UserForm()
    return render(request, 'registro.html', {'form': form})


def usuario_es_personal(request):
    usuario_id = usuario_id_desde_cookie(request)
    if usuario_id is None:
        return False

    return usuario_id_es_personal(usuario_id)


def usuario_id_es_personal(usuario_id):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT EXISTS (
                SELECT 1
                FROM public.personal AS personal
                WHERE personal.usuario_id = %s
                  AND personal.estado = 'activo'
                  AND personal.fecha_salida IS NULL
            )
            """,
            [usuario_id],
        )
        return cursor.fetchone()[0]


def usuario_id_desde_cookie(request):
    token = request.COOKIES.get(USER_COOKIE_NAME)
    if not token:
        return None

    try:
        payload = signing.loads(
            token,
            salt=USER_COOKIE_SALT,
            max_age=USER_COOKIE_MAX_AGE,
        )
    except signing.BadSignature:
        return None

    usuario_id = payload.get('usuario_id') if isinstance(payload, dict) else None
    return usuario_id if isinstance(usuario_id, int) and usuario_id > 0 else None


def usuario_autenticado(request):
    usuario_id = usuario_id_desde_cookie(request)
    if usuario_id is None:
        return False

    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT EXISTS (SELECT 1 FROM public.usuario WHERE usuario_id = %s)',
            [usuario_id],
        )
        return cursor.fetchone()[0]


def personal_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not usuario_es_personal(request):
            return redirect('iniciar_sesion')
        return view_func(request, *args, **kwargs)

    return wrapped_view


def iniciar_sesion(request):
    error = None
    if request.method == 'POST':
        correo = request.POST.get('correo', '').strip()
        contrasena = request.POST.get('contrasena', '')
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT usuario.usuario_id, usuario.contrasena_hash
                FROM public.usuario AS usuario
                WHERE LOWER(BTRIM(usuario.correo)) = LOWER(BTRIM(%s))
                LIMIT 1
                """,
                [correo],
            )
            cuenta = cursor.fetchone()

        contrasena_valida = False
        if cuenta and contrasena:
            try:
                contrasena_valida = bcrypt.checkpw(
                    contrasena.encode('utf-8'),
                    cuenta[1].encode('utf-8'),
                )
            except (AttributeError, ValueError):
                contrasena_valida = False

        if contrasena_valida:
            token = signing.dumps(
                {'usuario_id': cuenta[0]},
                salt=USER_COOKIE_SALT,
            )
            destino = 'nuevo_animal' if usuario_id_es_personal(cuenta[0]) else 'index'
            response = redirect(destino)
            response.set_cookie(
                USER_COOKIE_NAME,
                token,
                max_age=USER_COOKIE_MAX_AGE,
                httponly=True,
                secure=request.is_secure(),
                samesite='Lax',
            )
            return response

        error = 'El correo o la contraseña son incorrectos.'

    return render(request, 'login_personal.html', {'error': error})


@require_POST
def cerrar_sesion_personal(request):
    response = redirect('index')
    response.delete_cookie(USER_COOKIE_NAME, samesite='Lax')
    return response


@personal_required
def nuevo_animal(request):
    if request.method == 'POST':
        form = AnimalForm(request.POST)
        if form.is_valid():
            animal = form.save()
            return redirect('detalle_animal', animal_id=animal.id_animal)
    else:
        form = AnimalForm()
    return render(request, 'animal_nuevo.html', {'form': form})