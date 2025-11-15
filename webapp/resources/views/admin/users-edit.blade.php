@extends('layouts.app')

@section('content')
<div class="py-12">
    <div class="max-w-4xl mx-auto sm:px-6 lg:px-8">
        <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
            <div class="p-6">
                <div class="flex justify-between items-center mb-6">
                    <h2 class="text-2xl font-bold">Editar Usuario #{{ $user->id }}</h2>
                    <a href="{{ route('admin.users') }}" class="px-4 py-2 bg-gray-500 hover:bg-gray-600 text-white rounded-lg">
                        ← Volver
                    </a>
                </div>

                <form action="{{ route('admin.users.update', $user->id) }}" method="POST" class="space-y-6">
                    @csrf
                    @method('PUT')

                    <!-- Información básica -->
                    <div class="bg-gray-50 p-6 rounded-lg">
                        <h3 class="text-lg font-semibold mb-4">Información Básica</h3>

                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Nombre</label>
                                <input type="text" name="name" value="{{ old('name', $user->name) }}"
                                       class="w-full px-4 py-2 border rounded-lg @error('name') border-red-500 @enderror">
                                @error('name')
                                    <p class="text-red-500 text-xs mt-1">{{ $message }}</p>
                                @enderror
                            </div>

                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Email</label>
                                <input type="email" name="email" value="{{ old('email', $user->email) }}"
                                       class="w-full px-4 py-2 border rounded-lg @error('email') border-red-500 @enderror">
                                @error('email')
                                    <p class="text-red-500 text-xs mt-1">{{ $message }}</p>
                                @enderror
                            </div>
                        </div>
                    </div>

                    <!-- Rol -->
                    <div class="bg-gray-50 p-6 rounded-lg">
                        <h3 class="text-lg font-semibold mb-4">Rol y Permisos</h3>

                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Rol</label>
                            <select name="role" class="w-full px-4 py-2 border rounded-lg @error('role') border-red-500 @enderror">
                                <option value="user" {{ $user->role === 'user' ? 'selected' : '' }}>Usuario</option>
                                <option value="admin" {{ $user->role === 'admin' ? 'selected' : '' }}>Administrador</option>
                            </select>
                            @error('role')
                                <p class="text-red-500 text-xs mt-1">{{ $message }}</p>
                            @enderror
                        </div>
                    </div>

                    <!-- Trial -->
                    <div class="bg-gray-50 p-6 rounded-lg">
                        <h3 class="text-lg font-semibold mb-4">Trial Period</h3>

                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Inicio de Trial</label>
                                <input type="date" name="trial_start" value="{{ $user->trial_start ? $user->trial_start->format('Y-m-d') : '' }}"
                                       class="w-full px-4 py-2 border rounded-lg">
                            </div>

                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Fin de Trial</label>
                                <input type="date" name="trial_end" value="{{ $user->trial_end ? $user->trial_end->format('Y-m-d') : '' }}"
                                       class="w-full px-4 py-2 border rounded-lg">
                            </div>
                        </div>
                    </div>

                    <!-- Cambiar contraseña (opcional) -->
                    <div class="bg-gray-50 p-6 rounded-lg">
                        <h3 class="text-lg font-semibold mb-4">Cambiar Contraseña (Opcional)</h3>

                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-2">Nueva Contraseña</label>
                            <input type="password" name="password"
                                   class="w-full px-4 py-2 border rounded-lg @error('password') border-red-500 @enderror"
                                   placeholder="Dejar en blanco para no cambiar">
                            @error('password')
                                <p class="text-red-500 text-xs mt-1">{{ $message }}</p>
                            @enderror
                            <p class="text-gray-500 text-xs mt-1">Mínimo 8 caracteres</p>
                        </div>
                    </div>

                    <!-- Estadísticas -->
                    <div class="bg-blue-50 p-6 rounded-lg">
                        <h3 class="text-lg font-semibold mb-4">Estadísticas</h3>

                        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                            <div>
                                <p class="text-sm text-gray-600">Suscripciones Activas</p>
                                <p class="text-2xl font-bold text-blue-600">{{ $user->subscriptions()->where('status', 'active')->count() }}</p>
                            </div>
                            <div>
                                <p class="text-sm text-gray-600">Pagos Totales</p>
                                <p class="text-2xl font-bold text-green-600">{{ $user->payments()->count() }}</p>
                            </div>
                            <div>
                                <p class="text-sm text-gray-600">Registrado</p>
                                <p class="text-sm font-semibold">{{ $user->created_at->format('d/m/Y') }}</p>
                            </div>
                            <div>
                                <p class="text-sm text-gray-600">Última Actualización</p>
                                <p class="text-sm font-semibold">{{ $user->updated_at->format('d/m/Y') }}</p>
                            </div>
                        </div>
                    </div>

                    <!-- Botones -->
                    <div class="flex justify-between items-center pt-4">
                        <a href="{{ route('admin.users') }}" class="px-6 py-2 bg-gray-300 hover:bg-gray-400 text-gray-700 rounded-lg">
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
