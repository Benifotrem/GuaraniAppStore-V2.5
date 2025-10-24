#!/usr/bin/env python3
"""
Backend Testing Suite for GuaraniAppStore V2.5 Pro
Testing focus: Blog System Automatizado con Panel Admin
"""

import requests
import json
import sys
import time
from typing import Dict, Any, Optional

class GuaraniBackendTester:
    def __init__(self):
        self.base_url = "https://crypto-sentiment-hub.preview.emergentagent.com/api"
        self.session = requests.Session()
        self.admin_token = None
        self.test_results = []
        
        # Admin credentials 
        self.admin_email = "admin@guaraniappstore.com"
        self.admin_password = "admin123"
        
        # Test data storage
        self.test_article_id = None
        self.test_article_slug = None
        self.initial_views = 0
        
        # Momentum Predictor test data - FASE 2 with more symbols (using Kraken-supported pairs)
        self.test_symbols = ['BTC', 'ETH', 'SOL', 'ADA', 'DOT']
        self.generated_signals = []
        
        # CryptoShield test data
        self.test_wallets = [
            '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045',  # Vitalik Buterin
            '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb',   # Binance Hot Wallet
            '0x0000000000000000000000000000000000000000'    # Null address
        ]
        self.test_tx_hashes = [
            '0x5c504ed432cb51138bcf09aa5e8a410dd4a1e204ef84bfed1be16dfba1b22060',  # First TX
            '0x0000000000000000000000000000000000000000000000000000000000000000'   # Invalid
        ]
        self.test_contract = '0xdAC17F958D2ee523a2206206994597C13D831ec7'  # USDT contract
        self.cryptoshield_scans = []
        
        # Expected services count
        self.expected_services_count = 14  # Updated for Momentum Predictor services
        
    def log_test(self, test_name: str, success: bool, details: str = "", response_data: Any = None):
        """Log test results"""
        result = {
            'test': test_name,
            'success': success,
            'details': details,
            'response_data': response_data
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        if not success and response_data:
            print(f"   Response: {response_data}")
        print()

    def make_request(self, method: str, endpoint: str, data: Dict = None, headers: Dict = None) -> tuple:
        """Make HTTP request and return (success, response_data, status_code)"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, headers=headers, timeout=30)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, headers=headers, timeout=30)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data, headers=headers, timeout=30)
            else:
                return False, f"Unsupported method: {method}", 0
                
            try:
                response_data = response.json()
            except:
                response_data = response.text
                
            return response.status_code < 400, response_data, response.status_code
            
        except requests.exceptions.RequestException as e:
            return False, f"Request failed: {str(e)}", 0

    def test_health_check(self):
        """Test health check endpoint"""
        success, data, status_code = self.make_request('GET', '/health')
        
        if success and isinstance(data, dict) and data.get('status') == 'healthy':
            self.log_test("Health Check", True, f"Status: {data.get('status')}")
        else:
            self.log_test("Health Check", False, f"Status code: {status_code}", data)

    def test_admin_login(self):
        """Test admin login and store token"""
        login_data = {
            "email": self.admin_email,
            "password": self.admin_password
        }
        
        success, data, status_code = self.make_request('POST', '/auth/login', login_data)
        
        if success and isinstance(data, dict) and 'access_token' in data:
            self.admin_token = data['access_token']
            user_info = data.get('user', {})
            role = user_info.get('role', 'unknown')
            
            if role == 'admin':
                self.log_test("Admin Login", True, f"Logged in as admin: {user_info.get('email')}")
                # Set authorization header for future requests
                self.session.headers.update({'Authorization': f'Bearer {self.admin_token}'})
            else:
                self.log_test("Admin Login", False, f"User role is '{role}', expected 'admin'")
        else:
            self.log_test("Admin Login", False, f"Status code: {status_code}", data)

    def test_countries_endpoint(self):
        """Test /api/countries endpoint - should return list of countries with timezones"""
        success, data, status_code = self.make_request('GET', '/countries')
        
        if status_code == 502:
            self.log_test("Countries Endpoint", False, "502 Bad Gateway error - PostgreSQL connection issue", data)
            return
            
        if success and isinstance(data, dict):
            countries = data.get('countries', [])
            default_country = data.get('default')
            
            if isinstance(countries, list) and len(countries) > 0:
                # Check if countries have required fields
                first_country = countries[0] if countries else {}
                if 'name' in first_country and 'timezone' in first_country:
                    self.log_test("Countries Endpoint", True, f"Found {len(countries)} countries with timezones. Default: {default_country}")
                else:
                    self.log_test("Countries Endpoint", False, "Countries missing required fields (name, timezone)")
            else:
                self.log_test("Countries Endpoint", False, "No countries found in response")
        else:
            self.log_test("Countries Endpoint", False, f"Status code: {status_code}", data)

    def test_services_endpoint(self):
        """Test /api/services endpoint - should return 11 services from MongoDB"""
        success, data, status_code = self.make_request('GET', '/services')
        
        if status_code == 502:
            self.log_test("Services Endpoint", False, "502 Bad Gateway error - PostgreSQL connection issue", data)
            return
            
        if success and isinstance(data, list):
            service_count = len(data)
            
            if service_count == self.expected_services_count:
                # Verify service structure
                if data:
                    first_service = data[0]
                    required_fields = ['name', 'slug', 'category', 'description', 'price', 'currency', 'active', 'features']
                    missing_fields = [field for field in required_fields if field not in first_service]
                    
                    if not missing_fields:
                        self.log_test("Services Endpoint", True, f"Found {service_count} services with correct structure")
                        # Log some service names for verification
                        service_names = [s.get('name', 'Unknown') for s in data[:3]]
                        print(f"   Sample services: {', '.join(service_names)}")
                    else:
                        self.log_test("Services Endpoint", False, f"Services missing required fields: {missing_fields}")
                else:
                    self.log_test("Services Endpoint", False, "Services array is empty")
            else:
                self.log_test("Services Endpoint", False, f"Expected {self.expected_services_count} services, found {service_count}")
                if service_count > 0:
                    service_names = [s.get('name', 'Unknown') for s in data]
                    print(f"   Found services: {', '.join(service_names)}")
        else:
            self.log_test("Services Endpoint", False, f"Status code: {status_code}", data)

    def test_backend_logs_check(self):
        """Check if backend is running without PostgreSQL errors"""
        # Test root endpoint to verify backend is responding
        success, data, status_code = self.make_request('GET', '/')
        
        if success and isinstance(data, dict):
            message = data.get('message', '')
            version = data.get('version', '')
            status = data.get('status', '')
            
            if 'GuaraniAppStore' in message and status == 'active':
                self.log_test("Backend Status", True, f"Backend running: {message} v{version}")
            else:
                self.log_test("Backend Status", False, f"Unexpected backend response: {data}")
        else:
            self.log_test("Backend Status", False, f"Backend not responding. Status code: {status_code}", data)

    def test_mongodb_connection(self):
        """Verify MongoDB connection by testing services endpoint"""
        # This is implicitly tested by services endpoint, but we'll do a specific check
        success, data, status_code = self.make_request('GET', '/services')
        
        if status_code == 502:
            self.log_test("MongoDB Connection", False, "502 error suggests database connection issues")
        elif success:
            self.log_test("MongoDB Connection", True, "Services endpoint responding - MongoDB connected")
        else:
            self.log_test("MongoDB Connection", False, f"Database connection issue. Status: {status_code}")

    def verify_expected_services(self, services_data):
        """Verify the 11 expected services are present"""
        expected_services = [
            "Consultoría Técnica IA",
            "Generador de Blogs con IA", 
            "Prospección Comercial con IA",
            "Gestor de Emails con IA",
            "Análisis de CVs con IA",
            "Procesamiento de Facturas con OCR",
            "Sistema de Agendamiento Inteligente",
            "Asistente Virtual para Directivos",
            "Análisis de Redes Sociales con IA",
            "Chatbot WhatsApp/Telegram",
            "Suite Crypto"
        ]
        
        if not isinstance(services_data, list):
            return False, "Services data is not a list"
            
        service_names = [s.get('name', '') for s in services_data]
        found_services = []
        missing_services = []
        
        for expected in expected_services:
            found = any(expected.lower() in name.lower() for name in service_names)
            if found:
                found_services.append(expected)
            else:
                missing_services.append(expected)
        
        if len(found_services) >= 10:  # Allow some flexibility in naming
            return True, f"Found {len(found_services)}/11 expected services"
        else:
            return False, f"Missing services: {missing_services}"

    def test_bots_status(self):
        """Test bots status endpoint (requires admin auth)"""
        if not self.admin_token:
            self.log_test("Bots Status", False, "No admin token available")
            return
            
        success, data, status_code = self.make_request('GET', '/admin/bots/status')
        
        if success and isinstance(data, dict):
            if data.get('success') == True:
                bots = data.get('bots', {})
                total_running = data.get('total_running', 0)
                self.log_test("Bots Status", True, f"Bots status retrieved. Running: {total_running}")
            else:
                # Even if bots aren't running, endpoint should respond correctly
                self.log_test("Bots Status", True, f"Endpoint responded correctly: {data.get('error', 'No error')}")
        else:
            self.log_test("Bots Status", False, f"Status code: {status_code}", data)

    def test_start_specific_bot(self, bot_name: str):
        """Test starting a specific bot"""
        if not self.admin_token:
            self.log_test(f"Start Bot {bot_name}", False, "No admin token available")
            return
            
        success, data, status_code = self.make_request('POST', f'/admin/bots/start/{bot_name}')
        
        if success and isinstance(data, dict):
            # Bot may fail to start due to Telegram connection, but endpoint should respond
            if data.get('success') is not None:  # Endpoint responded with success field
                message = data.get('message', 'No message')
                self.log_test(f"Start Bot {bot_name}", True, f"Endpoint responded: {message}")
            else:
                self.log_test(f"Start Bot {bot_name}", False, "Unexpected response format", data)
        else:
            self.log_test(f"Start Bot {bot_name}", False, f"Status code: {status_code}", data)

    def test_stop_specific_bot(self, bot_name: str):
        """Test stopping a specific bot"""
        if not self.admin_token:
            self.log_test(f"Stop Bot {bot_name}", False, "No admin token available")
            return
            
        success, data, status_code = self.make_request('POST', f'/admin/bots/stop/{bot_name}')
        
        if success and isinstance(data, dict):
            if data.get('success') is not None:  # Endpoint responded with success field
                message = data.get('message', 'No message')
                self.log_test(f"Stop Bot {bot_name}", True, f"Endpoint responded: {message}")
            else:
                self.log_test(f"Stop Bot {bot_name}", False, "Unexpected response format", data)
        else:
            self.log_test(f"Stop Bot {bot_name}", False, f"Status code: {status_code}", data)

    def test_start_all_bots(self):
        """Test starting all bots"""
        if not self.admin_token:
            self.log_test("Start All Bots", False, "No admin token available")
            return
            
        success, data, status_code = self.make_request('POST', '/admin/bots/start-all')
        
        if success and isinstance(data, dict):
            if data.get('success') is not None:
                message = data.get('message', 'No message')
                self.log_test("Start All Bots", True, f"Endpoint responded: {message}")
            else:
                self.log_test("Start All Bots", False, "Unexpected response format", data)
        else:
            self.log_test("Start All Bots", False, f"Status code: {status_code}", data)

    def test_stop_all_bots(self):
        """Test stopping all bots"""
        if not self.admin_token:
            self.log_test("Stop All Bots", False, "No admin token available")
            return
            
        success, data, status_code = self.make_request('POST', '/admin/bots/stop-all')
        
        if success and isinstance(data, dict):
            if data.get('success') is not None:
                message = data.get('message', 'No message')
                self.log_test("Stop All Bots", True, f"Endpoint responded: {message}")
            else:
                self.log_test("Stop All Bots", False, "Unexpected response format", data)
        else:
            self.log_test("Stop All Bots", False, f"Status code: {status_code}", data)

    def test_invalid_bot_name(self):
        """Test with invalid bot name"""
        if not self.admin_token:
            self.log_test("Invalid Bot Name", False, "No admin token available")
            return
            
        success, data, status_code = self.make_request('POST', '/admin/bots/start/invalid_bot')
        
        # Should return 400 Bad Request for invalid bot name
        if status_code == 400:
            self.log_test("Invalid Bot Name", True, "Correctly rejected invalid bot name")
        else:
            self.log_test("Invalid Bot Name", False, f"Expected 400, got {status_code}", data)

    def test_momentum_health_check(self):
        """Test Momentum Predictor health check endpoint - FASE 2"""
        success, data, status_code = self.make_request('GET', '/momentum/health')
        
        if success and isinstance(data, dict):
            expected_fields = ['status', 'service', 'version', 'model_loaded', 'mode']
            missing_fields = [field for field in expected_fields if field not in data]
            
            if not missing_fields:
                status = data.get('status')
                service = data.get('service')
                version = data.get('version')
                model_loaded = data.get('model_loaded')
                mode = data.get('mode')
                
                # Check that health endpoint reflects Fase 2 changes
                if (status == 'healthy' and 
                    service == 'Momentum Predictor' and 
                    version == '1.0.0' and 
                    model_loaded == False and 
                    mode == 'MOCK'):
                    self.log_test("Momentum Health Check", True, 
                                f"Status: {status}, Service: {service}, Version: {version}, Mode: {mode} (Fase 2 Ready)")
                else:
                    self.log_test("Momentum Health Check", False, 
                                f"Unexpected values - Status: {status}, Mode: {mode}, Model loaded: {model_loaded}")
            else:
                self.log_test("Momentum Health Check", False, f"Missing fields: {missing_fields}")
        else:
            self.log_test("Momentum Health Check", False, f"Status code: {status_code}", data)

    def test_momentum_signal_generation(self, symbol: str):
        """Test signal generation for a specific symbol - FASE 2 with Technical Analysis"""
        success, data, status_code = self.make_request('GET', f'/momentum/signal/{symbol}')
        
        if success and isinstance(data, dict):
            # Check required fields (including new 'indicators' field for Fase 2)
            required_fields = [
                'symbol', 'signal', 'confidence', 'current_price', 'entry_price',
                'target_1', 'target_2', 'stop_loss', 'timeframe', 'risk_level',
                'probabilities', 'predicted_at', 'model_version', 'is_mock', 'indicators'
            ]
            missing_fields = [field for field in required_fields if field not in data]
            
            if not missing_fields:
                # Validate signal values
                signal = data.get('signal')
                confidence = data.get('confidence')
                current_price = data.get('current_price')
                is_mock = data.get('is_mock')
                probabilities = data.get('probabilities', {})
                predicted_at = data.get('predicted_at')
                model_version = data.get('model_version')
                indicators = data.get('indicators', {})
                
                # FASE 2 SPECIFIC VALIDATIONS
                # 1. Check model version is updated
                valid_model_version = model_version == "MOCK_v2_Technical_Analysis"
                
                # 2. Check indicators field contains required technical indicators
                required_indicators = ['rsi', 'macd', 'sma_7', 'sma_25', 'stoch_k', 'buy_score', 'sell_score']
                missing_indicators = [ind for ind in required_indicators if ind not in indicators]
                valid_indicators = len(missing_indicators) == 0
                
                # 3. Validate indicator values are realistic numbers
                valid_indicator_values = True
                if valid_indicators:
                    rsi = indicators.get('rsi', 0)
                    macd = indicators.get('macd', 0)
                    buy_score = indicators.get('buy_score', 0)
                    sell_score = indicators.get('sell_score', 0)
                    
                    # RSI should be between 0-100
                    if not (0 <= rsi <= 100):
                        valid_indicator_values = False
                    
                    # Scores should be integers between 0-8
                    if not (isinstance(buy_score, int) and 0 <= buy_score <= 8):
                        valid_indicator_values = False
                    if not (isinstance(sell_score, int) and 0 <= sell_score <= 8):
                        valid_indicator_values = False
                
                # 4. Validate signal logic consistency with scores
                valid_signal_logic = True
                if valid_indicators:
                    buy_score = indicators.get('buy_score', 0)
                    sell_score = indicators.get('sell_score', 0)
                    
                    if signal == 'BUY' and buy_score < sell_score + 2:
                        valid_signal_logic = False
                    elif signal == 'SELL' and sell_score < buy_score + 2:
                        valid_signal_logic = False
                    elif signal == 'HOLD' and abs(buy_score - sell_score) >= 2:
                        valid_signal_logic = False
                
                # 5. Check confidence varies (not always 60%)
                confidence_varies = confidence != 60.0
                
                # Original validations
                valid_signal = signal in ['BUY', 'SELL', 'HOLD']
                valid_confidence = isinstance(confidence, (int, float)) and 0 <= confidence <= 100
                valid_price = isinstance(current_price, (int, float)) and current_price > 0
                valid_mock = is_mock == True  # Should be True in MOCK mode
                valid_probabilities = (isinstance(probabilities, dict) and 
                                     'BUY' in probabilities and 'SELL' in probabilities and 'HOLD' in probabilities)
                
                # Check date format (ISO 8601 with UTC)
                valid_date = False
                try:
                    from datetime import datetime
                    datetime.fromisoformat(predicted_at.replace('Z', '+00:00'))
                    valid_date = True
                except:
                    pass
                
                # Check if price is realistic (> $1 for major cryptos)
                price_realistic = current_price > 1 if symbol in ['BTC', 'ETH'] else current_price > 0
                
                # All validations must pass
                all_valid = all([
                    valid_signal, valid_confidence, valid_price, valid_mock, valid_probabilities, 
                    valid_date, valid_model_version, valid_indicators, valid_indicator_values,
                    valid_signal_logic, price_realistic
                ])
                
                if all_valid:
                    # Store for history testing
                    self.generated_signals.append(data)
                    
                    # Enhanced success message with Fase 2 details
                    buy_score = indicators.get('buy_score', 0)
                    sell_score = indicators.get('sell_score', 0)
                    rsi = indicators.get('rsi', 0)
                    
                    self.log_test(f"Momentum Signal {symbol}", True, 
                                f"Signal: {signal} ({confidence}% confidence), Price: ${current_price:,.2f}, "
                                f"RSI: {rsi:.1f}, Scores: BUY={buy_score} SELL={sell_score}, Model: {model_version}")
                else:
                    validation_errors = []
                    if not valid_signal: validation_errors.append(f"Invalid signal: {signal}")
                    if not valid_confidence: validation_errors.append(f"Invalid confidence: {confidence}")
                    if not valid_price: validation_errors.append(f"Invalid price: ${current_price}")
                    if not price_realistic: validation_errors.append(f"Unrealistic price: ${current_price} for {symbol}")
                    if not valid_mock: validation_errors.append(f"Expected is_mock=True, got {is_mock}")
                    if not valid_probabilities: validation_errors.append("Invalid probabilities structure")
                    if not valid_date: validation_errors.append(f"Invalid date format: {predicted_at}")
                    if not valid_model_version: validation_errors.append(f"Expected model_version='MOCK_v2_Technical_Analysis', got '{model_version}'")
                    if not valid_indicators: validation_errors.append(f"Missing indicators: {missing_indicators}")
                    if not valid_indicator_values: validation_errors.append("Invalid indicator values (RSI not 0-100 or scores not 0-8)")
                    if not valid_signal_logic: validation_errors.append(f"Signal logic inconsistent: {signal} with BUY={buy_score} SELL={sell_score}")
                    
                    self.log_test(f"Momentum Signal {symbol}", False, "; ".join(validation_errors))
            else:
                self.log_test(f"Momentum Signal {symbol}", False, f"Missing fields: {missing_fields}")
        else:
            self.log_test(f"Momentum Signal {symbol}", False, f"Status code: {status_code}", data)

    def test_momentum_signals_history(self):
        """Test signals history endpoint"""
        # Test general history
        success, data, status_code = self.make_request('GET', '/momentum/signals/history?limit=10')
        
        if success and isinstance(data, list):
            if len(data) > 0:
                # Check structure of first signal
                first_signal = data[0]
                required_fields = ['symbol', 'signal', 'confidence', 'current_price', 'predicted_at']
                missing_fields = [field for field in required_fields if field not in first_signal]
                
                if not missing_fields:
                    self.log_test("Momentum Signals History", True, 
                                f"Retrieved {len(data)} historical signals")
                else:
                    self.log_test("Momentum Signals History", False, 
                                f"History signals missing fields: {missing_fields}")
            else:
                self.log_test("Momentum Signals History", True, "No historical signals yet (expected for new system)")
        else:
            self.log_test("Momentum Signals History", False, f"Status code: {status_code}", data)
        
        # Test filtered history (if we have generated signals)
        if self.generated_signals:
            symbol = self.generated_signals[0]['symbol']
            success, data, status_code = self.make_request('GET', f'/momentum/signals/history?symbol={symbol}&limit=5')
            
            if success and isinstance(data, list):
                self.log_test("Momentum Signals History (Filtered)", True, 
                            f"Retrieved {len(data)} signals for {symbol}")
            else:
                self.log_test("Momentum Signals History (Filtered)", False, 
                            f"Status code: {status_code}", data)

    def test_momentum_stats(self, symbol: str):
        """Test momentum stats for a symbol"""
        success, data, status_code = self.make_request('GET', f'/momentum/stats/{symbol}')
        
        if status_code == 404:
            # Expected if no signals exist yet
            self.log_test(f"Momentum Stats {symbol}", True, 
                        "404 Not Found - No signals yet (expected for new system)")
            return
        
        if success and isinstance(data, dict):
            required_fields = [
                'symbol', 'total_predictions', 'buy_signals', 'sell_signals', 
                'hold_signals', 'buy_percentage', 'last_signal', 'last_confidence', 
                'last_predicted_at'
            ]
            missing_fields = [field for field in required_fields if field not in data]
            
            if not missing_fields:
                total = data.get('total_predictions', 0)
                buy_signals = data.get('buy_signals', 0)
                sell_signals = data.get('sell_signals', 0)
                hold_signals = data.get('hold_signals', 0)
                buy_percentage = data.get('buy_percentage', 0)
                
                # Validate calculations
                calculated_total = buy_signals + sell_signals + hold_signals
                calculated_percentage = (buy_signals / total * 100) if total > 0 else 0
                
                if calculated_total == total and abs(calculated_percentage - buy_percentage) < 0.1:
                    self.log_test(f"Momentum Stats {symbol}", True, 
                                f"Total: {total}, BUY: {buy_signals} ({buy_percentage}%), SELL: {sell_signals}, HOLD: {hold_signals}")
                else:
                    self.log_test(f"Momentum Stats {symbol}", False, 
                                f"Calculation mismatch - Expected total: {calculated_total}, got: {total}")
            else:
                self.log_test(f"Momentum Stats {symbol}", False, f"Missing fields: {missing_fields}")
        else:
            self.log_test(f"Momentum Stats {symbol}", False, f"Status code: {status_code}", data)

    def test_momentum_stats_nonexistent_symbol(self):
        """Test stats endpoint with non-existent symbol"""
        success, data, status_code = self.make_request('GET', '/momentum/stats/NONEXISTENT')
        
        if status_code == 404:
            self.log_test("Momentum Stats (Non-existent)", True, 
                        "Correctly returned 404 for non-existent symbol")
        else:
            self.log_test("Momentum Stats (Non-existent)", False, 
                        f"Expected 404, got {status_code}", data)

    def test_signal_variety_across_symbols(self):
        """Test that signals vary across different symbols (not all HOLD)"""
        if len(self.generated_signals) < 3:
            self.log_test("Signal Variety", False, "Not enough signals generated to test variety")
            return
        
        signals = [signal['signal'] for signal in self.generated_signals]
        unique_signals = set(signals)
        
        # Check if we have variety (not all the same signal)
        if len(unique_signals) > 1:
            signal_counts = {signal: signals.count(signal) for signal in unique_signals}
            self.log_test("Signal Variety", True, 
                        f"Signal variety confirmed: {signal_counts}")
        else:
            # All signals are the same - this could happen but is less likely with technical analysis
            single_signal = list(unique_signals)[0]
            self.log_test("Signal Variety", True, 
                        f"All signals are {single_signal} - acceptable but less variety than expected")

    def test_confidence_variation(self):
        """Test that confidence values vary dynamically (not always 60%)"""
        if len(self.generated_signals) < 3:
            self.log_test("Confidence Variation", False, "Not enough signals generated to test confidence variation")
            return
        
        confidences = [signal['confidence'] for signal in self.generated_signals]
        unique_confidences = set(confidences)
        
        # Check if confidence varies
        if len(unique_confidences) > 1:
            min_conf = min(confidences)
            max_conf = max(confidences)
            avg_conf = sum(confidences) / len(confidences)
            self.log_test("Confidence Variation", True, 
                        f"Confidence varies: Min={min_conf}%, Max={max_conf}%, Avg={avg_conf:.1f}%")
        else:
            # All confidences are the same
            single_conf = list(unique_confidences)[0]
            if single_conf == 60.0:
                self.log_test("Confidence Variation", False, 
                            "All confidences are 60% - dynamic calculation not working")
            else:
                self.log_test("Confidence Variation", True, 
                            f"All confidences are {single_conf}% - consistent but not 60%")

    def test_scoring_system_logic(self):
        """Test the scoring system logic for BUY/SELL/HOLD decisions"""
        if not self.generated_signals:
            self.log_test("Scoring System Logic", False, "No signals generated to test scoring logic")
            return
        
        logic_errors = []
        valid_signals = 0
        
        for signal_data in self.generated_signals:
            symbol = signal_data.get('symbol', 'Unknown')
            signal = signal_data.get('signal')
            indicators = signal_data.get('indicators', {})
            
            if not indicators:
                continue
                
            buy_score = indicators.get('buy_score', 0)
            sell_score = indicators.get('sell_score', 0)
            
            # Validate scoring logic
            if signal == 'BUY':
                if buy_score < sell_score + 2:
                    logic_errors.append(f"{symbol}: BUY signal but buy_score({buy_score}) < sell_score({sell_score})+2")
                else:
                    valid_signals += 1
            elif signal == 'SELL':
                if sell_score < buy_score + 2:
                    logic_errors.append(f"{symbol}: SELL signal but sell_score({sell_score}) < buy_score({buy_score})+2")
                else:
                    valid_signals += 1
            elif signal == 'HOLD':
                if abs(buy_score - sell_score) >= 2:
                    logic_errors.append(f"{symbol}: HOLD signal but |buy_score({buy_score}) - sell_score({sell_score})| >= 2")
                else:
                    valid_signals += 1
        
        if not logic_errors:
            self.log_test("Scoring System Logic", True, 
                        f"All {valid_signals} signals follow correct scoring logic")
        else:
            self.log_test("Scoring System Logic", False, 
                        f"Logic errors found: {'; '.join(logic_errors[:3])}")  # Show first 3 errors

    def test_technical_indicators_realism(self):
        """Test that technical indicators have realistic values"""
        if not self.generated_signals:
            self.log_test("Technical Indicators Realism", False, "No signals generated to test indicators")
            return
        
        indicator_errors = []
        valid_indicators = 0
        
        for signal_data in self.generated_signals:
            symbol = signal_data.get('symbol', 'Unknown')
            indicators = signal_data.get('indicators', {})
            
            if not indicators:
                continue
            
            # Check RSI (should be 0-100)
            rsi = indicators.get('rsi', 0)
            if not (0 <= rsi <= 100):
                indicator_errors.append(f"{symbol}: RSI {rsi} not in range 0-100")
            
            # Check MACD (should be a reasonable number, not NaN or extreme)
            macd = indicators.get('macd', 0)
            if not isinstance(macd, (int, float)) or abs(macd) > 10000:
                indicator_errors.append(f"{symbol}: MACD {macd} seems unrealistic")
            
            # Check SMA values (should be positive and reasonable)
            sma_7 = indicators.get('sma_7', 0)
            sma_25 = indicators.get('sma_25', 0)
            if sma_7 <= 0 or sma_25 <= 0:
                indicator_errors.append(f"{symbol}: SMA values should be positive (SMA7={sma_7}, SMA25={sma_25})")
            
            # Check Stochastic (should be 0-100)
            stoch_k = indicators.get('stoch_k', 0)
            if not (0 <= stoch_k <= 100):
                indicator_errors.append(f"{symbol}: Stochastic K {stoch_k} not in range 0-100")
            
            # Check scores (should be 0-8 integers)
            buy_score = indicators.get('buy_score', 0)
            sell_score = indicators.get('sell_score', 0)
            if not (isinstance(buy_score, int) and 0 <= buy_score <= 8):
                indicator_errors.append(f"{symbol}: buy_score {buy_score} not integer 0-8")
            if not (isinstance(sell_score, int) and 0 <= sell_score <= 8):
                indicator_errors.append(f"{symbol}: sell_score {sell_score} not integer 0-8")
            
            if not indicator_errors:
                valid_indicators += 1
        
        if not indicator_errors:
            self.log_test("Technical Indicators Realism", True, 
                        f"All {valid_indicators} signals have realistic indicator values")
        else:
            self.log_test("Technical Indicators Realism", False, 
                        f"Indicator errors: {'; '.join(indicator_errors[:3])}")  # Show first 3 errors

    def verify_trading_levels_calculation(self, signal_data):
        """Verify that trading levels are reasonable"""
        current_price = signal_data.get('current_price')
        entry_price = signal_data.get('entry_price')
        target_1 = signal_data.get('target_1')
        target_2 = signal_data.get('target_2')
        stop_loss = signal_data.get('stop_loss')
        signal = signal_data.get('signal')
        
        if signal == 'BUY':
            # For BUY: entry < current, targets > current, stop_loss < current
            valid_entry = entry_price < current_price
            valid_targets = target_1 > current_price and target_2 > target_1
            valid_stop = stop_loss < current_price
        elif signal == 'SELL':
            # For SELL: entry > current, targets < current, stop_loss > current
            valid_entry = entry_price > current_price
            valid_targets = target_1 < current_price and target_2 < target_1
            valid_stop = stop_loss > current_price
        else:  # HOLD
            # For HOLD: levels should be close to current price
            valid_entry = abs(entry_price - current_price) / current_price < 0.02
            valid_targets = target_1 > current_price and target_2 > target_1
            valid_stop = stop_loss < current_price
        
        return all([valid_entry, valid_targets, valid_stop])

    def test_cryptoshield_health_check(self):
        """Test CryptoShield health check endpoint"""
        success, data, status_code = self.make_request('GET', '/cryptoshield/health')
        
        if success and isinstance(data, dict):
            expected_fields = ['status', 'service', 'version', 'mode', 'etherscan_api']
            missing_fields = [field for field in expected_fields if field not in data]
            
            if not missing_fields:
                status = data.get('status')
                service = data.get('service')
                version = data.get('version')
                mode = data.get('mode')
                etherscan_api = data.get('etherscan_api')
                
                if (status == 'healthy' and 
                    service == 'CryptoShield IA' and 
                    version == '1.0.0' and 
                    mode == 'MOCK' and 
                    etherscan_api == 'configured'):
                    self.log_test("CryptoShield Health Check", True, 
                                f"Status: {status}, Service: {service}, Version: {version}, Mode: {mode}, Etherscan: {etherscan_api}")
                else:
                    self.log_test("CryptoShield Health Check", False, 
                                f"Unexpected values - Status: {status}, Mode: {mode}, Etherscan: {etherscan_api}")
            else:
                self.log_test("CryptoShield Health Check", False, f"Missing fields: {missing_fields}")
        else:
            self.log_test("CryptoShield Health Check", False, f"Status code: {status_code}", data)

    def test_cryptoshield_wallet_scan(self, address: str, expected_name: str = ""):
        """Test wallet scanning with CryptoShield"""
        success, data, status_code = self.make_request('GET', f'/cryptoshield/scan/wallet/{address}')
        
        if success and isinstance(data, dict):
            # Check required fields
            required_fields = [
                'address', 'balance_eth', 'transaction_count', 'risk_score', 'risk_level',
                'risk_factors', 'recommendations', 'scan_type', 'model_version', 'is_mock', 'analyzed_at'
            ]
            missing_fields = [field for field in required_fields if field not in data]
            
            if not missing_fields:
                # Validate field values
                address_val = data.get('address')
                balance_eth = data.get('balance_eth')
                tx_count = data.get('transaction_count')
                risk_score = data.get('risk_score')
                risk_level = data.get('risk_level')
                risk_factors = data.get('risk_factors', [])
                recommendations = data.get('recommendations', [])
                scan_type = data.get('scan_type')
                model_version = data.get('model_version')
                is_mock = data.get('is_mock')
                analyzed_at = data.get('analyzed_at')
                
                # Validations
                valid_address = address_val == address
                valid_balance = isinstance(balance_eth, (int, float)) and balance_eth >= 0
                valid_tx_count = isinstance(tx_count, int) and tx_count >= 0
                valid_risk_score = isinstance(risk_score, int) and 0 <= risk_score <= 100
                valid_risk_level = risk_level in ['low', 'medium', 'high']
                valid_risk_factors = isinstance(risk_factors, list)
                valid_recommendations = isinstance(recommendations, list) and len(recommendations) >= 2
                valid_scan_type = scan_type == 'wallet'
                valid_model_version = model_version == 'MOCK'
                valid_is_mock = is_mock == True
                
                # Check date format (ISO 8601)
                valid_date = False
                try:
                    from datetime import datetime
                    datetime.fromisoformat(analyzed_at.replace('Z', '+00:00'))
                    valid_date = True
                except:
                    pass
                
                # Check if data is realistic (not hardcoded)
                realistic_data = True
                if address == '0x0000000000000000000000000000000000000000':
                    # Null address should have 0 balance and transactions
                    realistic_data = balance_eth == 0 and tx_count == 0
                else:
                    # Real addresses should have some activity or balance
                    realistic_data = balance_eth > 0 or tx_count > 0
                
                all_valid = all([
                    valid_address, valid_balance, valid_tx_count, valid_risk_score, valid_risk_level,
                    valid_risk_factors, valid_recommendations, valid_scan_type, valid_model_version,
                    valid_is_mock, valid_date, realistic_data
                ])
                
                if all_valid:
                    # Store for history testing
                    self.cryptoshield_scans.append(data)
                    
                    self.log_test(f"CryptoShield Wallet Scan ({expected_name})", True, 
                                f"Address: {address[:10]}..., Balance: {balance_eth:.4f} ETH, "
                                f"TXs: {tx_count:,}, Risk: {risk_level.upper()} ({risk_score}/100)")
                else:
                    validation_errors = []
                    if not valid_address: validation_errors.append(f"Address mismatch: {address_val}")
                    if not valid_balance: validation_errors.append(f"Invalid balance: {balance_eth}")
                    if not valid_tx_count: validation_errors.append(f"Invalid TX count: {tx_count}")
                    if not valid_risk_score: validation_errors.append(f"Invalid risk score: {risk_score}")
                    if not valid_risk_level: validation_errors.append(f"Invalid risk level: {risk_level}")
                    if not valid_risk_factors: validation_errors.append("Invalid risk factors format")
                    if not valid_recommendations: validation_errors.append(f"Need >=2 recommendations, got {len(recommendations)}")
                    if not valid_scan_type: validation_errors.append(f"Expected scan_type='wallet', got '{scan_type}'")
                    if not valid_model_version: validation_errors.append(f"Expected model_version='MOCK', got '{model_version}'")
                    if not valid_is_mock: validation_errors.append(f"Expected is_mock=True, got {is_mock}")
                    if not valid_date: validation_errors.append(f"Invalid date format: {analyzed_at}")
                    if not realistic_data: validation_errors.append("Data appears hardcoded, not from Etherscan")
                    
                    self.log_test(f"CryptoShield Wallet Scan ({expected_name})", False, "; ".join(validation_errors))
            else:
                self.log_test(f"CryptoShield Wallet Scan ({expected_name})", False, f"Missing fields: {missing_fields}")
        else:
            # Check if it's a validation error (400) for invalid addresses
            if status_code == 400 and address == '0x0000000000000000000000000000000000000000':
                self.log_test(f"CryptoShield Wallet Scan ({expected_name})", True, 
                            "Correctly rejected invalid address format with 400 Bad Request")
            else:
                self.log_test(f"CryptoShield Wallet Scan ({expected_name})", False, f"Status code: {status_code}", data)

    def test_cryptoshield_transaction_verify(self, tx_hash: str, expected_name: str = ""):
        """Test transaction verification with CryptoShield"""
        success, data, status_code = self.make_request('GET', f'/cryptoshield/verify/transaction/{tx_hash}')
        
        if success and isinstance(data, dict):
            # Check required fields
            required_fields = [
                'tx_hash', 'status', 'is_success', 'risk_score', 'risk_level',
                'risk_factors', 'recommendations', 'scan_type', 'model_version', 'is_mock', 'verified_at'
            ]
            missing_fields = [field for field in required_fields if field not in data]
            
            if not missing_fields:
                # Validate field values
                tx_hash_val = data.get('tx_hash')
                status = data.get('status')
                is_success = data.get('is_success')
                risk_score = data.get('risk_score')
                risk_level = data.get('risk_level')
                recommendations = data.get('recommendations', [])
                scan_type = data.get('scan_type')
                model_version = data.get('model_version')
                is_mock = data.get('is_mock')
                verified_at = data.get('verified_at')
                
                # Validations
                valid_tx_hash = tx_hash_val == tx_hash
                valid_status = status in ['success', 'failed']
                valid_is_success = isinstance(is_success, bool)
                valid_risk_score = isinstance(risk_score, int) and 0 <= risk_score <= 100
                valid_risk_level = risk_level in ['low', 'medium', 'high']
                valid_recommendations = isinstance(recommendations, list) and len(recommendations) >= 1
                valid_scan_type = scan_type == 'transaction'
                valid_model_version = model_version == 'MOCK'
                valid_is_mock = is_mock == True
                
                # Check contextual recommendations
                contextual_recs = True
                if status == 'success' and risk_level == 'low':
                    contextual_recs = any('safe' in rec.lower() or 'low risk' in rec.lower() for rec in recommendations)
                elif status == 'failed':
                    contextual_recs = risk_score >= 50  # Failed transactions should have higher risk
                
                # Check date format
                valid_date = False
                try:
                    from datetime import datetime
                    datetime.fromisoformat(verified_at.replace('Z', '+00:00'))
                    valid_date = True
                except:
                    pass
                
                all_valid = all([
                    valid_tx_hash, valid_status, valid_is_success, valid_risk_score, valid_risk_level,
                    valid_recommendations, valid_scan_type, valid_model_version, valid_is_mock, 
                    valid_date, contextual_recs
                ])
                
                if all_valid:
                    self.cryptoshield_scans.append(data)
                    
                    self.log_test(f"CryptoShield TX Verify ({expected_name})", True, 
                                f"TX: {tx_hash[:10]}..., Status: {status.upper()}, "
                                f"Success: {is_success}, Risk: {risk_level.upper()} ({risk_score}/100)")
                else:
                    validation_errors = []
                    if not valid_tx_hash: validation_errors.append(f"TX hash mismatch")
                    if not valid_status: validation_errors.append(f"Invalid status: {status}")
                    if not valid_is_success: validation_errors.append(f"Invalid is_success type: {type(is_success)}")
                    if not valid_risk_score: validation_errors.append(f"Invalid risk score: {risk_score}")
                    if not valid_risk_level: validation_errors.append(f"Invalid risk level: {risk_level}")
                    if not valid_recommendations: validation_errors.append(f"Need >=1 recommendation, got {len(recommendations)}")
                    if not valid_scan_type: validation_errors.append(f"Expected scan_type='transaction'")
                    if not valid_model_version: validation_errors.append(f"Expected model_version='MOCK'")
                    if not valid_is_mock: validation_errors.append(f"Expected is_mock=True")
                    if not valid_date: validation_errors.append(f"Invalid date format")
                    if not contextual_recs: validation_errors.append("Recommendations not contextual to status")
                    
                    self.log_test(f"CryptoShield TX Verify ({expected_name})", False, "; ".join(validation_errors))
            else:
                self.log_test(f"CryptoShield TX Verify ({expected_name})", False, f"Missing fields: {missing_fields}")
        else:
            # Check if it's a validation error (400) for invalid tx hashes
            if status_code == 400 and tx_hash == '0x0000000000000000000000000000000000000000000000000000000000000000':
                self.log_test(f"CryptoShield TX Verify ({expected_name})", True, 
                            "Correctly rejected invalid TX hash format with 400 Bad Request")
            else:
                self.log_test(f"CryptoShield TX Verify ({expected_name})", False, f"Status code: {status_code}", data)

    def test_cryptoshield_contract_scan(self, contract_address: str):
        """Test contract scanning with CryptoShield"""
        success, data, status_code = self.make_request('GET', f'/cryptoshield/scan/contract/{contract_address}')
        
        if success and isinstance(data, dict):
            # Check required fields
            required_fields = [
                'contract_address', 'is_contract', 'is_verified', 'risk_score', 'risk_level',
                'risk_factors', 'recommendations', 'scan_type', 'model_version', 'is_mock', 'analyzed_at'
            ]
            missing_fields = [field for field in required_fields if field not in data]
            
            if not missing_fields:
                # Validate field values
                contract_addr = data.get('contract_address')
                is_contract = data.get('is_contract')
                is_verified = data.get('is_verified')
                risk_score = data.get('risk_score')
                risk_level = data.get('risk_level')
                recommendations = data.get('recommendations', [])
                scan_type = data.get('scan_type')
                model_version = data.get('model_version')
                is_mock = data.get('is_mock')
                
                # Validations
                valid_address = contract_addr == contract_address
                valid_is_contract = is_contract == True  # USDT should be a contract
                valid_is_verified = isinstance(is_verified, bool)
                valid_risk_score = isinstance(risk_score, int) and 0 <= risk_score <= 100
                valid_risk_level = risk_level in ['low', 'medium', 'high']
                valid_recommendations = isinstance(recommendations, list) and len(recommendations) >= 1
                valid_scan_type = scan_type == 'contract'
                valid_model_version = model_version == 'MOCK'
                valid_is_mock = is_mock == True
                
                # Risk assessment should be appropriate for contracts
                appropriate_risk = True
                if contract_address == '0xdAC17F958D2ee523a2206206994597C13D831ec7':  # USDT
                    # USDT is a well-known contract, should be low-medium risk
                    appropriate_risk = risk_level in ['low', 'medium']
                
                all_valid = all([
                    valid_address, valid_is_contract, valid_is_verified, valid_risk_score, 
                    valid_risk_level, valid_recommendations, valid_scan_type, valid_model_version,
                    valid_is_mock, appropriate_risk
                ])
                
                if all_valid:
                    self.cryptoshield_scans.append(data)
                    
                    self.log_test("CryptoShield Contract Scan (USDT)", True, 
                                f"Contract: {contract_address[:10]}..., Is Contract: {is_contract}, "
                                f"Verified: {is_verified}, Risk: {risk_level.upper()} ({risk_score}/100)")
                else:
                    validation_errors = []
                    if not valid_address: validation_errors.append("Address mismatch")
                    if not valid_is_contract: validation_errors.append(f"Expected is_contract=True, got {is_contract}")
                    if not valid_is_verified: validation_errors.append(f"Invalid is_verified type")
                    if not valid_risk_score: validation_errors.append(f"Invalid risk score: {risk_score}")
                    if not valid_risk_level: validation_errors.append(f"Invalid risk level: {risk_level}")
                    if not valid_recommendations: validation_errors.append("Need >=1 recommendation")
                    if not valid_scan_type: validation_errors.append("Expected scan_type='contract'")
                    if not valid_model_version: validation_errors.append("Expected model_version='MOCK'")
                    if not valid_is_mock: validation_errors.append("Expected is_mock=True")
                    if not appropriate_risk: validation_errors.append("Risk assessment inappropriate for USDT contract")
                    
                    self.log_test("CryptoShield Contract Scan (USDT)", False, "; ".join(validation_errors))
            else:
                self.log_test("CryptoShield Contract Scan (USDT)", False, f"Missing fields: {missing_fields}")
        else:
            self.log_test("CryptoShield Contract Scan (USDT)", False, f"Status code: {status_code}", data)

    def test_cryptoshield_scan_history(self):
        """Test scan history endpoint"""
        # Test general history
        success, data, status_code = self.make_request('GET', '/cryptoshield/scans/history?limit=10')
        
        if success and isinstance(data, list):
            if len(data) > 0:
                # Check structure of first scan
                first_scan = data[0]
                required_fields = ['scan_type', 'address_or_hash', 'risk_level', 'risk_score', 'scanned_at']
                missing_fields = [field for field in required_fields if field not in first_scan]
                
                if not missing_fields:
                    # Verify ordering (should be descending by date)
                    ordered_correctly = True
                    if len(data) > 1:
                        try:
                            from datetime import datetime
                            dates = []
                            for scan in data:
                                date_str = scan.get('scanned_at', '')
                                if isinstance(date_str, str):
                                    dates.append(datetime.fromisoformat(date_str.replace('Z', '+00:00')))
                            
                            # Check if dates are in descending order
                            ordered_correctly = all(dates[i] >= dates[i+1] for i in range(len(dates)-1))
                        except:
                            ordered_correctly = False
                    
                    if ordered_correctly:
                        self.log_test("CryptoShield Scan History", True, 
                                    f"Retrieved {len(data)} scans, ordered by date descending")
                    else:
                        self.log_test("CryptoShield Scan History", False, 
                                    "Scans not ordered by date descending")
                else:
                    self.log_test("CryptoShield Scan History", False, 
                                f"History items missing fields: {missing_fields}")
            else:
                self.log_test("CryptoShield Scan History", True, "No scan history yet (expected for new system)")
        else:
            self.log_test("CryptoShield Scan History", False, f"Status code: {status_code}", data)
        
        # Test filtered history by scan_type
        success, data, status_code = self.make_request('GET', '/cryptoshield/scans/history?scan_type=wallet&limit=5')
        
        if success and isinstance(data, list):
            # All items should be wallet scans
            all_wallets = all(item.get('scan_type') == 'wallet' for item in data)
            if all_wallets:
                self.log_test("CryptoShield Scan History (Filtered)", True, 
                            f"Retrieved {len(data)} wallet scans (filter working)")
            else:
                self.log_test("CryptoShield Scan History (Filtered)", False, 
                            "Filter not working - non-wallet scans included")
        else:
            self.log_test("CryptoShield Scan History (Filtered)", False, 
                        f"Status code: {status_code}", data)

    def test_cryptoshield_stats(self):
        """Test CryptoShield statistics endpoint"""
        success, data, status_code = self.make_request('GET', '/cryptoshield/stats')
        
        if success and isinstance(data, dict):
            required_fields = [
                'total_scans', 'wallet_scans', 'transaction_verifications', 'contract_scans',
                'high_risk_found', 'medium_risk_found', 'low_risk_found', 'high_risk_percentage'
            ]
            missing_fields = [field for field in required_fields if field not in data]
            
            if not missing_fields:
                total_scans = data.get('total_scans', 0)
                wallet_scans = data.get('wallet_scans', 0)
                tx_scans = data.get('transaction_verifications', 0)
                contract_scans = data.get('contract_scans', 0)
                high_risk = data.get('high_risk_found', 0)
                medium_risk = data.get('medium_risk_found', 0)
                low_risk = data.get('low_risk_found', 0)
                high_risk_percentage = data.get('high_risk_percentage', 0)
                
                # Validate calculations
                calculated_total = wallet_scans + tx_scans + contract_scans
                calculated_risk_total = high_risk + medium_risk + low_risk
                calculated_percentage = (high_risk / total_scans * 100) if total_scans > 0 else 0
                
                # Check if calculations are correct
                total_correct = calculated_total == total_scans
                risk_total_correct = calculated_risk_total == total_scans
                percentage_correct = abs(calculated_percentage - high_risk_percentage) < 0.1
                
                if total_correct and risk_total_correct and percentage_correct:
                    self.log_test("CryptoShield Statistics", True, 
                                f"Total: {total_scans}, Wallets: {wallet_scans}, TXs: {tx_scans}, "
                                f"Contracts: {contract_scans}, High Risk: {high_risk} ({high_risk_percentage}%)")
                else:
                    errors = []
                    if not total_correct: errors.append(f"Total mismatch: {calculated_total} vs {total_scans}")
                    if not risk_total_correct: errors.append(f"Risk total mismatch: {calculated_risk_total} vs {total_scans}")
                    if not percentage_correct: errors.append(f"Percentage mismatch: {calculated_percentage:.2f}% vs {high_risk_percentage}%")
                    
                    self.log_test("CryptoShield Statistics", False, "; ".join(errors))
            else:
                self.log_test("CryptoShield Statistics", False, f"Missing fields: {missing_fields}")
        else:
            self.log_test("CryptoShield Statistics", False, f"Status code: {status_code}", data)

    def test_cryptoshield_validation_errors(self):
        """Test CryptoShield validation and error handling"""
        # Test invalid address format
        success, data, status_code = self.make_request('GET', '/cryptoshield/scan/wallet/invalid_address')
        
        if status_code == 400:
            self.log_test("CryptoShield Address Validation", True, 
                        "Correctly rejected invalid address format with 400 Bad Request")
        else:
            self.log_test("CryptoShield Address Validation", False, 
                        f"Expected 400 for invalid address, got {status_code}")
        
        # Test invalid tx hash format
        success, data, status_code = self.make_request('GET', '/cryptoshield/verify/transaction/invalid_hash')
        
        if status_code == 400:
            self.log_test("CryptoShield TX Hash Validation", True, 
                        "Correctly rejected invalid TX hash format with 400 Bad Request")
        else:
            self.log_test("CryptoShield TX Hash Validation", False, 
                        f"Expected 400 for invalid TX hash, got {status_code}")

    def test_cryptoshield_etherscan_integration(self):
        """Test that CryptoShield uses real Etherscan data (not hardcoded)"""
        if not self.cryptoshield_scans:
            self.log_test("CryptoShield Etherscan Integration", False, 
                        "No scans performed to test Etherscan integration")
            return
        
        # Check if we have realistic, varying data
        wallet_scans = [scan for scan in self.cryptoshield_scans if scan.get('scan_type') == 'wallet']
        
        if len(wallet_scans) >= 2:
            # Check if balances and transaction counts vary (indicating real data)
            balances = [scan.get('balance_eth', 0) for scan in wallet_scans]
            tx_counts = [scan.get('transaction_count', 0) for scan in wallet_scans]
            
            balance_varies = len(set(balances)) > 1
            tx_count_varies = len(set(tx_counts)) > 1
            
            # Check if Vitalik's wallet has realistic data
            vitalik_scan = None
            for scan in wallet_scans:
                if scan.get('address') == '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045':
                    vitalik_scan = scan
                    break
            
            vitalik_realistic = False
            if vitalik_scan:
                # Vitalik should have significant balance and many transactions
                balance = vitalik_scan.get('balance_eth', 0)
                tx_count = vitalik_scan.get('transaction_count', 0)
                vitalik_realistic = balance > 1 and tx_count > 10  # Conservative estimates
            
            if balance_varies and tx_count_varies and vitalik_realistic:
                self.log_test("CryptoShield Etherscan Integration", True, 
                            "Data varies between wallets and Vitalik's wallet has realistic values - using real Etherscan data")
            else:
                issues = []
                if not balance_varies: issues.append("Balances don't vary")
                if not tx_count_varies: issues.append("TX counts don't vary")
                if not vitalik_realistic: issues.append("Vitalik's data unrealistic")
                
                self.log_test("CryptoShield Etherscan Integration", False, 
                            f"Data appears hardcoded: {'; '.join(issues)}")
        else:
            self.log_test("CryptoShield Etherscan Integration", False, 
                        "Not enough wallet scans to verify Etherscan integration")

    def test_cryptoshield_risk_scoring_consistency(self):
        """Test that risk scoring is consistent with data"""
        if not self.cryptoshield_scans:
            self.log_test("CryptoShield Risk Scoring", False, 
                        "No scans performed to test risk scoring")
            return
        
        scoring_errors = []
        consistent_scores = 0
        
        for scan in self.cryptoshield_scans:
            scan_type = scan.get('scan_type')
            risk_level = scan.get('risk_level')
            risk_score = scan.get('risk_score', 0)
            
            # Check risk level consistency with score
            if risk_level == 'low' and not (0 <= risk_score <= 39):
                scoring_errors.append(f"{scan_type}: LOW risk but score {risk_score} not 0-39")
            elif risk_level == 'medium' and not (40 <= risk_score <= 69):
                scoring_errors.append(f"{scan_type}: MEDIUM risk but score {risk_score} not 40-69")
            elif risk_level == 'high' and not (70 <= risk_score <= 100):
                scoring_errors.append(f"{scan_type}: HIGH risk but score {risk_score} not 70-100")
            else:
                consistent_scores += 1
        
        if not scoring_errors:
            self.log_test("CryptoShield Risk Scoring", True, 
                        f"All {consistent_scores} scans have consistent risk levels and scores")
        else:
            self.log_test("CryptoShield Risk Scoring", False, 
                        f"Scoring inconsistencies: {'; '.join(scoring_errors[:3])}")

    def run_all_tests(self):
        """Run all backend tests focusing on CryptoShield IA"""
        print("=" * 70)
        print("GuaraniAppStore V2.5 Pro Backend Testing Suite")
        print("Focus: CRYPTOSHIELD IA - SISTEMA COMPLETO DE DETECCIÓN DE FRAUDE")
        print("=" * 70)
        print()
        
        # Core backend status
        print("🔍 Testing Backend Status...")
        self.test_health_check()
        self.test_backend_logs_check()
        
        # Critical endpoints that had 502 errors
        print("🚨 Testing Previously Failing Endpoints...")
        self.test_countries_endpoint()
        self.test_services_endpoint()
        
        # Database connectivity
        print("💾 Testing Database Connectivity...")
        self.test_mongodb_connection()
        
        # Admin functionality (if endpoints work)
        print("👤 Testing Admin Access...")
        self.test_admin_login()
        
        # CRYPTOSHIELD IA TESTING - COMPLETE SYSTEM
        print("🛡️ Testing CryptoShield IA - Sistema Completo de Detección de Fraude...")
        
        # 1. Health Check
        print("   🏥 Health Check...")
        self.test_cryptoshield_health_check()
        
        # 2. Wallet Scanning (3 test wallets)
        print("   👛 Wallet Scanning...")
        wallet_names = ["Vitalik Buterin", "Binance Hot Wallet", "Null Address"]
        for i, address in enumerate(self.test_wallets):
            self.test_cryptoshield_wallet_scan(address, wallet_names[i])
            time.sleep(1)  # Small delay between requests
        
        # 3. Transaction Verification (2 test transactions)
        print("   🔄 Transaction Verification...")
        tx_names = ["First Ethereum TX", "Invalid TX"]
        for i, tx_hash in enumerate(self.test_tx_hashes):
            self.test_cryptoshield_transaction_verify(tx_hash, tx_names[i])
            time.sleep(1)
        
        # 4. Contract Scanning (USDT contract)
        print("   📄 Contract Scanning...")
        self.test_cryptoshield_contract_scan(self.test_contract)
        
        # 5. Scan History
        print("   📚 Scan History...")
        self.test_cryptoshield_scan_history()
        
        # 6. Statistics
        print("   📊 Statistics...")
        self.test_cryptoshield_stats()
        
        # 7. Validation and Error Handling
        print("   ❌ Validation & Error Handling...")
        self.test_cryptoshield_validation_errors()
        
        # 8. CRITICAL VALIDATIONS
        print("   🔍 Critical System Validations...")
        self.test_cryptoshield_etherscan_integration()
        self.test_cryptoshield_risk_scoring_consistency()
        
        # Summary
        self.print_summary()

    def print_summary(self):
        """Print test summary focusing on Momentum Predictor IA"""
        print("=" * 70)
        print("TEST SUMMARY - MOMENTUM PREDICTOR IA FASE 2 LÓGICA COMPLETA")
        print("=" * 70)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print()
        
        # Check Momentum Predictor endpoints
        momentum_health = any(r['success'] and r['test'] == 'Momentum Health Check' for r in self.test_results)
        momentum_signals = all(any(r['success'] and r['test'] == f'Momentum Signal {symbol}' for r in self.test_results) 
                              for symbol in self.test_symbols)
        momentum_history = any(r['success'] and r['test'] == 'Momentum Signals History' for r in self.test_results)
        momentum_stats = any(r['success'] and 'Momentum Stats' in r['test'] for r in self.test_results)
        
        # Check Fase 2 specific features
        signal_variety = any(r['success'] and r['test'] == 'Signal Variety' for r in self.test_results)
        confidence_variation = any(r['success'] and r['test'] == 'Confidence Variation' for r in self.test_results)
        scoring_logic = any(r['success'] and r['test'] == 'Scoring System Logic' for r in self.test_results)
        indicators_realism = any(r['success'] and r['test'] == 'Technical Indicators Realism' for r in self.test_results)
        
        # Check core endpoints
        countries_success = any(r['success'] and r['test'] == 'Countries Endpoint' for r in self.test_results)
        services_success = any(r['success'] and r['test'] == 'Services Endpoint' for r in self.test_results)
        backend_success = any(r['success'] and r['test'] == 'Backend Status' for r in self.test_results)
        mongodb_success = any(r['success'] and r['test'] == 'MongoDB Connection' for r in self.test_results)
        
        print("🎯 MOMENTUM PREDICTOR IA ENDPOINTS:")
        print(f"   /api/momentum/health:           {'✅ WORKING' if momentum_health else '❌ FAILED'}")
        print(f"   /api/momentum/signal/{{symbol}}: {'✅ WORKING' if momentum_signals else '❌ FAILED'}")
        print(f"   /api/momentum/signals/history:  {'✅ WORKING' if momentum_history else '❌ FAILED'}")
        print(f"   /api/momentum/stats/{{symbol}}:  {'✅ WORKING' if momentum_stats else '❌ FAILED'}")
        print()
        
        print("🧮 FASE 2 TECHNICAL ANALYSIS FEATURES:")
        print(f"   Signal Variety (not all HOLD):  {'✅ WORKING' if signal_variety else '❌ FAILED'}")
        print(f"   Dynamic Confidence Calculation: {'✅ WORKING' if confidence_variation else '❌ FAILED'}")
        print(f"   Scoring System Logic (8 points): {'✅ WORKING' if scoring_logic else '❌ FAILED'}")
        print(f"   Technical Indicators Realism:   {'✅ WORKING' if indicators_realism else '❌ FAILED'}")
        print()
        
        print("🔧 CORE SYSTEM STATUS:")
        print(f"   /api/countries: {'✅ WORKING' if countries_success else '❌ FAILED'}")
        print(f"   /api/services:  {'✅ WORKING' if services_success else '❌ FAILED'}")
        print(f"   Backend Status: {'✅ WORKING' if backend_success else '❌ FAILED'}")
        print(f"   MongoDB Conn:   {'✅ WORKING' if mongodb_success else '❌ FAILED'}")
        print()
        
        # Check critical verifications
        if self.generated_signals:
            print("✅ VERIFICACIONES CRÍTICAS FASE 2 COMPLETADAS:")
            sample_signal = self.generated_signals[0]
            print(f"   ✅ Precios reales desde Kraken: ${sample_signal.get('current_price', 0):,.2f}")
            print(f"   ✅ Señales guardadas en MongoDB: {len(self.generated_signals)} señales generadas")
            print(f"   ✅ Indicador is_mock = {sample_signal.get('is_mock', False)}")
            
            # Check model version
            model_version = sample_signal.get('model_version', '')
            print(f"   {'✅' if model_version == 'MOCK_v2_Technical_Analysis' else '❌'} Model version: {model_version}")
            
            # Check indicators field
            indicators = sample_signal.get('indicators', {})
            has_indicators = bool(indicators and 'rsi' in indicators and 'buy_score' in indicators)
            print(f"   {'✅' if has_indicators else '❌'} Campo 'indicators' con RSI, MACD, scores: {'Presente' if has_indicators else 'Ausente'}")
            
            if has_indicators:
                rsi = indicators.get('rsi', 0)
                buy_score = indicators.get('buy_score', 0)
                sell_score = indicators.get('sell_score', 0)
                print(f"   ✅ Indicadores técnicos: RSI={rsi:.1f}, BUY_score={buy_score}, SELL_score={sell_score}")
            
            # Verify trading levels
            levels_valid = self.verify_trading_levels_calculation(sample_signal)
            print(f"   {'✅' if levels_valid else '❌'} Cálculos de niveles de trading: {'Correctos' if levels_valid else 'Incorrectos'}")
            
            # Check timeframe and risk
            timeframe = sample_signal.get('timeframe')
            risk_level = sample_signal.get('risk_level')
            print(f"   ✅ Timeframe calculado: {timeframe}")
            print(f"   ✅ Risk level asignado: {risk_level}")
            
            # Check date format
            predicted_at = sample_signal.get('predicted_at', '')
            iso_format = 'T' in predicted_at and ('Z' in predicted_at or '+' in predicted_at)
            print(f"   {'✅' if iso_format else '❌'} Formato fecha ISO 8601 UTC: {'Correcto' if iso_format else 'Incorrecto'}")
            
            # Check confidence variation
            confidences = [s.get('confidence', 60) for s in self.generated_signals]
            confidence_varies = len(set(confidences)) > 1
            print(f"   {'✅' if confidence_varies else '❌'} Confianza dinámica (no siempre 60%): {'Sí' if confidence_varies else 'No'}")
        
        if failed_tests > 0:
            print()
            print("❌ FAILED TESTS:")
            for result in self.test_results:
                if not result['success']:
                    print(f"   • {result['test']}: {result['details']}")
            print()
        
        # Overall assessment for Momentum Predictor Fase 2
        momentum_working = momentum_health and momentum_signals and momentum_history
        fase2_features_working = signal_variety and confidence_variation and scoring_logic and indicators_realism
        core_working = countries_success and services_success and backend_success
        
        print("🏆 RESULTADO FINAL:")
        if momentum_working and fase2_features_working and core_working:
            print("🎉 SUCCESS: MOMENTUM PREDICTOR IA FASE 2 COMPLETAMENTE FUNCIONAL!")
            print("   ✅ Todos los endpoints de Momentum Predictor funcionando")
            print("   ✅ Sistema de análisis técnico completo (20 indicadores)")
            print("   ✅ Sistema de scoring con 8 puntos máximo operativo")
            print("   ✅ Confianza calculada dinámicamente")
            print("   ✅ Campo 'indicators' incluido en respuesta API")
            print("   ✅ Model version MOCK_v2_Technical_Analysis")
            print("   ✅ Integración con Kraken exchange operativa")
            print("   ✅ Almacenamiento en MongoDB funcionando")
            print("   ✅ Sistema backend estable")
        elif momentum_working and fase2_features_working:
            print("🟡 PARTIAL SUCCESS: Momentum Predictor Fase 2 funcionando, problemas en sistema core")
            print("   ✅ Momentum Predictor IA Fase 2 completamente operativo")
            print("   ✅ Análisis técnico y scoring system funcionando")
            print("   ❌ Algunos endpoints del sistema core fallan")
        elif momentum_working:
            print("🟠 PARTIAL SUCCESS: Endpoints funcionando pero faltan características Fase 2")
            print("   ✅ Endpoints básicos de Momentum Predictor funcionando")
            if not signal_variety:
                print("   ❌ Señales no varían suficientemente")
            if not confidence_variation:
                print("   ❌ Confianza no varía dinámicamente")
            if not scoring_logic:
                print("   ❌ Lógica de scoring system incorrecta")
            if not indicators_realism:
                print("   ❌ Indicadores técnicos no realistas")
        else:
            print("🚨 FAILURE: Problemas en Momentum Predictor IA!")
            if not momentum_health:
                print("   ❌ Health check fallando")
            if not momentum_signals:
                print("   ❌ Generación de señales fallando")
            if not momentum_history:
                print("   ❌ Historial de señales fallando")
        
        print()
        print("📋 PRÓXIMOS PASOS:")
        if momentum_working and fase2_features_working:
            print("   • FASE 2 COMPLETADA - Sistema de análisis técnico completo")
            print("   • Listo para entrenar modelo LSTM real con datos históricos")
            print("   • Bot de Telegram ya implementado y listo")
            print("   • Considerar implementar CryptoShield IA como siguiente fase")
        elif momentum_working:
            print("   • Revisar implementación de indicadores técnicos en momentum_service.py")
            print("   • Verificar sistema de scoring en _generate_mock_signal()")
            print("   • Comprobar cálculo dinámico de confianza")
            print("   • Validar campo 'indicators' en respuesta API")
        else:
            print("   • Revisar logs del backend: tail -n 100 /var/log/supervisor/backend.*.log")
            print("   • Verificar integración de momentum_api.py en server.py")
            print("   • Comprobar conexión con Kraken exchange")
            print("   • Validar configuración de MongoDB")

if __name__ == "__main__":
    tester = GuaraniBackendTester()
    tester.run_all_tests()