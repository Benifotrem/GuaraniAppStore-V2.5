<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Appointment extends Model
{
    protected $fillable = [
        'user_id',
        'client_name',
        'client_email',
        'client_phone',
        'appointment_date',
        'duration_minutes',
        'status',
        'notes',
        'reminder_sent',
    ];

    protected $casts = [
        'appointment_date' => 'datetime',
        'reminder_sent' => 'boolean',
    ];

    /**
     * Relaciones
     */
    public function user()
    {
        return $this->belongsTo(User::class);
    }
}
