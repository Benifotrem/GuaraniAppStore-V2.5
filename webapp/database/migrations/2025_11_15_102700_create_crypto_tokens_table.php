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
        Schema::create('crypto_tokens', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->onDelete('cascade');
            $table->string('symbol');
            $table->string('name');
            $table->string('contract_address')->nullable();
            $table->enum('blockchain', ['ethereum', 'bsc', 'polygon']);
            $table->integer('fraud_score')->nullable();
            $table->integer('sentiment_score')->nullable();
            $table->enum('momentum_signal', ['buy', 'sell', 'hold'])->nullable();
            $table->json('analysis_data')->nullable();
            $table->timestamp('last_analyzed_at')->nullable();
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('crypto_tokens');
    }
};
