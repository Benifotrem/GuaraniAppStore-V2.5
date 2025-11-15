@extends('layouts.app')

@section('content')
<div class="py-12">
    <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
        <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
            <div class="p-6">
                <div class="flex justify-between items-center mb-6">
                    <h2 class="text-2xl font-bold">Configuración de Pasarelas de Pago</h2>
                    <a href="{{ route('admin.dashboard') }}" class="px-4 py-2 bg-gray-500 hover:bg-gray-600 text-white rounded-lg">
                        ← Volver al Dashboard
                    </a>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    @foreach($gateways as $gateway)
                    <div class="bg-gray-50 rounded-lg p-6 border-2 {{ $gateway->is_active ? 'border-green-500' : 'border-gray-300' }}">
                        <form action="{{ route('admin.gateways.update', $gateway->id) }}" method="POST">
                            @csrf
                            @method('PUT')

                            <div class="flex items-center justify-between mb-4">
                                <div class="flex items-center">
                                    @if($gateway->gateway_name === 'paypal')
                                        <div class="text-4xl mr-3">💳</div>
                                    @elseif($gateway->gateway_name === 'pagopar')
                                        <div class="text-4xl mr-3">🏦</div>
                                    @elseif($gateway->gateway_name === 'bancard')
                                        <div class="text-4xl mr-3">💰</div>
                                    @else
                                        <div class="text-4xl mr-3">🪙</div>
                                    @endif
                                    <div>
                                        <h3 class="text-xl font-bold">{{ ucfirst($gateway->gateway_name) }}</h3>
                                        <p class="text-sm text-gray-600">{{ $gateway->display_name }}</p>
                                    </div>
                                </div>

                                <label class="relative inline-flex items-center cursor-pointer">
                                    <input type="checkbox" name="is_active" value="1"
                                           {{ $gateway->is_active ? 'checked' : '' }}
                                           class="sr-only peer"
                                           onchange="this.form.submit()">
                                    <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-600"></div>
                                    <span class="ml-3 text-sm font-medium text-gray-900">
                                        {{ $gateway->is_active ? 'Activo' : 'Inactivo' }}
                                    </span>
                                </label>
                            </div>

                            <div class="space-y-3">
                                <!-- Comisión -->
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-1">Comisión (%)</label>
                                    <input type="number" step="0.01" name="commission_percentage"
                                           value="{{ $gateway->commission_percentage }}"
                                           class="w-full px-3 py-2 border rounded-lg">
                                </div>

                                <!-- Configuración específica por gateway -->
                                @if($gateway->gateway_name === 'paypal')
                                    <div class="bg-blue-50 p-3 rounded">
                                        <p class="text-xs text-gray-600 mb-2">Configuración PayPal (.env):</p>
                                        <code class="text-xs">PAYPAL_CLIENT_ID<br>PAYPAL_CLIENT_SECRET</code>
                                    </div>
                                @elseif($gateway->gateway_name === 'pagopar')
                                    <div class="bg-green-50 p-3 rounded">
                                        <p class="text-xs text-gray-600 mb-2">Configuración Pagopar (.env):</p>
                                        <code class="text-xs">PAGOPAR_PUBLIC_KEY<br>PAGOPAR_PRIVATE_KEY</code>
                                    </div>
                                @elseif($gateway->gateway_name === 'bancard')
                                    <div class="bg-purple-50 p-3 rounded">
                                        <p class="text-xs text-gray-600 mb-2">Configuración Bancard (.env):</p>
                                        <code class="text-xs">BANCARD_PUBLIC_KEY<br>BANCARD_PRIVATE_KEY</code>
                                    </div>
                                @else
                                    <div class="bg-orange-50 p-3 rounded">
                                        <p class="text-xs text-gray-600 mb-2">Direcciones Crypto (.env):</p>
                                        <code class="text-xs">CRYPTO_BTC_ADDRESS<br>CRYPTO_ETH_ADDRESS<br>CRYPTO_USDT_ADDRESS</code>
                                    </div>
                                @endif

                                <!-- Estadísticas -->
                                <div class="grid grid-cols-2 gap-2 pt-3 border-t">
                                    <div class="text-center">
                                        <p class="text-xs text-gray-600">Transacciones</p>
                                        <p class="text-lg font-bold text-blue-600">
                                            {{ $gateway->payments()->count() }}
                                        </p>
                                    </div>
                                    <div class="text-center">
                                        <p class="text-xs text-gray-600">Completadas</p>
                                        <p class="text-lg font-bold text-green-600">
                                            {{ $gateway->payments()->where('status', 'completed')->count() }}
                                        </p>
                                    </div>
                                </div>

                                <button type="submit" class="w-full mt-4 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg">
                                    Guardar Cambios
                                </button>
                            </div>
                        </form>
                    </div>
                    @endforeach
                </div>

                <!-- Información general -->
                <div class="mt-8 bg-yellow-50 border border-yellow-200 rounded-lg p-6">
                    <h3 class="text-lg font-semibold mb-3">⚠️ Importante</h3>
                    <ul class="list-disc list-inside space-y-2 text-sm text-gray-700">
                        <li>Las credenciales de las pasarelas se configuran en el archivo <code class="bg-white px-2 py-1 rounded">.env</code></li>
                        <li>Asegúrate de usar el modo "production" en todas las pasarelas para ambiente productivo</li>
                        <li>Las comisiones se calculan automáticamente en cada transacción</li>
                        <li>Desactivar una pasarela no afecta los pagos ya procesados</li>
                        <li>Para Crypto, verifica manualmente las transacciones en blockchain</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</div>
@endsection
