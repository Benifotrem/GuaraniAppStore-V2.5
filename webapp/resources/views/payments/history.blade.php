<x-app-layout>
    <x-slot name="header">
        <h2 class="font-semibold text-xl text-gray-800 leading-tight">
            Historial de Pagos
        </h2>
    </x-slot>

    <div class="py-12">
        <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
            <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
                <div class="p-6">
                    <h3 class="text-2xl font-bold text-gray-900 mb-6">Todos tus pagos</h3>

                    @if($payments->count() > 0)
                    <div class="overflow-x-auto">
                        <table class="w-full">
                            <thead class="bg-gray-50">
                                <tr>
                                    <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Fecha</th>
                                    <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Servicio</th>
                                    <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Método</th>
                                    <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Monto</th>
                                    <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Estado</th>
                                    <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">ID Transacción</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-gray-200">
                                @foreach($payments as $payment)
                                <tr class="hover:bg-gray-50">
                                    <td class="px-4 py-4 text-sm text-gray-900">
                                        {{ $payment->created_at->format('d/m/Y H:i') }}
                                    </td>
                                    <td class="px-4 py-4">
                                        <div class="flex items-center">
                                            <span class="text-2xl mr-2">{{ $payment->service->icon }}</span>
                                            <span class="text-sm font-medium text-gray-900">{{ $payment->service->name }}</span>
                                        </div>
                                    </td>
                                    <td class="px-4 py-4 text-sm">
                                        @if($payment->gateway === 'paypal')
                                            <span class="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs font-semibold">PayPal</span>
                                        @elseif($payment->gateway === 'pagopar')
                                            <span class="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs font-semibold">Pagopar</span>
                                        @elseif($payment->gateway === 'bancard')
                                            <span class="bg-red-100 text-red-800 px-2 py-1 rounded-full text-xs font-semibold">Bancard</span>
                                        @else
                                            <span class="bg-orange-100 text-orange-800 px-2 py-1 rounded-full text-xs font-semibold">Crypto</span>
                                        @endif
                                    </td>
                                    <td class="px-4 py-4 text-sm font-semibold text-gray-900">
                                        @if($payment->currency === 'PYG')
                                            Gs. {{ number_format($payment->amount, 0, ',', '.') }}
                                        @elseif(in_array($payment->currency, ['BTC', 'ETH', 'USDT']))
                                            {{ number_format($payment->amount, 8) }} {{ $payment->currency }}
                                        @else
                                            {{ $payment->currency }} ${{ number_format($payment->amount, 2) }}
                                        @endif
                                    </td>
                                    <td class="px-4 py-4 text-sm">
                                        @if($payment->status === 'completed')
                                            <span class="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs font-semibold">✓ Completado</span>
                                        @elseif($payment->status === 'pending')
                                            <span class="bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full text-xs font-semibold">⏳ Pendiente</span>
                                        @else
                                            <span class="bg-red-100 text-red-800 px-2 py-1 rounded-full text-xs font-semibold">✗ Fallido</span>
                                        @endif
                                    </td>
                                    <td class="px-4 py-4 text-xs text-gray-500 font-mono">
                                        {{ Str::limit($payment->transaction_id, 20) }}
                                    </td>
                                </tr>
                                @endforeach
                            </tbody>
                        </table>
                    </div>
                    @else
                    <div class="text-center py-12">
                        <span class="text-6xl">📭</span>
                        <p class="text-gray-600 mt-4 text-lg">No tienes pagos registrados</p>
                        <a href="{{ route('home') }}#servicios"
                           class="inline-block mt-6 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white px-8 py-3 rounded-lg font-semibold transition">
                            Explorar Servicios
                        </a>
                    </div>
                    @endif
                </div>
            </div>

            <div class="mt-6 text-center">
                <a href="{{ route('subscriptions.index') }}" class="text-gray-600 hover:text-gray-900">
                    ← Volver a mis suscripciones
                </a>
            </div>
        </div>
    </div>
</x-app-layout>
