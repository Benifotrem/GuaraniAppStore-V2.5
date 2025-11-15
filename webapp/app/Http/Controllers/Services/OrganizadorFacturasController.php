<?php

namespace App\Http\Controllers\Services;

use App\Http\Controllers\Controller;
use App\Models\Service;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class OrganizadorFacturasController extends Controller
{
    /**
     * Display the service dashboard
     */
    public function index()
    {
        $service = Service::where('slug', 'organizador-facturas')->firstOrFail();
        $user = Auth::user();

        $hasAccess = $user->hasActiveSubscription($service->id);

        if (!$hasAccess) {
            return redirect()->route('services.show', $service->slug)
                ->with('error', 'Necesitas suscribirte a este servicio para acceder.');
        }

        $subscription = $user->subscriptions()->where('service_id', $service->id)->where('status', 'active')->first();
        $onTrial = $subscription && $subscription->isOnTrial();
        $trialDaysLeft = $onTrial ? $subscription->trialDaysRemaining() : 0;

        return view('services.organizador-facturas.index', compact('service', 'user', 'onTrial', 'trialDaysLeft'));
    }

    /**
     * Upload and process invoice
     */
    public function processInvoice(Request $request)
    {
        $request->validate([
            'invoice_file' => 'required|file|mimes:pdf,jpg,jpeg,png|max:10240',
            'document_type' => 'required|in:factura,contrato,formulario,recibo'
        ]);

        $user = Auth::user();
        $service = Service::where('slug', 'organizador-facturas')->firstOrFail();

        if (!$user->hasActiveSubscription($service->id)) {
            return response()->json(['error' => 'Suscripción inactiva'], 403);
        }

        // TODO: Implement OCR with Tesseract or Google Vision
        // TODO: Extract structured data with AI
        // TODO: Validate calculations
        $extractedData = [
            'invoice_number' => 'FAC-2025-001',
            'date' => '2025-11-15',
            'vendor' => 'Proveedor Ejemplo S.A.',
            'ruc' => '80012345-6',
            'subtotal' => 1000000,
            'iva' => 100000,
            'total' => 1100000,
            'items' => [
                ['description' => 'Servicio 1', 'quantity' => 1, 'price' => 500000],
                ['description' => 'Servicio 2', 'quantity' => 1, 'price' => 500000]
            ],
            'validation' => [
                'calculations_ok' => true,
                'iva_percentage' => 10,
                'confidence' => 95
            ]
        ];

        return response()->json([
            'success' => true,
            'data' => $extractedData,
            'message' => 'Factura procesada. Implementar OCR y validación con IA.'
        ]);
    }

    /**
     * Export invoices to Google Sheets
     */
    public function exportToSheets(Request $request)
    {
        $request->validate([
            'invoices' => 'required|array',
            'sheet_name' => 'required|string|max:255'
        ]);

        // TODO: Implement Google Sheets integration
        return response()->json([
            'success' => true,
            'message' => 'Facturas exportadas - Implementar Google Sheets API',
            'sheet_url' => 'https://docs.google.com/spreadsheets/...'
        ]);
    }

    /**
     * Get processing history
     */
    public function getHistory()
    {
        $user = Auth::user();

        // TODO: Fetch real history from database
        $history = [
            ['date' => '2025-11-15', 'vendor' => 'Proveedor 1', 'total' => 1100000, 'status' => 'processed'],
            ['date' => '2025-11-14', 'vendor' => 'Proveedor 2', 'total' => 850000, 'status' => 'processed'],
        ];

        return response()->json($history);
    }
}
