<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ $service->name }} - {{ config('app.name') }}</title>

    @vite(['resources/css/app.css', 'resources/js/app.js'])

    <style>
        .video-background {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            background: linear-gradient(135deg, #0f766e 0%, #065f46 100%);
        }
    </style>
</head>
<body class="font-sans antialiased">
    <div class="video-background"></div>

    <!-- Navbar -->
    <nav class="relative z-10 bg-white/10 backdrop-blur-md border-b border-white/20">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <a href="{{ route('home') }}" class="flex items-center space-x-2">
                    <span class="text-3xl">🤖</span>
                    <span class="text-white font-bold text-xl">{{ config('app.name') }}</span>
                </a>
                <div class="flex items-center space-x-4">
                    <a href="{{ route('dashboard') }}" class="text-white hover:text-emerald-300 transition">Dashboard</a>
                    <form method="POST" action="{{ route('logout') }}">
                        @csrf
                        <button type="submit" class="text-white hover:text-emerald-300 transition">Cerrar Sesión</button>
                    </form>
                </div>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="relative z-10 py-12 px-6">
        <div class="max-w-7xl mx-auto">
            <!-- Header -->
            <div class="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-8 mb-8 shadow-2xl">
                <div class="flex items-center justify-between">
                    <div>
                        <h1 class="text-4xl font-bold text-white mb-2">{{ $service->icon }} {{ $service->name }}</h1>
                        <p class="text-white/80">{{ $service->description }}</p>
                    </div>
                </div>
            </div>

            <!-- Search Section -->
            <div class="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-8 mb-8 shadow-2xl">
                <h2 class="text-2xl font-bold text-white mb-6">Buscar Leads en Google Maps</h2>

                <form id="searchForm" class="space-y-4">
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div>
                            <label class="block text-white mb-2">Búsqueda *</label>
                            <input type="text" name="query" required
                                   class="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/60"
                                   placeholder="ej: Restaurantes, Abogados, etc.">
                        </div>
                        <div>
                            <label class="block text-white mb-2">Ubicación</label>
                            <input type="text" name="location"
                                   class="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/60"
                                   placeholder="ej: Asunción, Paraguay">
                        </div>
                        <div>
                            <label class="block text-white mb-2">Radio (km)</label>
                            <input type="number" name="radius" min="1" max="50" value="10"
                                   class="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white">
                        </div>
                    </div>
                    <button type="submit" class="px-6 py-3 bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg font-semibold transition">
                        🔍 Buscar Leads
                    </button>
                </form>

                <div id="resultsSection" class="mt-8 hidden">
                    <h3 class="text-xl font-bold text-white mb-4">Resultados</h3>
                    <div id="resultsContainer" class="space-y-4"></div>
                </div>
            </div>

            <!-- Ice Breaker Generator -->
            <div class="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-8 mb-8 shadow-2xl">
                <h2 class="text-2xl font-bold text-white mb-6">Generar Mensaje Ice Breaker con IA</h2>

                <form id="iceBreakerForm" class="space-y-4">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label class="block text-white mb-2">Nombre del Lead *</label>
                            <input type="text" name="lead_name" required
                                   class="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white">
                        </div>
                        <div>
                            <label class="block text-white mb-2">Tipo de Negocio *</label>
                            <input type="text" name="business_type" required
                                   class="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white">
                        </div>
                    </div>
                    <div>
                        <label class="block text-white mb-2">Contexto Adicional</label>
                        <textarea name="context" rows="3"
                                  class="w-full px-4 py-2 rounded-lg bg-white/20 border border-white/30 text-white"></textarea>
                    </div>
                    <button type="submit" class="px-6 py-3 bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg font-semibold transition">
                        ✨ Generar Mensaje
                    </button>
                </form>

                <div id="messageResult" class="mt-6 hidden">
                    <div class="bg-white/20 rounded-lg p-4">
                        <p class="text-white" id="generatedMessage"></p>
                    </div>
                </div>
            </div>

            <!-- Export Section -->
            <div class="bg-white/10 backdrop-blur-md border border-white/20 rounded-2xl p-8 shadow-2xl">
                <h2 class="text-2xl font-bold text-white mb-6">Exportar a Google Sheets</h2>
                <p class="text-white/80 mb-4">Los leads encontrados se pueden exportar directamente a Google Sheets para su análisis.</p>
                <button onclick="alert('Función de export - Requiere integración con Google Sheets API')"
                        class="px-6 py-3 bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg font-semibold transition">
                    📊 Exportar a Sheets
                </button>
            </div>
        </div>
    </main>

    <script>
        // Note: This is placeholder JavaScript. In production, implement proper API calls
        document.getElementById('searchForm').addEventListener('submit', function(e) {
            e.preventDefault();
            alert('Función de búsqueda - Requiere integración con Google Maps API');
        });

        document.getElementById('iceBreakerForm').addEventListener('submit', function(e) {
            e.preventDefault();
            alert('Generación de mensajes - Requiere integración con API de IA');
        });
    </script>
</body>
</html>
