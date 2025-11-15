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
        Schema::create('consultancy_requests', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->onDelete('cascade');
            $table->string('company_name');
            $table->string('industry');
            $table->integer('employees_count')->nullable();
            $table->json('questionnaire_answers');
            $table->boolean('report_generated')->default(false);
            $table->string('report_file_path')->nullable();
            $table->enum('status', ['pending', 'in_progress', 'completed', 'cancelled']);
            $table->timestamp('completed_at')->nullable();
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('consultancy_requests');
    }
};
