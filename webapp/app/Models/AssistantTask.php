<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class AssistantTask extends Model
{
    protected $fillable = [
        'user_id',
        'task_type',
        'title',
        'description',
        'due_date',
        'status',
        'metadata',
    ];

    protected $casts = [
        'due_date' => 'datetime',
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
