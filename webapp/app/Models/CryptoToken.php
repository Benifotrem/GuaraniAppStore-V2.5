<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class CryptoToken extends Model
{
    protected $fillable = [
        'user_id',
        'symbol',
        'name',
        'contract_address',
        'blockchain',
        'fraud_score',
        'sentiment_score',
        'momentum_signal',
        'analysis_data',
        'last_analyzed_at',
    ];

    protected $casts = [
        'analysis_data' => 'array',
        'last_analyzed_at' => 'datetime',
    ];

    /**
     * Relaciones
     */
    public function user()
    {
        return $this->belongsTo(User::class);
    }
}
