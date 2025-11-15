<?php

namespace App\Console\Commands;

use App\Services\TelegramService;
use Illuminate\Console\Command;

class SetupTelegramWebhooks extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'telegram:setup-webhooks {--delete : Delete webhooks instead of setting them}';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Setup or delete webhooks for all Telegram bots';

    /**
     * Execute the console command.
     */
    public function handle()
    {
        $bots = config('telegram.bots');
        $delete = $this->option('delete');

        if ($delete) {
            $this->info('Deleting all Telegram webhooks...');
        } else {
            $this->info('Setting up Telegram webhooks...');
        }

        $this->newLine();

        foreach ($bots as $botName => $botConfig) {
            if (!$botConfig['token']) {
                $this->warn("⚠️  {$botConfig['username']}: Token not configured (skipped)");
                continue;
            }

            $service = new TelegramService($botName);

            if ($delete) {
                $result = $service->deleteWebhook();
            } else {
                $result = $service->setWebhook($botConfig['webhook_url']);
            }

            if ($result['ok']) {
                if ($delete) {
                    $this->info("✅ {$botConfig['username']}: Webhook deleted");
                } else {
                    $this->info("✅ {$botConfig['username']}: Webhook set to {$botConfig['webhook_url']}");
                }
            } else {
                $this->error("❌ {$botConfig['username']}: Failed - " . ($result['description'] ?? 'Unknown error'));
            }
        }

        $this->newLine();

        if (!$delete) {
            $this->info('✨ All webhooks configured!');
            $this->newLine();
            $this->comment('You can verify webhooks with: php artisan telegram:info');
        } else {
            $this->info('✨ All webhooks deleted!');
        }
    }
}
