<x-app-layout>
    <x-slot name="header">
        <div class="flex items-center justify-between">
            <h2 class="font-semibold text-xl text-gray-800 leading-tight">
                Dashboard
            </h2>
            @if(Auth::user()->isAdmin())
            <a href="{{ route('admin.dashboard') }}" class="bg-purple-500 hover:bg-purple-600 text-white px-4 py-2 rounded-lg font-semibold transition text-sm">
                🔐 Panel Admin
            </a>
            @endif
        </div>
    </x-slot>

    <div class="py-12">
        <div class="max-w-7xl mx-auto sm:px-6 lg:px-8 space-y-6">
            <!-- Welcome & Trial Banner -->
            <div class="bg-gradient-to-r from-emerald-500 to-teal-600 rounded-xl p-6 text-white">
                <h3 class="text-2xl font-bold mb-2">¡Bienvenido, {{ $user->name }}! 👋</h3>
                @if($onTrial)
                <p class="text-white/90">
                    🎁 Tienes <strong>{{ $trialDaysLeft }} días</strong> restantes de tu trial gratuito
                </p>
                @else
                <p class="text-white/90">Gestiona tus suscripciones y servicios desde aquí</p>
                @endif
            </div>

            <!-- Active Subscriptions -->
            <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
                <div class="p-6">
                    <div class="flex items-center justify-between mb-6">
                        <h3 class="text-2xl font-bold text-gray-900">Mis Suscripciones Activas</h3>
                        <a href="{{ route('subscriptions.index') }}" class="text-emerald-600 hover:text-emerald-700 font-semibold text-sm">
                            Ver todas →
                        </a>
                    </div>

                    @if($subscriptions->count() > 0)
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        @foreach($subscriptions as $subscription)
                        <div class="border-2 border-emerald-200 rounded-xl p-4 hover:shadow-lg transition">
                            <div class="flex items-center justify-between mb-3">
                                <span class="text-4xl">{{ $subscription->service->icon }}</span>
                                <span class="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs font-semibold">
                                    Activa
                                </span>
                            </div>
                            <h4 class="font-bold text-gray-900 mb-2">{{ $subscription->service->name }}</h4>
                            <p class="text-sm text-gray-600 mb-3">
                                Desde {{ $subscription->starts_at->format('d/m/Y') }}
                            </p>
                            <a href="{{ route('services.show', $subscription->service->slug) }}"
                               class="block text-center bg-emerald-50 hover:bg-emerald-100 text-emerald-700 py-2 rounded-lg font-semibold transition text-sm">
                                Acceder
                            </a>
                        </div>
                        @endforeach
                    </div>
                    @else
                    <div class="text-center py-8">
                        <span class="text-6xl mb-4 block">📭</span>
                        <p class="text-gray-600 mb-4">No tienes suscripciones activas</p>
                        <a href="{{ route('home') }}#servicios"
                           class="inline-block bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white px-6 py-3 rounded-lg font-semibold transition">
                            Explorar Servicios
                        </a>
                    </div>
                    @endif
                </div>
            </div>

            <!-- Available Services -->
            <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
                <div class="p-6">
                    <h3 class="text-2xl font-bold text-gray-900 mb-6">Servicios Disponibles</h3>

                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                        @foreach($services as $service)
                        <a href="{{ route('services.show', $service->slug) }}"
                           class="border-2 border-gray-200 hover:border-emerald-400 rounded-xl p-4 transition group">
                            <div class="text-center">
                                <span class="text-5xl mb-3 block group-hover:scale-110 transition">{{ $service->icon }}</span>
                                <h4 class="font-bold text-gray-900 text-sm mb-2">{{ $service->name }}</h4>
                                <p class="text-emerald-600 font-semibold text-lg">
                                    Gs. {{ number_format($service->price, 0, ',', '.') }}
                                </p>
                                @if($service->trial_days > 0)
                                <p class="text-xs text-green-600 font-semibold mt-1">
                                    {{ $service->trial_days }} días gratis
                                </p>
                                @endif
                            </div>
                        </a>
                        @endforeach
                    </div>
                </div>
            </div>

            <!-- Recent Payments -->
            @if($recentPayments->count() > 0)
            <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
                <div class="p-6">
                    <div class="flex items-center justify-between mb-6">
                        <h3 class="text-2xl font-bold text-gray-900">Pagos Recientes</h3>
                        <a href="{{ route('payments.history') }}" class="text-emerald-600 hover:text-emerald-700 font-semibold text-sm">
                            Ver historial completo →
                        </a>
                    </div>

                    <div class="overflow-x-auto">
                        <table class="w-full">
                            <thead class="bg-gray-50">
                                <tr>
                                    <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600">Servicio</th>
                                    <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600">Fecha</th>
                                    <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600">Método</th>
                                    <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600">Monto</th>
                                    <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600">Estado</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-gray-200">
                                @foreach($recentPayments as $payment)
                                <tr class="hover:bg-gray-50">
                                    <td class="px-4 py-3 text-sm font-medium">
                                        <div class="flex items-center">
                                            <span class="text-2xl mr-2">{{ $payment->service->icon }}</span>
                                            <span>{{ $payment->service->name }}</span>
                                        </div>
                                    </td>
                                    <td class="px-4 py-3 text-sm text-gray-600">
                                        {{ $payment->created_at->format('d/m/Y') }}
                                    </td>
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
                                            <span class="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs font-semibold">✓ Completado</span>
                                        @elseif($payment->status === 'pending')
                                            <span class="bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full text-xs font-semibold">⏳ Pendiente</span>
                                        @else
                                            <span class="bg-red-100 text-red-800 px-2 py-1 rounded-full text-xs font-semibold">✗ Fallido</span>
                                        @endif
                                    </td>
                                </tr>
                                @endforeach
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            @endif

            <!-- Quick Actions -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <a href="{{ route('subscriptions.index') }}"
                   class="bg-blue-500 hover:bg-blue-600 text-white rounded-xl p-6 transition">
                    <div class="flex items-center justify-between mb-3">
                        <span class="text-3xl">📋</span>
                        <span class="text-sm opacity-80">Gestionar</span>
                    </div>
                    <h4 class="font-bold text-lg">Mis Suscripciones</h4>
                </a>

                <a href="{{ route('payments.history') }}"
                   class="bg-purple-500 hover:bg-purple-600 text-white rounded-xl p-6 transition">
                    <div class="flex items-center justify-between mb-3">
                        <span class="text-3xl">💰</span>
                        <span class="text-sm opacity-80">Ver</span>
                    </div>
                    <h4 class="font-bold text-lg">Historial de Pagos</h4>
                </a>

                <a href="{{ route('home') }}#servicios"
                   class="bg-emerald-500 hover:bg-emerald-600 text-white rounded-xl p-6 transition">
                    <div class="flex items-center justify-between mb-3">
                        <span class="text-3xl">🚀</span>
                        <span class="text-sm opacity-80">Explorar</span>
                    </div>
                    <h4 class="font-bold text-lg">Más Servicios</h4>
                </a>
            </div>
        </div>
    </div>
</x-app-layout>
