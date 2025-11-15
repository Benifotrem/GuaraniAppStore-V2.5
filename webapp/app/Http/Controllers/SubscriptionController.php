<?php

namespace App\Http\Controllers;

use App\Models\Service;
use App\Models\Subscription;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class SubscriptionController extends Controller
{
    /**
     * Display user's subscriptions
     */
    public function index()
    {
        $user = Auth::user();
        $subscriptions = $user->subscriptions()->with('service')->get();

        // Check trial status
        $onTrial = $user->trial_ends_at && $user->trial_ends_at->isFuture();
        $trialDaysLeft = $onTrial ? now()->diffInDays($user->trial_ends_at) : 0;

        return view('subscriptions.index', compact('subscriptions', 'onTrial', 'trialDaysLeft'));
    }

    /**
     * Subscribe to a service
     */
    public function subscribe(Request $request, $serviceSlug)
    {
        $service = Service::where('slug', $serviceSlug)->firstOrFail();
        $user = Auth::user();

        // Check if user already has an active subscription to this service
        $existingSubscription = $user->subscriptions()
            ->where('service_id', $service->id)
            ->where('status', 'active')
            ->first();

        if ($existingSubscription) {
            return redirect()->back()->with('error', 'Ya tienes una suscripción activa a este servicio.');
        }

        // Create subscription with trial if available
        $subscription = Subscription::create([
            'user_id' => $user->id,
            'service_id' => $service->id,
            'status' => 'active',
            'starts_at' => now(),
            'trial_ends_at' => $service->trial_days > 0 ? now()->addDays($service->trial_days) : null,
            'next_billing_date' => $service->trial_days > 0
                ? now()->addDays($service->trial_days)
                : now()->addMonth(),
        ]);

        return redirect()->route('subscriptions.index')
            ->with('success', 'Te has suscrito exitosamente a ' . $service->name .
                ($service->trial_days > 0 ? ' con ' . $service->trial_days . ' días de prueba gratis.' : '.'));
    }

    /**
     * Cancel a subscription
     */
    public function cancel($subscriptionId)
    {
        $subscription = Subscription::where('id', $subscriptionId)
            ->where('user_id', Auth::id())
            ->firstOrFail();

        $subscription->update([
            'status' => 'cancelled',
            'ends_at' => now(),
        ]);

        return redirect()->route('subscriptions.index')
            ->with('success', 'Tu suscripción ha sido cancelada.');
    }

    /**
     * Resume a cancelled subscription
     */
    public function resume($subscriptionId)
    {
        $subscription = Subscription::where('id', $subscriptionId)
            ->where('user_id', Auth::id())
            ->firstOrFail();

        if ($subscription->status !== 'cancelled') {
            return redirect()->back()->with('error', 'Solo puedes reactivar suscripciones canceladas.');
        }

        $subscription->update([
            'status' => 'active',
            'ends_at' => null,
            'next_billing_date' => now()->addMonth(),
        ]);

        return redirect()->route('subscriptions.index')
            ->with('success', 'Tu suscripción ha sido reactivada.');
    }
}
