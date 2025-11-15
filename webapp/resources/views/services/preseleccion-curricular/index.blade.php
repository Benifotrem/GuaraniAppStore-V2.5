@extends('layouts.app')

@section('content')
<div class="py-12">
    <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
        <!-- Header -->
        <div class="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-8 mb-8 shadow-2xl">
            <h1 class="text-4xl font-bold text-gray-800 dark:text-white mb-2">{{ $service->icon }} {{ $service->name }}</h1>
            <p class="text-gray-600 dark:text-gray-300">{{ $service->description }}</p>
        </div>

        <!-- Upload CV Section -->
        <div class="bg-white dark:bg-gray-800 overflow-hidden shadow-sm sm:rounded-lg mb-8">
            <div class="p-6">
                <h2 class="text-2xl font-bold mb-6">Analizar CV con IA</h2>

                <form id="cvUploadForm" class="space-y-4">
                    <div>
                        <label class="block text-sm font-medium mb-2">Archivo CV (PDF, DOC, DOCX, JPG, PNG)</label>
                        <input type="file" name="cv_file" accept=".pdf,.doc,.docx,.jpg,.png" required
                               class="w-full px-4 py-2 border rounded-lg">
                    </div>
                    <div>
                        <label class="block text-sm font-medium mb-2">Requisitos del Puesto (opcional)</label>
                        <textarea name="job_requirements" rows="4"
                                  class="w-full px-4 py-2 border rounded-lg"
                                  placeholder="Ej: 3 años experiencia en Laravel, conocimientos de Vue.js, inglés avanzado..."></textarea>
                    </div>
                    <button type="submit" class="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold">
                        📄 Analizar CV
                    </button>
                </form>

                <div id="cvResults" class="mt-8 hidden">
                    <h3 class="text-xl font-bold mb-4">Resultado del Análisis</h3>
                    <div id="analysisData" class="space-y-4"></div>
                </div>
            </div>
        </div>

        <!-- Features -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
                <div class="text-3xl mb-2">🔍</div>
                <h3 class="font-bold mb-2">OCR Avanzado</h3>
                <p class="text-sm text-gray-600 dark:text-gray-400">Extracción precisa de texto de cualquier formato</p>
            </div>
            <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
                <div class="text-3xl mb-2">🎯</div>
                <h3 class="font-bold mb-2">Scoring 0-100</h3>
                <p class="text-sm text-gray-600 dark:text-gray-400">Evaluación inteligente con IA</p>
            </div>
            <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
                <div class="text-3xl mb-2">✅</div>
                <h3 class="font-bold mb-2">Validación</h3>
                <p class="text-sm text-gray-600 dark:text-gray-400">Verificación de email y teléfono</p>
            </div>
            <div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
                <div class="text-3xl mb-2">📊</div>
                <h3 class="font-bold mb-2">Export</h3>
                <p class="text-sm text-gray-600 dark:text-gray-400">Datos a Google Sheets</p>
            </div>
        </div>
    </div>
</div>

<script>
    document.getElementById('cvUploadForm').addEventListener('submit', function(e) {
        e.preventDefault();
        alert('Análisis de CV - Requiere integración con OCR y IA');
    });
</script>
@endsection
