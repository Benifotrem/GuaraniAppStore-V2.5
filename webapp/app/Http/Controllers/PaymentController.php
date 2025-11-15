<?php

namespace App\Http\Controllers;

use App\Models\Payment;
use App\Models\PaymentGateway;
use App\Models\Service;
use App\Models\Subscription;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Str;
use Srmklive\PayPal\Services\PayPal as PayPalClient;

class PaymentController extends Controller
{
    /**
     * Show payment options for a service
     */
    public function show($serviceSlug)
    {
        $service = Service::where('slug', $serviceSlug)->firstOrFail();

        // Get active payment gateways
        $gateways = PaymentGateway::where('is_active', true)->get();

        // Calculate crypto discount
        $cryptoPrice = $service->price * (1 - (config('app.crypto_discount_percent', 25) / 100));

        return view('payments.show', compact('service', 'gateways', 'cryptoPrice'));
    }

    /**
     * Process payment with selected gateway
     */
    public function process(Request $request, $serviceSlug)
    {
        $request->validate([
            'gateway' => 'required|in:paypal,pagopar,bancard,crypto',
            'currency' => 'nullable|in:PYG,USD,BTC,ETH,USDT',
        ]);

        $service = Service::where('slug', $serviceSlug)->firstOrFail();
        $gateway = $request->input('gateway');
        $currency = $request->input('currency', 'PYG');

        // Route to specific gateway handler
        switch ($gateway) {
            case 'paypal':
                return $this->processPayPal($service, $currency);
            case 'pagopar':
                return $this->processPagopar($service, $currency);
            case 'bancard':
                return $this->processBancard($service, $currency);
            case 'crypto':
                return $this->processCrypto($service, $request->input('currency', 'USDT'));
            default:
                return redirect()->back()->with('error', 'Método de pago no válido.');
        }
    }

    /**
     * Process PayPal payment
     */
    protected function processPayPal(Service $service, $currency)
    {
        try {
            $provider = new PayPalClient;
            $provider->setApiCredentials(config('paypal'));
            $paypalToken = $provider->getAccessToken();

            $amount = $currency === 'USD' ? round($service->price / 7500, 2) : $service->price; // Approx conversion

            $response = $provider->createOrder([
                "intent" => "CAPTURE",
                "application_context" => [
                    "return_url" => route('payments.paypal.success'),
                    "cancel_url" => route('payments.paypal.cancel'),
                ],
                "purchase_units" => [[
                    "reference_id" => Str::uuid(),
                    "amount" => [
                        "currency_code" => $currency,
                        "value" => $amount
                    ],
                    "description" => $service->name,
                ]]
            ]);

            if (isset($response['id']) && $response['id'] != null) {
                // Create payment record
                Payment::create([
                    'user_id' => Auth::id(),
                    'service_id' => $service->id,
                    'gateway' => 'paypal',
                    'transaction_id' => $response['id'],
                    'amount' => $amount,
                    'currency' => $currency,
                    'status' => 'pending',
                    'meta' => json_encode($response),
                ]);

                // Redirect to PayPal
                foreach ($response['links'] as $links) {
                    if ($links['rel'] == 'approve') {
                        return redirect()->away($links['href']);
                    }
                }
            }

            return redirect()->back()->with('error', 'Error al crear el pago de PayPal.');
        } catch (\Exception $e) {
            return redirect()->back()->with('error', 'Error: ' . $e->getMessage());
        }
    }

