<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <meta name="csrf-token" content="{{ csrf_token() }}">
        <meta name="description" content="Plataforma de servicios digitales premium con 7 días de prueba gratuita. Marketing, gestión de redes, automatización, desarrollo web y más.">
        <meta name="keywords" content="servicios digitales, suscripción, marketing digital, automatización, desarrollo web, Guarani App Store">

        <title>{{ config('app.name', 'Laravel') }}</title>

        <!-- Schema.org Organization Markup -->
        <script type="application/ld+json">
        {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": "Guarani App Store",
            "description": "Plataforma de servicios digitales premium con trial gratuito de 7 días",
            "url": "{{ url('/') }}",
            "logo": "{{ url('/images/logo.png') }}",
            "sameAs": [
                "https://twitter.com/guaraniappstore",
                "https://facebook.com/guaraniappstore"
            ],
            "contactPoint": {
                "@type": "ContactPoint",
                "contactType": "Customer Support",
                "email": "soporte@guaraniappstore.com"
            }
        }
        </script>

        <!-- Fonts -->
        <link rel="preconnect" href="https://fonts.bunny.net">
        <link href="https://fonts.bunny.net/css?family=figtree:400,500,600&display=swap" rel="stylesheet" />

        <!-- Scripts -->
        @vite(['resources/css/app.css', 'resources/js/app.js'])
    </head>
    <body class="font-sans antialiased">
        <div class="min-h-screen bg-gray-100 dark:bg-gray-900">
            @include('layouts.navigation')

            <!-- Page Heading -->
            @isset($header)
                <header class="bg-white dark:bg-gray-800 shadow">
                    <div class="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
                        {{ $header }}
                    </div>
                </header>
            @endisset

            <!-- Page Content -->
            <main>
                {{ $slot }}
            </main>
        </div>
    </body>
</html>
