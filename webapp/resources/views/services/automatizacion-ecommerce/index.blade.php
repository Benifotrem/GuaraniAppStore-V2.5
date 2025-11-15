@if($service->status === 'coming_soon')
    @include('services.coming-soon', ['service' => $service])
@else
@extends('layouts.app')

@section('content')
<div class="py-12">
    <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
        @if($onTrial)
        <div class="bg-yellow-100 border border-yellow-400 text-yellow-800 px-6 py-4 rounded-lg mb-6">
            <p class="font-semibold">🎁 Trial Activo - {{ $trialDaysLeft }} días restantes</p>
        </div>
        @endif

        <h1 class="text-3xl font-bold mb-8">{{ $service->icon }} {{ $service->name }}</h1>

        <!-- Connect Platform -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6 mb-8">
            <h2 class="text-2xl font-bold mb-6">Conectar Plataforma E-commerce</h2>

            <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                <button onclick="alert('Conectar Shopify')" class="p-4 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700">
                    <div class="text-2xl mb-2">🛍️</div>
                    <p class="font-semibold">Shopify</p>
                </button>
                <button onclick="alert('Conectar WooCommerce')" class="p-4 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700">
                    <div class="text-2xl mb-2">🛒</div>
                    <p class="font-semibold">WooCommerce</p>
                </button>
                <button onclick="alert('Conectar BigCommerce')" class="p-4 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700">
                    <div class="text-2xl mb-2">📦</div>
                    <p class="font-semibold">BigCommerce</p>
                </button>
                <button onclick="alert('Conectar Magento')" class="p-4 border rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700">
                    <div class="text-2xl mb-2">🏪</div>
                    <p class="font-semibold">Magento</p>
                </button>
            </div>
        </div>

        <!-- E-commerce Stats -->
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                <div class="text-3xl mb-2">💰</div>
                <h3 class="text-2xl font-bold">₲12.5M</h3>
                <p class="text-sm text-gray-600 dark:text-gray-400">Ventas del Mes</p>
            </div>
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                <div class="text-3xl mb-2">📦</div>
                <h3 class="text-2xl font-bold">145</h3>
                <p class="text-sm text-gray-600 dark:text-gray-400">Pedidos</p>
            </div>
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                <div class="text-3xl mb-2">📊</div>
                <h3 class="text-2xl font-bold">₲5.4M</h3>
                <p class="text-sm text-gray-600 dark:text-gray-400">Valor Inventario</p>
            </div>
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                <div class="text-3xl mb-2">⚠️</div>
                <h3 class="text-2xl font-bold">8</h3>
                <p class="text-sm text-gray-600 dark:text-gray-400">Stock Bajo</p>
            </div>
        </div>

        <!-- Find Suppliers -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h2 class="text-2xl font-bold mb-6">Buscar Proveedores con IA</h2>

            <form id="supplierForm" class="space-y-4">
                <div>
                    <label class="block text-sm font-medium mb-2">Nombre del Producto</label>
                    <input type="text" name="product_name" class="w-full px-4 py-2 border rounded-lg">
                </div>
                <button type="submit" class="px-6 py-3 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg font-semibold">
                    🔍 Buscar Proveedores
                </button>
            </form>
        </div>
    </div>
</div>

<script>
    document.getElementById('supplierForm').addEventListener('submit', function(e) {
        e.preventDefault();
        alert('Búsqueda de proveedores - Requiere integración con APIs');
    });
</script>
@endsection
@endif
