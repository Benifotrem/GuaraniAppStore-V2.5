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

        <!-- Calendar View -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-8">
            <h2 class="text-2xl font-bold mb-6">Calendario de Citas</h2>
            <div class="bg-gray-100 dark:bg-gray-700 rounded-lg p-8 text-center">
                <p class="text-gray-600 dark:text-gray-400">Vista de calendario - Integrar librería de calendario</p>
            </div>
        </div>

        <!-- Create Appointment -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-8">
            <h2 class="text-2xl font-bold mb-6">Crear Nueva Cita</h2>

            <form id="appointmentForm" class="space-y-4">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-medium mb-2">Título *</label>
                        <input type="text" name="title" required class="w-full px-4 py-2 border rounded-lg">
                    </div>
                    <div>
                        <label class="block text-sm font-medium mb-2">Fecha y Hora *</label>
                        <input type="datetime-local" name="date" required class="w-full px-4 py-2 border rounded-lg">
                    </div>
                    <div>
                        <label class="block text-sm font-medium mb-2">Duración (minutos) *</label>
                        <input type="number" name="duration" min="15" max="480" required class="w-full px-4 py-2 border rounded-lg">
                    </div>
                    <div>
                        <label class="block text-sm font-medium mb-2">Nombre del Cliente *</label>
                        <input type="text" name="client_name" required class="w-full px-4 py-2 border rounded-lg">
                    </div>
                    <div>
                        <label class="block text-sm font-medium mb-2">Email del Cliente</label>
                        <input type="email" name="client_email" class="w-full px-4 py-2 border rounded-lg">
                    </div>
                    <div>
                        <label class="block text-sm font-medium mb-2">Teléfono del Cliente</label>
                        <input type="tel" name="client_phone" class="w-full px-4 py-2 border rounded-lg">
                    </div>
                </div>
                <div>
                    <label class="block text-sm font-medium mb-2">Notas</label>
                    <textarea name="notes" rows="3" class="w-full px-4 py-2 border rounded-lg"></textarea>
                </div>
                <button type="submit" class="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold">
                    📅 Crear Cita
                </button>
            </form>
        </div>

        <!-- Connect Services -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                <h3 class="text-xl font-bold mb-4">Telegram Reminders</h3>
                <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">Recibe recordatorios automáticos vía Telegram</p>
                <button onclick="alert('Conectar Telegram bot')" class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg">
                    📱 Conectar
                </button>
            </div>
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                <h3 class="text-xl font-bold mb-4">Google Calendar Sync</h3>
                <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">Sincroniza con tu Google Calendar</p>
                <button onclick="alert('OAuth Google Calendar')" class="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg">
                    📅 Conectar
                </button>
            </div>
        </div>
    </div>
</div>

<script>
    document.getElementById('appointmentForm').addEventListener('submit', function(e) {
        e.preventDefault();
        alert('Cita creada - Implementar guardado en BD y sincronización');
    });
</script>
@endsection
