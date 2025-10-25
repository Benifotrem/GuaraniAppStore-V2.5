import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
const API = `${BACKEND_URL}/api`;

const SuiteCryptoDashboard = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [suiteData, setSuiteData] = useState(null);
  const [activeService, setActiveService] = useState('overview');
  
  // CryptoShield states
  const [walletAddress, setWalletAddress] = useState('');
  const [txHash, setTxHash] = useState('');
  const [scanResult, setScanResult] = useState(null);
  const [scanLoading, setScanLoading] = useState(false);
  const [scanHistory, setScanHistory] = useState([]);
  const [cryptoshieldStats, setCryptoshieldStats] = useState(null);
  
  // Momentum states
  const [cryptoSymbol, setCryptoSymbol] = useState('BTC');
  const [signal, setSignal] = useState(null);
  const [signalLoading, setSignalLoading] = useState(false);
  const [signalHistory, setSignalHistory] = useState([]);
  const [momentumStats, setMomentumStats] = useState(null);
  
  // Pulse states
  const [pulseData, setPulseData] = useState(null);
  const [pulseLoading, setPulseLoading] = useState(false);

  useEffect(() => {
    loadSuiteData();
  }, []);

  useEffect(() => {
    if (activeService === 'cryptoshield-ia') {
      loadCryptoShieldHistory();
      loadCryptoShieldStats();
    } else if (activeService === 'momentum-predictor-ia') {
      loadSignalHistory();
      loadMomentumStats();
    } else if (activeService === 'pulse-ia') {
      loadPulseData();
    }
  }, [activeService]);

  const loadSuiteData = async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/');
      return;
    }

    try {
      const response = await axios.get(`${API}/suite-crypto/services-list`);
      setSuiteData(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error loading suite data:', error);
      setLoading(false);
    }
  };

  const loadCryptoShieldHistory = async () => {
    try {
      const response = await axios.get(`${API}/cryptoshield/scans/history?limit=10`);
      setScanHistory(response.data);
    } catch (error) {
      console.error('Error loading scan history:', error);
    }
  };

  const loadCryptoShieldStats = async () => {
    try {
      const response = await axios.get(`${API}/cryptoshield/stats`);
      setCryptoshieldStats(response.data);
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  };

  const loadSignalHistory = async () => {
    try {
      const response = await axios.get(`${API}/momentum/signals/history?limit=10`);
      setSignalHistory(response.data);
    } catch (error) {
      console.error('Error loading signal history:', error);
    }
  };

  const loadMomentumStats = async () => {
    try {
      const response = await axios.get(`${API}/momentum/stats/${cryptoSymbol}`);
      setMomentumStats(response.data);
    } catch (error) {
      console.error('Error loading momentum stats:', error);
    }
  };

  const loadPulseData = async () => {
    setPulseLoading(true);
    try {
      // Simular datos de sentimiento para el gráfico
      const mockData = [
        { date: '24/10', sentiment: 65, fomo: 45, fud: 30 },
        { date: '25/10', sentiment: 72, fomo: 55, fud: 25 },
        { date: '26/10', sentiment: 58, fomo: 35, fud: 40 },
        { date: '27/10', sentiment: 75, fomo: 60, fud: 20 },
        { date: '28/10', sentiment: 68, fomo: 50, fud: 28 },
        { date: '29/10', sentiment: 80, fomo: 70, fud: 15 },
        { date: '30/10', sentiment: 85, fomo: 75, fud: 10 }
      ];
      setPulseData(mockData);
    } catch (error) {
      console.error('Error loading pulse data:', error);
    } finally {
      setPulseLoading(false);
    }
  };

  const scanWallet = async () => {
    if (!walletAddress || walletAddress.length !== 42) {
      alert('Por favor ingresa una dirección Ethereum válida (42 caracteres)');
      return;
    }

    setScanLoading(true);
    try {
      const response = await axios.get(`${API}/cryptoshield/scan/wallet/${walletAddress}`);
      setScanResult(response.data);
    } catch (error) {
      console.error('Error scanning wallet:', error);
      alert('Error al escanear la wallet');
    } finally {
      setScanLoading(false);
    }
  };

  const verifyTransaction = async () => {
    if (!txHash || txHash.length !== 66) {
      alert('Por favor ingresa un hash de transacción válido (66 caracteres)');
      return;
    }

    setScanLoading(true);
    try {
      const response = await axios.get(`${API}/cryptoshield/verify/transaction/${txHash}`);
      setScanResult(response.data);
    } catch (error) {
      console.error('Error verifying transaction:', error);
      alert('Error al verificar la transacción');
    } finally {
      setScanLoading(false);
    }
  };

  const getSignal = async () => {
    setSignalLoading(true);
    try {
      const response = await axios.get(`${API}/momentum/signal/${cryptoSymbol}`);
      setSignal(response.data);
    } catch (error) {
      console.error('Error getting signal:', error);
      alert('Error al obtener la señal');
    } finally {
      setSignalLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center">
        <div className="text-white text-xl">Cargando Suite Crypto IA...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 py-8 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <button 
            onClick={() => navigate('/dashboard')}
            className="text-white/70 hover:text-white mb-4 flex items-center gap-2"
          >
            ← Volver al Dashboard
          </button>
          <h1 className="text-4xl font-bold text-white mb-2">Suite Crypto IA</h1>
          <p className="text-white/70">3 servicios especializados para el mundo cripto</p>
        </div>

        {/* Services Overview */}
        {activeService === 'overview' && suiteData && (
          <div className="grid md:grid-cols-3 gap-6 mb-8">
            {suiteData.services.map((service) => (
              <div 
                key={service.id}
                className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20 hover:border-emerald-400 transition cursor-pointer"
                onClick={() => setActiveService(service.id)}
              >
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-2xl font-bold text-white">{service.name}</h3>
                  {service.status === 'GRATIS' && (
                    <span className="bg-green-500 text-white text-xs px-3 py-1 rounded-full font-bold">
                      GRATIS
                    </span>
                  )}
                </div>
                <p className="text-white/70 mb-4">{service.description}</p>
                <ul className="space-y-2">
                  {service.features.slice(0, 3).map((feature, idx) => (
                    <li key={idx} className="text-sm text-white/60 flex items-start gap-2">
                      <span className="text-emerald-400">✓</span>
                      <span>{feature}</span>
                    </li>
                  ))}
                </ul>
                <button className="mt-4 w-full bg-gradient-to-r from-emerald-500 to-teal-600 text-white py-2 rounded-lg font-semibold hover:from-emerald-600 hover:to-teal-700">
                  Usar Servicio
                </button>
              </div>
            ))}
          </div>
        )}

        {/* CryptoShield Scanner */}
        {activeService === 'cryptoshield-ia' && (
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
            <button 
              onClick={() => setActiveService('overview')}
              className="text-white/70 hover:text-white mb-4"
            >
              ← Volver
            </button>
            <h2 className="text-3xl font-bold text-white mb-6">🛡️ CryptoShield IA</h2>
            
            <div className="grid md:grid-cols-2 gap-6 mb-6">
              {/* Scan Wallet */}
              <div className="bg-white/5 rounded-xl p-6">
                <h3 className="text-xl font-bold text-white mb-4">Escanear Wallet</h3>
                <input
                  type="text"
                  placeholder="0x..."
                  value={walletAddress}
                  onChange={(e) => setWalletAddress(e.target.value)}
                  className="w-full px-4 py-3 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/50 mb-4"
                />
                <button
                  onClick={scanWallet}
                  disabled={scanLoading}
                  className="w-full bg-gradient-to-r from-emerald-500 to-teal-600 text-white py-3 rounded-lg font-semibold hover:from-emerald-600 hover:to-teal-700 disabled:opacity-50"
                >
                  {scanLoading ? 'Escaneando...' : 'Escanear Wallet'}
                </button>
              </div>

              {/* Verify Transaction */}
              <div className="bg-white/5 rounded-xl p-6">
                <h3 className="text-xl font-bold text-white mb-4">Verificar Transacción</h3>
                <input
                  type="text"
                  placeholder="0x... (66 caracteres)"
                  value={txHash}
                  onChange={(e) => setTxHash(e.target.value)}
                  className="w-full px-4 py-3 rounded-lg bg-white/10 border border-white/20 text-white placeholder-white/50 mb-4"
                />
                <button
                  onClick={verifyTransaction}
                  disabled={scanLoading}
                  className="w-full bg-gradient-to-r from-blue-500 to-cyan-600 text-white py-3 rounded-lg font-semibold hover:from-blue-600 hover:to-cyan-700 disabled:opacity-50"
                >
                  {scanLoading ? 'Verificando...' : 'Verificar TX'}
                </button>
              </div>
            </div>

            {/* Scan Results */}
            {scanResult && (
              <div className="bg-white/5 rounded-xl p-6">
                <h3 className="text-xl font-bold text-white mb-4">Resultado del Análisis</h3>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-white/70">Nivel de Riesgo:</span>
                    <span className={`px-4 py-2 rounded-full font-bold ${
                      scanResult.risk_level === 'high' ? 'bg-red-500' :
                      scanResult.risk_level === 'medium' ? 'bg-yellow-500' :
                      'bg-green-500'
                    } text-white`}>
                      {scanResult.risk_level?.toUpperCase()}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-white/70">Risk Score:</span>
                    <span className="text-white font-bold">{scanResult.risk_score}/100</span>
                  </div>
                  {scanResult.risk_factors && scanResult.risk_factors.length > 0 && (
                    <div>
                      <p className="text-white/70 mb-2">Factores de Riesgo:</p>
                      <ul className="space-y-1">
                        {scanResult.risk_factors.map((factor, idx) => (
                          <li key={idx} className="text-sm text-red-400">• {factor}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                  {scanResult.recommendations && (
                    <div>
                      <p className="text-white/70 mb-2">Recomendaciones:</p>
                      <ul className="space-y-1">
                        {scanResult.recommendations.map((rec, idx) => (
                          <li key={idx} className="text-sm text-white/70">• {rec}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Momentum Predictor */}
        {activeService === 'momentum-predictor-ia' && (
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
            <button 
              onClick={() => setActiveService('overview')}
              className="text-white/70 hover:text-white mb-4"
            >
              ← Volver
            </button>
            <h2 className="text-3xl font-bold text-white mb-6">📈 Momentum Predictor IA</h2>
            
            <div className="bg-white/5 rounded-xl p-6 mb-6">
              <h3 className="text-xl font-bold text-white mb-4">Obtener Señal de Trading</h3>
              <div className="flex gap-4">
                <select
                  value={cryptoSymbol}
                  onChange={(e) => setCryptoSymbol(e.target.value)}
                  className="px-4 py-3 rounded-lg bg-white/10 border border-white/20 text-white"
                >
                  <option value="BTC">Bitcoin (BTC)</option>
                  <option value="ETH">Ethereum (ETH)</option>
                  <option value="SOL">Solana (SOL)</option>
                  <option value="ADA">Cardano (ADA)</option>
                  <option value="DOT">Polkadot (DOT)</option>
                </select>
                <button
                  onClick={getSignal}
                  disabled={signalLoading}
                  className="flex-1 bg-gradient-to-r from-emerald-500 to-teal-600 text-white py-3 rounded-lg font-semibold hover:from-emerald-600 hover:to-teal-700 disabled:opacity-50"
                >
                  {signalLoading ? 'Generando...' : 'Obtener Señal'}
                </button>
              </div>
            </div>

            {/* Signal Results */}
            {signal && (
              <div className="bg-white/5 rounded-xl p-6">
                <h3 className="text-xl font-bold text-white mb-4">Señal de Trading</h3>
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <div className="mb-6">
                      <p className="text-white/70 text-sm mb-2">Señal:</p>
                      <span className={`inline-block px-6 py-3 rounded-lg font-bold text-xl ${
                        signal.signal === 'BUY' ? 'bg-green-500' :
                        signal.signal === 'SELL' ? 'bg-red-500' :
                        'bg-yellow-500'
                      } text-white`}>
                        {signal.signal}
                      </span>
                    </div>
                    <div className="space-y-3">
                      <div>
                        <p className="text-white/70 text-sm">Precio Actual:</p>
                        <p className="text-white font-bold text-lg">${signal.current_price?.toLocaleString()}</p>
                      </div>
                      <div>
                        <p className="text-white/70 text-sm">Confianza:</p>
                        <p className="text-white font-bold">{signal.confidence}%</p>
                      </div>
                      <div>
                        <p className="text-white/70 text-sm">Timeframe:</p>
                        <p className="text-white">{signal.timeframe}</p>
                      </div>
                    </div>
                  </div>
                  <div>
                    <h4 className="text-white font-semibold mb-3">Niveles de Trading:</h4>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-white/70">Entrada:</span>
                        <span className="text-white font-semibold">${signal.entry_price?.toLocaleString()}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-green-400">Target 1:</span>
                        <span className="text-white font-semibold">${signal.target_1?.toLocaleString()}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-green-400">Target 2:</span>
                        <span className="text-white font-semibold">${signal.target_2?.toLocaleString()}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-red-400">Stop Loss:</span>
                        <span className="text-white font-semibold">${signal.stop_loss?.toLocaleString()}</span>
                      </div>
                    </div>
                    {signal.indicators && (
                      <div className="mt-4 p-3 bg-white/5 rounded-lg">
                        <p className="text-white/70 text-xs mb-2">Indicadores Técnicos:</p>
                        <div className="text-xs space-y-1 text-white/60">
                          <div>RSI: {signal.indicators.rsi}</div>
                          <div>MACD: {signal.indicators.macd?.toFixed(2)}</div>
                          <div>SMA7: ${signal.indicators.sma_7?.toFixed(2)}</div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Pulse IA */}
        {activeService === 'pulse-ia' && (
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
            <button 
              onClick={() => setActiveService('overview')}
              className="text-white/70 hover:text-white mb-4"
            >
              ← Volver
            </button>
            <h2 className="text-3xl font-bold text-white mb-6">📊 Pulse IA</h2>
            <p className="text-white/70 mb-4">
              Análisis de sentimiento del mercado cripto en tiempo real
            </p>
            <div className="bg-white/5 rounded-xl p-6">
              <p className="text-white/70">
                El dashboard de Pulse IA está en desarrollo. Por ahora, puedes acceder a las funciones vía Telegram bot.
              </p>
              <a 
                href="https://t.me/Pulse_IA_Bot" 
                target="_blank" 
                rel="noopener noreferrer"
                className="inline-block mt-4 bg-blue-500 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-600"
              >
                Abrir Bot de Telegram
              </a>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default SuiteCryptoDashboard;
