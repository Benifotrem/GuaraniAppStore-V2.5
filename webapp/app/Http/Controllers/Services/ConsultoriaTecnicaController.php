<?php

namespace App\Http\Controllers\Services;

use App\Http\Controllers\Controller;
use App\Models\Service;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class ConsultoriaTecnicaController extends Controller
{
    /**
     * Display the service dashboard
     */
    public function index()
    {
        $service = Service::where('slug', 'consultoria-tecnica')->firstOrFail();
        $user = Auth::user();

        $hasAccess = $user->hasActiveSubscription($service->id) ||
                     $user->payments()->where('service_id', $service->id)->where('status', 'completed')->exists();

        if (!$hasAccess) {
            return redirect()->route('services.show', $service->slug)
                ->with('error', 'Necesitas adquirir este servicio para acceder.');
        }

        return view('services.consultoria-tecnica.index', compact('service', 'user'));
    }

    /**
     * Submit company information for analysis
     */
    public function submitCompanyInfo(Request $request)
    {
        $request->validate([
            'company_name' => 'required|string|max:255',
            'industry' => 'required|string|max:255',
            'employees' => 'required|integer|min:1',
            'current_processes' => 'required|string|max:5000',
            'pain_points' => 'required|string|max:5000',
            'tech_stack' => 'nullable|string|max:2000',
            'budget_range' => 'nullable|string|max:100'
        ]);

        $user = Auth::user();

        // TODO: Store submission in database
        // TODO: Schedule consultation session
        // TODO: Send confirmation email

        return response()->json([
            'success' => true,
            'message' => 'Información recibida. Te contactaremos en 24-48 horas para agendar la sesión de consultoría.',
            'next_steps' => [
                'Análisis inicial de procesos',
                'Preparación de roadmap',
                'Sesión de 60 minutos vía Zoom',
                'Entrega de documento estratégico'
            ]
        ]);
    }

    /**
     * Schedule consultation session
     */
    public function scheduleSession(Request $request)
    {
        $request->validate([
            'preferred_date' => 'required|date|after:today',
            'preferred_time' => 'required|string',
            'timezone' => 'required|string'
        ]);

        // TODO: Integrate with Google Calendar
        // TODO: Send calendar invites
        return response()->json([
            'success' => true,
            'message' => 'Sesión agendada exitosamente. Recibirás invitación por email.'
        ]);
    }

    /**
     * Download strategic document
     */
    public function downloadDocument($documentId)
    {
        // TODO: Implement document generation and download
        return response()->json([
            'message' => 'Documento en preparación. Implementar generación de PDF.'
        ]);
    }
}
