<?php

use App\Http\Controllers\Auth\GoogleAuthController;
use App\Http\Controllers\HomeController;
use App\Http\Controllers\PaymentController;
use App\Http\Controllers\ProfileController;
use App\Http\Controllers\ServiceController;
use Illuminate\Support\Facades\Route;

// Landing Page
Route::get('/', [HomeController::class, 'index'])->name('home');

// Servicios públicos
Route::get('/servicios/{slug}', [ServiceController::class, 'show'])->name('services.show');

// Google OAuth
Route::get('/auth/google', [GoogleAuthController::class, 'redirect'])->name('auth.google');
Route::get('/auth/google/callback', [GoogleAuthController::class, 'callback'])->name('auth.google.callback');

// Dashboard (requiere autenticación)
Route::get('/dashboard', function () {
    return view('dashboard');
})->middleware(['auth', 'verified'])->name('dashboard');

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

require __DIR__.'/auth.php';
