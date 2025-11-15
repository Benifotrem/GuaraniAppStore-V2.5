<?php

namespace App\Http\Controllers\Admin;

use App\Http\Controllers\Controller;
use App\Models\ApiCredential;
use App\Models\Payment;
use App\Models\PaymentGateway;
use App\Models\Service;
use App\Models\Subscription;
use App\Models\User;
use Illuminate\Http\Request;

class AdminController extends Controller
{
    /**
     * Admin Dashboard
     */
    public function index()
    {
        $stats = [
            'total_users' => User::count(),
            'active_users' => User::where('is_active', true)->count(),
            'total_subscriptions' => Subscription::where('status', 'active')->count(),
            'total_revenue' => Payment::where('status', 'completed')->sum('amount'),
            'pending_payments' => Payment::where('status', 'pending')->count(),
        ];

        $recentUsers = User::latest()->take(10)->get();
        $recentPayments = Payment::with(['user', 'service'])->latest()->take(10)->get();

        return view('admin.dashboard', compact('stats', 'recentUsers', 'recentPayments'));
    }

    /**
     * Users Management
     */
    public function users()
    {
        $users = User::with('subscriptions')->latest()->paginate(20);
        return view('admin.users.index', compact('users'));
    }

    public function userEdit($id)
    {
        $user = User::with('subscriptions')->findOrFail($id);
        return view('admin.users.edit', compact('user'));
    }

    public function userUpdate(Request $request, $id)
    {
        $user = User::findOrFail($id);

        $request->validate([
            'name' => 'required|string|max:255',
            'email' => 'required|email|unique:users,email,' . $id,
            'role' => 'required|in:admin,user',
            'is_active' => 'boolean',
        ]);

        $user->update($request->only(['name', 'email', 'role', 'is_active']));

        return redirect()->route('admin.users')->with('success', 'Usuario actualizado exitosamente');
    }

    /**
     * Services Management
     */
    public function services()
    {
        $services = Service::latest()->get();
        return view('admin.services.index', compact('services'));
    }

    public function serviceEdit($id)
    {
        $service = Service::findOrFail($id);
        return view('admin.services.edit', compact('service'));
    }

    public function serviceUpdate(Request $request, $id)
    {
        $service = Service::findOrFail($id);

        $request->validate([
            'name' => 'required|string|max:255',
            'description' => 'required|string',
            'price' => 'required|numeric|min:0',
            'trial_days' => 'nullable|integer|min:0',
            'status' => 'required|in:active,coming_soon,inactive',
            'type' => 'required|in:subscription,one_time',
        ]);

        $service->update($request->only([
            'name', 'description', 'price', 'trial_days', 'status', 'type'
        ]));

        return redirect()->route('admin.services')->with('success', 'Servicio actualizado exitosamente');
    }

    /**
     * Payments Management
     */
    public function payments()
    {
        $payments = Payment::with(['user', 'service'])->latest()->paginate(30);
        return view('admin.payments.index', compact('payments'));
    }

    /**
     * Payment Gateways Management
     */
    public function gateways()
    {
        $gateways = PaymentGateway::all();
        return view('admin.gateways.index', compact('gateways'));
    }

    public function gatewayUpdate(Request $request, $id)
    {
        $gateway = PaymentGateway::findOrFail($id);

        $request->validate([
            'is_active' => 'boolean',
            'config' => 'nullable|json',
        ]);

        $gateway->update($request->only(['is_active', 'config']));

        return redirect()->route('admin.gateways')->with('success', 'Gateway actualizado');
    }

    /**
     * API Credentials Management
     */
    public function apiCredentials()
    {
        $credentials = ApiCredential::all();
        return view('admin.api-credentials.index', compact('credentials'));
    }

    public function apiCredentialEdit($id)
    {
        $credential = ApiCredential::findOrFail($id);
        return view('admin.api-credentials.edit', compact('credential'));
    }

    public function apiCredentialUpdate(Request $request, $id)
    {
        $credential = ApiCredential::findOrFail($id);

        $request->validate([
            'service_name' => 'required|string',
            'api_key' => 'nullable|string',
            'api_secret' => 'nullable|string',
            'is_active' => 'boolean',
        ]);

        $credential->update($request->only([
            'service_name', 'api_key', 'api_secret', 'is_active', 'config'
        ]));

        return redirect()->route('admin.api-credentials')->with('success', 'Credencial actualizada');
    }
}
