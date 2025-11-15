<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Términos y Condiciones - {{ config('app.name') }}</title>
    <meta name="description" content="Términos y condiciones de uso de {{ config('app.name') }}">

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
                <h1 class="text-4xl font-bold text-emerald-900 mb-3 text-center">Términos y Condiciones</h1>
                <p class="text-center text-gray-600 mb-8">Última actualización: {{ now()->format('d/m/Y') }}</p>

                <div class="prose prose-emerald max-w-none space-y-6 text-gray-700">
                    <section>
                        <h2 class="text-2xl font-bold text-emerald-800 mb-3">1. Aceptación de Términos</h2>
                        <p>Al acceder y utilizar {{ config('app.name') }}, aceptas estar sujeto a estos Términos y Condiciones. Si no estás de acuerdo con alguna parte de estos términos, no deberías utilizar nuestros servicios.</p>
                    </section>

                    <section>
                        <h2 class="text-2xl font-bold text-emerald-800 mb-3">2. Descripción del Servicio</h2>
                        <p>{{ config('app.name') }} proporciona servicios de automatización basados en Inteligencia Artificial, incluyendo pero no limitado a:</p>
                        <ul class="list-disc list-inside space-y-1 ml-4">
                            <li>Asistentes personales con IA</li>
                            <li>Organizadores de facturas con OCR</li>
                            <li>Organizadores de agenda</li>
                            <li>Suite de análisis cripto</li>
                            <li>Agentes de ventas con IA</li>
                            <li>Generadores de contenido</li>
                            <li>Automatización de e-commerce y redes sociales</li>
                        </ul>
                    </section>

                    <section>
                        <h2 class="text-2xl font-bold text-emerald-800 mb-3">3. Registro y Cuenta</h2>
                        <p>Para utilizar nuestros servicios, debes:</p>
                        <ul class="list-disc list-inside space-y-1 ml-4">
                            <li>Tener al menos 18 años de edad</li>
                            <li>Proporcionar información precisa y actualizada</li>
                            <li>Mantener la seguridad de tu cuenta y contraseña</li>
                            <li>Notificarnos inmediatamente sobre cualquier uso no autorizado</li>
                        </ul>
                    </section>

                    <section>
                        <h2 class="text-2xl font-bold text-emerald-800 mb-3">4. Trial Gratuito</h2>
                        <p>Ofrecemos un período de prueba gratuito de 7 días para servicios de suscripción:</p>
                        <ul class="list-disc list-inside space-y-1 ml-4">
                            <li>No se requiere tarjeta de crédito para comenzar el trial</li>
                            <li>Puedes cancelar en cualquier momento durante el trial sin cargo</li>
                            <li>El trial es válido una sola vez por usuario</li>
                            <li>Tras el trial, se aplicarán los cargos según el plan seleccionado</li>
                        </ul>
                    </section>

                    <section>
                        <h2 class="text-2xl font-bold text-emerald-800 mb-3">5. Pagos y Facturación</h2>
                        <p><strong>5.1 Métodos de Pago:</strong> Aceptamos PayPal, Pagopar, Bancard y criptomonedas (BTC, ETH, USDT).</p>
                        <p><strong>5.2 Suscripciones:</strong> Las suscripciones se renuevan automáticamente cada mes hasta que sean canceladas.</p>
                        <p><strong>5.3 Reembolsos:</strong> No se realizan reembolsos por períodos parciales. Al cancelar, mantienes acceso hasta el final del período pagado.</p>
                        <p><strong>5.4 Cambios de Precio:</strong> Nos reservamos el derecho de modificar precios con un aviso previo de 30 días.</p>
                    </section>

                    <section>
                        <h2 class="text-2xl font-bold text-emerald-800 mb-3">6. Uso Aceptable</h2>
                        <p>Al usar nuestros servicios, te comprometes a NO:</p>
                        <ul class="list-disc list-inside space-y-1 ml-4">
                            <li>Violar leyes o regulaciones aplicables</li>
                            <li>Infringir derechos de propiedad intelectual</li>
                            <li>Transmitir contenido dañino, ofensivo o ilegal</li>
                            <li>Intentar acceder sin autorización a sistemas o datos</li>
                            <li>Usar los servicios para spam o actividades maliciosas</li>
                            <li>Revender o redistribuir nuestros servicios sin autorización</li>
                        </ul>
                    </section>

                    <section>
                        <h2 class="text-2xl font-bold text-emerald-800 mb-3">7. Propiedad Intelectual</h2>
                        <p>Todo el contenido, software, diseños y marcas de {{ config('app.name') }} son propiedad exclusiva nuestra o de nuestros licenciantes. No se transfiere ningún derecho de propiedad intelectual al usar nuestros servicios.</p>
                    </section>

                    <section>
                        <h2 class="text-2xl font-bold text-emerald-800 mb-3">8. Limitación de Responsabilidad</h2>
                        <p>{{ config('app.name') }} se proporciona "tal cual" sin garantías de ningún tipo. No nos hacemos responsables por:</p>
                        <ul class="list-disc list-inside space-y-1 ml-4">
                            <li>Pérdidas de datos o interrupciones del servicio</li>
                            <li>Resultados específicos del uso de nuestros servicios</li>
                            <li>Daños indirectos, incidentales o consecuentes</li>
                            <li>Contenido generado por la IA que pueda ser inexacto</li>
                        </ul>
                    </section>

                    <section>
                        <h2 class="text-2xl font-bold text-emerald-800 mb-3">9. Terminación</h2>
                        <p>Podemos suspender o terminar tu acceso a los servicios si:</p>
                        <ul class="list-disc list-inside space-y-1 ml-4">
                            <li>Violas estos Términos y Condiciones</li>
                            <li>Usas los servicios de manera fraudulenta o ilegal</li>
                            <li>No pagas las tarifas aplicables</li>
                        </ul>
                    </section>

                    <section>
                        <h2 class="text-2xl font-bold text-emerald-800 mb-3">10. Modificaciones</h2>
                        <p>Nos reservamos el derecho de modificar estos términos en cualquier momento. Las modificaciones entrarán en vigencia inmediatamente tras su publicación. El uso continuado de los servicios constituye aceptación de los términos modificados.</p>
                    </section>

                    <section>
                        <h2 class="text-2xl font-bold text-emerald-800 mb-3">11. Ley Aplicable</h2>
                        <p>Estos términos se rigen por las leyes de Paraguay. Cualquier disputa se resolverá en los tribunales competentes de Paraguay.</p>
                    </section>

                    <section>
                        <h2 class="text-2xl font-bold text-emerald-800 mb-3">12. Contacto</h2>
                        <p>Para preguntas sobre estos términos, contacta con nosotros a través de nuestro sistema de soporte en el dashboard.</p>
                    </section>
                </div>

                <div class="mt-10 pt-8 border-t border-emerald-200 text-center">
                    <p class="text-gray-700 mb-4">Al usar {{ config('app.name') }}, aceptas estos términos y condiciones</p>
                    <div class="flex justify-center gap-4">
                        <a href="{{ route('privacy') }}" class="text-emerald-600 hover:text-emerald-700 font-semibold">
                            Ver Política de Privacidad →
                        </a>
                        <span class="text-gray-400">|</span>
                        <a href="{{ route('faq') }}" class="text-emerald-600 hover:text-emerald-700 font-semibold">
                            Ver FAQ →
                        </a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
