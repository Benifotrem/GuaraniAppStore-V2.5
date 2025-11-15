<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('payment_gateways', function (Blueprint $table) {
            $table->id();
            $table->enum('name', ['paypal', 'pagopar', 'bancard', 'crypto']);
            $table->boolean('is_active')->default(false);
            $table->boolean('is_sandbox')->default(true); // Modo sandbox/test
            $table->json('credentials')->nullable(); // Client ID, Secret, API Keys, Wallet Addresses
            $table->json('settings')->nullable(); // Configuraciones adicionales
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('payment_gateways');
    }
};
