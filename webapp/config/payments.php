<?php

return [

    /*
    |--------------------------------------------------------------------------
    | Payment Gateway Configurations
    |--------------------------------------------------------------------------
    |
    | Configuration for all payment gateways: PayPal, Pagopar, Bancard, Crypto
    |
    */

    'pagopar' => [
        'public_key' => env('PAGOPAR_PUBLIC_KEY'),
        'private_key' => env('PAGOPAR_PRIVATE_KEY'),
        'sandbox' => env('PAGOPAR_SANDBOX', true),
        'base_url' => env('PAGOPAR_SANDBOX', true)
            ? 'https://sandbox.pagopar.com'
            : 'https://api.pagopar.com',
    ],

    'bancard' => [
        'public_key' => env('BANCARD_PUBLIC_KEY'),
        'private_key' => env('BANCARD_PRIVATE_KEY'),
        'process_id' => env('BANCARD_PROCESS_ID'),
        'sandbox' => env('BANCARD_SANDBOX', true),
        'base_url' => env('BANCARD_SANDBOX', true)
            ? 'https://vpos.infonet.com.py:8888'
            : 'https://vpos.infonet.com.py',
    ],

    'crypto' => [
        'wallet_btc' => env('CRYPTO_WALLET_BTC'),
        'wallet_eth' => env('CRYPTO_WALLET_ETH'),
        'wallet_usdt' => env('CRYPTO_WALLET_USDT_ERC20'),
        'wallet_usdt_trc20' => env('CRYPTO_WALLET_USDT_TRC20'),

        // Optional: NOWPayments API for automatic verification
        'nowpayments_api_key' => env('NOWPAYMENTS_API_KEY'),
        'nowpayments_ipn_secret' => env('NOWPAYMENTS_IPN_SECRET'),
    ],

];
