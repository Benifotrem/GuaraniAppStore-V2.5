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
        'google_id',
        'role',
        'is_active',
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

    /**
     * Helper Methods
     */

    /**
     * Check if user is on trial
     */
    public function onTrial(): bool
    {
        return $this->trial_ends_at && $this->trial_ends_at->isFuture();
    }

    /**
     * Get trial days remaining
     */
    public function trialDaysRemaining(): int
    {
        if (!$this->onTrial()) {
            return 0;
        }

        return now()->diffInDays($this->trial_ends_at);
    }

    /**
     * Check if user has active subscription to a service
     */
    public function hasActiveSubscription($serviceSlug): bool
    {
        return $this->subscriptions()
            ->whereHas('service', function ($query) use ($serviceSlug) {
                $query->where('slug', $serviceSlug);
            })
            ->where('status', 'active')
            ->exists();
    }

    /**
     * Check if user is admin
     */
    public function isAdmin(): bool
    {
        return $this->role === 'admin';
    }

    /**
     * Check if user can access a service (has subscription or on trial)
     */
    public function canAccessService($serviceSlug): bool
    {
        return $this->onTrial() || $this->hasActiveSubscription($serviceSlug);
    }
}
