<?php

namespace App\Http\Controllers\Services;

use App\Http\Controllers\Controller;
use App\Models\Service;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class RupturaDelHieloController extends Controller
{
    /**
     * Display the service dashboard for Ruptura del Hielo
     */
    public function index()
    {
        $service = Service::where('slug', 'ruptura-del-hielo')->firstOrFail();
        $user = Auth::user();

        // Check if user has access
        $hasAccess = $user->hasActiveSubscription($service->id) ||
                     $user->payments()->where('service_id', $service->id)->where('status', 'completed')->exists();

        if (!$hasAccess) {
            return redirect()->route('services.show', $service->slug)
                ->with('error', 'Necesitas adquirir este servicio para acceder.');
        }

        return view('services.ruptura-del-hielo.index', compact('service', 'user'));
    }

    /**
     * Search leads in Google Maps
     */
    public function searchLeads(Request $request)
    {
        $request->validate([
            'query' => 'required|string|max:255',
            'location' => 'nullable|string|max:255',
            'radius' => 'nullable|integer|min:1|max:50'
        ]);

        $service = Service::where('slug', 'ruptura-del-hielo')->firstOrFail();
        $user = Auth::user();

        // Verify access
        if (!$user->hasActiveSubscription($service->id) &&
            !$user->payments()->where('service_id', $service->id)->where('status', 'completed')->exists()) {
            return response()->json(['error' => 'No tienes acceso a este servicio'], 403);
        }

        // TODO: Implement Google Maps API integration
        // This is a placeholder for the actual implementation
        $leads = [
            [
                'name' => 'Ejemplo Lead 1',
                'address' => 'Dirección ejemplo',
                'phone' => '+595 21 123456',
                'email' => 'ejemplo@email.com',
                'rating' => 4.5
            ]
        ];

        return response()->json([
            'success' => true,
            'leads' => $leads,
            'message' => 'Búsqueda completada. Implementar integración con Google Maps API.'
        ]);
    }

    /**
     * Generate ice breaker messages with AI
     */
    public function generateIceBreaker(Request $request)
    {
        $request->validate([
            'lead_name' => 'required|string|max:255',
            'business_type' => 'required|string|max:255',
            'context' => 'nullable|string|max:1000'
        ]);

        // TODO: Implement AI integration for message generation
        $message = "Hola {$request->lead_name}, vi que te dedicas a {$request->business_type} y me gustaría compartir contigo una solución que podría beneficiar tu negocio...";

        return response()->json([
            'success' => true,
            'message' => $message,
            'note' => 'Implementar integración con API de IA (OpenAI/Gemini)'
        ]);
    }

    /**
     * Export leads to Google Sheets
     */
    public function exportToSheets(Request $request)
    {
        $request->validate([
            'leads' => 'required|array',
            'sheet_name' => 'required|string|max:255'
        ]);

        // TODO: Implement Google Sheets API integration
        return response()->json([
            'success' => true,
            'message' => 'Export a Google Sheets - Implementar integración con Google Sheets API',
            'sheet_url' => 'https://docs.google.com/spreadsheets/...'
        ]);
    }
}
