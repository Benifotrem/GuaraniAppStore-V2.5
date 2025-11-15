@if($service->status === 'coming_soon')
    @include('services.coming-soon', ['service' => $service])
@else
@extends('layouts.app')

@section('content')
<div class="py-12">
    <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
        @if($onTrial)
        <div class="bg-yellow-100 border border-yellow-400 text-yellow-800 px-6 py-4 rounded-lg mb-6">
            <p class="font-semibold">🎁 Trial Activo - {{ $trialDaysLeft }} días restantes</p>
        </div>
        @endif

        <h1 class="text-3xl font-bold mb-8">{{ $service->icon }} {{ $service->name }}</h1>

        <!-- Configure Blog -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-8">
            <h2 class="text-2xl font-bold mb-6">Configurar Blog</h2>

            <form id="blogConfigForm" class="space-y-4">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-medium mb-2">URL del Blog *</label>
                        <input type="url" name="blog_url" required class="w-full px-4 py-2 border rounded-lg">
                    </div>
                    <div>
                        <label class="block text-sm font-medium mb-2">Plataforma *</label>
                        <select name="platform" class="w-full px-4 py-2 border rounded-lg">
                            <option value="wordpress">WordPress</option>
                            <option value="medium">Medium</option>
                            <option value="blogger">Blogger</option>
                            <option value="custom">Custom API</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-medium mb-2">Tono *</label>
                        <select name="tone" class="w-full px-4 py-2 border rounded-lg">
                            <option value="professional">Profesional</option>
                            <option value="casual">Casual</option>
                            <option value="technical">Técnico</option>
                            <option value="friendly">Amigable</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-medium mb-2">Hora de Publicación</label>
                        <input type="time" name="publish_time" value="09:00" class="w-full px-4 py-2 border rounded-lg">
                    </div>
                </div>
                <button type="submit" class="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold">
                    Guardar Configuración
                </button>
            </form>
        </div>

        <!-- Generate Article Manually -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-8">
            <h2 class="text-2xl font-bold mb-6">Generar Artículo Manualmente</h2>

            <form id="generateForm" class="space-y-4">
                <div>
                    <label class="block text-sm font-medium mb-2">Tema *</label>
                    <input type="text" name="topic" required class="w-full px-4 py-2 border rounded-lg">
                </div>
                <button type="submit" class="px-6 py-3 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg font-semibold">
                    ✨ Generar Artículo
                </button>
            </form>
        </div>

        <!-- Published Articles -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h2 class="text-2xl font-bold mb-6">Artículos Publicados</h2>
            <div class="space-y-4">
                <p class="text-gray-500">No hay artículos publicados aún</p>
            </div>
        </div>
    </div>
</div>

<script>
    document.getElementById('blogConfigForm').addEventListener('submit', function(e) {
        e.preventDefault();
        alert('Configuración guardada');
    });

    document.getElementById('generateForm').addEventListener('submit', function(e) {
        e.preventDefault();
        alert('Generación de artículo - Requiere integración con IA');
    });
</script>
@endsection
@endif
