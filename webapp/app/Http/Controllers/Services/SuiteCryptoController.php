<?php

namespace App\Http\Controllers\Services;

use App\Http\Controllers\Controller;
use App\Models\Service;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class SuiteCryptoController extends Controller
{
    /**
     * Display the service dashboard with 3 bots
     */
    public function index()
    {
        $service = Service::where('slug', 'suite-crypto')->firstOrFail();
        $user = Auth::user();

        $hasAccess = $user->hasActiveSubscription($service->id);

        if (!$hasAccess) {
            return redirect()->route('services.show', $service->slug)
                ->with('error', 'Necesitas suscribirte a este servicio para acceder.');
        }

        $subscription = $user->subscriptions()->where('service_id', $service->id)->where('status', 'active')->first();
        $onTrial = $subscription && $subscription->isOnTrial();
        $trialDaysLeft = $onTrial ? $subscription->trialDaysRemaining() : 0;

        return view('services.suite-crypto.index', compact('service', 'user', 'onTrial', 'trialDaysLeft'));
    }

    /**
     * Connect to CryptoShield Bot (fraud detection)
     */
    public function connectCryptoShield(Request $request)
    {
        $user = Auth::user();
        $token = hash('sha256', $user->id . 'cryptoshield' . time());

        return response()->json([
            'success' => true,
            'bot_username' => '@CryptoShieldBot',
            'token' => $token,
            'features' => [
                'Detección de contratos fraudulentos',
                'Análisis de seguridad de tokens',
                'Alertas de scams y rugpulls',
                'Verificación de liquidez'
            ],
            'instructions' => "Envía /start {$token} a @CryptoShieldBot"
        ]);
    }

    /**
     * Connect to Pulse IA Bot (sentiment analysis)
     */
    public function connectPulseIA(Request $request)
    {
        $user = Auth::user();
        $token = hash('sha256', $user->id . 'pulseia' . time());

        return response()->json([
            'success' => true,
            'bot_username' => '@PulseIABot',
            'token' => $token,
            'features' => [
                'Análisis de sentimiento en redes sociales',
                'Trending topics crypto',
                'Influencers tracking',
                'Fear & Greed Index'
            ],
            'instructions' => "Envía /start {$token} a @PulseIABot"
        ]);
    }

    /**
     * Connect to Momentum Predictor Bot (trading signals)
     */
    public function connectMomentumPredictor(Request $request)
    {
        $user = Auth::user();
        $token = hash('sha256', $user->id . 'momentum' . time());

        return response()->json([
            'success' => true,
            'bot_username' => '@MomentumPredictorBot',
            'token' => $token,
            'features' => [
                'Señales de trading automáticas',
                'Análisis técnico con IA',
                'Niveles de soporte y resistencia',
                'Alertas de volumen inusual'
            ],
            'instructions' => "Envía /start {$token} a @MomentumPredictorBot"
        ]);
    }

    /**
     * Get portfolio analysis
     */
    public function getPortfolioAnalysis(Request $request)
    {
        $request->validate([
            'wallet_address' => 'nullable|string',
            'tokens' => 'nullable|array'
        ]);

        // TODO: Implement blockchain API integration (Etherscan, BSCScan, etc.)
        $analysis = [
            'total_value_usd' => 5000,
            'total_value_pyg' => 35000000,
            'risk_score' => 45,
            'diversification_score' => 72,
            'top_holdings' => [
                ['token' => 'BTC', 'value_usd' => 2000, 'percentage' => 40],
                ['token' => 'ETH', 'value_usd' => 1500, 'percentage' => 30],
                ['token' => 'BNB', 'value_usd' => 1500, 'percentage' => 30]
            ],
            'recommendations' => [
                'Considerar diversificar en stablecoins',
                'Alto riesgo en tokens de bajo market cap'
            ]
        ];

        return response()->json($analysis);
    }

    /**
     * Get market alerts
     */
    public function getAlerts()
    {
        // TODO: Fetch real-time alerts
        $alerts = [
            ['type' => 'scam', 'token' => 'FAKE', 'message' => 'Posible scam detectado', 'severity' => 'high'],
            ['type' => 'sentiment', 'token' => 'BTC', 'message' => 'Sentimiento positivo en redes', 'severity' => 'medium'],
            ['type' => 'signal', 'token' => 'ETH', 'message' => 'Señal de compra detectada', 'severity' => 'medium']
        ];

        return response()->json($alerts);
    }
}
