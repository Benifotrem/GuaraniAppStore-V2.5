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
        <p class="text-lg mb-8">3 bots especializados para trading de criptomonedas</p>

        <!-- Three Bots -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <!-- CryptoShield -->
            <div class="bg-gradient-to-br from-red-500 to-red-700 text-white rounded-lg shadow-xl p-6">
                <div class="text-4xl mb-4">🛡️</div>
                <h3 class="text-2xl font-bold mb-2">CryptoShield</h3>
                <p class="text-sm mb-4 opacity-90">Detección de fraudes y scams</p>
                <ul class="text-sm space-y-1 mb-4">
                    <li>✓ Análisis de contratos</li>
                    <li>✓ Detección de rugpulls</li>
                    <li>✓ Verificación de liquidez</li>
                    <li>✓ Alertas de seguridad</li>
                </ul>
                <button onclick="connectBot('cryptoshield')" class="w-full px-4 py-2 bg-white text-red-700 rounded-lg font-semibold hover:bg-gray-100">
                    Conectar Bot
                </button>
            </div>

            <!-- Pulse IA -->
            <div class="bg-gradient-to-br from-purple-500 to-purple-700 text-white rounded-lg shadow-xl p-6">
                <div class="text-4xl mb-4">📊</div>
                <h3 class="text-2xl font-bold mb-2">Pulse IA</h3>
                <p class="text-sm mb-4 opacity-90">Análisis de sentimiento</p>
                <ul class="text-sm space-y-1 mb-4">
                    <li>✓ Sentimiento en redes</li>
                    <li>✓ Trending topics</li>
                    <li>✓ Influencers tracking</li>
                    <li>✓ Fear & Greed Index</li>
                </ul>
                <button onclick="connectBot('pulseia')" class="w-full px-4 py-2 bg-white text-purple-700 rounded-lg font-semibold hover:bg-gray-100">
                    Conectar Bot
                </button>
            </div>

            <!-- Momentum Predictor -->
            <div class="bg-gradient-to-br from-green-500 to-green-700 text-white rounded-lg shadow-xl p-6">
                <div class="text-4xl mb-4">⚡</div>
                <h3 class="text-2xl font-bold mb-2">Momentum Predictor</h3>
                <p class="text-sm mb-4 opacity-90">Señales de trading</p>
                <ul class="text-sm space-y-1 mb-4">
                    <li>✓ Señales automáticas</li>
                    <li>✓ Análisis técnico IA</li>
                    <li>✓ Soportes y resistencias</li>
                    <li>✓ Alertas de volumen</li>
                </ul>
                <button onclick="connectBot('momentum')" class="w-full px-4 py-2 bg-white text-green-700 rounded-lg font-semibold hover:bg-gray-100">
                    Conectar Bot
                </button>
            </div>
        </div>

        <!-- Portfolio Analysis -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-8">
            <h2 class="text-2xl font-bold mb-6">Análisis de Portfolio</h2>

            <form id="portfolioForm" class="space-y-4">
                <div>
                    <label class="block text-sm font-medium mb-2">Dirección de Wallet (opcional)</label>
                    <input type="text" name="wallet_address" placeholder="0x..." class="w-full px-4 py-2 border rounded-lg">
                </div>
                <button type="submit" class="px-6 py-3 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg font-semibold">
                    Analizar Portfolio
                </button>
            </form>
        </div>

        <!-- Market Alerts -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h2 class="text-2xl font-bold mb-6">Alertas Recientes</h2>
            <div id="alertsContainer" class="space-y-3">
                <p class="text-gray-500">No hay alertas recientes</p>
            </div>
        </div>
    </div>
</div>

<script>
    function connectBot(botType) {
        alert(`Conectar bot ${botType} - Implementar integración con Telegram`);
    }

    document.getElementById('portfolioForm').addEventListener('submit', function(e) {
        e.preventDefault();
        alert('Análisis de portfolio - Implementar integración con blockchain APIs');
    });
</script>
@endsection
