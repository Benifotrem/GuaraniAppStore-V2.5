<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ $service->name }} - {{ config('app.name') }}</title>
    <meta name="description" content="{{ $service->description }}">

    <!-- Schema.org Product Markup -->
    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": "{{ $service->name }}",
        "description": "{{ $service->description }}",
        "brand": {
            "@type": "Organization",
            "name": "Guarani App Store"
        },
        "offers": {
            "@type": "Offer",
            "price": "{{ $service->price }}",
            "priceCurrency": "PYG",
            "availability": "{{ $service->status === 'active' ? 'https://schema.org/InStock' : 'https://schema.org/PreOrder' }}",
            "seller": {
                "@type": "Organization",
                "name": "Guarani App Store"
            }
            @if($service->trial_days > 0)
            ,
            "priceSpecification": {
                "@type": "UnitPriceSpecification",
                "price": "0",
                "priceCurrency": "PYG",
                "name": "Trial gratuito {{ $service->trial_days }} días"
            }
            @endif
        }
    }
    </script>

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
<body class="font-sans antialiased">
    <!-- Video Background -->
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
                    @auth
                        <a href="{{ route('subscriptions.index') }}" class="text-white hover:text-emerald-300 transition">
                            Mis Suscripciones
                        </a>
                        <a href="{{ route('dashboard') }}" class="bg-white/20 hover:bg-white/30 text-white px-4 py-2 rounded-lg transition">
                            Dashboard
                        </a>
                    @else
                        <a href="{{ route('login') }}" class="text-white hover:text-emerald-300 transition">
                            Iniciar Sesión
                        </a>
                        <a href="{{ route('register') }}" class="bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white px-6 py-2 rounded-lg font-semibold transition">
                            Registrarse Gratis
                        </a>
                    @endauth
                </div>
            </div>
        </div>
    </nav>

    <!-- Service Details -->
    <div class="relative z-10 min-h-screen py-12">
        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
            <!-- Service Card -->
            <div class="glass-strong rounded-2xl p-8 shadow-2xl border-2 border-white/20 mb-6">
                <!-- Status Badge -->
                @if($service->status === 'coming_soon')
                <div class="text-center mb-6">
                    <span class="bg-yellow-500 text-white px-4 py-2 rounded-full text-sm font-bold">
                        🔜 Próximamente
                    </span>
                </div>
                @elseif($service->trial_days > 0)
                <div class="bg-gradient-to-r from-green-50 to-emerald-50 border-2 border-green-400 rounded-xl p-4 mb-6">
                    <div class="flex items-center justify-center">
                        <span class="text-2xl mr-2">🎁</span>
                        <p class="text-emerald-900 font-bold">Trial Gratuito de {{ $service->trial_days }} Días</p>
                    </div>
                </div>
                @endif

                <!-- Service Icon & Name -->
                <div class="text-center mb-8">
                    <span class="text-8xl animate-float inline-block mb-4">{{ $service->icon }}</span>
                    <h1 class="text-4xl font-bold text-emerald-900 mb-3">{{ $service->name }}</h1>
                    <p class="text-xl text-gray-700">{{ $service->description }}</p>
                </div>

                <!-- Features -->
                <div class="mb-8">
                    <h3 class="text-2xl font-bold text-emerald-900 mb-4">✨ Características</h3>
                    <ul class="grid grid-cols-1 md:grid-cols-2 gap-3">
                        @foreach($service->features as $feature)
                        <li class="flex items-start bg-white/50 rounded-lg p-3">
                            <span class="text-emerald-600 text-xl mr-2">✓</span>
                            <span class="text-gray-800">{{ $feature }}</span>
                        </li>
                        @endforeach
                    </ul>
                </div>

                <!-- Pricing -->
                <div class="border-t border-emerald-200 pt-6 mb-6">
                    <h3 class="text-2xl font-bold text-emerald-900 mb-4">💰 Precios</h3>

                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <!-- Regular Price -->
                        <div class="bg-white/50 rounded-xl p-6">
                            <div class="text-center">
                                <p class="text-gray-600 text-sm mb-2">Precio Regular</p>
                                <p class="text-4xl font-bold text-emerald-900 mb-1">
                                    Gs. {{ number_format($service->price, 0, ',', '.') }}
                                </p>
                                @if($service->type === 'subscription')
                                <p class="text-gray-600">/mes</p>
                                @else
                                <p class="text-gray-600">pago único</p>
                                @endif
                            </div>
                        </div>

                        <!-- Crypto Price -->
                        <div class="bg-gradient-to-r from-orange-500 to-yellow-500 text-white rounded-xl p-6 relative">
                            <div class="absolute -top-3 -right-3 bg-white text-orange-600 px-3 py-1 rounded-full text-xs font-bold">
                                -25% OFF
                            </div>
                            <div class="text-center">
                                <p class="text-white/90 text-sm mb-2">Con Criptomonedas</p>
                                <p class="text-4xl font-bold mb-1">
                                    Gs. {{ number_format($cryptoPrice, 0, ',', '.') }}
                                </p>
                                @if($service->type === 'subscription')
                                <p class="text-white/90">/mes</p>
                                @else
                                <p class="text-white/90">pago único</p>
                                @endif
                            </div>
                        </div>
                    </div>
                </div>

                <!-- CTA Buttons -->
                <div class="space-y-3">
                    @auth
                        @if($service->status === 'active')
                            <a href="{{ route('payments.show', $service->slug) }}"
                               class="block w-full text-center bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white py-4 rounded-lg font-bold text-lg transition shadow-lg">
                                🚀 Suscribirme Ahora
                            </a>
                        @else
                            <button disabled
                                    class="block w-full text-center bg-gray-300 text-gray-600 py-4 rounded-lg font-bold text-lg cursor-not-allowed">
                                Próximamente
                            </button>
                        @endif
                    @else
                        <a href="{{ route('register') }}"
                           class="block w-full text-center bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white py-4 rounded-lg font-bold text-lg transition shadow-lg">
                            🎁 Comenzar Trial GRATIS
                        </a>
                        <p class="text-center text-gray-700 text-sm">
                            ¿Ya tienes cuenta?
                            <a href="{{ route('login') }}" class="text-emerald-600 hover:text-emerald-700 font-semibold">
                                Inicia sesión
                            </a>
                        </p>
                    @endauth
                </div>
            </div>

            <!-- Back Button -->
            <div class="text-center">
                <a href="{{ route('home') }}" class="text-white/80 hover:text-white text-sm transition">
                    ← Volver al inicio
                </a>
            </div>
        </div>
    </div>
</body>
</html>
