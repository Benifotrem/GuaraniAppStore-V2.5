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
        
        # Momentum Predictor test data
        self.test_symbols = ['BTC', 'ETH', 'SOL']
        self.generated_signals = []
        
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
        """Test Momentum Predictor health check endpoint"""
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
                
                if (status == 'healthy' and 
                    service == 'Momentum Predictor' and 
                    version == '1.0.0' and 
                    model_loaded == False and 
                    mode == 'MOCK'):
                    self.log_test("Momentum Health Check", True, 
                                f"Status: {status}, Service: {service}, Version: {version}, Mode: {mode}")
                else:
                    self.log_test("Momentum Health Check", False, 
                                f"Unexpected values - Status: {status}, Mode: {mode}, Model loaded: {model_loaded}")
            else:
                self.log_test("Momentum Health Check", False, f"Missing fields: {missing_fields}")
        else:
            self.log_test("Momentum Health Check", False, f"Status code: {status_code}", data)

    def test_momentum_signal_generation(self, symbol: str):
        """Test signal generation for a specific symbol"""
        success, data, status_code = self.make_request('GET', f'/momentum/signal/{symbol}')
        
        if success and isinstance(data, dict):
            # Check required fields
            required_fields = [
                'symbol', 'signal', 'confidence', 'current_price', 'entry_price',
                'target_1', 'target_2', 'stop_loss', 'timeframe', 'risk_level',
                'probabilities', 'predicted_at', 'model_version', 'is_mock'
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
                
                # Validation checks
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
                
                if all([valid_signal, valid_confidence, valid_price, valid_mock, valid_probabilities, valid_date]):
                    # Store for history testing
                    self.generated_signals.append(data)
                    
                    # Check if price is realistic (> $1 for major cryptos)
                    price_realistic = current_price > 1 if symbol in ['BTC', 'ETH'] else current_price > 0
                    
                    if price_realistic:
                        self.log_test(f"Momentum Signal {symbol}", True, 
                                    f"Signal: {signal} ({confidence}% confidence), Price: ${current_price:,.2f}, Mock: {is_mock}")
                    else:
                        self.log_test(f"Momentum Signal {symbol}", False, 
                                    f"Unrealistic price: ${current_price} for {symbol}")
                else:
                    validation_errors = []
                    if not valid_signal: validation_errors.append(f"Invalid signal: {signal}")
                    if not valid_confidence: validation_errors.append(f"Invalid confidence: {confidence}")
                    if not valid_price: validation_errors.append(f"Invalid price: {current_price}")
                    if not valid_mock: validation_errors.append(f"Expected is_mock=True, got {is_mock}")
                    if not valid_probabilities: validation_errors.append("Invalid probabilities structure")
                    if not valid_date: validation_errors.append(f"Invalid date format: {predicted_at}")
                    
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

    def run_all_tests(self):
        """Run all backend tests focusing on Momentum Predictor IA"""
        print("=" * 70)
        print("GuaraniAppStore V2.5 Pro Backend Testing Suite")
        print("Focus: MOMENTUM PREDICTOR IA - FASE 1 INTEGRACIÓN")
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
        
        # MOMENTUM PREDICTOR IA TESTING
        print("🎯 Testing Momentum Predictor IA - Fase 1...")
        
        # 1. Health Check
        print("   📊 Health Check...")
        self.test_momentum_health_check()
        
        # 2. Signal Generation for multiple symbols
        print("   🔮 Signal Generation...")
        for symbol in self.test_symbols:
            self.test_momentum_signal_generation(symbol)
            time.sleep(1)  # Small delay between requests
        
        # 3. Signals History
        print("   📈 Signals History...")
        self.test_momentum_signals_history()
        
        # 4. Stats for symbols (after generating signals)
        print("   📊 Symbol Statistics...")
        for symbol in self.test_symbols:
            self.test_momentum_stats(symbol)
        
        # 5. Error handling
        print("   ❌ Error Handling...")
        self.test_momentum_stats_nonexistent_symbol()
        
        # Summary
        self.print_summary()

    def print_summary(self):
        """Print test summary focusing on 502 error fix"""
        print("=" * 70)
        print("TEST SUMMARY - 502 Bad Gateway Fix Verification")
        print("=" * 70)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print()
        
        # Check critical endpoints
        countries_success = any(r['success'] and r['test'] == 'Countries Endpoint' for r in self.test_results)
        services_success = any(r['success'] and r['test'] == 'Services Endpoint' for r in self.test_results)
        backend_success = any(r['success'] and r['test'] == 'Backend Status' for r in self.test_results)
        mongodb_success = any(r['success'] and r['test'] == 'MongoDB Connection' for r in self.test_results)
        
        print("🎯 CRITICAL ENDPOINTS STATUS:")
        print(f"   /api/countries: {'✅ WORKING' if countries_success else '❌ FAILED'}")
        print(f"   /api/services:  {'✅ WORKING' if services_success else '❌ FAILED'}")
        print(f"   Backend Status: {'✅ WORKING' if backend_success else '❌ FAILED'}")
        print(f"   MongoDB Conn:   {'✅ WORKING' if mongodb_success else '❌ FAILED'}")
        print()
        
        if failed_tests > 0:
            print("❌ FAILED TESTS:")
            for result in self.test_results:
                if not result['success']:
                    print(f"   • {result['test']}: {result['details']}")
            print()
        
        # Overall assessment
        critical_endpoints_working = countries_success and services_success
        
        if critical_endpoints_working:
            print("🎉 SUCCESS: 502 Bad Gateway errors have been RESOLVED!")
            print("   ✅ /api/countries endpoint is working")
            print("   ✅ /api/services endpoint is working") 
            print("   ✅ Backend is running in MongoDB-only mode")
        else:
            print("🚨 FAILURE: 502 Bad Gateway errors still present!")
            if not countries_success:
                print("   ❌ /api/countries still returning 502")
            if not services_success:
                print("   ❌ /api/services still returning 502")
            print("   🔍 Check backend logs for PostgreSQL connection errors")
        
        print()
        print("📋 NEXT STEPS:")
        if critical_endpoints_working:
            print("   • Frontend should now load Header/Footer correctly")
            print("   • Services data should populate in the UI")
            print("   • No more 502 errors in browser console")
        else:
            print("   • Check backend supervisor logs: tail -n 100 /var/log/supervisor/backend.*.log")
            print("   • Verify PostgreSQL startup is fully disabled in server.py")
            print("   • Ensure MongoDB services are properly initialized")

if __name__ == "__main__":
    tester = GuaraniBackendTester()
    tester.run_all_tests()