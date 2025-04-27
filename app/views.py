from django.shortcuts import render
from django.db.models import Count
from .logic.maps  import Maps
from app.models import Cars
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import RegistroUsuarioForm
from django.contrib import messages

estados_validos = {
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
}

def inicio(request):
    return render(request, 'core/index.html')

def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            
            messages.success(request, '¡Registro exitoso! Ahora puedes iniciar sesión.')
            return redirect('login')
        else:
            messages.error(request, 'Hubo un error al registrarte. Revisa el formulario.')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'register.html', {'form': form})

@login_required(login_url='login')
def mapa_1(request):
    year = request.GET.get('year')
    make = request.GET.get('make')

    filtros = {}
    if year:
        filtros['year'] = year
    if make:
        filtros['make'] = make

    # Agrupación directa sin cargar registros individuales
    queryset = Cars.objects.filter(**filtros).values('state').annotate(ventas=Count('make')).order_by('-ventas')[:10000]
    mapa_html = Maps.generar_mapa_ventas(queryset)

    # Para popular los filtros (únicos disponibles en la BD)
    años = Cars.objects.values_list('year', flat=True).distinct().order_by('year')
    marcas = Cars.objects.values_list('make', flat=True).distinct().order_by('make')

    return render(request, 'dashboard/graph1.html', {
        'mapa_html': mapa_html,
        'años': años,
        'marcas': marcas
    })

@login_required(login_url='login')
def mapa_2(request):
    año_inicio = request.GET.get('año_inicio')
    año_fin = request.GET.get('año_fin')
    make = request.GET.get('make')

    ventas = Cars.objects.all()

    if año_inicio:
        ventas = ventas.filter(year__gte=año_inicio)
    if año_fin:
        ventas = ventas.filter(year__lte=año_fin)
    if make:
        ventas = ventas.filter(make=make)

    queryset = ventas.exclude(year=None).values('year').annotate(ventas=Count('make')).order_by('year')
    mapa_html = Maps.generar_grafico_ventas(queryset)

    años = Cars.objects.values_list('year', flat=True).distinct().order_by('year')
    marcas = Cars.objects.values_list('make', flat=True).distinct().order_by('make')

    return render(request, 'dashboard/graph2.html', {
        'mapa_html': mapa_html,
        'años': años,
        'marcas': marcas,
    })

@login_required(login_url='login')
def mapa_3(request):
    año_inicio = request.GET.get('año_inicio')
    año_fin = request.GET.get('año_fin')
    top_n = int(request.GET.get('top_n', 10))  # por defecto top 10

    filtros = {}
    if año_inicio:
        filtros['year__gte'] = año_inicio
    if año_fin:
        filtros['year__lte'] = año_fin

    # Agrupación directa sin pandas
    queryset = (
        Cars.objects
        .filter(**filtros)
        .exclude(make=None)
        .values('make')
        .annotate(ventas=Count('make'))
        .order_by('-ventas')[:top_n]
    )

    # Graficar usando la función personalizada
    grafico_html = Maps.generar_grafico_marcas(queryset, top_n)

    # Para los selects
    años = Cars.objects.values_list('year', flat=True).distinct().order_by('year')

    return render(request, 'dashboard/graph3.html', {
        'grafico_html': grafico_html,
        'años': años,
        'top_n': top_n
    })

@login_required(login_url='login')
def mapa_4(request):
    año_inicio = request.GET.get('año_inicio')
    año_fin = request.GET.get('año_fin')
    make = request.GET.get('make')

    filter_kwargs = {}
    if año_inicio:
        filter_kwargs['year__gte'] = año_inicio
    if año_fin:
        filter_kwargs['year__lte'] = año_fin
    if make:
        filter_kwargs['make'] = make

    queryset = Cars.objects.exclude(condition__isnull=True).exclude(sellingprice__isnull=True).filter(**filter_kwargs)
    registros = queryset.values('condition', 'sellingprice')

    mapa_html = Maps.generar_grafico_condicion_vs_precio(registros)

    años = Cars.objects.values_list('year', flat=True).distinct().order_by('year')
    marcas = Cars.objects.values_list('make', flat=True).distinct().order_by('make')

    return render(request, 'dashboard/graph4.html', {
        'mapa_html': mapa_html,
        'años': años,
        'marcas': marcas,
    })

@login_required(login_url='login')
def mapa_5(request):
    año_inicio = request.GET.get('año_inicio')
    año_fin = request.GET.get('año_fin')
    make = request.GET.get('make')

    filter_kwargs = {}
    if año_inicio:
        filter_kwargs['year__gte'] = año_inicio
    if año_fin:
        filter_kwargs['year__lte'] = año_fin
    if make:
        filter_kwargs['make'] = make

    queryset = Cars.objects.exclude(model__isnull=True).filter(**filter_kwargs)
    registros = queryset.values('model')

    mapa_html = Maps.generar_grafico_modelos(registros)

    años = Cars.objects.values_list('year', flat=True).distinct().order_by('year')
    marcas = Cars.objects.values_list('make', flat=True).distinct().order_by('make')

    return render(request, 'dashboard/graph5.html', {
        'mapa_html': mapa_html,
        'años': años,
        'marcas': marcas,
    })

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'dashboard/inicio.html', {
    })
