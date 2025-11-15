<?php

namespace App\Http\Controllers\Services;

use App\Http\Controllers\Controller;
use App\Models\Service;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class OrganizadorAgendaController extends Controller
{
    /**
     * Display the service dashboard
     */
    public function index()
    {
        $service = Service::where('slug', 'organizador-agenda')->firstOrFail();
        $user = Auth::user();

        $hasAccess = $user->hasActiveSubscription($service->id);

        if (!$hasAccess) {
            return redirect()->route('services.show', $service->slug)
                ->with('error', 'Necesitas suscribirte a este servicio para acceder.');
        }

        $subscription = $user->subscriptions()->where('service_id', $service->id)->where('status', 'active')->first();
        $onTrial = $subscription && $subscription->isOnTrial();
        $trialDaysLeft = $onTrial ? $subscription->trialDaysRemaining() : 0;

        return view('services.organizador-agenda.index', compact('service', 'user', 'onTrial', 'trialDaysLeft'));
    }

    /**
     * Create appointment
     */
    public function createAppointment(Request $request)
    {
        $request->validate([
            'title' => 'required|string|max:255',
            'date' => 'required|date|after:now',
            'duration' => 'required|integer|min:15|max:480',
            'client_name' => 'required|string|max:255',
            'client_email' => 'nullable|email',
            'client_phone' => 'nullable|string|max:20',
            'notes' => 'nullable|string|max:1000'
        ]);

        $user = Auth::user();

        // TODO: Store appointment in database
        // TODO: Sync with Google Calendar
        // TODO: Send Telegram reminder

        return response()->json([
            'success' => true,
            'appointment_id' => 'APT-' . time(),
            'message' => 'Cita creada exitosamente. Se enviará recordatorio vía Telegram.'
        ]);
    }

    /**
     * Get appointments
     */
    public function getAppointments(Request $request)
    {
        $user = Auth::user();
        $start = $request->input('start_date', now()->startOfMonth());
        $end = $request->input('end_date', now()->endOfMonth());

        // TODO: Fetch from database
        $appointments = [
            [
                'id' => 'APT-001',
                'title' => 'Reunión con Cliente',
                'date' => '2025-11-16 10:00:00',
                'duration' => 60,
                'client_name' => 'Juan Pérez',
                'status' => 'confirmed'
            ]
        ];

        return response()->json($appointments);
    }

    /**
     * Connect Telegram for reminders
     */
    public function connectTelegram(Request $request)
    {
        $user = Auth::user();
        $token = hash('sha256', $user->id . 'agenda' . time());

        return response()->json([
            'success' => true,
            'bot_username' => '@OrganizadorAgendaBot',
            'token' => $token,
            'instructions' => "Envía /start {$token} al bot para recibir recordatorios"
        ]);
    }

    /**
     * Sync with Google Calendar
     */
    public function syncGoogleCalendar(Request $request)
    {
        // TODO: Implement Google Calendar OAuth
        return response()->json([
            'success' => true,
            'message' => 'Implementar sincronización con Google Calendar'
        ]);
    }
}
