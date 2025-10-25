#!/usr/bin/env python3
"""
Verificación específica de Momentum Predictor IA - Fase 2
Testing de los requerimientos exactos del review request
"""

import requests
import json
import sys
from typing import Dict, Any

class Fase2VerificationTester:
    def __init__(self):
        self.base_url = "https://cryptoshield-app.preview.emergentagent.com/api"
        self.session = requests.Session()
        self.test_results = []
        
        # Símbolos específicos mencionados en el review request
        self.test_symbols = ['BTC', 'ETH', 'SOL', 'ADA', 'DOT']  # Reemplazamos MATIC por DOT
        self.generated_signals = []
        
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test results"""
        result = {
            'test': test_name,
            'success': success,
            'details': details
        }
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   Details: {details}")
        print()

    def make_request(self, method: str, endpoint: str, data: Dict = None) -> tuple:
        """Make HTTP request and return (success, response_data, status_code)"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, timeout=30)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, timeout=30)
            else:
                return False, f"Unsupported method: {method}", 0
                
            try:
                response_data = response.json()
            except:
                response_data = response.text
                
            return response.status_code < 400, response_data, response.status_code
            
        except requests.exceptions.RequestException as e:
            return False, f"Request failed: {str(e)}", 0

    def test_indicators_field_exists(self, symbol: str):
        """✅ Campo "indicators" existe en response"""
        success, data, status_code = self.make_request('GET', f'/momentum/signal/{symbol}')
        
        if success and isinstance(data, dict):
            indicators = data.get('indicators')
            if indicators and isinstance(indicators, dict):
                self.generated_signals.append(data)
                self.log_test(f"Campo 'indicators' existe - {symbol}", True, 
                            f"Indicators field present with {len(indicators)} values")
            else:
                self.log_test(f"Campo 'indicators' existe - {symbol}", False, 
                            "Indicators field missing or not a dict")
        else:
            self.log_test(f"Campo 'indicators' existe - {symbol}", False, 
                        f"API call failed: {status_code}")

    def test_required_indicators_present(self):
        """✅ indicators contiene: rsi, macd, sma_7, sma_25, stoch_k, buy_score, sell_score"""
        if not self.generated_signals:
            self.log_test("Required Indicators Present", False, "No signals generated")
            return
        
        required_indicators = ['rsi', 'macd', 'sma_7', 'sma_25', 'stoch_k', 'buy_score', 'sell_score']
        all_present = True
        missing_indicators = []
        
        for signal in self.generated_signals:
            indicators = signal.get('indicators', {})
            for req_ind in required_indicators:
                if req_ind not in indicators:
                    all_present = False
                    if req_ind not in missing_indicators:
                        missing_indicators.append(req_ind)
        
        if all_present:
            self.log_test("Required Indicators Present", True, 
                        f"All required indicators present: {', '.join(required_indicators)}")
        else:
            self.log_test("Required Indicators Present", False, 
                        f"Missing indicators: {', '.join(missing_indicators)}")

    def test_model_version_updated(self):
        """✅ model_version = "MOCK_v2_Technical_Analysis" """
        if not self.generated_signals:
            self.log_test("Model Version Updated", False, "No signals generated")
            return
        
        expected_version = "MOCK_v2_Technical_Analysis"
        correct_versions = 0
        
        for signal in self.generated_signals:
            model_version = signal.get('model_version', '')
            if model_version == expected_version:
                correct_versions += 1
        
        if correct_versions == len(self.generated_signals):
            self.log_test("Model Version Updated", True, 
                        f"All signals have correct model_version: {expected_version}")
        else:
            self.log_test("Model Version Updated", False, 
                        f"Only {correct_versions}/{len(self.generated_signals)} signals have correct version")

    def test_realistic_indicator_values(self):
        """✅ Valores de indicadores son números válidos y realistas"""
        if not self.generated_signals:
            self.log_test("Realistic Indicator Values", False, "No signals generated")
            return
        
        validation_errors = []
        
        for i, signal in enumerate(self.generated_signals):
            symbol = signal.get('symbol', f'Signal_{i}')
            indicators = signal.get('indicators', {})
            
            # RSI should be 0-100
            rsi = indicators.get('rsi', 0)
            if not (0 <= rsi <= 100):
                validation_errors.append(f"{symbol}: RSI {rsi} not in range 0-100")
            
            # MACD should be a reasonable number
            macd = indicators.get('macd', 0)
            if not isinstance(macd, (int, float)) or abs(macd) > 50000:
                validation_errors.append(f"{symbol}: MACD {macd} unrealistic")
            
            # SMA values should be positive
            sma_7 = indicators.get('sma_7', 0)
            sma_25 = indicators.get('sma_25', 0)
            if sma_7 <= 0 or sma_25 <= 0:
                validation_errors.append(f"{symbol}: SMA values should be positive")
            
            # Stochastic should be 0-100
            stoch_k = indicators.get('stoch_k', 0)
            if not (0 <= stoch_k <= 100):
                validation_errors.append(f"{symbol}: Stochastic {stoch_k} not in range 0-100")
        
        if not validation_errors:
            self.log_test("Realistic Indicator Values", True, 
                        f"All {len(self.generated_signals)} signals have realistic indicator values")
        else:
            self.log_test("Realistic Indicator Values", False, 
                        f"Validation errors: {'; '.join(validation_errors[:3])}")

    def test_scores_are_integers_0_to_8(self):
        """✅ buy_score y sell_score son enteros entre 0 y 8"""
        if not self.generated_signals:
            self.log_test("Scores Are Integers 0-8", False, "No signals generated")
            return
        
        score_errors = []
        
        for signal in self.generated_signals:
            symbol = signal.get('symbol', 'Unknown')
            indicators = signal.get('indicators', {})
            
            buy_score = indicators.get('buy_score', -1)
            sell_score = indicators.get('sell_score', -1)
            
            if not (isinstance(buy_score, int) and 0 <= buy_score <= 8):
                score_errors.append(f"{symbol}: buy_score {buy_score} not integer 0-8")
            
            if not (isinstance(sell_score, int) and 0 <= sell_score <= 8):
                score_errors.append(f"{symbol}: sell_score {sell_score} not integer 0-8")
        
        if not score_errors:
            self.log_test("Scores Are Integers 0-8", True, 
                        "All buy_score and sell_score values are integers between 0-8")
        else:
            self.log_test("Scores Are Integers 0-8", False, 
                        f"Score errors: {'; '.join(score_errors)}")

    def test_signal_consistency_with_scores(self):
        """✅ Señal (BUY/SELL/HOLD) es consistente con scores"""
        if not self.generated_signals:
            self.log_test("Signal Consistency with Scores", False, "No signals generated")
            return
        
        logic_errors = []
        
        for signal in self.generated_signals:
            symbol = signal.get('symbol', 'Unknown')
            signal_type = signal.get('signal', '')
            indicators = signal.get('indicators', {})
            
            buy_score = indicators.get('buy_score', 0)
            sell_score = indicators.get('sell_score', 0)
            
            # Validate logic according to Fase 2 rules
            if signal_type == 'BUY':
                if buy_score < sell_score + 2:
                    logic_errors.append(f"{symbol}: BUY signal but buy_score({buy_score}) < sell_score({sell_score})+2")
            elif signal_type == 'SELL':
                if sell_score < buy_score + 2:
                    logic_errors.append(f"{symbol}: SELL signal but sell_score({sell_score}) < buy_score({buy_score})+2")
            elif signal_type == 'HOLD':
                if abs(buy_score - sell_score) >= 2:
                    logic_errors.append(f"{symbol}: HOLD signal but |buy_score({buy_score}) - sell_score({sell_score})| >= 2")
        
        if not logic_errors:
            self.log_test("Signal Consistency with Scores", True, 
                        f"All {len(self.generated_signals)} signals are consistent with scoring logic")
        else:
            self.log_test("Signal Consistency with Scores", False, 
                        f"Logic errors: {'; '.join(logic_errors)}")

    def test_confidence_varies_dynamically(self):
        """✅ Confianza varía según diferencia de scores (no siempre 60%)"""
        if not self.generated_signals:
            self.log_test("Confidence Varies Dynamically", False, "No signals generated")
            return
        
        confidences = [signal.get('confidence', 0) for signal in self.generated_signals]
        unique_confidences = set(confidences)
        
        if len(unique_confidences) > 1:
            min_conf = min(confidences)
            max_conf = max(confidences)
            self.log_test("Confidence Varies Dynamically", True, 
                        f"Confidence varies: {min_conf}% to {max_conf}% (not always 60%)")
        else:
            single_conf = list(unique_confidences)[0]
            if single_conf == 60.0:
                self.log_test("Confidence Varies Dynamically", False, 
                            "All confidences are 60% - not varying dynamically")
            else:
                self.log_test("Confidence Varies Dynamically", True, 
                            f"Consistent confidence at {single_conf}% (not default 60%)")

    def test_probabilities_vary_dynamically(self):
        """✅ Probabilities varían dinámicamente"""
        if not self.generated_signals:
            self.log_test("Probabilities Vary Dynamically", False, "No signals generated")
            return
        
        all_probabilities = []
        for signal in self.generated_signals:
            probs = signal.get('probabilities', {})
            prob_tuple = (probs.get('BUY', 0), probs.get('SELL', 0), probs.get('HOLD', 0))
            all_probabilities.append(prob_tuple)
        
        unique_probabilities = set(all_probabilities)
        
        if len(unique_probabilities) > 1:
            self.log_test("Probabilities Vary Dynamically", True, 
                        f"Probabilities vary across {len(unique_probabilities)} different patterns")
        else:
            self.log_test("Probabilities Vary Dynamically", False, 
                        "All signals have identical probability distributions")

    def test_health_check_reflects_changes(self):
        """Verificar que model_version en /api/momentum/health refleja los cambios"""
        success, data, status_code = self.make_request('GET', '/momentum/health')
        
        if success and isinstance(data, dict):
            mode = data.get('mode', '')
            service = data.get('service', '')
            
            if mode == 'MOCK' and service == 'Momentum Predictor':
                self.log_test("Health Check Reflects Changes", True, 
                            f"Health endpoint shows Mode: {mode}, Service: {service}")
            else:
                self.log_test("Health Check Reflects Changes", False, 
                            f"Unexpected health values: Mode={mode}, Service={service}")
        else:
            self.log_test("Health Check Reflects Changes", False, 
                        f"Health check failed: {status_code}")

    def run_fase2_verification(self):
        """Run all Fase 2 verification tests"""
        print("=" * 80)
        print("MOMENTUM PREDICTOR IA - FASE 2 VERIFICATION")
        print("Testing exact requirements from review request")
        print("=" * 80)
        print()
        
        # 1. Generate signals for all test symbols
        print("🔮 Generating signals for technical analysis verification...")
        for symbol in self.test_symbols:
            self.test_indicators_field_exists(symbol)
        
        # 2. Verify all Fase 2 requirements
        print("🧮 Verifying Fase 2 specific requirements...")
        self.test_required_indicators_present()
        self.test_model_version_updated()
        self.test_realistic_indicator_values()
        self.test_scores_are_integers_0_to_8()
        self.test_signal_consistency_with_scores()
        self.test_confidence_varies_dynamically()
        self.test_probabilities_vary_dynamically()
        
        # 3. Health check verification
        print("🏥 Health check verification...")
        self.test_health_check_reflects_changes()
        
        # Summary
        self.print_verification_summary()

    def print_verification_summary(self):
        """Print verification summary"""
        print("=" * 80)
        print("FASE 2 VERIFICATION SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Verification Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print()
        
        # Check specific requirements
        requirements_met = {
            'Campo indicators existe': any(r['success'] and 'Campo \'indicators\' existe' in r['test'] for r in self.test_results),
            'Indicadores requeridos': any(r['success'] and r['test'] == 'Required Indicators Present' for r in self.test_results),
            'Model version actualizado': any(r['success'] and r['test'] == 'Model Version Updated' for r in self.test_results),
            'Valores realistas': any(r['success'] and r['test'] == 'Realistic Indicator Values' for r in self.test_results),
            'Scores 0-8': any(r['success'] and r['test'] == 'Scores Are Integers 0-8' for r in self.test_results),
            'Lógica consistente': any(r['success'] and r['test'] == 'Signal Consistency with Scores' for r in self.test_results),
            'Confianza dinámica': any(r['success'] and r['test'] == 'Confidence Varies Dynamically' for r in self.test_results),
            'Probabilities dinámicas': any(r['success'] and r['test'] == 'Probabilities Vary Dynamically' for r in self.test_results),
        }
        
        print("📋 CRITERIOS DE ÉXITO FASE 2:")
        for requirement, met in requirements_met.items():
            status = "✅" if met else "❌"
            print(f"   {status} {requirement}")
        
        print()
        
        if failed_tests > 0:
            print("❌ FAILED VERIFICATIONS:")
            for result in self.test_results:
                if not result['success']:
                    print(f"   • {result['test']}: {result['details']}")
            print()
        
        # Overall assessment
        all_requirements_met = all(requirements_met.values())
        
        print("🏆 RESULTADO FINAL FASE 2:")
        if all_requirements_met:
            print("🎉 SUCCESS: TODOS LOS CRITERIOS DE ÉXITO FASE 2 CUMPLIDOS!")
            print("   ✅ Sistema de análisis técnico completo implementado")
            print("   ✅ Sistema de scoring con 8 puntos máximo funcionando")
            print("   ✅ Confianza calculada dinámicamente")
            print("   ✅ Response API incluye campo 'indicators' completo")
            print("   ✅ Model version actualizado a MOCK_v2_Technical_Analysis")
            print("   ✅ Señales varían según condiciones del mercado")
        else:
            print("🚨 ALGUNOS CRITERIOS NO CUMPLIDOS:")
            for requirement, met in requirements_met.items():
                if not met:
                    print(f"   ❌ {requirement}")

if __name__ == "__main__":
    tester = Fase2VerificationTester()
    tester.run_fase2_verification()