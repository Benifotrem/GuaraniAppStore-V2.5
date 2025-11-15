@extends('layouts.app')

@section('content')
<div class="py-12">
    <div class="max-w-7xl mx-auto sm:px-6 lg:px-8">
        @if($onTrial)
        <div class="bg-yellow-100 border border-yellow-400 text-yellow-800 px-6 py-4 rounded-lg mb-6">
            <p class="font-semibold">🎁 Trial Activo - {{ $trialDaysLeft }} días restantes</p>
        </div>
        @endif

        <div class="bg-white dark:bg-gray-800 overflow-hidden shadow-sm sm:rounded-lg mb-8">
            <div class="p-6">
                <h1 class="text-3xl font-bold mb-4">{{ $service->icon }} {{ $service->name }}</h1>
                <p class="text-gray-600 dark:text-gray-400 mb-8">OCR avanzado para facturas y documentos</p>

                <!-- Upload Form -->
                <div class="bg-emerald-50 dark:bg-emerald-900 rounded-lg p-6 mb-8">
                    <h2 class="text-xl font-bold mb-4">Procesar Factura</h2>

                    <form id="invoiceUploadForm" class="space-y-4">
                        <div>
                            <label class="block text-sm font-medium mb-2">Tipo de Documento</label>
                            <select name="document_type" class="w-full px-4 py-2 border rounded-lg">
                                <option value="factura">Factura</option>
                                <option value="contrato">Contrato</option>
                                <option value="formulario">Formulario</option>
                                <option value="recibo">Recibo</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-sm font-medium mb-2">Archivo (PDF, JPG, PNG)</label>
                            <input type="file" name="invoice_file" accept=".pdf,.jpg,.jpeg,.png" required
                                   class="w-full px-4 py-2 border rounded-lg">
                        </div>
                        <button type="submit" class="px-6 py-3 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg font-semibold">
                            🧾 Procesar Documento
                        </button>
                    </form>
                </div>

                <!-- Results Section -->
                <div id="resultsSection" class="hidden bg-gray-50 dark:bg-gray-900 rounded-lg p-6 mb-8">
                    <h3 class="text-xl font-bold mb-4">Datos Extraídos</h3>
                    <div id="extractedData" class="space-y-2"></div>
                </div>

                <!-- Processing History -->
                <div class="bg-gray-50 dark:bg-gray-900 rounded-lg p-6">
                    <h3 class="text-xl font-bold mb-4">Historial de Procesamiento</h3>
                    <div class="overflow-x-auto">
                        <table class="min-w-full">
                            <thead>
                                <tr class="border-b">
                                    <th class="text-left py-2">Fecha</th>
                                    <th class="text-left py-2">Proveedor</th>
                                    <th class="text-left py-2">Total</th>
                                    <th class="text-left py-2">Estado</th>
                                </tr>
                            </thead>
                            <tbody id="historyTable">
                                <tr>
                                    <td colspan="4" class="text-center py-4 text-gray-500">No hay facturas procesadas aún</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
    document.getElementById('invoiceUploadForm').addEventListener('submit', function(e) {
        e.preventDefault();
        alert('Procesamiento de facturas - Requiere integración con OCR y IA');
    });
</script>
@endsection
