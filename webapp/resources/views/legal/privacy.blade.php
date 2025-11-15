<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Política de Privacidad - {{ config('app.name') }}</title>
    <meta name="description" content="Política de privacidad y protección de datos de {{ config('app.name') }}">

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
                <h1 class="text-4xl font-bold text-emerald-900 mb-3 text-center">Política de Privacidad</h1>
                <p class="text-center text-gray-600 mb-8">Última actualización: {{ now()->format('d/m/Y') }}</p>

                <div class="prose prose-emerald max-w-none space-y-6 text-gray-700">
                    <section>
                        <h2 class="text-2xl font-bold text-emerald-800 mb-3">1. Introducción</h2>
                        <p>En {{ config('app.name') }}, respetamos tu privacidad y nos comprometemos a proteger tus datos personales. Esta Política de Privacidad explica cómo recopilamos, usamos, compartimos y protegemos tu información cuando utilizas nuestros servicios.</p>
                    </section>

                    <section>
                        <h2 class="text-2xl font-bold text-emerald-800 mb-3">2. Información que Recopilamos</h2>

                        <p><strong>2.1 Información de Registro:</strong></p>
                        <ul class="list-disc list-inside space-y-1 ml-4">
                            <li>Nombre completo</li>
                            <li>Dirección de correo electrónico</li>
                            <li>Contraseña (encriptada)</li>
                            <li>Información de Google OAuth (si usas inicio de sesión con Google)</li>
                        </ul>

                        <p class="mt-4"><strong>2.2 Información de Pago:</strong></p>
                        <ul class="list-disc list-inside space-y-1 ml-4">
                            <li>Detalles de transacciones (monto, fecha, método)</li>
                            <li>No almacenamos números de tarjetas de crédito completos</li>
                            <li>Los pagos se procesan a través de proveedores seguros (PayPal, Pagopar, Bancard)</li>
                        </ul>

                        <p class="mt-4"><strong>2.3 Información de Uso:</strong></p>
                        <ul class="list-disc list-inside space-y-1 ml-4">
                            <li>Servicios que utilizas y frecuencia de uso</li>
                            <li>Configuraciones y preferencias</li>
                            <li>Datos generados por los servicios de IA</li>
                            <li>Registros de actividad y logs técnicos</li>
                        </ul>

                        <p class="mt-4"><strong>2.4 Información Técnica:</strong></p>
                        <ul class="list-disc list-inside space-y-1 ml-4">
                            <li>Dirección IP</li>
                            <li>Tipo de navegador y dispositivo</li>
                            <li>Cookies y tecnologías similares</li>
                        </ul>
                    </section>

                    <section>
                        <h2 class="text-2xl font-bold text-emerald-800 mb-3">3. Cómo Usamos tu Información</h2>
                        <p>Utilizamos tu información para:</p>
                        <ul class="list-disc list-inside space-y-1 ml-4">
                            <li>Proveer y mantener nuestros servicios</li>
                            <li>Procesar pagos y suscripciones</li>
                            <li>Personalizar tu experiencia</li>
                            <li>Mejorar nuestros servicios mediante análisis y retroalimentación</li>
                            <li>Enviar comunicaciones importantes sobre tu cuenta</li>
                            <li>Detectar y prevenir fraudes o abusos</li>
                            <li>Cumplir con obligaciones legales</li>
                        </ul>
                    </section>

                    <section>
                        <h2 class="text-2xl font-bold text-emerald-800 mb-3">4. Compartir Información</h2>
                        <p><strong>NO vendemos tu información personal.</strong> Solo compartimos información en los siguientes casos:</p>

                        <p class="mt-4"><strong>4.1 Proveedores de Servicios:</strong></p>
                        <ul class="list-disc list-inside space-y-1 ml-4">
                            <li>Procesadores de pago (PayPal, Pagopar, Bancard)</li>
                            <li>Proveedores de APIs (OpenRouter, Google, Telegram)</li>
                            <li>Servicios de hosting y almacenamiento</li>
                        </ul>

                        <p class="mt-4"><strong>4.2 Requerimientos Legales:</strong></p>
                        <ul class="list-disc list-inside space-y-1 ml-4">
                            <li>Cuando sea requerido por ley</li>
                            <li>Para proteger nuestros derechos legales</li>
                            <li>Para prevenir fraudes o actividades ilegales</li>
                        </ul>

                        <p class="mt-4"><strong>4.3 Con tu Consentimiento:</strong></p>
                        <p class="ml-4">Podemos compartir información si nos das tu consentimiento explícito.</p>
                    </section>

                    <section>
                        <h2 class="text-2xl font-bold text-emerald-800 mb-3">5. Seguridad de Datos</h2>
                        <p>Implementamos medidas de seguridad para proteger tu información:</p>
                        <ul class="list-disc list-inside space-y-1 ml-4">
                            <li>Encriptación SSL/TLS para todas las comunicaciones</li>
                            <li>Encriptación AES-256 para datos sensibles almacenados</li>
                            <li>Contraseñas hasheadas con bcrypt</li>
                            <li>Acceso restringido a datos personales</li>
                            <li>Auditorías de seguridad regulares</li>
                            <li>Backups automáticos encriptados</li>
                        </ul>
                    </section>

                    <section>
                        <h2 class="text-2xl font-bold text-emerald-800 mb-3">6. Tus Derechos</h2>
                        <p>Tienes los siguientes derechos sobre tus datos personales:</p>

                        <p class="mt-4"><strong>6.1 Acceso:</strong> Puedes solicitar una copia de tus datos personales.</p>
                        <p><strong>6.2 Rectificación:</strong> Puedes corregir datos inexactos o incompletos.</p>
                        <p><strong>6.3 Eliminación:</strong> Puedes solicitar la eliminación de tus datos ("derecho al olvido").</p>
                        <p><strong>6.4 Portabilidad:</strong> Puedes solicitar tus datos en formato portable.</p>
                        <p><strong>6.5 Objeción:</strong> Puedes objetar ciertos usos de tus datos.</p>
                        <p><strong>6.6 Restricción:</strong> Puedes solicitar limitar el procesamiento de tus datos.</p>

                        <p class="mt-4">Para ejercer estos derechos, contacta con nosotros a través del dashboard.</p>
                    </section>

                    <section>
                        <h2 class="text-2xl font-bold text-emerald-800 mb-3">7. Cookies</h2>
                        <p>Utilizamos cookies para:</p>
                        <ul class="list-disc list-inside space-y-1 ml-4">
                            <li>Mantener tu sesión activa</li>
                            <li>Recordar tus preferencias</li>
                            <li>Analizar el uso del sitio</li>
                            <li>Mejorar la seguridad</li>
                        </ul>
                        <p class="mt-4">Puedes configurar tu navegador para rechazar cookies, pero esto puede afectar la funcionalidad del sitio.</p>
                    </section>

                    <section>
                        <h2 class="text-2xl font-bold text-emerald-800 mb-3">8. Retención de Datos</h2>
                        <p>Conservamos tus datos personales mientras:</p>
                        <ul class="list-disc list-inside space-y-1 ml-4">
                            <li>Tu cuenta permanezca activa</li>
                            <li>Sea necesario para proveer los servicios</li>
                            <li>Sea requerido por obligaciones legales</li>
                            <li>Sea necesario para resolver disputas</li>
                        </ul>
                        <p class="mt-4">Tras eliminar tu cuenta, conservamos algunos datos por razones legales durante el período requerido por ley.</p>
                    </section>

                    <section>
                        <h2 class="text-2xl font-bold text-emerald-800 mb-3">9. Transferencias Internacionales</h2>
                        <p>Tus datos pueden ser transferidos y procesados en servidores ubicados fuera de tu país. Cuando esto ocurra, nos aseguraremos de que existan salvaguardias adecuadas para proteger tu información.</p>
                    </section>

                    <section>
                        <h2 class="text-2xl font-bold text-emerald-800 mb-3">10. Menores de Edad</h2>
                        <p>Nuestros servicios no están dirigidos a menores de 18 años. No recopilamos intencionalmente información de menores. Si descubres que un menor nos ha proporcionado información personal, contacta con nosotros inmediatamente.</p>
                    </section>

                    <section>
                        <h2 class="text-2xl font-bold text-emerald-800 mb-3">11. Cambios a esta Política</h2>
                        <p>Podemos actualizar esta Política de Privacidad ocasionalmente. Te notificaremos sobre cambios significativos mediante:</p>
                        <ul class="list-disc list-inside space-y-1 ml-4">
                            <li>Un aviso en nuestro sitio web</li>
                            <li>Un correo electrónico a tu dirección registrada</li>
                        </ul>
                        <p class="mt-4">El uso continuado de nuestros servicios tras la publicación de cambios constituye aceptación de la nueva política.</p>
                    </section>

                    <section>
                        <h2 class="text-2xl font-bold text-emerald-800 mb-3">12. Contacto</h2>
                        <p>Para preguntas sobre esta Política de Privacidad o para ejercer tus derechos, contacta con nosotros a través del sistema de soporte en tu dashboard.</p>
                    </section>
                </div>

                <div class="mt-10 pt-8 border-t border-emerald-200 text-center">
                    <p class="text-gray-700 mb-4">Tu privacidad es nuestra prioridad</p>
                    <div class="flex justify-center gap-4">
                        <a href="{{ route('terms') }}" class="text-emerald-600 hover:text-emerald-700 font-semibold">
                            Ver Términos y Condiciones →
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
