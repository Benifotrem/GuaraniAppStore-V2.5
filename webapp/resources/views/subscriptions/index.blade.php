<x-app-layout>
    <x-slot name="header">
        <h2 class="font-semibold text-xl text-gray-800 leading-tight">
            Mis Suscripciones
        </h2>
    </x-slot>

    <div class="py-12">
        <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
            <!-- Trial Status Banner -->
            @if($onTrial)
            <div class="mb-6 bg-gradient-to-r from-green-50 to-emerald-50 border-2 border-green-400 rounded-xl p-6">
                <div class="flex items-center justify-between">
                    <div class="flex items-center">
                        <span class="text-3xl mr-3">🎁</span>
                        <div>
                            <h3 class="text-emerald-900 font-bold text-xl">Trial Activo</h3>
                            <p class="text-gray-700 mt-1">
                                Te quedan <strong>{{ $trialDaysLeft }} días</strong> de prueba gratis
                            </p>
                        </div>
                    </div>
                    <a href="{{ route('home') }}#servicios"
                       class="bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white px-6 py-3 rounded-lg font-semibold transition">
                        Explorar Servicios
                    </a>
                </div>
            </div>
            @endif

            <!-- Success/Error Messages -->
            @if(session('success'))
            <div class="mb-6 bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded-lg">
                {{ session('success') }}
            </div>
            @endif

            @if(session('error'))
            <div class="mb-6 bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg">
                {{ session('error') }}
            </div>
            @endif

            <!-- Active Subscriptions -->
            <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
                <div class="p-6">
                    <h3 class="text-2xl font-bold text-gray-900 mb-6">Suscripciones Activas</h3>

                    @if($subscriptions->where('status', 'active')->count() > 0)
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        @foreach($subscriptions->where('status', 'active') as $subscription)
                        <div class="border-2 border-emerald-200 rounded-xl p-6 hover:shadow-lg transition">
                            <div class="text-center mb-4">
                                <span class="text-5xl">{{ $subscription->service->icon }}</span>
                                <h4 class="text-lg font-bold text-gray-900 mt-3">{{ $subscription->service->name }}</h4>
                            </div>

                            <div class="space-y-2 mb-4">
                                <div class="flex justify-between text-sm">
                                    <span class="text-gray-600">Estado:</span>
                                    <span class="text-green-600 font-semibold">✓ Activa</span>
                                </div>
                                <div class="flex justify-between text-sm">
                                    <span class="text-gray-600">Inicio:</span>
                                    <span class="font-semibold">{{ $subscription->starts_at->format('d/m/Y') }}</span>
                                </div>
                                @if($subscription->trial_ends_at && $subscription->trial_ends_at->isFuture())
                                <div class="flex justify-between text-sm">
                                    <span class="text-gray-600">Trial hasta:</span>
                                    <span class="text-emerald-600 font-semibold">{{ $subscription->trial_ends_at->format('d/m/Y') }}</span>
                                </div>
                                @else
                                <div class="flex justify-between text-sm">
                                    <span class="text-gray-600">Próximo pago:</span>
                                    <span class="font-semibold">{{ $subscription->next_billing_date->format('d/m/Y') }}</span>
                                </div>
                                @endif
                            </div>

                            <form method="POST" action="{{ route('subscriptions.cancel', $subscription->id) }}"
                                  onsubmit="return confirm('¿Estás seguro de que deseas cancelar esta suscripción?')">
                                @csrf
                                <button type="submit"
                                        class="w-full bg-red-500 hover:bg-red-600 text-white py-2 rounded-lg font-semibold transition">
                                    Cancelar Suscripción
                                </button>
                            </form>
                        </div>
                        @endforeach
                    </div>
                    @else
                    <div class="text-center py-12">
                        <span class="text-6xl">📭</span>
                        <p class="text-gray-600 mt-4 text-lg">No tienes suscripciones activas</p>
                        <a href="{{ route('home') }}#servicios"
                           class="inline-block mt-6 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white px-8 py-3 rounded-lg font-semibold transition">
                            Ver Servicios Disponibles
                        </a>
                    </div>
                    @endif
                </div>
            </div>

            <!-- Cancelled Subscriptions -->
            @if($subscriptions->where('status', 'cancelled')->count() > 0)
            <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg mt-6">
                <div class="p-6">
                    <h3 class="text-2xl font-bold text-gray-900 mb-6">Suscripciones Canceladas</h3>

                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        @foreach($subscriptions->where('status', 'cancelled') as $subscription)
                        <div class="border-2 border-gray-200 rounded-xl p-6 opacity-75">
                            <div class="text-center mb-4">
                                <span class="text-5xl">{{ $subscription->service->icon }}</span>
                                <h4 class="text-lg font-bold text-gray-900 mt-3">{{ $subscription->service->name }}</h4>
                            </div>

                            <div class="space-y-2 mb-4">
                                <div class="flex justify-between text-sm">
                                    <span class="text-gray-600">Estado:</span>
                                    <span class="text-red-600 font-semibold">✗ Cancelada</span>
                                </div>
                                <div class="flex justify-between text-sm">
                                    <span class="text-gray-600">Cancelada el:</span>
                                    <span class="font-semibold">{{ $subscription->ends_at->format('d/m/Y') }}</span>
                                </div>
                            </div>

                            <form method="POST" action="{{ route('subscriptions.resume', $subscription->id) }}">
                                @csrf
                                <button type="submit"
                                        class="w-full bg-emerald-500 hover:bg-emerald-600 text-white py-2 rounded-lg font-semibold transition">
                                    Reactivar Suscripción
                                </button>
                            </form>
                        </div>
                        @endforeach
                    </div>
                </div>
            </div>
            @endif
        </div>
    </div>
</x-app-layout>
