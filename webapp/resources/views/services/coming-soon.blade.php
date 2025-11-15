<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ $service->name }} - Próximamente</title>

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
                <a href="{{ route('home') }}" class="text-white hover:text-emerald-300 transition">← Volver</a>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main class="relative z-10 py-20 px-6">
        <div class="max-w-4xl mx-auto text-center">
            <!-- Coming Soon Badge -->
            <div class="inline-block bg-yellow-500 text-white px-6 py-2 rounded-full font-bold mb-8 shadow-xl">
                🚀 PRÓXIMAMENTE
            </div>

            <!-- Service Info -->
            <div class="bg-white/10 backdrop-blur-md border border-white/20 rounded-3xl p-12 shadow-2xl">
                <div class="text-6xl mb-6">{{ $service->icon }}</div>
                <h1 class="text-5xl font-bold text-white mb-6">{{ $service->name }}</h1>
                <p class="text-2xl text-white/90 mb-12">{{ $service->description }}</p>

                <!-- Features Preview -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-12 text-left">
                    @foreach($service->features as $feature)
                    <div class="bg-white/10 backdrop-blur-sm rounded-lg p-4 border border-white/20">
                        <p class="text-white">✨ {{ $feature }}</p>
                    </div>
                    @endforeach
                </div>

                <!-- Price Preview -->
                <div class="bg-emerald-500/20 backdrop-blur-sm border border-emerald-400/30 rounded-2xl p-8 mb-12">
                    <p class="text-white/80 mb-2">Precio cuando esté disponible:</p>
                    <p class="text-4xl font-bold text-white">
                        ₲{{ number_format($service->price, 0, ',', '.') }}
                        <span class="text-lg font-normal">/mes</span>
                    </p>
                    @if($service->trial_days > 0)
                    <p class="text-emerald-300 mt-4 font-semibold">
                        🎁 {{ $service->trial_days }} días de prueba GRATIS
                    </p>
                    @endif
                </div>

                <!-- Notify Me Form -->
                <div class="bg-white/5 backdrop-blur-sm border border-white/20 rounded-2xl p-8">
                    <h3 class="text-2xl font-bold text-white mb-4">¿Quieres ser notificado cuando esté disponible?</h3>
                    <p class="text-white/80 mb-6">Te avisaremos por email cuando este servicio esté listo.</p>

                    <form id="notifyForm" class="flex flex-col sm:flex-row gap-4 max-w-md mx-auto">
                        <input type="email" name="email" required
                               class="flex-1 px-6 py-3 rounded-lg bg-white/20 border border-white/30 text-white placeholder-white/60"
                               placeholder="tu@email.com">
                        <button type="submit"
                                class="px-8 py-3 bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg font-semibold transition shadow-xl">
                            Notificarme
                        </button>
                    </form>

                    <p id="notifySuccess" class="text-emerald-300 mt-4 hidden">
                        ✅ Te notificaremos cuando esté disponible
                    </p>
                </div>

                <!-- Back to Home -->
                <div class="mt-12">
                    <a href="{{ route('home') }}"
                       class="inline-block px-8 py-4 bg-white/20 hover:bg-white/30 border border-white/30 text-white rounded-lg font-semibold transition">
                        ← Ver otros servicios disponibles
                    </a>
                </div>
            </div>
        </div>
    </main>

    <script>
        document.getElementById('notifyForm').addEventListener('submit', function(e) {
            e.preventDefault();
            // TODO: Store email in database for notifications
            document.getElementById('notifySuccess').classList.remove('hidden');
            this.reset();
        });
    </script>
</body>
</html>
