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
        Schema::create('services', function (Blueprint $table) {
            $table->id();
            $table->string('name'); // Nombre del servicio
            $table->string('slug')->unique(); // URL amigable
            $table->text('description'); // Descripción
            $table->enum('type', ['subscription', 'one_time']); // Tipo de servicio
            $table->decimal('price', 10, 2)->default(0); // Precio en Gs
            $table->integer('trial_days')->default(0); // Días de trial
            $table->enum('status', ['active', 'coming_soon', 'inactive'])->default('active');
            $table->json('features')->nullable(); // Características del servicio
            $table->string('icon')->nullable(); // Icono del servicio
            $table->integer('sort_order')->default(0); // Orden de visualización
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('services');
    }
};
