<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class SalesConversation extends Model
{
    protected $fillable = [
        'user_id',
        'lead_name',
        'lead_email',
        'lead_phone',
        'conversation_history',
        'score',
        'status',
    ];

    protected $casts = [
        'conversation_history' => 'array',
    ];

    /**
     * Relaciones
     */
    public function user()
    {
        return $this->belongsTo(User::class);
    }
}
