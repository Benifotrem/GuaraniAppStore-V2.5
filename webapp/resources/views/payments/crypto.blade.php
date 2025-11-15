<x-app-layout>
    <x-slot name="header">
        <h2 class="font-semibold text-xl text-gray-800 leading-tight">
            Pago con {{ $currency }}
        </h2>
    </x-slot>

    <div class="py-12">
        <div class="max-w-3xl mx-auto sm:px-6 lg:px-8">
            <!-- Success Banner -->
            <div class="bg-gradient-to-r from-orange-50 to-yellow-50 border-2 border-orange-400 rounded-xl p-6 mb-6">
                <div class="flex items-center justify-center mb-2">
                    <span class="text-3xl mr-3">🎉</span>
                    <h3 class="text-orange-900 font-bold text-xl">¡25% de Descuento Aplicado!</h3>
                </div>
                <p class="text-center text-gray-700">
                    Ahorraste <strong>Gs. {{ number_format($service->price * 0.25, 0, ',', '.') }}</strong> pagando con cripto
                </p>
            </div>

            <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
                <div class="p-8">
                    <div class="text-center mb-8">
                        <span class="text-6xl mb-4 block">
                            @if($currency === 'BTC') ₿
                            @elseif($currency === 'ETH') Ξ
                            @else ₮
                            @endif
                        </span>
                        <h3 class="text-2xl font-bold text-gray-900">{{ $service->name }}</h3>
                        <p class="text-gray-600 mt-2">Pago con {{ $currency }}</p>
                    </div>

                    <!-- Payment Instructions -->
                    <div class="bg-gray-50 rounded-xl p-6 mb-6">
                        <h4 class="font-bold text-gray-900 mb-4 text-lg">Instrucciones de pago</h4>
                        <ol class="list-decimal list-inside space-y-2 text-gray-700">
                            <li>Envía exactamente <strong class="text-orange-600">{{ number_format($cryptoAmount, 8) }} {{ $currency }}</strong> a la dirección de abajo</li>
                            <li>Espera la confirmación en la blockchain (1-6 confirmaciones)</li>
                            <li>Tu suscripción se activará automáticamente</li>
                        </ol>
                    </div>

                    <!-- Amount to Send -->
                    <div class="bg-gradient-to-r from-orange-500 to-yellow-500 text-white rounded-xl p-6 mb-6">
                        <p class="text-sm opacity-90 mb-2">Cantidad a enviar:</p>
                        <div class="flex items-center justify-between">
                            <p class="text-3xl font-bold">{{ number_format($cryptoAmount, 8) }} {{ $currency }}</p>
                            <button onclick="copyAmount()" class="bg-white/20 hover:bg-white/30 px-4 py-2 rounded-lg transition">
                                📋 Copiar
                            </button>
                        </div>
                        <p class="text-sm opacity-90 mt-2">
                            ≈ Gs. {{ number_format($service->price * 0.75, 0, ',', '.') }} (con 25% descuento)
                        </p>
                    </div>

                    <!-- Wallet Address -->
                    <div class="mb-6">
                        <label class="block text-sm font-semibold text-gray-700 mb-2">
                            Dirección de la Wallet
                            @if($currency === 'USDT')
                                <span class="text-xs text-gray-500">(ERC-20)</span>
                            @endif
                        </label>
                        <div class="flex items-center space-x-2">
                            <input type="text"
                                   id="walletAddress"
                                   value="{{ $walletAddress }}"
                                   readonly
                                   class="flex-1 bg-gray-100 border-2 border-gray-300 rounded-lg px-4 py-3 font-mono text-sm">
                            <button onclick="copyWallet()" class="bg-emerald-500 hover:bg-emerald-600 text-white px-6 py-3 rounded-lg font-semibold transition">
                                📋 Copiar
                            </button>
                        </div>
                    </div>

                    <!-- QR Code Placeholder -->
                    <div class="bg-gray-100 rounded-xl p-8 mb-6 text-center">
                        <div class="bg-white inline-block p-4 rounded-xl shadow-lg">
                            <div class="w-48 h-48 bg-gray-200 flex items-center justify-center">
                                <p class="text-gray-500 text-sm">Código QR<br>{{ $walletAddress }}</p>
                            </div>
                        </div>
                        <p class="text-gray-600 text-sm mt-4">Escanea con tu wallet móvil</p>
                    </div>

                    <!-- Transaction Hash Form -->
                    <form method="POST" action="{{ route('payments.crypto.verify', $payment->id) }}" class="mb-6">
                        @csrf
                        <label class="block text-sm font-semibold text-gray-700 mb-2">
                            Hash de Transacción (Opcional)
                        </label>
                        <div class="flex items-center space-x-2">
                            <input type="text"
                                   name="tx_hash"
                                   placeholder="0x..."
                                   class="flex-1 border-2 border-gray-300 rounded-lg px-4 py-3">
                            <button type="submit" class="bg-orange-500 hover:bg-orange-600 text-white px-6 py-3 rounded-lg font-semibold transition">
                                Verificar Pago
                            </button>
                        </div>
                        <p class="text-gray-600 text-xs mt-2">
                            Pega el hash de tu transacción para verificación manual inmediata
                        </p>
                    </form>

                    <!-- Important Notes -->
                    <div class="bg-yellow-50 border-2 border-yellow-400 rounded-xl p-4">
                        <h5 class="font-bold text-yellow-900 mb-2">⚠️ Importante</h5>
                        <ul class="list-disc list-inside text-yellow-900 text-sm space-y-1">
                            <li>Envía solo {{ $currency }} a esta dirección</li>
                            @if($currency === 'USDT')
                                <li>Asegúrate de usar la red ERC-20 (Ethereum)</li>
                            @endif
                            <li>El monto debe ser exacto</li>
                            <li>La activación puede tardar hasta 30 minutos</li>
                            <li>Guarda el hash de transacción como comprobante</li>
                        </ul>
                    </div>
                </div>
            </div>

            <div class="mt-6 text-center space-x-4">
                <a href="{{ route('subscriptions.index') }}" class="text-gray-600 hover:text-gray-900">
                    Ver Mis Suscripciones
                </a>
                <span class="text-gray-400">|</span>
                <a href="{{ route('payments.history') }}" class="text-gray-600 hover:text-gray-900">
                    Historial de Pagos
                </a>
            </div>
        </div>
    </div>

    <script>
        function copyWallet() {
            const walletInput = document.getElementById('walletAddress');
            walletInput.select();
            document.execCommand('copy');

            alert('✓ Dirección copiada al portapapeles');
        }

        function copyAmount() {
            const amount = "{{ $cryptoAmount }}";
            navigator.clipboard.writeText(amount);
            alert('✓ Cantidad copiada al portapapeles');
        }
    </script>
</x-app-layout>
