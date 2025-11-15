<?php

namespace App\Http\Controllers;

use App\Models\Service;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class DashboardController extends Controller
{
    public function index()
    {
        $user = Auth::user();

        // Get user subscriptions
        $subscriptions = $user->subscriptions()->with('service')->where('status', 'active')->get();

        // Get available services
        $services = Service::where('status', 'active')->orderBy('sort_order')->get();

        // Get recent payments
        $recentPayments = $user->payments()->with('service')->latest()->take(5)->get();

        // Trial status
        $onTrial = $user->onTrial();
        $trialDaysLeft = $user->trialDaysRemaining();

        return view('dashboard', compact('user', 'subscriptions', 'services', 'recentPayments', 'onTrial', 'trialDaysLeft'));
    }
}
