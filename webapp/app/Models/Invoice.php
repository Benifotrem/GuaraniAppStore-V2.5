<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Invoice extends Model
{
    protected $fillable = [
        'user_id',
        'invoice_number',
        'date',
        'vendor_name',
        'vendor_ruc',
        'client_name',
        'client_ruc',
        'items',
        'subtotal',
        'tax',
        'total',
        'currency',
        'file_path',
        'extracted_data',
    ];

    protected $casts = [
        'date' => 'date',
        'items' => 'array',
        'subtotal' => 'decimal:2',
        'tax' => 'decimal:2',
        'total' => 'decimal:2',
        'extracted_data' => 'array',
    ];

    /**
     * Relaciones
     */
    public function user()
    {
        return $this->belongsTo(User::class);
    }
}
