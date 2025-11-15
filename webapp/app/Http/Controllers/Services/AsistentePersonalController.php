<?php

namespace App\Http\Controllers\Services;

use App\Http\Controllers\Controller;
use App\Models\Service;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class AsistentePersonalController extends Controller
{
    /**
     * Display the service dashboard
     */
    public function index()
    {
        $service = Service::where('slug', 'asistente-personal')->firstOrFail();
        $user = Auth::user();

        $hasAccess = $user->hasActiveSubscription($service->id);

        if (!$hasAccess) {
            return redirect()->route('services.show', $service->slug)
                ->with('error', 'Necesitas suscribirte a este servicio para acceder.');
        }

        // Check trial status
        $subscription = $user->subscriptions()->where('service_id', $service->id)->where('status', 'active')->first();
        $onTrial = $subscription && $subscription->isOnTrial();
        $trialDaysLeft = $onTrial ? $subscription->trialDaysRemaining() : 0;

        return view('services.asistente-personal.index', compact('service', 'user', 'onTrial', 'trialDaysLeft'));
    }

    /**
     * Connect Telegram bot
     */
    public function connectTelegram(Request $request)
    {
        $user = Auth::user();

        // Generate unique token for this user
        $token = hash('sha256', $user->id . time() . config('app.key'));

        // TODO: Store token in user_service_configs table
        // TODO: Send instructions via Telegram bot

        return response()->json([
            'success' => true,
            'bot_username' => '@AsistentePersonalBot',
            'token' => $token,
            'instructions' => "1. Abre Telegram y busca @AsistentePersonalBot\n2. Envía el comando: /start {$token}\n3. El bot confirmará la conexión"
        ]);
    }

    /**
     * Sync Google Calendar
     */
    public function syncGoogleCalendar(Request $request)
    {
        // TODO: Implement Google Calendar OAuth flow
        // TODO: Store calendar credentials
        return response()->json([
            'success' => true,
            'message' => 'Implementar OAuth de Google Calendar'
        ]);
    }

    /**
     * Get assistant statistics
     */
    public function getStats()
    {
        $user = Auth::user();

        // TODO: Fetch real statistics from database
        $stats = [
            'tasks_completed' => 45,
            'calendar_events' => 12,
            'searches_performed' => 28,
            'financial_entries' => 34,
            'active_days' => 15
        ];

        return response()->json($stats);
    }
}
