@extends('layouts.app')

@section('content')
<div class="py-12">
    <div class="max-w-4xl mx-auto sm:px-6 lg:px-8">
        <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
            <div class="p-6">
                <div class="flex justify-between items-center mb-6">
                    <h2 class="text-2xl font-bold">Editar Servicio: {{ $service->name }}</h2>
                    <a href="{{ route('admin.services') }}" class="px-4 py-2 bg-gray-500 hover:bg-gray-600 text-white rounded-lg">
                        ← Volver
                    </a>
                </div>

                <form action="{{ route('admin.services.update', $service->id) }}" method="POST" class="space-y-6">
                    @csrf
                    @method('PUT')

                    <!-- Información básica -->
                    <div class="bg-gray-50 p-6 rounded-lg">
                        <h3 class="text-lg font-semibold mb-4">Información Básica</h3>

                        <div class="space-y-4">
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Nombre del Servicio</label>
                                <input type="text" name="name" value="{{ old('name', $service->name) }}"
                                       class="w-full px-4 py-2 border rounded-lg @error('name') border-red-500 @enderror">
                                @error('name')
                                    <p class="text-red-500 text-xs mt-1">{{ $message }}</p>
                                @enderror
                            </div>

                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Slug</label>
                                <input type="text" name="slug" value="{{ old('slug', $service->slug) }}"
                                       class="w-full px-4 py-2 border rounded-lg bg-gray-100" readonly>
                                <p class="text-gray-500 text-xs mt-1">El slug no se puede modificar</p>
                            </div>

                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Descripción</label>
                                <textarea name="description" rows="3"
                                          class="w-full px-4 py-2 border rounded-lg @error('description') border-red-500 @enderror">{{ old('description', $service->description) }}</textarea>
                                @error('description')
                                    <p class="text-red-500 text-xs mt-1">{{ $message }}</p>
                                @enderror
                            </div>

                            <div class="grid grid-cols-2 gap-4">
                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-2">Icono (Emoji)</label>
                                    <input type="text" name="icon" value="{{ old('icon', $service->icon) }}"
                                           class="w-full px-4 py-2 border rounded-lg">
                                </div>

                                <div>
                                    <label class="block text-sm font-medium text-gray-700 mb-2">Orden</label>
                                    <input type="number" name="sort_order" value="{{ old('sort_order', $service->sort_order) }}"
                                           class="w-full px-4 py-2 border rounded-lg">
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Pricing -->
                    <div class="bg-gray-50 p-6 rounded-lg">
                        <h3 class="text-lg font-semibold mb-4">Precio y Tipo</h3>

                        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Tipo</label>
                                <select name="type" class="w-full px-4 py-2 border rounded-lg @error('type') border-red-500 @enderror">
                                    <option value="subscription" {{ $service->type === 'subscription' ? 'selected' : '' }}>Suscripción</option>
                                    <option value="one_time" {{ $service->type === 'one_time' ? 'selected' : '' }}>Pago Único</option>
                                </select>
                                @error('type')
                                    <p class="text-red-500 text-xs mt-1">{{ $message }}</p>
                                @enderror
                            </div>

                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Precio (Gs.)</label>
                                <input type="number" name="price" value="{{ old('price', $service->price) }}"
                                       class="w-full px-4 py-2 border rounded-lg @error('price') border-red-500 @enderror">
                                @error('price')
                                    <p class="text-red-500 text-xs mt-1">{{ $message }}</p>
                                @enderror
                            </div>

                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Trial (días)</label>
                                <input type="number" name="trial_days" value="{{ old('trial_days', $service->trial_days) }}"
                                       class="w-full px-4 py-2 border rounded-lg">
                                <p class="text-gray-500 text-xs mt-1">0 = sin trial</p>
                            </div>
                        </div>
                    </div>

                    <!-- Estado -->
                    <div class="bg-gray-50 p-6 rounded-lg">
                        <h3 class="text-lg font-semibold mb-4">Estado</h3>

                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Estado del Servicio</label>
                            <select name="status" class="w-full px-4 py-2 border rounded-lg @error('status') border-red-500 @enderror">
                                <option value="active" {{ $service->status === 'active' ? 'selected' : '' }}>Activo</option>
                                <option value="coming_soon" {{ $service->status === 'coming_soon' ? 'selected' : '' }}>Próximamente</option>
                                <option value="inactive" {{ $service->status === 'inactive' ? 'selected' : '' }}>Inactivo</option>
                            </select>
                            @error('status')
                                <p class="text-red-500 text-xs mt-1">{{ $message }}</p>
                            @enderror
                        </div>
                    </div>

                    <!-- Estadísticas -->
                    <div class="bg-blue-50 p-6 rounded-lg">
                        <h3 class="text-lg font-semibold mb-4">Estadísticas</h3>

                        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                            <div>
                                <p class="text-sm text-gray-600">Suscripciones Activas</p>
                                <p class="text-2xl font-bold text-blue-600">
                                    @if($service->type === 'subscription')
                                        {{ $service->subscriptions()->where('status', 'active')->count() }}
                                    @else
                                        N/A
                                    @endif
                                </p>
                            </div>
                            <div>
                                <p class="text-sm text-gray-600">Pagos Completados</p>
                                <p class="text-2xl font-bold text-green-600">{{ $service->payments()->where('status', 'completed')->count() }}</p>
                            </div>
                            <div>
                                <p class="text-sm text-gray-600">Ingresos Totales</p>
                                <p class="text-xl font-bold text-purple-600">
                                    ₲{{ number_format($service->payments()->where('status', 'completed')->sum('amount'), 0, ',', '.') }}
                                </p>
                            </div>
                            <div>
                                <p class="text-sm text-gray-600">Usuarios Únicos</p>
                                <p class="text-2xl font-bold text-orange-600">{{ $service->payments()->distinct('user_id')->count() }}</p>
                            </div>
                        </div>
                    </div>

                    <!-- Botones -->
                    <div class="flex justify-between items-center pt-4">
                        <a href="{{ route('admin.services') }}" class="px-6 py-2 bg-gray-300 hover:bg-gray-400 text-gray-700 rounded-lg">
                            Cancelar
                        </a>
                        <button type="submit" class="px-6 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg">
                            Guardar Cambios
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
@endsection
