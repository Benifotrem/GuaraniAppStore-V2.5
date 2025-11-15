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

        <!-- Setup Catalog -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-8">
            <h2 class="text-2xl font-bold mb-6">Configurar Catálogo de Productos</h2>
            <p class="text-gray-600 dark:text-gray-400 mb-4">Añade hasta 200 productos para que el bot pueda venderlos.</p>

            <button onclick="alert('Modal para añadir productos')" class="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold">
                ➕ Añadir Productos
            </button>
        </div>

        <!-- Connect Telegram Bot -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-8">
            <h2 class="text-2xl font-bold mb-6">Conectar Bot de Ventas</h2>
            <button onclick="alert('Conectar con Telegram')" class="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold">
                📱 Conectar Telegram
            </button>
        </div>

        <!-- Sales Stats -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                <div class="text-3xl mb-2">💬</div>
                <h3 class="text-2xl font-bold">156</h3>
                <p class="text-sm text-gray-600 dark:text-gray-400">Conversaciones</p>
            </div>
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                <div class="text-3xl mb-2">✅</div>
                <h3 class="text-2xl font-bold">45</h3>
                <p class="text-sm text-gray-600 dark:text-gray-400">Leads Calificados</p>
            </div>
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                <div class="text-3xl mb-2">💰</div>
                <h3 class="text-2xl font-bold">12</h3>
                <p class="text-sm text-gray-600 dark:text-gray-400">Conversiones</p>
            </div>
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                <div class="text-3xl mb-2">📈</div>
                <h3 class="text-2xl font-bold">7.7%</h3>
                <p class="text-sm text-gray-600 dark:text-gray-400">Tasa Conversión</p>
            </div>
        </div>

        <!-- Recent Conversations -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h2 class="text-2xl font-bold mb-6">Conversaciones Recientes</h2>
            <div class="overflow-x-auto">
                <table class="min-w-full">
                    <thead>
                        <tr class="border-b">
                            <th class="text-left py-2">Cliente</th>
                            <th class="text-left py-2">Estado</th>
                            <th class="text-left py-2">Score</th>
                            <th class="text-left py-2">Último Mensaje</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td colspan="4" class="text-center py-4 text-gray-500">No hay conversaciones aún</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>
@endsection
@endif
