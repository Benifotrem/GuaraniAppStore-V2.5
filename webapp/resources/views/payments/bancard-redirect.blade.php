<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Redirigiendo a Bancard...</title>
    @vite(['resources/css/app.css'])
</head>
<body class="bg-gray-100">
    <div class="min-h-screen flex items-center justify-center">
        <div class="bg-white rounded-2xl p-8 max-w-md w-full mx-4 text-center">
            <div class="mb-6">
                <div class="animate-spin rounded-full h-16 w-16 border-b-4 border-red-500 mx-auto"></div>
            </div>
            <h2 class="text-2xl font-bold text-gray-900 mb-2">Redirigiendo a Bancard VPOS</h2>
            <p class="text-gray-600 mb-6">Por favor espera mientras te redirigimos al procesador de pagos seguro...</p>

            <form id="bancardForm" action="{{ config('payments.bancard.base_url') }}/vpos/api/0.3/single_buy" method="POST">
                <input type="hidden" name="public_key" value="{{ $publicKey }}">
                <input type="hidden" name="operation" value="{{ json_encode([
                    'token' => $paymentData['reference'],
                    'amount' => $paymentData['amount'],
                    'currency' => $paymentData['currency'],
                    'description' => $paymentData['description'],
                    'return_url' => $paymentData['return_url'],
                    'cancel_url' => $paymentData['cancel_url'],
                ]) }}">
            </form>

            <p class="text-sm text-gray-500 mt-4">
                Si no eres redirigido automáticamente,
                <button onclick="document.getElementById('bancardForm').submit()" class="text-red-600 hover:underline font-semibold">
                    haz clic aquí
                </button>
            </p>
        </div>
    </div>

    <script>
        // Auto-submit form after 2 seconds
        setTimeout(function() {
            document.getElementById('bancardForm').submit();
        }, 2000);
    </script>
</body>
</html>
