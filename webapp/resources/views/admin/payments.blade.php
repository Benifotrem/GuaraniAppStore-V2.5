@extends('layouts.app')

@section('content')
<div class="py-12">
    <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
        <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
            <div class="p-6">
                <div class="flex justify-between items-center mb-6">
                    <h2 class="text-2xl font-bold">Historial de Pagos</h2>
                    <a href="{{ route('admin.dashboard') }}" class="px-4 py-2 bg-gray-500 hover:bg-gray-600 text-white rounded-lg">
                        ← Volver al Dashboard
                    </a>
                </div>

                <!-- Estadísticas -->
                <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
                    <div class="bg-green-50 p-4 rounded-lg">
                        <p class="text-sm text-gray-600">Pagos Completados</p>
                        <p class="text-2xl font-bold text-green-600">{{ $stats['completed'] }}</p>
                    </div>
                    <div class="bg-yellow-50 p-4 rounded-lg">
                        <p class="text-sm text-gray-600">Pendientes</p>
                        <p class="text-2xl font-bold text-yellow-600">{{ $stats['pending'] }}</p>
                    </div>
                    <div class="bg-red-50 p-4 rounded-lg">
                        <p class="text-sm text-gray-600">Fallidos</p>
                        <p class="text-2xl font-bold text-red-600">{{ $stats['failed'] }}</p>
                    </div>
                    <div class="bg-purple-50 p-4 rounded-lg">
                        <p class="text-sm text-gray-600">Total Ingresos</p>
                        <p class="text-xl font-bold text-purple-600">₲{{ number_format($stats['revenue'], 0, ',', '.') }}</p>
                    </div>
                </div>

                <!-- Filtros -->
                <div class="mb-6 flex gap-4">
                    <select class="px-4 py-2 border rounded-lg">
                        <option value="">Todos los estados</option>
                        <option value="completed">Completado</option>
                        <option value="pending">Pendiente</option>
                        <option value="failed">Fallido</option>
                    </select>
                    <select class="px-4 py-2 border rounded-lg">
                        <option value="">Todas las pasarelas</option>
                        <option value="paypal">PayPal</option>
                        <option value="pagopar">Pagopar</option>
                        <option value="bancard">Bancard</option>
                        <option value="crypto">Crypto</option>
                    </select>
                    <input type="date" class="px-4 py-2 border rounded-lg" placeholder="Desde">
                    <input type="date" class="px-4 py-2 border rounded-lg" placeholder="Hasta">
                </div>

                <!-- Tabla de pagos -->
                <div class="overflow-x-auto">
                    <table class="min-w-full bg-white">
                        <thead class="bg-gray-100">
                            <tr>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Usuario</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Servicio</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Monto</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Gateway</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fecha</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Detalles</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-200">
                            @forelse($payments as $payment)
                            <tr class="hover:bg-gray-50">
                                <td class="px-6 py-4 whitespace-nowrap text-sm font-mono text-gray-900">
                                    #{{ $payment->id }}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    <div class="text-sm font-medium text-gray-900">{{ $payment->user->name }}</div>
                                    <div class="text-sm text-gray-500">{{ $payment->user->email }}</div>
                                </td>
                                <td class="px-6 py-4">
                                    <div class="text-sm font-medium text-gray-900">{{ $payment->service->name }}</div>
                                    <div class="text-sm text-gray-500">{{ $payment->service->slug }}</div>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm font-semibold">
                                    ₲{{ number_format($payment->amount, 0, ',', '.') }}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    @if($payment->gateway === 'paypal')
                                        <span class="px-2 py-1 text-xs font-semibold rounded bg-blue-100 text-blue-800">PayPal</span>
                                    @elseif($payment->gateway === 'pagopar')
                                        <span class="px-2 py-1 text-xs font-semibold rounded bg-green-100 text-green-800">Pagopar</span>
                                    @elseif($payment->gateway === 'bancard')
                                        <span class="px-2 py-1 text-xs font-semibold rounded bg-purple-100 text-purple-800">Bancard</span>
                                    @else
                                        <span class="px-2 py-1 text-xs font-semibold rounded bg-orange-100 text-orange-800">Crypto</span>
                                    @endif
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    @if($payment->status === 'completed')
                                        <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                                            Completado
                                        </span>
                                    @elseif($payment->status === 'pending')
                                        <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800">
                                            Pendiente
                                        </span>
                                    @else
                                        <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800">
                                            Fallido
                                        </span>
                                    @endif
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    {{ $payment->created_at->format('d/m/Y H:i') }}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm">
                                    <button onclick="showDetails({{ $payment->id }})" class="text-indigo-600 hover:text-indigo-900">
                                        Ver detalles
                                    </button>
                                </td>
                            </tr>
                            @empty
                            <tr>
                                <td colspan="8" class="px-6 py-4 text-center text-gray-500">
                                    No hay pagos registrados
                                </td>
                            </tr>
                            @endforelse
                        </tbody>
                    </table>
                </div>

                <!-- Paginación -->
                <div class="mt-6">
                    {{ $payments->links() }}
                </div>
            </div>
        </div>
    </div>
</div>

<script>
function showDetails(paymentId) {
    // TODO: Implementar modal con detalles del pago
    console.log('Ver detalles del pago:', paymentId);
}
</script>
@endsection
