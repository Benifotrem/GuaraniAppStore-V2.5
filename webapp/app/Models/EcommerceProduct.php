<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class EcommerceProduct extends Model
{
    protected $fillable = [
        'user_id',
        'name',
        'sku',
        'description',
        'price',
        'stock',
        'images',
        'status',
        'metadata',
    ];

    protected $casts = [
        'price' => 'decimal:2',
        'images' => 'array',
        'metadata' => 'array',
    ];

    /**
     * Relaciones
     */
    public function user()
    {
        return $this->belongsTo(User::class);
    }
}
