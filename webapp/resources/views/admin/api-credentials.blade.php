@extends('layouts.app')

@section('content')
<div class="py-12">
    <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
        <div class="bg-white overflow-hidden shadow-sm sm:rounded-lg">
            <div class="p-6">
                <div class="flex justify-between items-center mb-6">
                    <h2 class="text-2xl font-bold">Credenciales API Externas</h2>
                    <a href="{{ route('admin.dashboard') }}" class="px-4 py-2 bg-gray-500 hover:bg-gray-600 text-white rounded-lg">
                        ← Volver al Dashboard
                    </a>
                </div>

                <!-- Información de seguridad -->
                <div class="mb-6 bg-red-50 border border-red-200 rounded-lg p-4">
                    <div class="flex items-start">
                        <div class="text-2xl mr-3">🔒</div>
                        <div>
                            <h3 class="font-semibold text-red-800">Seguridad de Credenciales</h3>
                            <p class="text-sm text-red-700 mt-1">
                                Las credenciales API se almacenan encriptadas en la base de datos.
                                Solo usuarios administradores pueden verlas y modificarlas.
                            </p>
                        </div>
                    </div>
                </div>

                <!-- Tabla de credenciales -->
                <div class="overflow-x-auto">
                    <table class="min-w-full bg-white">
                        <thead class="bg-gray-100">
                            <tr>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Servicio</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">API</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Estado</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Última Actualización</th>
                                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Acciones</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-gray-200">
                            @forelse($credentials as $credential)
                            <tr class="hover:bg-gray-50">
                                <td class="px-6 py-4">
                                    <div class="flex items-center">
                                        @if($credential->service)
                                            <div class="text-2xl mr-3">{{ $credential->service->icon }}</div>
                                            <div>
                                                <div class="text-sm font-medium text-gray-900">{{ $credential->service->name }}</div>
                                                <div class="text-sm text-gray-500">{{ $credential->service->slug }}</div>
                                            </div>
                                        @else
                                            <div class="text-sm text-gray-500">Sistema Global</div>
                                        @endif
                                    </div>
                                </td>
                                <td class="px-6 py-4">
                                    <div class="text-sm font-medium text-gray-900">{{ $credential->api_name }}</div>
                                    <div class="text-xs text-gray-500">{{ $credential->api_type }}</div>
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap">
                                    @if($credential->is_active)
                                        <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                                            Activa
                                        </span>
                                    @else
                                        <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-100 text-gray-800">
                                            Inactiva
                                        </span>
                                    @endif
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    {{ $credential->updated_at->format('d/m/Y H:i') }}
                                </td>
                                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium">
                                    <a href="{{ route('admin.api-credentials.edit', $credential->id) }}" class="text-indigo-600 hover:text-indigo-900">
                                        Editar
                                    </a>
                                </td>
                            </tr>
                            @empty
                            <tr>
                                <td colspan="5" class="px-6 py-4 text-center text-gray-500">
                                    No hay credenciales API configuradas
                                </td>
                            </tr>
                            @endforelse
                        </tbody>
                    </table>
                </div>

                <!-- Paginación -->
                <div class="mt-6">
                    {{ $credentials->links() }}
                </div>

                <!-- APIs Disponibles -->
                <div class="mt-8 grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div class="bg-blue-50 p-4 rounded-lg">
                        <h4 class="font-semibold mb-2">APIs de IA</h4>
                        <ul class="text-sm text-gray-700 space-y-1">
                            <li>• OpenRouter (Principal)</li>
                            <li>• Google Gemini</li>
                            <li>• OpenAI (Opcional)</li>
                        </ul>
                    </div>

                    <div class="bg-green-50 p-4 rounded-lg">
                        <h4 class="font-semibold mb-2">APIs de Google</h4>
                        <ul class="text-sm text-gray-700 space-y-1">
                            <li>• Google Calendar</li>
                            <li>• Google Drive</li>
                            <li>• Google Maps</li>
                            <li>• Google Vision OCR</li>
                        </ul>
                    </div>

                    <div class="bg-purple-50 p-4 rounded-lg">
                        <h4 class="font-semibold mb-2">Otras APIs</h4>
                        <ul class="text-sm text-gray-700 space-y-1">
                            <li>• Outscraper (Maps)</li>
                            <li>• CoinGecko (Crypto)</li>
                            <li>• Blockchain APIs</li>
                            <li>• Social Media APIs</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
@endsection
