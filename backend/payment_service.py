"""
Payment Service - Pagopar and Crypto integrations
"""
import os
import httpx
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, Optional

# Pagopar credentials
PAGOPAR_PUBLIC_KEY = os.environ.get('PAGOPAR_PUBLIC_KEY')
PAGOPAR_PRIVATE_KEY = os.environ.get('PAGOPAR_PRIVATE_KEY')
PAGOPAR_ENV = os.environ.get('PAGOPAR_ENV', 'sandbox')
PAGOPAR_SANDBOX_URL = os.environ.get('PAGOPAR_SANDBOX_URL', 'https://sandbox.pagopar.com')
PAGOPAR_PRODUCTION_URL = os.environ.get('PAGOPAR_PRODUCTION_URL', 'https://api.pagopar.com')

# Crypto wallets
BTC_WALLET = os.environ.get('BTC_WALLET')
ETH_WALLET = os.environ.get('ETH_WALLET')
USDT_ETH_WALLET = os.environ.get('USDT_ETH_WALLET')  # USDT ERC-20 on Ethereum network

# Backend URL for callbacks
BACKEND_URL = os.environ.get('REACT_APP_BACKEND_URL', 'http://localhost:8001')

def get_pagopar_url() -> str:
    """Get Pagopar API URL based on environment"""
    return PAGOPAR_SANDBOX_URL if PAGOPAR_ENV == 'sandbox' else PAGOPAR_PRODUCTION_URL

def calculate_price_with_discount(base_price: float, platform: Optional[str], payment_method: str) -> tuple[float, float]:
    """
    Calculate final price with discounts
    Returns: (final_price, discount_percentage)
    """
    discount = 0.0
    
    # Telegram discount (20%)
    if platform == 'telegram':
        discount += 20.0
    
    # Crypto discount (25%) - ONLY BTC and ETH, NOT USDT
    if payment_method in ['btc', 'eth']:
        discount += 25.0
    
    # Apply discount
    final_price = base_price * (1 - discount / 100)
    
    return final_price, discount

def generate_order_number() -> str:
    """Generate unique order number"""
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    random = secrets.token_hex(3).upper()
    return f'ORD-{timestamp}-{random}'

async def create_pagopar_payment(
    order_id: str,
    amount: float,
    description: str,
    user_email: str
) -> Dict:
    """
    Create payment with Pagopar
    """
    try:
        url = f'{get_pagopar_url()}/api/v2/payment'
        
        # Prepare payment data
        payload = {
            'public_key': PAGOPAR_PUBLIC_KEY,
            'amount': int(amount),  # Pagopar expects amount in guaraníes (integer)
            'currency': 'PYG',
            'description': description,
            'external_reference': order_id,
            'email': user_email,
            'callback_url': f'{BACKEND_URL}/api/payments/pagopar/webhook',
            'success_url': f'{BACKEND_URL}/api/payments/success',
            'cancel_url': f'{BACKEND_URL}/api/payments/cancel'
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'payment_id': data.get('id'),
                    'payment_url': data.get('payment_url'),
                    'expires_at': datetime.utcnow() + timedelta(hours=24)
                }
            else:
                return {
                    'success': False,
                    'error': f'Pagopar error: {response.text}'
                }
    
    except Exception as e:
        return {
            'success': False,
            'error': f'Error creating Pagopar payment: {str(e)}'
        }

def get_crypto_wallet(payment_method: str) -> Optional[str]:
    """Get crypto wallet address for payment method"""
    wallets = {
        'btc': BTC_WALLET,
        'eth': ETH_WALLET,
        'usdt': USDT_ETH_WALLET  # USDT ERC-20 on Ethereum
    }
    return wallets.get(payment_method)

async def verify_crypto_payment(
    payment_method: str,
    tx_hash: str,
    expected_amount: float,
    wallet_address: str
) -> Dict:
    """
    Verify crypto payment on blockchain
    This is a simplified version - real implementation would use blockchain APIs
    """
    # TODO: Implement actual blockchain verification
    # For now, return a mock response
    
    # In production, you would:
    # 1. Query blockchain explorer API (Etherscan, Blockchain.com, etc.)
    # 2. Verify transaction exists
    # 3. Check recipient address matches
    # 4. Verify amount is correct
    # 5. Check number of confirmations
    
    return {
        'success': True,
        'verified': False,  # Set to True once real verification is implemented
        'confirmations': 0,
        'amount': 0,
        'message': 'Manual verification required - blockchain integration pending'
    }

def convert_pyg_to_crypto(amount_pyg: float, crypto: str) -> float:
    """
    Convert PYG to crypto amount
    This should use real-time exchange rates in production
    """
    # Mock conversion rates (these should be fetched from an API in production)
    # Using approximate rates as of late 2024
    rates = {
        'btc': 0.000000015,  # 1 PYG ≈ 0.000000015 BTC
        'eth': 0.00000025,   # 1 PYG ≈ 0.00000025 ETH
        'usdt': 0.00014      # 1 PYG ≈ 0.00014 USDT
    }
    
    rate = rates.get(crypto, 0)
    return round(amount_pyg * rate, 8)
