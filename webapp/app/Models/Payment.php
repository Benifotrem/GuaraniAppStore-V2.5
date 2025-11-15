<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Payment extends Model
{
    protected $fillable = [
        'user_id',
        'service_id',
        'subscription_id',
        'gateway',
        'transaction_id',
        'amount',
        'currency',
        'status',
        'meta',
        'completed_at',
    ];

    protected $casts = [
        'amount' => 'decimal:2',
        'meta' => 'array',
        'completed_at' => 'datetime',
    ];

    /**
     * Relaciones
     */
    public function user()
    {
        return $this->belongsTo(User::class);
    }

    public function service()
    {
        return $this->belongsTo(Service::class);
    }

    public function subscription()
    {
        return $this->belongsTo(Subscription::class);
    }
}
