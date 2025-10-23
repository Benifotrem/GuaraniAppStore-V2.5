import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const CryptoSuite = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [serviceData, setServiceData] = useState(null);
  const [activeBot, setActiveBot] = useState('cryptoshield');
  const [contractAddress, setContractAddress] = useState('');
  const [coin, setCoin] = useState('BTC');
  const [scanResult, setScanResult] = useState(null);
  const [sentimentResult, setSentimentResult] = useState(null);
  const [signalsResult, setSignalsResult] = useState(null);
  const [predictionResult, setPredictionResult] = useState(null);

  useEffect(() => {
    initializeService();
  }, []);

  const initializeService = async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/');
      return;
    }

    try {
      const response = await axios.post(
        `${API}/services/suite-crypto/initialize`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      );
      
      if (response.data.success) {
        setServiceData(response.data);
      }
      setLoading(false);
    } catch (e) {
      console.error('Error:', e);
      alert('Error al cargar el servicio');
      navigate('/dashboard');
    }
  };

  const handleScanFraud = async () => {
    if (!contractAddress.trim()) {
      alert('Ingresa una dirección de contrato');
      return;
    }

    const token = localStorage.getItem('token');
    try {
      const response = await axios.post(
        `${API}/services/suite-crypto/execute`,
        {
          action: 'scan_fraud',
          params: { contract_address: contractAddress }
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      
      setScanResult(response.data);
    } catch (e) {
      alert('Error al escanear contrato');
    }
  };

  const handleGetSentiment = async () => {
    if (!coin.trim()) {
      alert('Ingresa un símbolo de moneda');
      return;
    }

    const token = localStorage.getItem('token');
    try {
      const response = await axios.post(
        `${API}/services/suite-crypto/execute`,
        {
          action: 'get_sentiment',
          params: { coin: coin }
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      
      setSentimentResult(response.data);
    } catch (e) {
      alert('Error al obtener sentimiento');
    }
  };

  const handleGetSignals = async () => {
    const token = localStorage.getItem('token');
    try {
      const response = await axios.post(
        `${API}/services/suite-crypto/execute`,
        {
          action: 'get_signals',
          params: {}
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      
      setSignalsResult(response.data);
    } catch (e) {
      alert('Error al obtener señales');
    }
  };

  const handlePredict = async () => {
    if (!coin.trim()) {
      alert('Ingresa un símbolo de moneda');
      return;
    }

    const token = localStorage.getItem('token');
    try {
      const response = await axios.post(
        `${API}/services/suite-crypto/execute`,
        {
          action: 'predict',
          params: { coin: coin }
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      
      setPredictionResult(response.data);
    } catch (e) {
      alert('Error al predecir');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-emerald-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Cargando Suite Crypto...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div>
              <button
                onClick={() => navigate('/dashboard')}
                className="text-sm text-gray-600 hover:text-emerald-600 mb-2"
              >
                ← Volver al Dashboard
              </button>
              <h1 className="text-2xl font-bold text-gray-900">Suite Crypto IA</h1>
              <p className="text-sm text-gray-500 mt-1">3 Bots de Telegram para inversores</p>
            </div>
          </div>
        </div>
      </header>

      {/* Bot Selector */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8">
            {[
              { id: 'cryptoshield', label: '🛡️ CryptoShield IA', desc: 'Escáner Fraude' },
              { id: 'pulse', label: '📊 Pulse IA', desc: 'Sentimiento' },
              { id: 'momentum', label: '🚀 Momentum IA', desc: 'Señales Trading' }
            ].map((bot) => (
              <button
                key={bot.id}
                onClick={() => setActiveBot(bot.id)}
                className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                  activeBot === bot.id
                    ? 'border-emerald-500 text-emerald-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                <div>{bot.label}</div>
                <div className="text-xs text-gray-500">{bot.desc}</div>
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* CryptoShield */}
        {activeBot === 'cryptoshield' && (
          <div className="space-y-6">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-4">🛡️ CryptoShield IA - Escáner de Fraude</h2>
              <p className="text-gray-600 mb-6">Escanea contratos smart para detectar fraudes, honeypots y rugpulls</p>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Dirección del Contrato
                  </label>
                  <input
                    type="text"
                    value={contractAddress}
                    onChange={(e) => setContractAddress(e.target.value)}
                    placeholder="0x..."
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                  />
                </div>
                
                <button
                  onClick={handleScanFraud}
                  className="w-full px-6 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700"
                >
                  🔍 Escanear Contrato
                </button>
              </div>

              {scanResult && scanResult.success && (
                <div className="mt-6 p-4 bg-gray-50 rounded-lg">
                  <h3 className="font-semibold text-gray-900 mb-4">Resultado del Escaneo</h3>
                  
                  <div className="grid grid-cols-2 gap-4 mb-4">
                    <div>
                      <p className="text-sm text-gray-600">Risk Score</p>
                      <p className={`text-2xl font-bold ${
                        scanResult.risk_score < 30 ? 'text-green-600' :
                        scanResult.risk_score < 60 ? 'text-yellow-600' : 'text-red-600'
                      }`}>
                        {scanResult.risk_score}/100
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Risk Level</p>
                      <p className={`text-xl font-bold ${
                        scanResult.risk_level === 'LOW' ? 'text-green-600' :
                        scanResult.risk_level === 'MEDIUM' ? 'text-yellow-600' : 'text-red-600'
                      }`}>
                        {scanResult.risk_level}
                      </p>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <h4 className="font-medium text-gray-900">Indicadores:</h4>
                    {Object.entries(scanResult.indicators).map(([key, value]) => (
                      <div key={key} className="flex justify-between items-center p-2 bg-white rounded">
                        <span className="text-sm capitalize">{key.replace(/_/g, ' ')}</span>
                        <span className={`px-2 py-1 text-xs rounded ${
                          value === false || value === 'LOW' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                        }`}>
                          {value.toString()}
                        </span>
                      </div>
                    ))}
                  </div>

                  <div className="mt-4 p-3 bg-blue-50 rounded">
                    <p className="text-sm text-blue-900">
                      <strong>Recomendación:</strong> {scanResult.recommendation}
                    </p>
                  </div>
                </div>
              )}
            </div>

            {serviceData?.bots?.cryptoshield && (
              <div className="bg-blue-50 p-4 rounded-lg">
                <p className="text-sm text-blue-900">
                  <strong>💡 Telegram Bot:</strong> <a href={serviceData.bots.cryptoshield} target="_blank" rel="noopener noreferrer" className="underline">{serviceData.bots.cryptoshield}</a>
                </p>
              </div>
            )}
          </div>
        )}

        {/* Pulse */}
        {activeBot === 'pulse' && (
          <div className="space-y-6">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-4">📊 Pulse IA - Análisis de Sentimiento</h2>
              <p className="text-gray-600 mb-6">Analiza el sentimiento del mercado en Twitter, Reddit y noticias</p>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Símbolo de la Moneda
                  </label>
                  <input
                    type="text"
                    value={coin}
                    onChange={(e) => setCoin(e.target.value.toUpperCase())}
                    placeholder="BTC, ETH, SOL..."
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                  />
                </div>
                
                <button
                  onClick={handleGetSentiment}
                  className="w-full px-6 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700"
                >
                  📊 Analizar Sentimiento
                </button>
              </div>

              {sentimentResult && sentimentResult.success && (
                <div className="mt-6 p-4 bg-gray-50 rounded-lg">
                  <h3 className="font-semibold text-gray-900 mb-4">Análisis de {sentimentResult.coin}</h3>
                  
                  <div className="grid grid-cols-3 gap-4 mb-4">
                    <div className="text-center">
                      <p className="text-sm text-gray-600">Sentiment Score</p>
                      <p className="text-3xl font-bold text-emerald-600">{sentimentResult.sentiment_score}/100</p>
                    </div>
                    <div className="text-center">
                      <p className="text-sm text-gray-600">Sentiment</p>
                      <p className={`text-xl font-bold ${
                        sentimentResult.sentiment === 'BULLISH' ? 'text-green-600' :
                        sentimentResult.sentiment === 'BEARISH' ? 'text-red-600' : 'text-gray-600'
                      }`}>
                        {sentimentResult.sentiment}
                      </p>
                    </div>
                    <div className="text-center">
                      <p className="text-sm text-gray-600">Confidence</p>
                      <p className="text-xl font-bold text-blue-600">{sentimentResult.confidence}%</p>
                    </div>
                  </div>

                  <div className="space-y-3">
                    <h4 className="font-medium text-gray-900">Fuentes:</h4>
                    {Object.entries(sentimentResult.sources).map(([source, data]) => (
                      <div key={source} className="p-3 bg-white rounded">
                        <div className="flex justify-between items-center">
                          <span className="font-medium capitalize">{source}</span>
                          <span className="text-sm text-gray-600">Score: {data.score}/100</span>
                        </div>
                        <p className="text-xs text-gray-500 mt-1">
                          {source === 'twitter' && `${data.mentions} menciones`}
                          {source === 'reddit' && `${data.posts} posts`}
                          {source === 'news' && `${data.articles} artículos`}
                        </p>
                      </div>
                    ))}
                  </div>

                  <div className="mt-4 p-3 bg-blue-50 rounded">
                    <p className="text-sm text-blue-900">
                      <strong>Trend:</strong> {sentimentResult.trend}
                    </p>
                  </div>
                </div>
              )}
            </div>

            {serviceData?.bots?.pulse && (
              <div className="bg-blue-50 p-4 rounded-lg">
                <p className="text-sm text-blue-900">
                  <strong>💡 Telegram Bot:</strong> <a href={serviceData.bots.pulse} target="_blank" rel="noopener noreferrer" className="underline">{serviceData.bots.pulse}</a>
                </p>
              </div>
            )}
          </div>
        )}

        {/* Momentum */}
        {activeBot === 'momentum' && (
          <div className="space-y-6">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-4">🚀 Momentum Predictor IA</h2>
              <p className="text-gray-600 mb-6">Señales diarias de trading con IA</p>
              
              <div className="space-y-4">
                <button
                  onClick={handleGetSignals}
                  className="w-full px-6 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700"
                >
                  📈 Ver Señales del Día
                </button>

                <div className="border-t pt-4">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    O predice una moneda específica:
                  </label>
                  <div className="flex gap-2">
                    <input
                      type="text"
                      value={coin}
                      onChange={(e) => setCoin(e.target.value.toUpperCase())}
                      placeholder="BTC, ETH..."
                      className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                    />
                    <button
                      onClick={handlePredict}
                      className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                    >
                      Predecir
                    </button>
                  </div>
                </div>
              </div>

              {signalsResult && signalsResult.success && (
                <div className="mt-6 space-y-4">
                  <h3 className="font-semibold text-gray-900">Señales del Día</h3>
                  {signalsResult.signals.map((signal, idx) => (
                    <div key={idx} className="p-4 bg-gray-50 rounded-lg">
                      <div className="flex justify-between items-start mb-2">
                        <div>
                          <h4 className="font-bold text-lg">{signal.coin}</h4>
                          <p className={`text-sm font-medium ${
                            signal.action === 'BUY' ? 'text-green-600' :
                            signal.action === 'SELL' ? 'text-red-600' : 'text-gray-600'
                          }`}>
                            {signal.action} - Confianza: {signal.confidence}%
                          </p>
                        </div>
                      </div>
                      <div className="grid grid-cols-3 gap-2 text-sm">
                        <div>
                          <p className="text-gray-600">Entry</p>
                          <p className="font-medium">${signal.entry}</p>
                        </div>
                        <div>
                          <p className="text-gray-600">Target</p>
                          <p className="font-medium text-green-600">${signal.target}</p>
                        </div>
                        <div>
                          <p className="text-gray-600">Stop Loss</p>
                          <p className="font-medium text-red-600">${signal.stop_loss}</p>
                        </div>
                      </div>
                    </div>
                  ))}

                  <div className="p-4 bg-blue-50 rounded-lg">
                    <h4 className="font-medium text-blue-900 mb-2">Mercado General</h4>
                    <div className="grid grid-cols-3 gap-4 text-sm">
                      <div>
                        <p className="text-blue-700">Trend</p>
                        <p className="font-medium">{signalsResult.market_overview.trend}</p>
                      </div>
                      <div>
                        <p className="text-blue-700">Volatility</p>
                        <p className="font-medium">{signalsResult.market_overview.volatility}</p>
                      </div>
                      <div>
                        <p className="text-blue-700">Fear & Greed</p>
                        <p className="font-medium">{signalsResult.market_overview.fear_greed_index}</p>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {predictionResult && predictionResult.success && (
                <div className="mt-6 p-4 bg-gray-50 rounded-lg">
                  <h3 className="font-semibold text-gray-900 mb-4">Predicción para {predictionResult.coin}</h3>
                  <p className="text-sm text-gray-600 mb-4">Precio Actual: ${predictionResult.current_price}</p>
                  
                  <div className="space-y-2">
                    {Object.entries(predictionResult.prediction).map(([timeframe, data]) => (
                      <div key={timeframe} className="flex justify-between items-center p-2 bg-white rounded">
                        <span className="text-sm font-medium">{timeframe}</span>
                        <div className="text-right">
                          <p className={`font-bold ${data.direction === 'UP' ? 'text-green-600' : 'text-red-600'}`}>
                            ${data.price} {data.direction === 'UP' ? '↑' : '↓'}
                          </p>
                          <p className="text-xs text-gray-500">Confianza: {data.confidence}%</p>
                        </div>
                      </div>
                    ))}
                  </div>

                  <div className="mt-4 p-3 bg-blue-50 rounded">
                    <p className="text-sm text-blue-900">
                      <strong>Momentum Score:</strong> {predictionResult.momentum_score}/100
                    </p>
                    <p className="text-sm text-blue-900 mt-1">
                      <strong>Recomendación:</strong> {predictionResult.recommendation}
                    </p>
                  </div>
                </div>
              )}
            </div>

            {serviceData?.bots?.momentum && (
              <div className="bg-blue-50 p-4 rounded-lg">
                <p className="text-sm text-blue-900">
                  <strong>💡 Telegram Bot:</strong> <a href={serviceData.bots.momentum} target="_blank" rel="noopener noreferrer" className="underline">{serviceData.bots.momentum}</a>
                </p>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
};

export default CryptoSuite;
