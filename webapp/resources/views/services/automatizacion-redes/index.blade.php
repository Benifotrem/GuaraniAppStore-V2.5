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

        <!-- Connect Social Media -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-8">
            <h2 class="text-2xl font-bold mb-6">Conectar Redes Sociales</h2>

            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <button onclick="alert('Conectar LinkedIn')" class="p-4 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700">
                    <div class="text-3xl mb-2">💼</div>
                    <p class="font-semibold">LinkedIn</p>
                    <p class="text-xs text-green-600">Conectado</p>
                </button>
                <button onclick="alert('Conectar Twitter')" class="p-4 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700">
                    <div class="text-3xl mb-2">🐦</div>
                    <p class="font-semibold">Twitter</p>
                    <p class="text-xs text-gray-500">No conectado</p>
                </button>
                <button onclick="alert('Conectar Instagram')" class="p-4 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700">
                    <div class="text-3xl mb-2">📷</div>
                    <p class="font-semibold">Instagram</p>
                    <p class="text-xs text-gray-500">No conectado</p>
                </button>
                <button onclick="alert('Conectar Facebook')" class="p-4 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700">
                    <div class="text-3xl mb-2">📘</div>
                    <p class="font-semibold">Facebook</p>
                    <p class="text-xs text-gray-500">No conectado</p>
                </button>
            </div>
        </div>

        <!-- Generate Content -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-8">
            <h2 class="text-2xl font-bold mb-6">Generar Contenido Adaptado</h2>

            <form id="contentForm" class="space-y-4">
                <div>
                    <label class="block text-sm font-medium mb-2">URL Fuente o Texto</label>
                    <textarea name="source" rows="4" class="w-full px-4 py-2 border rounded-lg"></textarea>
                </div>
                <div>
                    <label class="block text-sm font-medium mb-2">Tono</label>
                    <select name="tone" class="w-full px-4 py-2 border rounded-lg">
                        <option value="professional">Profesional</option>
                        <option value="casual">Casual</option>
                        <option value="technical">Técnico</option>
                        <option value="friendly">Amigable</option>
                    </select>
                </div>
                <div>
                    <label class="block text-sm font-medium mb-2">Plataformas</label>
                    <div class="space-y-2">
                        <label class="flex items-center">
                            <input type="checkbox" name="platforms[]" value="linkedin" class="mr-2"> LinkedIn
                        </label>
                        <label class="flex items-center">
                            <input type="checkbox" name="platforms[]" value="twitter" class="mr-2"> Twitter
                        </label>
                        <label class="flex items-center">
                            <input type="checkbox" name="platforms[]" value="instagram" class="mr-2"> Instagram
                        </label>
                    </div>
                </div>
                <button type="submit" class="px-6 py-3 bg-purple-600 hover:bg-purple-700 text-white rounded-lg font-semibold">
                    ✨ Generar Contenido
                </button>
            </form>
        </div>

        <!-- Scheduled Posts -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h2 class="text-2xl font-bold mb-6">Posts Programados</h2>
            <div class="space-y-4">
                <p class="text-gray-500">No hay posts programados</p>
            </div>
        </div>
    </div>
</div>

<script>
    document.getElementById('contentForm').addEventListener('submit', function(e) {
        e.preventDefault();
        alert('Generación de contenido - Requiere integración con IA');
    });
</script>
@endsection
@endif
