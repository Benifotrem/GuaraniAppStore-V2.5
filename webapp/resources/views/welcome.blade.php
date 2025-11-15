<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ config('app.name') }} - Plataforma de Automatización</title>

    <!-- SEO Meta Tags -->
    <meta name="description" content="Automatiza tu empresa con 11 servicios de IA: Agente de Ventas, Organizador de Facturas OCR, Suite Crypto y más. Trial 7 días GRATIS.">
    <meta name="keywords" content="automatización, IA, chatbot, OCR facturas, criptomonedas, Paraguay">

    @vite(['resources/css/app.css', 'resources/js/app.js'])

    <style>
        /* Video Background */
        .video-background {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: -1;
            background: linear-gradient(135deg, #0f766e 0%, #065f46 100%);
        }

        .video-background::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.3);
        }
    </style>
</head>
<body class="antialiased">
    <!-- Video Background -->
    <div class="video-background"></div>

    <!-- Header -->
    <header class="relative z-50 w-full py-4 px-6 bg-black/20 backdrop-blur-sm">
        <div class="max-w-7xl mx-auto flex items-center justify-between">
            <div class="flex items-center space-x-2">
                <span class="text-2xl">🤖</span>
                <h1 class="text-white font-bold text-xl">{{ config('app.name') }}</h1>
            </div>

            <nav class="flex items-center space-x-4">
                @auth
                    <a href="{{ route('dashboard') }}"
                       class="px-6 py-2 bg-emerald-500 hover:bg-emerald-600 text-white rounded-full font-semibold transition">
                        Dashboard
                    </a>
                @else
                    <a href="{{ route('login') }}"
                       class="px-6 py-2 text-white hover:text-emerald-300 transition">
                        Iniciar Sesión
                    </a>
                    <a href="{{ route('register') }}"
                       class="px-6 py-2 bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white rounded-full font-semibold btn-primary shadow-xl">
                        Prueba Gratis 7 Días
                    </a>
                @endauth
            </nav>
        </div>
    </header>

    <!-- Main Content -->
    <main class="relative z-10">
        <!-- Hero Section -->
        <section class="pt-32 pb-12 px-6">
            <div class="max-w-7xl mx-auto text-center">
                <div class="animate-fade-in-up">
                    <h2 class="text-5xl sm:text-6xl lg:text-7xl font-bold mb-6 leading-tight text-white text-shadow-strong">
                        Automatiza tu Empresa
                        <br />
                        <span class="text-emerald-300">con Soluciones Inteligentes</span>
                    </h2>
                    <p class="text-xl text-white text-shadow mb-4 max-w-3xl mx-auto">
                        Desde contabilizar facturas a partir de una foto o pdf, pasando por prospección de leads, hasta agentes de ventas 24/7. Transforma tu negocio con automatización avanzada.
                    </p>

                    <!-- Banner Trial Gratuito -->
                    <div class="glass-strong rounded-2xl p-6 max-w-2xl mx-auto mb-4 border-4 border-green-400 bg-gradient-to-r from-green-50 to-emerald-50">
                        <div class="flex items-center justify-center mb-2">
                            <span class="text-3xl mr-2">🎁</span>
                            <p class="text-emerald-900 font-bold text-2xl">
                                ¡Trial Gratuito de 7 Días!
                            </p>
                        </div>
                        <p class="text-gray-800 text-base">
                            Prueba <strong>cualquier servicio sin tarjeta de crédito</strong>
                        </p>
                        <p class="text-green-700 text-sm mt-2 font-semibold">
                            ✓ Sin compromiso &nbsp;|&nbsp; ✓ Cancela cuando quieras &nbsp;|&nbsp; ✓ Full acceso
                        </p>
                    </div>

                    <!-- Banner Crypto -->
                    <div class="glass-strong rounded-2xl p-4 max-w-2xl mx-auto mb-8 border-2 border-yellow-400 bg-yellow-50">
                        <p class="text-emerald-900 font-semibold text-lg">
                            ⚡ Servicios para inversores en criptomonedas
                        </p>
                        <p class="text-gray-700 text-sm mt-1">
                            Regístrate hoy y obtén nuestro <strong>Escáner de Fraude CryptoShield IA GRATIS... para siempre</strong>
                        </p>
                        <p class="text-orange-600 text-xs mt-2 font-semibold">
                            🪙 25% OFF en planes anuales pagando con BTC/ETH
                        </p>
                    </div>

                    @guest
                    <div class="flex flex-col sm:flex-row gap-4 justify-center">
                        <a href="{{ route('register') }}"
                           class="bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white px-8 py-6 text-lg rounded-full btn-primary shadow-xl font-semibold">
                            🚀 Comienza Tu Trial GRATIS
                        </a>
                        <a href="#servicios"
                           class="glass-strong text-emerald-900 px-8 py-6 text-lg rounded-full font-semibold hover:bg-white/95 transition">
                            📋 Ver Servicios
                        </a>
                    </div>
                    @endguest
                </div>
            </div>
        </section>

        <!-- Services Grid -->
        <section id="servicios" class="py-16 px-6">
            <div class="max-w-7xl mx-auto">
                <h3 class="text-4xl font-bold text-center text-white mb-12 text-shadow">
                    Nuestros Servicios de Automatización
                </h3>

                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    @foreach($services as $service)
                    <div class="service-card glass-strong rounded-2xl p-6 hover:scale-105 transition-all duration-300 relative">
                        <!-- Badge "Próximamente" -->
                        @if($service->status === 'coming_soon')
                        <div class="absolute top-4 right-4 bg-yellow-500 text-white px-3 py-1 rounded-full text-xs font-bold">
                            🔜 Próximamente
                        </div>
                        @endif

                        <!-- Icon & Title -->
                        <div class="text-center mb-4">
                            <span class="text-6xl mb-3 block animate-float">{{ $service->icon }}</span>
                            <h4 class="text-xl font-bold text-emerald-900 mb-2">{{ $service->name }}</h4>
                            <p class="text-gray-700 text-sm">{{ $service->description }}</p>
                        </div>

                        <!-- Features -->
                        <ul class="space-y-2 mb-4">
                            @foreach($service->features as $feature)
                            <li class="flex items-start text-sm text-gray-800">
                                <span class="text-emerald-600 mr-2">✓</span>
                                <span>{{ $feature }}</span>
                            </li>
                            @endforeach
                        </ul>

                        <!-- Price & CTA -->
                        <div class="border-t border-emerald-200 pt-4">
                            <div class="flex items-center justify-between mb-3">
                                <div>
                                    <span class="text-2xl font-bold text-emerald-900">
                                        @if($service->price == 0)
                                            GRATIS
                                        @else
                                            Gs. {{ number_format($service->price, 0, ',', '.') }}
                                        @endif
                                    </span>
                                    @if($service->type === 'subscription')
                                    <span class="text-sm text-gray-600">/mes</span>
                                    @else
                                    <span class="text-sm text-gray-600">único</span>
                                    @endif
                                </div>

                                @if($service->trial_days > 0)
                                <span class="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full font-bold">
                                    {{ $service->trial_days }} días gratis
                                </span>
                                @endif
                            </div>

                            @if($service->status === 'active')
                            <a href="{{ route('services.show', $service->slug) }}"
                               class="block w-full text-center bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white py-3 rounded-lg font-semibold transition">
                                Ver Detalles
                            </a>
                            @else
                            <button disabled
                                    class="block w-full text-center bg-gray-300 text-gray-600 py-3 rounded-lg font-semibold cursor-not-allowed">
                                Próximamente
                            </button>
                            @endif
                        </div>
                    </div>
                    @endforeach
                </div>
            </div>
        </section>

        <!-- CTA Section -->
        <section class="py-16 px-6">
            <div class="max-w-4xl mx-auto text-center">
                <div class="glass-strong rounded-3xl p-12 border-2 border-emerald-400">
                    <h3 class="text-3xl font-bold text-emerald-900 mb-4">
                        ¿Listo para Automatizar tu Empresa?
                    </h3>
                    <p class="text-gray-800 text-lg mb-6">
                        Comienza tu trial gratuito de 7 días. Sin tarjeta de crédito. Cancela cuando quieras.
                    </p>
                    <a href="{{ route('register') }}"
                       class="inline-block bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white px-12 py-4 text-lg rounded-full btn-primary shadow-2xl font-bold">
                        Comenzar Ahora →
                    </a>
                </div>
            </div>
        </section>
    </main>

    <!-- Footer -->
    <footer class="relative z-10 bg-black/40 backdrop-blur-sm text-white py-12 px-6 mt-16">
        <div class="max-w-7xl mx-auto">
            <div class="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
                <div>
                    <h5 class="font-bold text-lg mb-4">{{ config('app.name') }}</h5>
                    <p class="text-sm text-gray-300">
                        Plataforma de automatización con IA para empresas en Paraguay y Latinoamérica.
                    </p>
                </div>

                <div>
                    <h5 class="font-bold text-lg mb-4">Servicios</h5>
                    <ul class="space-y-2 text-sm text-gray-300">
                        <li><a href="#" class="hover:text-emerald-300">Ruptura del Hielo</a></li>
                        <li><a href="#" class="hover:text-emerald-300">Agente de Ventas IA</a></li>
                        <li><a href="#" class="hover:text-emerald-300">Asistente Personal</a></li>
                        <li><a href="#" class="hover:text-emerald-300">Suite Crypto</a></li>
                    </ul>
                </div>

                <div>
                    <h5 class="font-bold text-lg mb-4">Empresa</h5>
                    <ul class="space-y-2 text-sm text-gray-300">
                        <li><a href="#" class="hover:text-emerald-300">Acerca de</a></li>
                        <li><a href="#" class="hover:text-emerald-300">Blog</a></li>
                        <li><a href="#" class="hover:text-emerald-300">FAQ</a></li>
                        <li><a href="#" class="hover:text-emerald-300">Contacto</a></li>
                    </ul>
                </div>

                <div>
                    <h5 class="font-bold text-lg mb-4">Legal</h5>
                    <ul class="space-y-2 text-sm text-gray-300">
                        <li><a href="#" class="hover:text-emerald-300">Términos y Condiciones</a></li>
                        <li><a href="#" class="hover:text-emerald-300">Política de Privacidad</a></li>
                        <li><a href="#" class="hover:text-emerald-300">Política de Cookies</a></li>
                    </ul>
                </div>
            </div>

            <div class="border-t border-white/20 pt-8 text-center text-sm text-gray-400">
                <p>&copy; {{ date('Y') }} {{ config('app.name') }}. Todos los derechos reservados.</p>
                <p class="mt-2">Hecho con ❤️ en Paraguay 🇵🇾</p>
            </div>
        </div>
    </footer>
</body>
</html>
