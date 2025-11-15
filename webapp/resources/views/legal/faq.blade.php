<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Preguntas Frecuentes (FAQ) - {{ config('app.name') }}</title>
    <meta name="description" content="Encuentra respuestas a las preguntas más frecuentes sobre nuestros servicios de automatización con IA">

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
    <div class="video-background"></div>

    <nav class="relative z-10 bg-white/10 backdrop-blur-md border-b border-white/20">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between items-center h-16">
                <a href="{{ route('home') }}" class="flex items-center space-x-2">
                    <span class="text-3xl">🤖</span>
                    <span class="text-white font-bold text-xl">{{ config('app.name') }}</span>
                </a>
                <a href="{{ route('home') }}" class="text-white hover:text-emerald-300 transition">
                    ← Volver al inicio
                </a>
            </div>
        </div>
    </nav>

    <div class="relative z-10 min-h-screen py-12">
        <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="glass-strong rounded-2xl p-8 shadow-2xl border-2 border-white/20">
                <h1 class="text-4xl font-bold text-emerald-900 mb-3 text-center">Preguntas Frecuentes</h1>
                <p class="text-center text-gray-700 mb-8">Encuentra respuestas a las preguntas más comunes</p>

                <div class="space-y-6">
                    <!-- General -->
                    <div>
                        <h2 class="text-2xl font-bold text-emerald-800 mb-4 border-b-2 border-emerald-200 pb-2">General</h2>

                        <div class="space-y-4">
                            <div>
                                <h3 class="font-bold text-lg text-gray-900 mb-2">¿Qué es {{ config('app.name') }}?</h3>
                                <p class="text-gray-700">{{ config('app.name') }} es una plataforma que ofrece servicios de automatización potenciados por Inteligencia Artificial. Nuestros servicios incluyen desde asistentes personales hasta automatización de comercio electrónico y redes sociales.</p>
                            </div>

                            <div>
                                <h3 class="font-bold text-lg text-gray-900 mb-2">¿Cómo funciona el trial gratuito?</h3>
                                <p class="text-gray-700">Al registrarte, obtienes acceso GRATIS por 7 días a todos nuestros servicios de suscripción. No necesitas tarjeta de crédito para comenzar el trial. Puedes cancelar en cualquier momento sin cargos.</p>
                            </div>

                            <div>
                                <h3 class="font-bold text-lg text-gray-900 mb-2">¿Cuál es la diferencia entre servicios de suscripción y pago único?</h3>
                                <p class="text-gray-700">Los servicios de suscripción se renuevan mensualmente y ofrecen acceso continuo. Los servicios de pago único son herramientas que pagas una sola vez y puedes usar sin límite de tiempo.</p>
                            </div>
                        </div>
                    </div>

                    <!-- Pagos -->
                    <div>
                        <h2 class="text-2xl font-bold text-emerald-800 mb-4 border-b-2 border-emerald-200 pb-2">Pagos y Facturación</h2>

                        <div class="space-y-4">
                            <div>
                                <h3 class="font-bold text-lg text-gray-900 mb-2">¿Qué métodos de pago aceptan?</h3>
                                <p class="text-gray-700 mb-2">Aceptamos los siguientes métodos de pago:</p>
                                <ul class="list-disc list-inside text-gray-700 space-y-1">
                                    <li>PayPal (tarjetas de crédito/débito internacionales)</li>
                                    <li>Pagopar (Paraguay - tarjetas y transferencias)</li>
                                    <li>Bancard VPOS (Paraguay - tarjetas)</li>
                                    <li>Criptomonedas (BTC, ETH, USDT) con 25% de descuento</li>
                                </ul>
                            </div>

                            <div>
                                <h3 class="font-bold text-lg text-gray-900 mb-2">¿Por qué las criptomonedas tienen descuento?</h3>
                                <p class="text-gray-700">Ofrecemos un descuento del 25% en pagos con criptomonedas porque nos ahorramos las comisiones de procesamiento de tarjetas tradicionales, y trasladamos ese beneficio a nuestros usuarios.</p>
                            </div>

                            <div>
                                <h3 class="font-bold text-lg text-gray-900 mb-2">¿Puedo cambiar mi método de pago?</h3>
                                <p class="text-gray-700">Sí, puedes cambiar tu método de pago en cualquier momento desde tu panel de suscripciones. El cambio se aplicará en tu próxima renovación.</p>
                            </div>

                            <div>
                                <h3 class="font-bold text-lg text-gray-900 mb-2">¿Cómo cancelo mi suscripción?</h3>
                                <p class="text-gray-700">Puedes cancelar tu suscripción en cualquier momento desde tu dashboard. Ve a "Mis Suscripciones" y haz clic en "Cancelar Suscripción". Mantendrás acceso hasta el final del período pagado.</p>
                            </div>
                        </div>
                    </div>

                    <!-- Servicios -->
                    <div>
                        <h2 class="text-2xl font-bold text-emerald-800 mb-4 border-b-2 border-emerald-200 pb-2">Servicios</h2>

                        <div class="space-y-4">
                            <div>
                                <h3 class="font-bold text-lg text-gray-900 mb-2">¿Necesito conocimientos técnicos para usar los servicios?</h3>
                                <p class="text-gray-700">No, nuestros servicios están diseñados para ser simples de usar. Solo necesitas seguir las instrucciones y configurar tus preferencias. Todo está pensado para usuarios sin conocimientos técnicos.</p>
                            </div>

                            <div>
                                <h3 class="font-bold text-lg text-gray-900 mb-2">¿Los servicios se integran con mis herramientas actuales?</h3>
                                <p class="text-gray-700">Sí, muchos de nuestros servicios se integran con plataformas populares como Google Calendar, Gmail, Telegram, y más. Cada servicio indica sus integraciones disponibles.</p>
                            </div>

                            <div>
                                <h3 class="font-bold text-lg text-gray-900 mb-2">¿Qué servicios están "próximamente"?</h3>
                                <p class="text-gray-700">Los servicios marcados como "próximamente" están en desarrollo activo. Puedes registrarte ahora para recibir notificaciones cuando estén disponibles.</p>
                            </div>

                            <div>
                                <h3 class="font-bold text-lg text-gray-900 mb-2">¿Puedo usar los servicios desde cualquier país?</h3>
                                <p class="text-gray-700">Sí, nuestros servicios son accesibles globalmente. Sin embargo, algunos métodos de pago específicos de Paraguay (Pagopar, Bancard) están limitados a ese país.</p>
                            </div>
                        </div>
                    </div>

                    <!-- Soporte -->
                    <div>
                        <h2 class="text-2xl font-bold text-emerald-800 mb-4 border-b-2 border-emerald-200 pb-2">Soporte Técnico</h2>

                        <div class="space-y-4">
                            <div>
                                <h3 class="font-bold text-lg text-gray-900 mb-2">¿Cómo contacto con soporte?</h3>
                                <p class="text-gray-700">Puedes contactarnos a través de nuestro sistema de soporte en el dashboard. Los usuarios premium reciben soporte prioritario por email y Telegram.</p>
                            </div>

                            <div>
                                <h3 class="font-bold text-lg text-gray-900 mb-2">¿Hay documentación disponible?</h3>
                                <p class="text-gray-700">Sí, cada servicio incluye documentación completa con guías paso a paso, ejemplos de uso y mejores prácticas.</p>
                            </div>
                        </div>
                    </div>

                    <!-- Seguridad -->
                    <div>
                        <h2 class="text-2xl font-bold text-emerald-800 mb-4 border-b-2 border-emerald-200 pb-2">Seguridad y Privacidad</h2>

                        <div class="space-y-4">
                            <div>
                                <h3 class="font-bold text-lg text-gray-900 mb-2">¿Mis datos están seguros?</h3>
                                <p class="text-gray-700">Absolutamente. Utilizamos encriptación SSL/TLS para todas las comunicaciones, y almacenamos datos sensibles con encriptación AES-256. Nunca compartimos tus datos con terceros.</p>
                            </div>

                            <div>
                                <h3 class="font-bold text-lg text-gray-900 mb-2">¿Qué hacen con mis datos?</h3>
                                <p class="text-gray-700">Solo usamos tus datos para proveer los servicios que solicitas. Lee nuestra <a href="{{ route('privacy') }}" class="text-emerald-600 hover:underline font-semibold">Política de Privacidad</a> para más detalles.</p>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="mt-10 pt-8 border-t border-emerald-200 text-center">
                    <p class="text-gray-700 mb-4">¿No encuentras lo que buscas?</p>
                    <div class="flex justify-center gap-4">
                        <a href="{{ route('home') }}" class="bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white px-6 py-3 rounded-lg font-semibold transition">
                            Volver al Inicio
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
