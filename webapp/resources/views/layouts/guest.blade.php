<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="csrf-token" content="{{ csrf_token() }}">

        <title>{{ config('app.name') }} - Autenticación</title>

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
    <body class="font-sans antialiased">
        <!-- Video Background -->
        <div class="video-background"></div>

        <div class="min-h-screen flex flex-col sm:justify-center items-center pt-6 sm:pt-0 px-4">
            <div class="mb-6">
                <a href="/" class="flex items-center space-x-2">
                    <span class="text-4xl">🤖</span>
                    <h1 class="text-white font-bold text-2xl">{{ config('app.name') }}</h1>
                </a>
            </div>

            <div class="w-full sm:max-w-md glass-strong rounded-2xl p-8 shadow-2xl border-2 border-white/20">
                {{ $slot }}
            </div>

            <div class="mt-6 text-center">
                <a href="/" class="text-white/80 hover:text-white text-sm transition">
                    ← Volver al inicio
                </a>
            </div>
        </div>
    </body>
</html>
