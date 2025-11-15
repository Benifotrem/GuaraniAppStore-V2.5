<x-app-layout>
    <x-slot name="header">
        <h2 class="font-semibold text-xl text-gray-800 leading-tight">
            Panel de Administración
        </h2>
    </x-slot>

    <div class="py-12">
        <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
            <!-- Stats Overview -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-6 mb-8">
                <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg p-6">
                    <div class="text-gray-600 text-sm font-semibold">Usuarios Totales</div>
                    <div class="text-3xl font-bold text-emerald-600">{{ $stats['total_users'] }}</div>
                </div>

                <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg p-6">
                    <div class="text-gray-600 text-sm font-semibold">Usuarios Activos</div>
                    <div class="text-3xl font-bold text-green-600">{{ $stats['active_users'] }}</div>
                </div>

                <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg p-6">
                    <div class="text-gray-600 text-sm font-semibold">Suscripciones</div>
                    <div class="text-3xl font-bold text-blue-600">{{ $stats['total_subscriptions'] }}</div>
                </div>

                <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg p-6">
                    <div class="text-gray-600 text-sm font-semibold">Ingresos Totales</div>
                    <div class="text-3xl font-bold text-purple-600">
                        Gs. {{ number_format($stats['total_revenue'], 0, ',', '.') }}
                    </div>
                </div>

                <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg p-6">
                    <div class="text-gray-600 text-sm font-semibold">Pagos Pendientes</div>
                    <div class="text-3xl font-bold text-orange-600">{{ $stats['pending_payments'] }}</div>
                </div>
            </div>

            <!-- Quick Links -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                <a href="{{ route('admin.users') }}" class="bg-emerald-500 hover:bg-emerald-600 text-white rounded-xl p-6 transition group">
                    <div class="flex items-center justify-between mb-3">
                        <span class="text-3xl">👥</span>
                        <span class="text-sm opacity-80">Gestionar</span>
                    </div>
                    <h3 class="font-bold text-lg">Usuarios</h3>
                </a>

                <a href="{{ route('admin.services') }}" class="bg-teal-500 hover:bg-teal-600 text-white rounded-xl p-6 transition group">
                    <div class="flex items-center justify-between mb-3">
                        <span class="text-3xl">🚀</span>
                        <span class="text-sm opacity-80">Gestionar</span>
                    </div>
                    <h3 class="font-bold text-lg">Servicios</h3>
                </a>

                <a href="{{ route('admin.payments') }}" class="bg-blue-500 hover:bg-blue-600 text-white rounded-xl p-6 transition group">
                    <div class="flex items-center justify-between mb-3">
                        <span class="text-3xl">💰</span>
                        <span class="text-sm opacity-80">Ver</span>
                    </div>
                    <h3 class="font-bold text-lg">Pagos</h3>
                </a>

                <a href="{{ route('admin.api-credentials') }}" class="bg-purple-500 hover:bg-purple-600 text-white rounded-xl p-6 transition group">
                    <div class="flex items-center justify-between mb-3">
                        <span class="text-3xl">🔑</span>
                        <span class="text-sm opacity-80">Configurar</span>
                    </div>
                    <h3 class="font-bold text-lg">APIs</h3>
                </a>
            </div>

            <!-- Recent Users -->
            <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg mb-6">
                <div class="p-6">
                    <h3 class="text-xl font-bold text-gray-900 mb-4">Usuarios Recientes</h3>
                    <div class="overflow-x-auto">
                        <table class="w-full">
                            <thead class="bg-gray-50">
                                <tr>
                                    <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600">Nombre</th>
                                    <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600">Email</th>
                                    <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600">Rol</th>
                                    <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600">Trial</th>
                                    <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600">Fecha</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-gray-200">
                                @foreach($recentUsers as $user)
                                <tr class="hover:bg-gray-50">
                                    <td class="px-4 py-3 text-sm font-medium">{{ $user->name }}</td>
                                    <td class="px-4 py-3 text-sm">{{ $user->email }}</td>
                                    <td class="px-4 py-3 text-sm">
                                        <span class="bg-{{ $user->role === 'admin' ? 'purple' : 'blue' }}-100 text-{{ $user->role === 'admin' ? 'purple' : 'blue' }}-800 px-2 py-1 rounded-full text-xs">
                                            {{ ucfirst($user->role) }}
                                        </span>
                                    </td>
                                    <td class="px-4 py-3 text-sm">
                                        @if($user->onTrial())
                                            <span class="text-green-600 font-semibold">{{ $user->trialDaysRemaining() }} días</span>
                                        @else
                                            <span class="text-gray-400">-</span>
                                        @endif
                                    </td>
                                    <td class="px-4 py-3 text-sm text-gray-600">{{ $user->created_at->format('d/m/Y') }}</td>
                                </tr>
                                @endforeach
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- Recent Payments -->
            <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
                <div class="p-6">
                    <h3 class="text-xl font-bold text-gray-900 mb-4">Pagos Recientes</h3>
                    <div class="overflow-x-auto">
                        <table class="w-full">
                            <thead class="bg-gray-50">
                                <tr>
                                    <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600">Usuario</th>
                                    <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600">Servicio</th>
                                    <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600">Gateway</th>
                                    <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600">Monto</th>
                                    <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600">Estado</th>
                                    <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600">Fecha</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-gray-200">
                                @foreach($recentPayments as $payment)
                                <tr class="hover:bg-gray-50">
                                    <td class="px-4 py-3 text-sm">{{ $payment->user->name }}</td>
                                    <td class="px-4 py-3 text-sm">{{ $payment->service->name }}</td>
                                    <td class="px-4 py-3 text-sm">
                                        <span class="capitalize">{{ $payment->gateway }}</span>
                                    </td>
                                    <td class="px-4 py-3 text-sm font-semibold">
                                        @if($payment->currency === 'PYG')
                                            Gs. {{ number_format($payment->amount, 0, ',', '.') }}
                                        @else
                                            {{ $payment->currency }} {{ number_format($payment->amount, 2) }}
                                        @endif
                                    </td>
                                    <td class="px-4 py-3 text-sm">
                                        @if($payment->status === 'completed')
                                            <span class="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs">Completado</span>
                                        @elseif($payment->status === 'pending')
                                            <span class="bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full text-xs">Pendiente</span>
                                        @else
                                            <span class="bg-red-100 text-red-800 px-2 py-1 rounded-full text-xs">Fallido</span>
                                        @endif
                                    </td>
                                    <td class="px-4 py-3 text-sm text-gray-600">{{ $payment->created_at->format('d/m/Y H:i') }}</td>
                                </tr>
                                @endforeach
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</x-app-layout>
