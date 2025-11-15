<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class PaymentGateway extends Model
{
    protected $fillable = [
        'name',
        'is_active',
        'is_sandbox',
        'credentials',
        'settings',
    ];

    protected $casts = [
        'is_active' => 'boolean',
        'is_sandbox' => 'boolean',
        'credentials' => 'array',
        'settings' => 'array',
    ];
}
