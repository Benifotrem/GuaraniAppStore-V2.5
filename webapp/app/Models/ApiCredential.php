<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class ApiCredential extends Model
{
    protected $fillable = [
        'service_name',
        'key_name',
        'key_value',
        'is_active',
        'description',
    ];

    protected $casts = [
        'is_active' => 'boolean',
    ];

    protected $hidden = [
        'key_value',
    ];
}
