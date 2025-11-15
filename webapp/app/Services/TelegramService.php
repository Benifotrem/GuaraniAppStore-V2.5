<?php

namespace App\Services;

use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

class TelegramService
{
    protected $botToken;
    protected $apiUrl;

    public function __construct($botName = 'support')
    {
        $botConfig = config("telegram.bots.{$botName}");
        $this->botToken = $botConfig['token'] ?? null;
        $this->apiUrl = config('telegram.api_url') . $this->botToken;
    }

    /**
     * Set webhook for the bot
     */
    public function setWebhook($webhookUrl)
    {
        if (!$this->botToken) {
            return ['ok' => false, 'error' => 'Bot token not configured'];
        }

        $response = Http::post("{$this->apiUrl}/setWebhook", [
            'url' => $webhookUrl,
            'max_connections' => config('telegram.webhook.max_connections'),
            'allowed_updates' => config('telegram.webhook.allowed_updates'),
        ]);

        Log::info("Webhook set for {$webhookUrl}", $response->json());
        return $response->json();
    }

    /**
     * Delete webhook
     */
    public function deleteWebhook()
    {
        if (!$this->botToken) {
            return ['ok' => false, 'error' => 'Bot token not configured'];
        }

        $response = Http::post("{$this->apiUrl}/deleteWebhook");
        return $response->json();
    }

    /**
     * Get webhook info
     */
    public function getWebhookInfo()
    {
        if (!$this->botToken) {
            return ['ok' => false, 'error' => 'Bot token not configured'];
        }

        $response = Http::get("{$this->apiUrl}/getWebhookInfo");
        return $response->json();
    }

    /**
     * Send message
     */
    public function sendMessage($chatId, $text, $options = [])
    {
        if (!$this->botToken) {
            return ['ok' => false, 'error' => 'Bot token not configured'];
        }

        $params = array_merge([
            'chat_id' => $chatId,
            'text' => $text,
            'parse_mode' => 'HTML',
        ], $options);

        $response = Http::post("{$this->apiUrl}/sendMessage", $params);
        return $response->json();
    }

    /**
     * Send photo
     */
    public function sendPhoto($chatId, $photo, $caption = '', $options = [])
    {
        if (!$this->botToken) {
            return ['ok' => false, 'error' => 'Bot token not configured'];
        }

        $params = array_merge([
            'chat_id' => $chatId,
            'photo' => $photo,
            'caption' => $caption,
            'parse_mode' => 'HTML',
        ], $options);

        $response = Http::post("{$this->apiUrl}/sendPhoto", $params);
        return $response->json();
    }

    /**
     * Send document
     */
    public function sendDocument($chatId, $document, $caption = '', $options = [])
    {
        if (!$this->botToken) {
            return ['ok' => false, 'error' => 'Bot token not configured'];
        }

        $params = array_merge([
            'chat_id' => $chatId,
            'document' => $document,
            'caption' => $caption,
        ], $options);

        $response = Http::post("{$this->apiUrl}/sendDocument", $params);
        return $response->json();
    }

    /**
     * Send inline keyboard
     */
    public function sendKeyboard($chatId, $text, $keyboard)
    {
        return $this->sendMessage($chatId, $text, [
            'reply_markup' => json_encode(['inline_keyboard' => $keyboard])
        ]);
    }

    /**
     * Answer callback query
     */
    public function answerCallbackQuery($callbackQueryId, $text = '', $showAlert = false)
    {
        if (!$this->botToken) {
            return ['ok' => false, 'error' => 'Bot token not configured'];
        }

        $response = Http::post("{$this->apiUrl}/answerCallbackQuery", [
            'callback_query_id' => $callbackQueryId,
            'text' => $text,
            'show_alert' => $showAlert,
        ]);

        return $response->json();
    }

    /**
     * Get bot info
     */
    public function getMe()
    {
        if (!$this->botToken) {
            return ['ok' => false, 'error' => 'Bot token not configured'];
        }

        $response = Http::get("{$this->apiUrl}/getMe");
        return $response->json();
    }

    /**
     * Get chat info
     */
    public function getChat($chatId)
    {
        if (!$this->botToken) {
            return ['ok' => false, 'error' => 'Bot token not configured'];
        }

        $response = Http::get("{$this->apiUrl}/getChat", [
            'chat_id' => $chatId
        ]);

        return $response->json();
    }

    /**
     * Extract user ID from update
     */
    public static function getUserId($update)
    {
        return $update['message']['from']['id'] ?? $update['callback_query']['from']['id'] ?? null;
    }

    /**
     * Extract chat ID from update
     */
    public static function getChatId($update)
    {
        return $update['message']['chat']['id'] ?? $update['callback_query']['message']['chat']['id'] ?? null;
    }

    /**
     * Extract message text from update
     */
    public static function getMessageText($update)
    {
        return $update['message']['text'] ?? $update['callback_query']['data'] ?? '';
    }

    /**
     * Check if message is command
     */
    public static function isCommand($text)
    {
        return strpos($text, '/') === 0;
    }

    /**
     * Extract command from text
     */
    public static function getCommand($text)
    {
        if (!self::isCommand($text)) {
            return null;
        }

        $parts = explode(' ', $text);
        return ltrim($parts[0], '/');
    }

    /**
     * Extract command arguments
     */
    public static function getCommandArgs($text)
    {
        if (!self::isCommand($text)) {
            return [];
        }

        $parts = explode(' ', $text);
        array_shift($parts); // Remove command
        return $parts;
    }
}
