<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class ConsultancyRequest extends Model
{
    protected $fillable = [
        'user_id',
        'company_name',
        'industry',
        'employees_count',
        'questionnaire_answers',
        'report_generated',
        'report_file_path',
        'status',
        'completed_at',
    ];

    protected $casts = [
        'questionnaire_answers' => 'array',
        'report_generated' => 'boolean',
        'completed_at' => 'datetime',
    ];

    /**
     * Relaciones
     */
    public function user()
    {
        return $this->belongsTo(User::class);
    }
}
