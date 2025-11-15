<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Lead extends Model
{
    protected $fillable = [
        'user_id',
        'business_name',
        'category',
        'email',
        'phone',
        'website',
        'address',
        'city',
        'rating',
        'reviews',
        'ice_breaker_message',
        'status',
    ];

    protected $casts = [
        'rating' => 'float',
    ];

    /**
     * Relaciones
     */
    public function user()
    {
        return $this->belongsTo(User::class);
    }
}
