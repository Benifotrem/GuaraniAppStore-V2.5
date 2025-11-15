<?php

use App\Http\Controllers\Auth\GoogleAuthController;
use App\Http\Controllers\DashboardController;
use App\Http\Controllers\HomeController;
use App\Http\Controllers\LegalController;
use App\Http\Controllers\PaymentController;
use App\Http\Controllers\ProfileController;
use App\Http\Controllers\ServiceController;
use App\Http\Controllers\SitemapController;
use Illuminate\Support\Facades\Route;

// Landing Page
Route::get('/', [HomeController::class, 'index'])->name('home');

// Servicios públicos
Route::get('/servicios/{slug}', [ServiceController::class, 'show'])->name('services.show');

// Google OAuth
Route::get('/auth/google', [GoogleAuthController::class, 'redirect'])->name('auth.google');
Route::get('/auth/google/callback', [GoogleAuthController::class, 'callback'])->name('auth.google.callback');

// Dashboard (requiere autenticación)
Route::get('/dashboard', [DashboardController::class, 'index'])->middleware(['auth', 'verified'])->name('dashboard');

// Perfil de usuario
Route::middleware('auth')->group(function () {
    Route::get('/profile', [ProfileController::class, 'edit'])->name('profile.edit');
    Route::patch('/profile', [ProfileController::class, 'update'])->name('profile.update');
    Route::delete('/profile', [ProfileController::class, 'destroy'])->name('profile.destroy');

    // Subscriptions
    Route::get('/subscriptions', [\App\Http\Controllers\SubscriptionController::class, 'index'])->name('subscriptions.index');
    Route::post('/subscriptions/{serviceSlug}', [\App\Http\Controllers\SubscriptionController::class, 'subscribe'])->name('subscriptions.subscribe');
    Route::post('/subscriptions/{subscriptionId}/cancel', [\App\Http\Controllers\SubscriptionController::class, 'cancel'])->name('subscriptions.cancel');
    Route::post('/subscriptions/{subscriptionId}/resume', [\App\Http\Controllers\SubscriptionController::class, 'resume'])->name('subscriptions.resume');

    // Payments
    Route::get('/payments/{serviceSlug}', [PaymentController::class, 'show'])->name('payments.show');
    Route::post('/payments/{serviceSlug}/process', [PaymentController::class, 'process'])->name('payments.process');
    Route::get('/payments/history', [PaymentController::class, 'history'])->name('payments.history');

    // Crypto Payments
    Route::post('/payments/{paymentId}/crypto/verify', [PaymentController::class, 'verifyCrypto'])->name('payments.crypto.verify');
});

// Payment Gateway Callbacks (public routes)
Route::get('/payments/paypal/success', [PaymentController::class, 'paypalSuccess'])->name('payments.paypal.success');
Route::get('/payments/paypal/cancel', [PaymentController::class, 'paypalCancel'])->name('payments.paypal.cancel');

Route::get('/payments/pagopar/success', [PaymentController::class, 'pagoparSuccess'])->name('payments.pagopar.success');
Route::get('/payments/pagopar/cancel', [PaymentController::class, 'pagoparCancel'])->name('payments.pagopar.cancel');

Route::get('/payments/bancard/success', [PaymentController::class, 'bancardSuccess'])->name('payments.bancard.success');
Route::get('/payments/bancard/cancel', [PaymentController::class, 'bancardCancel'])->name('payments.bancard.cancel');

// Admin Routes (protected by admin middleware)
Route::middleware(['auth', 'admin'])->prefix('admin')->name('admin.')->group(function () {
    Route::get('/', [\App\Http\Controllers\Admin\AdminController::class, 'index'])->name('dashboard');

    // Users Management
    Route::get('/users', [\App\Http\Controllers\Admin\AdminController::class, 'users'])->name('users');
    Route::get('/users/{id}/edit', [\App\Http\Controllers\Admin\AdminController::class, 'userEdit'])->name('users.edit');
    Route::put('/users/{id}', [\App\Http\Controllers\Admin\AdminController::class, 'userUpdate'])->name('users.update');

    // Services Management
    Route::get('/services', [\App\Http\Controllers\Admin\AdminController::class, 'services'])->name('services');
    Route::get('/services/{id}/edit', [\App\Http\Controllers\Admin\AdminController::class, 'serviceEdit'])->name('services.edit');
    Route::put('/services/{id}', [\App\Http\Controllers\Admin\AdminController::class, 'serviceUpdate'])->name('services.update');

    // Payments Management
    Route::get('/payments', [\App\Http\Controllers\Admin\AdminController::class, 'payments'])->name('payments');

    // Payment Gateways
    Route::get('/gateways', [\App\Http\Controllers\Admin\AdminController::class, 'gateways'])->name('gateways');
    Route::put('/gateways/{id}', [\App\Http\Controllers\Admin\AdminController::class, 'gatewayUpdate'])->name('gateways.update');

    // API Credentials
    Route::get('/api-credentials', [\App\Http\Controllers\Admin\AdminController::class, 'apiCredentials'])->name('api-credentials');
    Route::get('/api-credentials/{id}/edit', [\App\Http\Controllers\Admin\AdminController::class, 'apiCredentialEdit'])->name('api-credentials.edit');
    Route::put('/api-credentials/{id}', [\App\Http\Controllers\Admin\AdminController::class, 'apiCredentialUpdate'])->name('api-credentials.update');
});

// Legal Pages
Route::get('/faq', [LegalController::class, 'faq'])->name('faq');
Route::get('/terms', [LegalController::class, 'terms'])->name('terms');
Route::get('/privacy', [LegalController::class, 'privacy'])->name('privacy');

// SEO
Route::get('/sitemap.xml', [SitemapController::class, 'index'])->name('sitemap');

// Telegram Webhooks (public routes)
Route::post('/telegram/webhook/asistente-personal', [\App\Http\Controllers\TelegramWebhookController::class, 'asistentePersonal'])->name('telegram.asistente');
Route::post('/telegram/webhook/organizador-agenda', [\App\Http\Controllers\TelegramWebhookController::class, 'organizadorAgenda'])->name('telegram.agenda');
Route::post('/telegram/webhook/cryptoshield', [\App\Http\Controllers\TelegramWebhookController::class, 'cryptoShield'])->name('telegram.cryptoshield');
Route::post('/telegram/webhook/pulse-ia', [\App\Http\Controllers\TelegramWebhookController::class, 'pulseIA'])->name('telegram.pulseia');
Route::post('/telegram/webhook/momentum-predictor', [\App\Http\Controllers\TelegramWebhookController::class, 'momentumPredictor'])->name('telegram.momentum');
Route::post('/telegram/webhook/agente-ventas', [\App\Http\Controllers\TelegramWebhookController::class, 'agenteVentas'])->name('telegram.ventas');
Route::post('/telegram/webhook/support', [\App\Http\Controllers\TelegramWebhookController::class, 'supportBot'])->name('telegram.support');

require __DIR__.'/auth.php';
