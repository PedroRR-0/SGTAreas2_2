from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.shortcuts import render, redirect
from .forms import LoginForm, RegistroForm, NuevaTareaForm, ModificarTareaForm
from .models import Usuario, Tarea
from django import forms
from django.core.exceptions import ValidationError
from datetime import date, datetime


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            password = form.cleaned_data['password']

            try:
                usuario = Usuario.objects.get(user=user)
                if usuario.check_password(password):
                    # Usuario autenticado
                    request.session['user_id'] = usuario.id
                    return redirect('tareas')
                else:
                    # Contraseña incorrecta
                    form.add_error('password', 'Contraseña incorrecta')
            except Usuario.DoesNotExist:
                # Usuario no encontrado
                form.add_error('user', 'Usuario no encontrado')

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def registro_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            try:
                user = form.cleaned_data['user']
                password = form.cleaned_data['password']
                confirm_password = form.cleaned_data['confirm_password']

                # Verificar si las contraseñas coinciden
                if password != confirm_password:
                    form.add_error('confirm_password', 'Las contraseñas no coinciden')
                else:
                    # Crear un nuevo usuario
                    usuario = Usuario(
                        user=user,
                        nombre=form.cleaned_data['nombre'],
                        apellidos=form.cleaned_data['apellidos'],
                        tlf=form.cleaned_data['tlf'],
                        mail=form.cleaned_data['mail']
                    )
                    usuario.set_password(password)
                    usuario.save()
                    request.session['user_id'] = usuario.id

                    # Redirigimos a la página de tareas
                    return redirect('tareas')
            except forms.ValidationError as e:
                # Capturar la excepción de validación y mostrar el mensaje de error en el formulario
                form.add_error('user', str(e))
    else:
        form = RegistroForm()

    return render(request, 'registro.html', {'form': form})


def tareas_view(request):
    usuario_actual = get_usuario_actual(request)
    estado = request.POST.get('estado')
    if request.method == 'POST':
        prioridad_filtrar = request.POST.get('prioridad')
        if prioridad_filtrar is None and estado is None:
            tarea_id = request.POST.get('tarea_id')
            tarea = Tarea.objects.get(pk=tarea_id)

            # Verificar si el usuario actual está asociado a la tarea
            if usuario_actual and usuario_actual in tarea.usuarios.all():
                tarea.cambiar_estado(usuario_actual)

    # Obtener la prioridad del formulario POST, si está presente
    prioridad_filtrar = request.POST.get('prioridad')
    if estado is not None:
        if estado == 'completadas':
            tareas = Tarea.objects.filter(estado=True).order_by('fecha_vencimiento')
        elif estado == 'pendientes':
            tareas = Tarea.objects.filter(estado=False).order_by('fecha_vencimiento')
        else:
            tareas = Tarea.objects.all().order_by('fecha_vencimiento')
    else:
        # Filtrar las tareas según la prioridad si se proporciona
        if prioridad_filtrar is not None:
            if prioridad_filtrar != "":
                tareas = Tarea.objects.filter(prioridad=prioridad_filtrar).order_by('fecha_vencimiento')
            else:
                tareas = Tarea.objects.all().order_by('fecha_vencimiento')
        else:
            # Si no hay solicitud POST o no se proporciona prioridad, mostrar todas las tareas
            tareas = Tarea.objects.all().order_by('fecha_vencimiento')

        # Obtener nombres de usuarios asociados a cada tarea
    usuarios_por_tarea = {tarea.id: ", ".join(tarea.usuarios.values_list('nombre', flat=True)) for tarea in tareas}
    # Obtener todos los usuarios
    return render(request, 'tareas.html', {'tareas': tareas, 'today': date.today(), 'usuario': usuario_actual,
                                           'usuarios_por_tarea': usuarios_por_tarea})


def get_usuario_actual(request):
    # Recupera el usuario actual
    usuario_id = request.session.get('user_id')
    if usuario_id:
        return Usuario.objects.get(pk=usuario_id)
    return None


def nueva_tarea_view(request):
    if request.method == 'POST':
        form = NuevaTareaForm(request.POST)
        if form.is_valid():
            # Guardar la nueva tarea sin commit para poder asociar usuarios
            nueva_tarea = form.save(commit=False)

            # Finalmente, guardar la tarea sin asociar usuarios
            nueva_tarea.save()

            # Asociar los usuarios seleccionados al formulario con la tarea
            usuarios_seleccionados = form.cleaned_data['usuarios']
            for usuario in usuarios_seleccionados:
                nueva_tarea.usuarios.add(usuario)

            # Guardar la tarea con los usuarios asociados
            nueva_tarea.save()

            return redirect('tareas')  # Redirigir a la página de tareas después de agregar la nueva tarea
    else:
        form = NuevaTareaForm()

    return render(request, 'nueva_tarea.html', {'form': form})


def modificar_tarea_view(request, tarea_id):
    tarea = get_object_or_404(Tarea, pk=tarea_id)

    if request.method == 'POST':
        form = ModificarTareaForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            return redirect('tareas')  # Redirigir a la página de tareas después de modificar la tarea
    else:
        fecha_str = tarea.fecha_vencimiento.strftime('%Y-%m-%d')
        tarea.fecha_vencimiento = fecha_str
        form = ModificarTareaForm(instance=tarea)

    return render(request, 'modificar_tarea.html', {'form': form, 'tarea': tarea})
