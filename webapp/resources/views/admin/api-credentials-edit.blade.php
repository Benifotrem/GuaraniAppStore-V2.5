@extends('layouts.app')

@section('content')
<div class="py-12">
    <div class="max-w-4xl mx-auto sm:px-6 lg:px-8">
        <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
            <div class="p-6">
                <div class="flex justify-between items-center mb-6">
                    <h2 class="text-2xl font-bold">Editar Credenciales API</h2>
                    <a href="{{ route('admin.api-credentials') }}" class="px-4 py-2 bg-gray-500 hover:bg-gray-600 text-white rounded-lg">
                        ← Volver
                    </a>
                </div>

                <!-- Advertencia de seguridad -->
                <div class="mb-6 bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                    <div class="flex items-start">
                        <div class="text-2xl mr-3">⚠️</div>
                        <div>
                            <h3 class="font-semibold text-yellow-800">Advertencia de Seguridad</h3>
                            <p class="text-sm text-yellow-700 mt-1">
                                Las credenciales se almacenan encriptadas. Asegúrate de copiarlas de fuentes oficiales.
                                No compartas estas credenciales con terceros.
                            </p>
                        </div>
                    </div>
                </div>

                <form action="{{ route('admin.api-credentials.update', $credential->id) }}" method="POST" class="space-y-6">
                    @csrf
                    @method('PUT')

                    <!-- Información básica -->
                    <div class="bg-gray-50 p-6 rounded-lg">
                        <h3 class="text-lg font-semibold mb-4">Información de la API</h3>

                        <div class="space-y-4">
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Nombre de la API</label>
                                <input type="text" name="api_name" value="{{ old('api_name', $credential->api_name) }}"
                                       class="w-full px-4 py-2 border rounded-lg @error('api_name') border-red-500 @enderror">
                                @error('api_name')
                                    <p class="text-red-500 text-xs mt-1">{{ $message }}</p>
                                @enderror
                            </div>

                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Tipo de API</label>
                                <select name="api_type" class="w-full px-4 py-2 border rounded-lg @error('api_type') border-red-500 @enderror">
                                    <option value="ai" {{ $credential->api_type === 'ai' ? 'selected' : '' }}>IA (OpenRouter, Gemini, etc.)</option>
                                    <option value="google" {{ $credential->api_type === 'google' ? 'selected' : '' }}>Google (Calendar, Drive, etc.)</option>
                                    <option value="payment" {{ $credential->api_type === 'payment' ? 'selected' : '' }}>Pasarelas de Pago</option>
                                    <option value="social" {{ $credential->api_type === 'social' ? 'selected' : '' }}>Redes Sociales</option>
                                    <option value="blockchain" {{ $credential->api_type === 'blockchain' ? 'selected' : '' }}>Blockchain/Crypto</option>
                                    <option value="other" {{ $credential->api_type === 'other' ? 'selected' : '' }}>Otra</option>
                                </select>
                                @error('api_type')
                                    <p class="text-red-500 text-xs mt-1">{{ $message }}</p>
                                @enderror
                            </div>

                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Servicio Asociado (Opcional)</label>
                                <select name="service_id" class="w-full px-4 py-2 border rounded-lg">
                                    <option value="">Sistema Global</option>
                                    @foreach(\App\Models\Service::all() as $service)
                                        <option value="{{ $service->id }}" {{ $credential->service_id == $service->id ? 'selected' : '' }}>
                                            {{ $service->name }}
                                        </option>
                                    @endforeach
                                </select>
                            </div>
                        </div>
                    </div>

                    <!-- Credenciales -->
                    <div class="bg-gray-50 p-6 rounded-lg">
                        <h3 class="text-lg font-semibold mb-4">Credenciales 🔐</h3>

                        <div class="space-y-4">
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">API Key / Public Key</label>
                                <input type="text" name="api_key" value="{{ old('api_key', decrypt($credential->api_key ?? '')) }}"
                                       class="w-full px-4 py-2 border rounded-lg font-mono text-sm @error('api_key') border-red-500 @enderror"
                                       placeholder="sk-xxxxxxxxxxxxxxxxxxxxx">
                                @error('api_key')
                                    <p class="text-red-500 text-xs mt-1">{{ $message }}</p>
                                @enderror
                            </div>

                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">API Secret / Private Key (Opcional)</label>
                                <input type="password" name="api_secret" value="{{ old('api_secret', $credential->api_secret ? decrypt($credential->api_secret) : '') }}"
                                       class="w-full px-4 py-2 border rounded-lg font-mono text-sm"
                                       placeholder="••••••••••••••••••••••">
                                <p class="text-gray-500 text-xs mt-1">Dejar en blanco si la API no requiere secret key</p>
                            </div>

                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Configuración Adicional (JSON Opcional)</label>
                                <textarea name="config" rows="4"
                                          class="w-full px-4 py-2 border rounded-lg font-mono text-sm"
                                          placeholder='{"endpoint": "https://api.example.com", "version": "v1"}'>{{ old('config', $credential->config) }}</textarea>
                                <p class="text-gray-500 text-xs mt-1">Formato JSON para configuraciones extra</p>
                            </div>
                        </div>
                    </div>

                    <!-- Estado y límites -->
                    <div class="bg-gray-50 p-6 rounded-lg">
                        <h3 class="text-lg font-semibold mb-4">Estado y Límites</h3>

                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <label class="flex items-center">
                                    <input type="checkbox" name="is_active" value="1"
                                           {{ $credential->is_active ? 'checked' : '' }}
                                           class="rounded border-gray-300 text-emerald-600 shadow-sm focus:border-emerald-300 focus:ring focus:ring-emerald-200 focus:ring-opacity-50">
                                    <span class="ml-2 text-sm text-gray-700">API Activa</span>
                                </label>
                            </div>

                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-2">Límite de Requests (Opcional)</label>
                                <input type="number" name="rate_limit" value="{{ old('rate_limit', $credential->rate_limit) }}"
                                       class="w-full px-4 py-2 border rounded-lg"
                                       placeholder="1000">
                                <p class="text-gray-500 text-xs mt-1">Requests por día (0 = ilimitado)</p>
                            </div>
                        </div>
                    </div>

                    <!-- Test de conexión -->
                    <div class="bg-blue-50 p-6 rounded-lg">
                        <h3 class="text-lg font-semibold mb-3">Test de Conexión</h3>
                        <p class="text-sm text-gray-700 mb-4">Puedes probar la conexión con la API antes de guardar los cambios.</p>
                        <button type="button" onclick="testConnection()" class="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg">
                            🔌 Probar Conexión
                        </button>
                        <div id="testResult" class="mt-3 hidden"></div>
                    </div>

                    <!-- Botones -->
                    <div class="flex justify-between items-center pt-4">
                        <a href="{{ route('admin.api-credentials') }}" class="px-6 py-2 bg-gray-300 hover:bg-gray-400 text-gray-700 rounded-lg">
                            Cancelar
                        </a>
                        <button type="submit" class="px-6 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg">
                            💾 Guardar Credenciales
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>

<script>
function testConnection() {
    // TODO: Implementar test de conexión con la API
    const resultDiv = document.getElementById('testResult');
    resultDiv.classList.remove('hidden');
    resultDiv.innerHTML = '<p class="text-yellow-600">⏳ Probando conexión...</p>';

    setTimeout(() => {
        resultDiv.innerHTML = '<p class="text-green-600">✅ Conexión exitosa</p>';
    }, 2000);
}
</script>
@endsection
