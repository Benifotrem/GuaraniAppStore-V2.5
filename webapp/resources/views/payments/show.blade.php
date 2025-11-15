<x-app-layout>
    <x-slot name="header">
        <h2 class="font-semibold text-xl text-gray-800 leading-tight">
            Realizar Pago - {{ $service->name }}
        </h2>
    </x-slot>

    <div class="py-12">
        <div class="max-w-4xl mx-auto sm:px-6 lg:px-8">
            <!-- Service Info -->
            <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg mb-6">
                <div class="p-6">
                    <div class="flex items-center space-x-4">
                        <span class="text-6xl">{{ $service->icon }}</span>
                        <div class="flex-1">
                            <h3 class="text-2xl font-bold text-gray-900">{{ $service->name }}</h3>
                            <p class="text-gray-600 mt-2">{{ $service->description }}</p>
                            <div class="mt-4">
                                <span class="text-3xl font-bold text-emerald-600">
                                    Gs. {{ number_format($service->price, 0, ',', '.') }}
                                </span>
                                @if($service->type === 'subscription')
                                    <span class="text-gray-600 text-sm">/mes</span>
                                @endif
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Payment Methods -->
            <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
                <div class="p-6">
                    <h3 class="text-xl font-bold text-gray-900 mb-6">Selecciona tu método de pago</h3>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <!-- PayPal -->
                        <form method="POST" action="{{ route('payments.process', $service->slug) }}">
                            @csrf
                            <input type="hidden" name="gateway" value="paypal">
                            <input type="hidden" name="currency" value="USD">
                            <button type="submit" class="w-full border-2 border-blue-500 hover:bg-blue-50 rounded-xl p-6 transition text-left group">
                                <div class="flex items-center justify-between mb-3">
                                    <span class="text-3xl">💳</span>
                                    <span class="text-blue-600 font-bold text-lg">PayPal</span>
                                </div>
                                <p class="text-gray-600 text-sm mb-2">Pago seguro con PayPal</p>
                                <p class="text-gray-900 font-semibold">
                                    USD ${{ number_format($service->price / 7500, 2) }}
                                </p>
                            </button>
                        </form>

                        <!-- Pagopar -->
                        <form method="POST" action="{{ route('payments.process', $service->slug) }}">
                            @csrf
                            <input type="hidden" name="gateway" value="pagopar">
                            <input type="hidden" name="currency" value="PYG">
                            <button type="submit" class="w-full border-2 border-green-500 hover:bg-green-50 rounded-xl p-6 transition text-left group">
                                <div class="flex items-center justify-between mb-3">
                                    <span class="text-3xl">🏦</span>
                                    <span class="text-green-600 font-bold text-lg">Pagopar</span>
                                </div>
                                <p class="text-gray-600 text-sm mb-2">Tarjetas y transferencias (PY)</p>
                                <p class="text-gray-900 font-semibold">
                                    Gs. {{ number_format($service->price, 0, ',', '.') }}
                                </p>
                            </button>
                        </form>

                        <!-- Bancard -->
                        <form method="POST" action="{{ route('payments.process', $service->slug) }}">
                            @csrf
                            <input type="hidden" name="gateway" value="bancard">
                            <input type="hidden" name="currency" value="PYG">
                            <button type="submit" class="w-full border-2 border-red-500 hover:bg-red-50 rounded-xl p-6 transition text-left group">
                                <div class="flex items-center justify-between mb-3">
                                    <span class="text-3xl">💳</span>
                                    <span class="text-red-600 font-bold text-lg">Bancard</span>
                                </div>
                                <p class="text-gray-600 text-sm mb-2">VPOS Bancard (PY)</p>
                                <p class="text-gray-900 font-semibold">
                                    Gs. {{ number_format($service->price, 0, ',', '.') }}
                                </p>
                            </button>
                        </form>

                        <!-- Cryptocurrency -->
                        <div class="relative">
                            <div class="absolute -top-3 -right-3 bg-gradient-to-r from-yellow-400 to-orange-500 text-white px-3 py-1 rounded-full text-xs font-bold z-10">
                                -25% OFF
                            </div>
                            <button type="button" onclick="showCryptoOptions()" class="w-full border-2 border-orange-500 hover:bg-orange-50 rounded-xl p-6 transition text-left group">
                                <div class="flex items-center justify-between mb-3">
                                    <span class="text-3xl">₿</span>
                                    <span class="text-orange-600 font-bold text-lg">Cripto</span>
                                </div>
                                <p class="text-gray-600 text-sm mb-2">BTC, ETH, USDT (25% descuento)</p>
                                <p class="text-gray-900 font-semibold line-through text-gray-400 text-sm">
                                    Gs. {{ number_format($service->price, 0, ',', '.') }}
                                </p>
                                <p class="text-orange-600 font-bold text-lg">
                                    Gs. {{ number_format($cryptoPrice, 0, ',', '.') }}
                                </p>
                            </button>
                        </div>
                    </div>

                    <!-- Crypto Currency Selection Modal -->
                    <div id="cryptoModal" class="hidden fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                        <div class="bg-white rounded-2xl p-8 max-w-md w-full mx-4">
                            <h4 class="text-2xl font-bold text-gray-900 mb-4">Selecciona tu criptomoneda</h4>
                            <div class="space-y-3">
                                <form method="POST" action="{{ route('payments.process', $service->slug) }}">
                                    @csrf
                                    <input type="hidden" name="gateway" value="crypto">
                                    <input type="hidden" name="currency" value="BTC">
                                    <button type="submit" class="w-full bg-orange-100 hover:bg-orange-200 border-2 border-orange-500 rounded-lg p-4 text-left transition">
                                        <div class="flex items-center justify-between">
                                            <span class="font-bold text-gray-900">Bitcoin (BTC)</span>
                                            <span class="text-2xl">₿</span>
                                        </div>
                                    </button>
                                </form>

                                <form method="POST" action="{{ route('payments.process', $service->slug) }}">
                                    @csrf
                                    <input type="hidden" name="gateway" value="crypto">
                                    <input type="hidden" name="currency" value="ETH">
                                    <button type="submit" class="w-full bg-purple-100 hover:bg-purple-200 border-2 border-purple-500 rounded-lg p-4 text-left transition">
                                        <div class="flex items-center justify-between">
                                            <span class="font-bold text-gray-900">Ethereum (ETH)</span>
                                            <span class="text-2xl">Ξ</span>
                                        </div>
                                    </button>
                                </form>

                                <form method="POST" action="{{ route('payments.process', $service->slug) }}">
                                    @csrf
                                    <input type="hidden" name="gateway" value="crypto">
                                    <input type="hidden" name="currency" value="USDT">
                                    <button type="submit" class="w-full bg-green-100 hover:bg-green-200 border-2 border-green-500 rounded-lg p-4 text-left transition">
                                        <div class="flex items-center justify-between">
                                            <span class="font-bold text-gray-900">Tether (USDT)</span>
                                            <span class="text-2xl">₮</span>
                                        </div>
                                    </button>
                                </form>
                            </div>
                            <button onclick="hideCryptoOptions()" class="w-full mt-4 bg-gray-200 hover:bg-gray-300 text-gray-700 py-2 rounded-lg font-semibold transition">
                                Cancelar
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="mt-6 text-center">
                <a href="{{ route('subscriptions.index') }}" class="text-gray-600 hover:text-gray-900">
                    ← Volver a mis suscripciones
                </a>
            </div>
        </div>
    </div>

    <script>
        function showCryptoOptions() {
            document.getElementById('cryptoModal').classList.remove('hidden');
        }

        function hideCryptoOptions() {
            document.getElementById('cryptoModal').classList.add('hidden');
        }
    </script>
</x-app-layout>
