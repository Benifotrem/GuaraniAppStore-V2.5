<?php

namespace App\Models;

// use Illuminate\Contracts\Auth\MustVerifyEmail;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable
{
    /** @use HasFactory<\Database\Factories\UserFactory> */
    use HasFactory, Notifiable;

    /**
     * The attributes that are mass assignable.
     *
     * @var list<string>
     */
    protected $fillable = [
        'name',
        'email',
        'password',
        'trial_ends_at',
    ];

    /**
     * The attributes that should be hidden for serialization.
     *
     * @var list<string>
     */
    protected $hidden = [
        'password',
        'remember_token',
    ];

    /**
     * Get the attributes that should be cast.
     *
     * @return array<string, string>
     */
    protected function casts(): array
    {
        return [
            'email_verified_at' => 'datetime',
            'password' => 'hashed',
            'trial_ends_at' => 'datetime',
        ];
    }

    /**
     * Relaciones
     */
    public function subscriptions()
    {
        return $this->hasMany(Subscription::class);
    }

    public function payments()
    {
        return $this->hasMany(Payment::class);
    }

    public function leads()
    {
        return $this->hasMany(Lead::class);
    }

    public function salesConversations()
    {
        return $this->hasMany(SalesConversation::class);
    }

    public function assistantTasks()
    {
        return $this->hasMany(AssistantTask::class);
    }

    public function blogPosts()
    {
        return $this->hasMany(BlogPost::class);
    }

    public function ecommerceProducts()
    {
        return $this->hasMany(EcommerceProduct::class);
    }

    public function cvAnalyses()
    {
        return $this->hasMany(CvAnalysis::class);
    }

    public function socialPosts()
    {
        return $this->hasMany(SocialPost::class);
    }

    public function invoices()
    {
        return $this->hasMany(Invoice::class);
    }

    public function appointments()
    {
        return $this->hasMany(Appointment::class);
    }

    public function cryptoTokens()
    {
        return $this->hasMany(CryptoToken::class);
    }

    public function consultancyRequests()
    {
        return $this->hasMany(ConsultancyRequest::class);
    }
}
