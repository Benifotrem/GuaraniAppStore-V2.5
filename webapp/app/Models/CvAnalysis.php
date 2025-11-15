<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class CvAnalysis extends Model
{
    protected $fillable = [
        'user_id',
        'candidate_name',
        'candidate_email',
        'candidate_phone',
        'cv_file_path',
        'extracted_data',
        'score',
        'recommendation',
        'strengths',
        'weaknesses',
    ];

    protected $casts = [
        'extracted_data' => 'array',
        'strengths' => 'array',
        'weaknesses' => 'array',
    ];

    /**
     * Relaciones
     */
    public function user()
    {
        return $this->belongsTo(User::class);
    }
}
