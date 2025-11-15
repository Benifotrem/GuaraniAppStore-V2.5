<x-guest-layout>
    <div class="mb-6 text-center">
        <h2 class="text-2xl font-bold text-emerald-900">Crear Cuenta</h2>
        <p class="text-gray-700 text-sm mt-2">Regístrate y prueba GRATIS por 7 días</p>
    </div>

    <!-- Trial Banner -->
    <div class="bg-gradient-to-r from-green-50 to-emerald-50 border-2 border-green-400 rounded-xl p-4 mb-6">
        <div class="flex items-center justify-center mb-2">
            <span class="text-2xl mr-2">🎁</span>
            <p class="text-emerald-900 font-bold text-lg">Trial Gratuito 7 Días</p>
        </div>
        <p class="text-gray-700 text-xs text-center">
            ✓ Sin tarjeta de crédito &nbsp;|&nbsp; ✓ Cancela cuando quieras
        </p>
    </div>

    <!-- Google OAuth Button -->
    <div class="mb-6">
        <a href="{{ route('auth.google') }}"
           class="w-full flex items-center justify-center gap-3 bg-white hover:bg-gray-50 text-gray-700 border-2 border-gray-300 px-6 py-3 rounded-lg font-semibold transition shadow-sm">
            <svg class="w-5 h-5" viewBox="0 0 24 24">
                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
            </svg>
            Registrarse con Google
        </a>
    </div>

    <div class="relative mb-6">
        <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-300"></div>
        </div>
        <div class="relative flex justify-center text-sm">
            <span class="px-2 bg-white text-gray-500">O usa tu email</span>
        </div>
    </div>

    <form method="POST" action="{{ route('register') }}">
        @csrf

        <!-- Name -->
        <div class="mb-4">
            <x-input-label for="name" value="Nombre completo" class="text-emerald-900 font-semibold" />
            <x-text-input id="name"
                          class="block mt-1 w-full border-emerald-200 focus:border-emerald-500 focus:ring-emerald-500"
                          type="text"
                          name="name"
                          :value="old('name')"
                          required
                          autofocus
                          autocomplete="name" />
            <x-input-error :messages="$errors->get('name')" class="mt-2" />
        </div>

        <!-- Email Address -->
        <div class="mb-4">
            <x-input-label for="email" value="Email" class="text-emerald-900 font-semibold" />
            <x-text-input id="email"
                          class="block mt-1 w-full border-emerald-200 focus:border-emerald-500 focus:ring-emerald-500"
                          type="email"
                          name="email"
                          :value="old('email')"
                          required
                          autocomplete="username" />
            <x-input-error :messages="$errors->get('email')" class="mt-2" />
        </div>

        <!-- Password -->
        <div class="mb-4">
            <x-input-label for="password" value="Contraseña" class="text-emerald-900 font-semibold" />
            <x-text-input id="password"
                          class="block mt-1 w-full border-emerald-200 focus:border-emerald-500 focus:ring-emerald-500"
                          type="password"
                          name="password"
                          required
                          autocomplete="new-password" />
            <x-input-error :messages="$errors->get('password')" class="mt-2" />
        </div>

        <!-- Confirm Password -->
        <div class="mb-6">
            <x-input-label for="password_confirmation" value="Confirmar contraseña" class="text-emerald-900 font-semibold" />
            <x-text-input id="password_confirmation"
                          class="block mt-1 w-full border-emerald-200 focus:border-emerald-500 focus:ring-emerald-500"
                          type="password"
                          name="password_confirmation"
                          required
                          autocomplete="new-password" />
            <x-input-error :messages="$errors->get('password_confirmation')" class="mt-2" />
        </div>

        <button type="submit"
                class="w-full bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white py-3 rounded-lg font-semibold transition shadow-lg">
            🚀 Comenzar Trial GRATIS
        </button>

        <p class="text-xs text-gray-600 text-center mt-4">
            Al registrarte aceptas nuestros
            <a href="#" class="text-emerald-600 hover:underline">Términos</a> y
            <a href="#" class="text-emerald-600 hover:underline">Política de Privacidad</a>
        </p>
    </form>

    <div class="mt-6 text-center">
        <p class="text-sm text-gray-700">
            ¿Ya tienes cuenta?
            <a href="{{ route('login') }}" class="text-emerald-600 hover:text-emerald-700 font-semibold">
                Inicia sesión
            </a>
        </p>
    </div>
</x-guest-layout>
