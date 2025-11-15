@extends('layouts.app')

@section('content')
<div class="py-12">
    <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
        <div class="bg-white dark:bg-gray-800 overflow-hidden shadow-sm sm:rounded-lg">
            <div class="p-6">
                <h1 class="text-3xl font-bold mb-4">{{ $service->icon }} {{ $service->name }}</h1>
                <p class="text-gray-600 dark:text-gray-400 mb-8">{{ $service->description }}</p>

                <!-- Process Timeline -->
                <div class="mb-12">
                    <h2 class="text-2xl font-bold mb-6">Proceso de Consultoría</h2>
                    <div class="space-y-4">
                        <div class="flex items-start space-x-4">
                            <div class="flex-shrink-0 w-12 h-12 bg-emerald-100 dark:bg-emerald-900 rounded-full flex items-center justify-center">
                                <span class="text-emerald-600 dark:text-emerald-400 font-bold">1</span>
                            </div>
                            <div>
                                <h3 class="font-bold">Análisis Inicial</h3>
                                <p class="text-sm text-gray-600 dark:text-gray-400">Completar formulario con información de tu empresa</p>
                            </div>
                        </div>
                        <div class="flex items-start space-x-4">
                            <div class="flex-shrink-0 w-12 h-12 bg-emerald-100 dark:bg-emerald-900 rounded-full flex items-center justify-center">
                                <span class="text-emerald-600 dark:text-emerald-400 font-bold">2</span>
                            </div>
                            <div>
                                <h3 class="font-bold">Preparación</h3>
                                <p class="text-sm text-gray-600 dark:text-gray-400">Nuestro equipo analiza tus procesos (24-48 horas)</p>
                            </div>
                        </div>
                        <div class="flex items-start space-x-4">
                            <div class="flex-shrink-0 w-12 h-12 bg-emerald-100 dark:bg-emerald-900 rounded-full flex items-center justify-center">
                                <span class="text-emerald-600 dark:text-emerald-400 font-bold">3</span>
                            </div>
                            <div>
                                <h3 class="font-bold">Sesión de 60 minutos</h3>
                                <p class="text-sm text-gray-600 dark:text-gray-400">Reunión personalizada vía Zoom</p>
                            </div>
                        </div>
                        <div class="flex items-start space-x-4">
                            <div class="flex-shrink-0 w-12 h-12 bg-emerald-100 dark:bg-emerald-900 rounded-full flex items-center justify-center">
                                <span class="text-emerald-600 dark:text-emerald-400 font-bold">4</span>
                            </div>
                            <div>
                                <h3 class="font-bold">Documento Estratégico</h3>
                                <p class="text-sm text-gray-600 dark:text-gray-400">Roadmap completo de 20-30 páginas</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Company Info Form -->
                <div class="bg-gray-50 dark:bg-gray-900 rounded-lg p-6">
                    <h2 class="text-2xl font-bold mb-6">Solicitar Consultoría</h2>

                    <form id="companyInfoForm" class="space-y-4">
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <label class="block text-sm font-medium mb-2">Nombre de la Empresa *</label>
                                <input type="text" name="company_name" required class="w-full px-4 py-2 border rounded-lg">
                            </div>
                            <div>
                                <label class="block text-sm font-medium mb-2">Industria *</label>
                                <input type="text" name="industry" required class="w-full px-4 py-2 border rounded-lg">
                            </div>
                        </div>
                        <div>
                            <label class="block text-sm font-medium mb-2">Número de Empleados *</label>
                            <input type="number" name="employees" required min="1" class="w-full px-4 py-2 border rounded-lg">
                        </div>
                        <div>
                            <label class="block text-sm font-medium mb-2">Procesos Actuales *</label>
                            <textarea name="current_processes" required rows="4" class="w-full px-4 py-2 border rounded-lg"></textarea>
                        </div>
                        <div>
                            <label class="block text-sm font-medium mb-2">Problemas/Desafíos *</label>
                            <textarea name="pain_points" required rows="4" class="w-full px-4 py-2 border rounded-lg"></textarea>
                        </div>
                        <button type="submit" class="px-6 py-3 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg font-semibold">
                            Enviar Solicitud
                        </button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
    document.getElementById('companyInfoForm').addEventListener('submit', function(e) {
        e.preventDefault();
        alert('Solicitud recibida. Te contactaremos en 24-48 horas.');
    });
</script>
@endsection
