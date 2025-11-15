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
        Schema::create('cv_analyses', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->onDelete('cascade');
            $table->string('candidate_name');
            $table->string('candidate_email');
            $table->string('candidate_phone')->nullable();
            $table->string('cv_file_path');
            $table->json('extracted_data');
            $table->integer('score');
            $table->enum('recommendation', ['interview', 'second_round', 'reject']);
            $table->json('strengths')->nullable();
            $table->json('weaknesses')->nullable();
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('cv_analyses');
    }
};
