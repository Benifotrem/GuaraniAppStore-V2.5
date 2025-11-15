@extends('layouts.app')

@section('content')
<div class="py-12">
    <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
        <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
            <div class="p-6">
                <div class="flex justify-between items-center mb-6">
                    <h2 class="text-2xl font-bold">Gestión de Servicios</h2>
                    <a href="{{ route('admin.dashboard') }}" class="px-4 py-2 bg-gray-500 hover:bg-gray-600 text-white rounded-lg">
                        ← Volver al Dashboard
                    </a>
                </div>

                <!-- Filtros -->
                <div class="mb-6 flex gap-4">
                    <select class="px-4 py-2 border rounded-lg">
                        <option value="">Todos los tipos</option>
                        <option value="subscription">Suscripción</option>
                        <option value="one_time">Pago único</option>
                    </select>
                    <select class="px-4 py-2 border rounded-lg">
                        <option value="">Todos los estados</option>
                        <option value="active">Activo</option>
                        <option value="coming_soon">Próximamente</option>
                        <option value="inactive">Inactivo</option>
                    </select>
                </div>

                <!-- Tabla de servicios -->
                <div class="overflow-x-auto">
                    <table class="min-w-full bg-white">
                        <thead class="bg-gray-100">
                            <tr>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Servicio</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Tipo</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Precio</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Trial</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Suscriptores</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-200">
                            @forelse($services as $service)
                            <tr class="hover:bg-gray-50">
                                <td class="px-6 py-4">
                                    <div class="flex items-center">
                                        <div class="text-2xl mr-3">{{ $service->icon }}</div>
                                        <div>
                                            <div class="text-sm font-medium text-gray-900">{{ $service->name }}</div>
                                            <div class="text-sm text-gray-500">{{ $service->slug }}</div>
                                        </div>
                                    </div>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    @if($service->type === 'subscription')
                                        <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800">
                                            Suscripción
                                        </span>
                                    @else
                                        <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-purple-100 text-purple-800">
                                            Pago Único
                                        </span>
                                    @endif
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                    ₲{{ number_format($service->price, 0, ',', '.') }}
                                    @if($service->type === 'subscription')
                                        <span class="text-gray-500">/mes</span>
                                    @endif
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    {{ $service->trial_days > 0 ? $service->trial_days . ' días' : 'N/A' }}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    @if($service->status === 'active')
                                        <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                                            Activo
                                        </span>
                                    @elseif($service->status === 'coming_soon')
                                        <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800">
                                            Próximamente
                                        </span>
                                    @else
                                        <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-100 text-gray-800">
                                            Inactivo
                                        </span>
                                    @endif
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    @if($service->type === 'subscription')
                                        {{ $service->subscriptions()->where('status', 'active')->count() }}
                                    @else
                                        {{ $service->payments()->where('status', 'completed')->distinct('user_id')->count() }}
                                    @endif
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                    <a href="{{ route('admin.services.edit', $service->id) }}" class="text-indigo-600 hover:text-indigo-900">
                                        Editar
                                    </a>
                                </td>
                            </tr>
                            @empty
                            <tr>
                                <td colspan="7" class="px-6 py-4 text-center text-gray-500">
                                    No hay servicios registrados
                                </td>
                            </tr>
                            @endforelse
                        </tbody>
                    </table>
                </div>

                <!-- Paginación -->
                <div class="mt-6">
                    {{ $services->links() }}
                </div>
            </div>
        </div>
    </div>
</div>
@endsection