    /**
     * PayPal Success Callback
     */
    public function paypalSuccess(Request $request)
    {
        try {
            $provider = new PayPalClient;
            $provider->setApiCredentials(config('paypal'));
            $provider->getAccessToken();
            $response = $provider->capturePaymentOrder($request['token']);

            if (isset($response['status']) && $response['status'] == 'COMPLETED') {
                $payment = Payment::where('transaction_id', $request['token'])->first();

                if ($payment) {
                    $payment->update([
                        'status' => 'completed',
                        'meta' => json_encode($response),
                    ]);

                    // Create subscription
                    $this->createSubscription($payment);

                    return redirect()->route('subscriptions.index')
                        ->with('success', '¡Pago completado exitosamente! Tu suscripción está activa.');
                }
            }

            return redirect()->route('subscriptions.index')
                ->with('error', 'Error al procesar el pago.');
        } catch (\Exception $e) {
            return redirect()->route('subscriptions.index')
                ->with('error', 'Error: ' . $e->getMessage());
        }
    }

    /**
     * PayPal Cancel Callback
     */
    public function paypalCancel()
    {
        return redirect()->route('subscriptions.index')
            ->with('error', 'Pago cancelado.');
    }

    /**
     * Process Pagopar payment
     */
    protected function processPagopar(Service $service, $currency)
    {
        // Pagopar integration (Paraguay local gateway)
        $publicKey = config('payments.pagopar.public_key');
        $privateKey = config('payments.pagopar.private_key');

        $paymentData = [
            'amount' => $service->price,
            'currency' => 'PYG',
            'description' => $service->name,
            'reference' => 'SUB-' . Str::uuid(),
            'success_url' => route('payments.pagopar.success'),
            'cancel_url' => route('payments.pagopar.cancel'),
        ];

        // Create payment record
        $payment = Payment::create([
            'user_id' => Auth::id(),
            'service_id' => $service->id,
            'gateway' => 'pagopar',
            'transaction_id' => $paymentData['reference'],
            'amount' => $service->price,
            'currency' => 'PYG',
            'status' => 'pending',
            'meta' => json_encode($paymentData),
        ]);

        // In production, this would redirect to Pagopar checkout
        // For now, we'll create a form that posts to Pagopar
        return view('payments.pagopar-redirect', compact('paymentData', 'publicKey', 'payment'));
    }

    /**
     * Pagopar Success Callback
     */
    public function pagoparSuccess(Request $request)
    {
        $transactionId = $request->input('reference');
        $payment = Payment::where('transaction_id', $transactionId)->first();

        if ($payment) {
            $payment->update([
                'status' => 'completed',
                'meta' => json_encode($request->all()),
            ]);

            $this->createSubscription($payment);

            return redirect()->route('subscriptions.index')
                ->with('success', '¡Pago completado exitosamente!');
        }

        return redirect()->route('subscriptions.index')
            ->with('error', 'Error al procesar el pago.');
    }

    /**
     * Pagopar Cancel Callback
     */
    public function pagoparCancel()
    {
        return redirect()->route('subscriptions.index')
            ->with('error', 'Pago cancelado.');
    }

    /**
     * Process Bancard payment
     */
    protected function processBancard(Service $service, $currency)
    {
        // Bancard integration (Paraguay local gateway)
        $publicKey = config('payments.bancard.public_key');
        $privateKey = config('payments.bancard.private_key');

        $paymentData = [
            'amount' => $service->price,
            'currency' => 'PYG',
            'description' => $service->name,
            'reference' => 'SUB-' . Str::uuid(),
            'return_url' => route('payments.bancard.success'),
            'cancel_url' => route('payments.bancard.cancel'),
        ];

        // Create payment record
        $payment = Payment::create([
            'user_id' => Auth::id(),
            'service_id' => $service->id,
            'gateway' => 'bancard',
            'transaction_id' => $paymentData['reference'],
            'amount' => $service->price,
            'currency' => 'PYG',
            'status' => 'pending',
            'meta' => json_encode($paymentData),
        ]);

        return view('payments.bancard-redirect', compact('paymentData', 'publicKey', 'payment'));
    }

