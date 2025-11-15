@extends('layouts.app')

@section('content')
<div class="py-12">
    <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
        <!-- Trial Banner -->
        @if($onTrial)
        <div class="bg-yellow-100 border border-yellow-400 text-yellow-800 px-6 py-4 rounded-lg mb-6">
            <p class="font-semibold">🎁 Trial Activo - {{ $trialDaysLeft }} días restantes</p>
        </div>
        @endif

        <div class="bg-white dark:bg-gray-800 overflow-hidden shadow-sm sm:rounded-lg mb-8">
            <div class="p-6">
                <h1 class="text-3xl font-bold mb-4">{{ $service->icon }} {{ $service->name }}</h1>
                <p class="text-gray-600 dark:text-gray-400 mb-8">Tu asistente ejecutivo 24/7 vía Telegram</p>

                <!-- Connect Telegram -->
                <div class="bg-blue-50 dark:bg-blue-900 rounded-lg p-6 mb-8">
                    <h2 class="text-xl font-bold mb-4">Conectar Bot de Telegram</h2>
                    <button onclick="connectTelegram()" class="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold">
                        📱 Conectar Telegram
                    </button>
                    <div id="telegramInstructions" class="mt-4 hidden">
                        <p class="text-sm mb-2">Sigue estos pasos:</p>
                        <ol class="list-decimal list-inside text-sm space-y-1">
                            <li>Abre Telegram y busca <strong id="botUsername"></strong></li>
                            <li>Envía el comando: <code class="bg-white dark:bg-gray-800 px-2 py-1 rounded" id="startCommand"></code></li>
                            <li>El bot confirmará la conexión</li>
                        </ol>
                    </div>
                </div>

                <!-- Google Calendar Sync -->
                <div class="bg-green-50 dark:bg-green-900 rounded-lg p-6 mb-8">
                    <h2 class="text-xl font-bold mb-4">Sincronizar Google Calendar</h2>
                    <button onclick="alert('OAuth de Google Calendar - En desarrollo')" class="px-6 py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg font-semibold">
                        📅 Conectar Calendar
                    </button>
                </div>

                <!-- Stats -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div class="bg-gray-50 dark:bg-gray-900 p-6 rounded-lg">
                        <div class="text-3xl mb-2">✅</div>
                        <h3 class="text-2xl font-bold">45</h3>
                        <p class="text-sm text-gray-600 dark:text-gray-400">Tareas Completadas</p>
                    </div>
                    <div class="bg-gray-50 dark:bg-gray-900 p-6 rounded-lg">
                        <div class="text-3xl mb-2">📅</div>
                        <h3 class="text-2xl font-bold">12</h3>
                        <p class="text-sm text-gray-600 dark:text-gray-400">Eventos Agendados</p>
                    </div>
                    <div class="bg-gray-50 dark:bg-gray-900 p-6 rounded-lg">
                        <div class="text-3xl mb-2">💰</div>
                        <h3 class="text-2xl font-bold">34</h3>
                        <p class="text-sm text-gray-600 dark:text-gray-400">Registros Financieros</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- Features -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            @foreach($service->features as $feature)
            <div class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow">
                <p>✓ {{ $feature }}</p>
            </div>
            @endforeach
        </div>
    </div>
</div>

<script>
    function connectTelegram() {
        fetch('/api/asistente-personal/connect-telegram', { method: 'POST' })
            .then(r => r.json())
            .then(data => {
                document.getElementById('botUsername').textContent = data.bot_username;
                document.getElementById('startCommand').textContent = '/start ' + data.token;
                document.getElementById('telegramInstructions').classList.remove('hidden');
            });
    }
</script>
@endsection
