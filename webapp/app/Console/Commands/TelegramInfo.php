<?php

namespace App\Console\Commands;

use App\Services\TelegramService;
use Illuminate\Console\Command;

class TelegramInfo extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'telegram:info {bot? : Bot name to check (leave empty for all)}';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Get information about Telegram bots and webhooks';

    /**
     * Execute the console command.
     */
    public function handle()
    {
        $botName = $this->argument('bot');

        if ($botName) {
            $this->showBotInfo($botName);
        } else {
            $this->showAllBotsInfo();
        }
    }

    /**
     * Show information for all bots
     */
    protected function showAllBotsInfo()
    {
        $bots = config('telegram.bots');

        $this->info('📱 Telegram Bots Status');
        $this->newLine();

        foreach ($bots as $botName => $botConfig) {
            if (!$botConfig['token']) {
                $this->warn("⚠️  {$botConfig['username']}: Token not configured");
                continue;
            }

            $service = new TelegramService($botName);

            // Get bot info
            $botInfo = $service->getMe();
            if (!$botInfo['ok']) {
                $this->error("❌ {$botConfig['username']}: Invalid token");
                continue;
            }

            $bot = $botInfo['result'];

            // Get webhook info
            $webhookInfo = $service->getWebhookInfo();
            $webhook = $webhookInfo['result'] ?? [];

            $this->line("✅ <fg=green>{$bot['username']}</> (@{$bot['username']})");
            $this->line("   Bot ID: {$bot['id']}");
            $this->line("   Name: {$bot['first_name']}");

            if (!empty($webhook['url'])) {
                $this->line("   Webhook: <fg=green>{$webhook['url']}</>");
                $this->line("   Pending updates: " . ($webhook['pending_update_count'] ?? 0));

                if (isset($webhook['last_error_date'])) {
                    $this->line("   <fg=red>Last error: {$webhook['last_error_message']}</>");
                }
            } else {
                $this->line("   Webhook: <fg=yellow>Not set</>");
            }

            $this->newLine();
        }
    }

    /**
     * Show information for a specific bot
     */
    protected function showBotInfo($botName)
    {
        $botConfig = config("telegram.bots.{$botName}");

        if (!$botConfig) {
            $this->error("Bot '{$botName}' not found in configuration");
            $this->comment("Available bots: " . implode(', ', array_keys(config('telegram.bots'))));
            return;
        }

        if (!$botConfig['token']) {
            $this->error("Token not configured for {$botConfig['username']}");
            return;
        }

        $service = new TelegramService($botName);

        // Get bot info
        $botInfo = $service->getMe();
        if (!$botInfo['ok']) {
            $this->error("Invalid token for {$botConfig['username']}");
            return;
        }

        $bot = $botInfo['result'];

        // Get webhook info
        $webhookInfo = $service->getWebhookInfo();
        $webhook = $webhookInfo['result'] ?? [];

        $this->info("📱 Bot Information:");
        $this->newLine();

        $this->table(
            ['Property', 'Value'],
            [
                ['ID', $bot['id']],
                ['Username', '@' . $bot['username']],
                ['Name', $bot['first_name']],
                ['Can Join Groups', $bot['can_join_groups'] ? 'Yes' : 'No'],
                ['Can Read Messages', $bot['can_read_all_group_messages'] ? 'Yes' : 'No'],
            ]
        );

        $this->info("🔗 Webhook Information:");
        $this->newLine();

        if (!empty($webhook['url'])) {
            $this->table(
                ['Property', 'Value'],
                [
                    ['URL', $webhook['url']],
                    ['Pending Updates', $webhook['pending_update_count'] ?? 0],
                    ['Max Connections', $webhook['max_connections'] ?? 'N/A'],
                    ['Last Error Date', isset($webhook['last_error_date']) ? date('Y-m-d H:i:s', $webhook['last_error_date']) : 'None'],
                    ['Last Error Message', $webhook['last_error_message'] ?? 'None'],
                ]
            );
        } else {
            $this->warn('Webhook is not configured for this bot');
            $this->comment("Run: php artisan telegram:setup-webhooks");
        }
    }
}