    /**
     * Bancard Success Callback
     */
    public function bancardSuccess(Request $request)
    {
        $transactionId = $request->input('reference');
        $payment = Payment::where('transaction_id', $transactionId)->first();

        if ($payment) {
            $payment->update([
                'status' => 'completed',
                'meta' => json_encode($request->all()),
            ]);

            $this->createSubscription($payment);

            return redirect()->route('subscriptions.index')
                ->with('success', '¡Pago completado exitosamente!');
        }

        return redirect()->route('subscriptions.index')
            ->with('error', 'Error al procesar el pago.');
    }

    /**
     * Bancard Cancel Callback
     */
    public function bancardCancel()
    {
        return redirect()->route('subscriptions.index')
            ->with('error', 'Pago cancelado.');
    }

    /**
     * Process Cryptocurrency payment
     */
    protected function processCrypto(Service $service, $currency)
    {
        // Apply crypto discount
        $discountPercent = config('app.crypto_discount_percent', 25);
        $amount = $service->price * (1 - ($discountPercent / 100));

        // Get wallet address based on currency
        $walletAddress = match($currency) {
            'BTC' => config('payments.crypto.wallet_btc'),
            'ETH' => config('payments.crypto.wallet_eth'),
            'USDT' => config('payments.crypto.wallet_usdt'),
            default => config('payments.crypto.wallet_usdt'),
        };

        // Convert PYG to crypto (approximate rates - should use real API)
        $cryptoAmount = match($currency) {
            'BTC' => $amount / 350000000, // ~$47k per BTC, 7500 PYG per USD
            'ETH' => $amount / 17500000,  // ~$2.3k per ETH
            'USDT' => $amount / 7500,     // 1 USDT = ~7500 PYG
            default => $amount / 7500,
        };

        // Create payment record
        $payment = Payment::create([
            'user_id' => Auth::id(),
            'service_id' => $service->id,
            'gateway' => 'crypto',
            'transaction_id' => 'CRYPTO-' . Str::uuid(),
            'amount' => $cryptoAmount,
            'currency' => $currency,
            'status' => 'pending',
            'meta' => json_encode([
                'wallet_address' => $walletAddress,
                'original_amount_pyg' => $service->price,
                'discounted_amount_pyg' => $amount,
                'discount_percent' => $discountPercent,
            ]),
        ]);

        return view('payments.crypto', compact('payment', 'walletAddress', 'cryptoAmount', 'currency', 'service', 'discountPercent'));
    }

    /**
     * Verify crypto payment (called manually or via webhook)
     */
    public function verifyCrypto(Request $request, $paymentId)
    {
        $payment = Payment::findOrFail($paymentId);

        // In production, this would verify the transaction on blockchain
        // For now, we'll allow manual confirmation
        if ($request->input('tx_hash')) {
            $payment->update([
                'status' => 'completed',
                'meta' => array_merge(
                    json_decode($payment->meta, true),
                    ['tx_hash' => $request->input('tx_hash')]
                ),
            ]);

            $this->createSubscription($payment);

            return redirect()->route('subscriptions.index')
                ->with('success', '¡Pago en criptomoneda verificado exitosamente!');
        }

        return redirect()->back()->with('error', 'Hash de transacción requerido.');
    }

    /**
     * Create subscription after successful payment
     */
    protected function createSubscription(Payment $payment)
    {
        $service = $payment->service;

        // Check if subscription already exists
        $existingSubscription = Subscription::where('user_id', $payment->user_id)
            ->where('service_id', $service->id)
            ->where('status', 'active')
            ->first();

        if (!$existingSubscription) {
            Subscription::create([
                'user_id' => $payment->user_id,
                'service_id' => $service->id,
                'payment_id' => $payment->id,
                'status' => 'active',
                'starts_at' => now(),
                'trial_ends_at' => null, // No trial for paid subscriptions
                'next_billing_date' => $service->type === 'subscription' ? now()->addMonth() : null,
            ]);
        }
    }

    /**
     * Show payment history
     */
    public function history()
    {
        $payments = Auth::user()->payments()->with('service')->latest()->get();

        return view('payments.history', compact('payments'));
    }
}
