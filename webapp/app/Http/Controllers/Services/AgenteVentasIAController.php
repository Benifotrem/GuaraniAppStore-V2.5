<?php

namespace App\Http\Controllers\Services;

use App\Http\Controllers\Controller;
use App\Models\Service;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class AgenteVentasIAController extends Controller
{
    /**
     * Display the service dashboard
     */
    public function index()
    {
        $service = Service::where('slug', 'agente-ventas-ia')->firstOrFail();
        $user = Auth::user();

        // Service is coming soon
        if ($service->status === 'coming_soon') {
            return view('services.coming-soon', compact('service'));
        }

        $hasAccess = $user->hasActiveSubscription($service->id);

        if (!$hasAccess) {
            return redirect()->route('services.show', $service->slug)
                ->with('error', 'Necesitas suscribirte a este servicio para acceder.');
        }

        $subscription = $user->subscriptions()->where('service_id', $service->id)->where('status', 'active')->first();
        $onTrial = $subscription && $subscription->isOnTrial();
        $trialDaysLeft = $onTrial ? $subscription->trialDaysRemaining() : 0;

        return view('services.agente-ventas-ia.index', compact('service', 'user', 'onTrial', 'trialDaysLeft'));
    }

    /**
     * Setup product catalog
     */
    public function setupCatalog(Request $request)
    {
        $request->validate([
            'products' => 'required|array|max:200',
            'products.*.name' => 'required|string|max:255',
            'products.*.description' => 'required|string|max:1000',
            'products.*.price' => 'required|numeric|min:0',
            'products.*.image_url' => 'nullable|url'
        ]);

        // TODO: Store catalog in database
        // TODO: Train AI model with product data
        return response()->json([
            'success' => true,
            'message' => 'Catálogo configurado. Entrenando bot con información de productos...'
        ]);
    }

    /**
     * Connect Telegram sales bot
     */
    public function connectTelegram(Request $request)
    {
        $user = Auth::user();
        $token = hash('sha256', $user->id . 'ventas' . time());

        return response()->json([
            'success' => true,
            'bot_username' => '@AgenteVentasIABot',
            'token' => $token,
            'instructions' => "Envía /start {$token} para activar tu agente de ventas"
        ]);
    }

    /**
     * Get sales statistics
     */
    public function getSalesStats()
    {
        $user = Auth::user();

        // TODO: Fetch real statistics
        $stats = [
            'total_conversations' => 156,
            'qualified_leads' => 45,
            'conversions' => 12,
            'conversion_rate' => 7.7,
            'average_response_time' => 2.5
        ];

        return response()->json($stats);
    }

    /**
     * Get conversation history
     */
    public function getConversations()
    {
        // TODO: Fetch from database
        $conversations = [
            ['client' => 'Cliente 1', 'status' => 'qualified', 'score' => 85, 'last_message' => '2025-11-15 10:30'],
            ['client' => 'Cliente 2', 'status' => 'in_progress', 'score' => 65, 'last_message' => '2025-11-15 11:00']
        ];

        return response()->json($conversations);
    }
}
