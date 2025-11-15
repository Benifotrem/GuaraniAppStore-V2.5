<?php

return [
    /*
    |--------------------------------------------------------------------------
    | Telegram Bots Configuration
    |--------------------------------------------------------------------------
    |
    | Configuration for the 7 Telegram bots used in the platform
    | Get bot tokens from @BotFather on Telegram
    |
    */

    'bots' => [
        // Bot 1: Agente de Ventas IA
        'sales' => [
            'token' => env('TELEGRAM_BOT_SALES_TOKEN'),
            'username' => '@AgenteVentasIABot',
            'webhook_url' => env('APP_URL') . '/telegram/webhook/agente-ventas',
            'description' => 'Chatbot de ventas 24/7 con IA'
        ],

        // Bot 2: Asistente Personal para Directivos
        'assistant' => [
            'token' => env('TELEGRAM_BOT_ASSISTANT_TOKEN'),
            'username' => '@AsistentePersonalBot',
            'webhook_url' => env('APP_URL') . '/telegram/webhook/asistente-personal',
            'description' => 'Asistente ejecutivo para gestión de agenda y finanzas'
        ],

        // Bot 3: CryptoShield (Detección de fraudes)
        'cryptoshield' => [
            'token' => env('TELEGRAM_BOT_CRYPTOSHIELD_TOKEN'),
            'username' => '@CryptoShieldBot',
            'webhook_url' => env('APP_URL') . '/telegram/webhook/cryptoshield',
            'description' => 'Detección de fraudes y scams en criptomonedas'
        ],

        // Bot 4: Pulse IA (Análisis de sentimiento)
        'pulse' => [
            'token' => env('TELEGRAM_BOT_PULSE_TOKEN'),
            'username' => '@PulseIABot',
            'webhook_url' => env('APP_URL') . '/telegram/webhook/pulse-ia',
            'description' => 'Análisis de sentimiento crypto en redes sociales'
        ],

        // Bot 5: Momentum Predictor (Señales de trading)
        'momentum' => [
            'token' => env('TELEGRAM_BOT_MOMENTUM_TOKEN'),
            'username' => '@MomentumPredictorBot',
            'webhook_url' => env('APP_URL') . '/telegram/webhook/momentum-predictor',
            'description' => 'Señales de trading y análisis técnico con IA'
        ],

        // Bot 6: Organizador de Agenda
        'agenda' => [
            'token' => env('TELEGRAM_BOT_AGENDA_TOKEN'),
            'username' => '@OrganizadorAgendaBot',
            'webhook_url' => env('APP_URL') . '/telegram/webhook/organizador-agenda',
            'description' => 'Recordatorios de citas y agendamiento'
        ],

        // Bot 7: Support Bot (General notifications and support)
        'support' => [
            'token' => env('TELEGRAM_BOT_SOCIAL_TOKEN'),
            'username' => '@GuaraniSupportBot',
            'webhook_url' => env('APP_URL') . '/telegram/webhook/support',
            'description' => 'Soporte y notificaciones generales'
        ],
    ],

    /*
    |--------------------------------------------------------------------------
    | Telegram API Base URL
    |--------------------------------------------------------------------------
    */
    'api_url' => 'https://api.telegram.org/bot',

    /*
    |--------------------------------------------------------------------------
    | Webhook Configuration
    |--------------------------------------------------------------------------
    */
    'webhook' => [
        'max_connections' => 100,
        'allowed_updates' => ['message', 'callback_query', 'inline_query'],
    ],
];
