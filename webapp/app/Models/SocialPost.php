<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class SocialPost extends Model
{
    protected $fillable = [
        'user_id',
        'platform',
        'content',
        'hashtags',
        'scheduled_for',
        'status',
        'published_at',
    ];

    protected $casts = [
        'hashtags' => 'array',
        'scheduled_for' => 'datetime',
        'published_at' => 'datetime',
    ];

    /**
     * Relaciones
     */
    public function user()
    {
        return $this->belongsTo(User::class);
    }
}
