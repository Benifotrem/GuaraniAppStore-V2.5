import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const AsistenteDirectivos = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('whatsapp');
  const [whatsappConfig, setWhatsappConfig] = useState({
    phone: '',
    apiKey: '',
    enabled: false
  });
  const [telegramConfig, setTelegramConfig] = useState({
    chatId: '',
    enabled: false
  });

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/');
      return;
    }

    try {
      const userRes = await axios.get(`${API}/auth/me`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setUser(userRes.data);
      
      // TODO: Load user's configuration from backend
      // const configRes = await axios.get(`${API}/user/assistant-config`, {
      //   headers: { Authorization: `Bearer ${token}` }
      // });
      // setWhatsappConfig(configRes.data.whatsapp);
      // setTelegramConfig(configRes.data.telegram);
      
      setLoading(false);
    } catch (e) {
      console.error('Auth error:', e);
      navigate('/');
    }
  };

  const handleSaveWhatsApp = async (e) => {
    e.preventDefault();
    alert('⏳ Configuración de WhatsApp guardada. Esta funcionalidad se integrará próximamente.');
    // TODO: Save to backend
    // const token = localStorage.getItem('token');
    // await axios.post(`${API}/user/assistant-config/whatsapp`, whatsappConfig, {
    //   headers: { Authorization: `Bearer ${token}` }
    // });
  };

  const handleSaveTelegram = async (e) => {
    e.preventDefault();
    alert('✅ Bot de Telegram configurado correctamente!');
    // TODO: Save to backend
    // const token = localStorage.getItem('token');
    // await axios.post(`${API}/user/assistant-config/telegram`, telegramConfig, {
    //   headers: { Authorization: `Bearer ${token}` }
    // });
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/');
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-emerald-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Cargando asistente...</p>
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
            <div className="flex items-center gap-4">
              <button
                onClick={() => navigate('/dashboard')}
                className="text-gray-600 hover:text-gray-900"
              >
                ← Volver
              </button>
              <div>
                <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
                  <span>👔</span>
                  Asistente Personal para Directivos
                </h1>
                <p className="text-sm text-gray-500 mt-1">Configura tu asistente ejecutivo 24/7</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-600">
                👤 {user?.full_name || user?.email}
              </span>
              <button
                onClick={handleLogout}
                className="px-4 py-2 text-sm bg-red-500 text-white rounded-lg hover:bg-red-600"
              >
                Cerrar Sesión
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Info Banner */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-start gap-3">
            <span className="text-2xl">🤖</span>
            <div>
              <h3 className="font-semibold text-blue-900 mb-1">Bot de Telegram Disponible</h3>
              <p className="text-sm text-blue-700 mb-2">
                Puedes interactuar con tu asistente directamente desde Telegram usando nuestro bot dedicado:
              </p>
              <a
                href="https://t.me/GuaraniAssistantBot"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm"
              >
                <span>📱</span>
                Abrir @GuaraniAssistantBot
              </a>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8">
            <button
              onClick={() => setActiveTab('whatsapp')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === 'whatsapp'
                  ? 'border-emerald-500 text-emerald-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              📱 Configuración WhatsApp
            </button>
            <button
              onClick={() => setActiveTab('telegram')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === 'telegram'
                  ? 'border-emerald-500 text-emerald-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              🤖 Configuración Telegram
            </button>
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* WhatsApp Tab */}
        {activeTab === 'whatsapp' && (
          <div className="space-y-6">
            <div>
              <h2 className="text-xl font-bold text-gray-900 mb-2">Configuración de WhatsApp</h2>
              <p className="text-gray-600">Conecta tu asistente con WhatsApp Business para recibir notificaciones y comandos.</p>
            </div>

            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <form onSubmit={handleSaveWhatsApp} className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Número de WhatsApp Business
                  </label>
                  <input
                    type="tel"
                    value={whatsappConfig.phone}
                    onChange={(e) => setWhatsappConfig({ ...whatsappConfig, phone: e.target.value })}
                    placeholder="+595 XXX XXX XXX"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    Formato internacional con código de país (ej: +595 para Paraguay)
                  </p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    API Key de WhatsApp Business
                  </label>
                  <input
                    type="password"
                    value={whatsappConfig.apiKey}
                    onChange={(e) => setWhatsappConfig({ ...whatsappConfig, apiKey: e.target.value })}
                    placeholder="Tu API Key de WhatsApp Business"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    <a href="https://developers.facebook.com/docs/whatsapp" target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                      ¿Cómo obtener mi API Key?
                    </a>
                  </p>
                </div>

                <div className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    id="whatsapp-enabled"
                    checked={whatsappConfig.enabled}
                    onChange={(e) => setWhatsappConfig({ ...whatsappConfig, enabled: e.target.checked })}
                    className="w-4 h-4 text-emerald-600 rounded focus:ring-emerald-500"
                  />
                  <label htmlFor="whatsapp-enabled" className="text-sm text-gray-700">
                    Habilitar integración de WhatsApp
                  </label>
                </div>

                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                  <div className="flex items-start gap-2">
                    <span className="text-yellow-600">⚠️</span>
                    <div className="text-sm text-yellow-800">
                      <p className="font-semibold mb-1">Integración en Desarrollo</p>
                      <p>La integración con WhatsApp Business estará disponible próximamente. Mientras tanto, puedes usar nuestro bot de Telegram.</p>
                    </div>
                  </div>
                </div>

                <button
                  type="submit"
                  className="w-full px-6 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors font-medium"
                >
                  💾 Guardar Configuración
                </button>
              </form>
            </div>
          </div>
        )}

        {/* Telegram Tab */}
        {activeTab === 'telegram' && (
          <div className="space-y-6">
            <div>
              <h2 className="text-xl font-bold text-gray-900 mb-2">Configuración de Telegram</h2>
              <p className="text-gray-600">Configura tu asistente para interactuar a través de Telegram.</p>
            </div>

            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <form onSubmit={handleSaveTelegram} className="space-y-6">
                <div className="bg-gradient-to-r from-blue-50 to-blue-100 rounded-lg p-6 mb-6">
                  <h3 className="font-bold text-blue-900 mb-3 text-lg">🚀 Pasos para Activar tu Asistente</h3>
                  <ol className="space-y-3 text-sm text-blue-800">
                    <li className="flex items-start gap-2">
                      <span className="font-bold">1.</span>
                      <span>Abre Telegram y busca <span className="font-mono bg-white px-2 py-1 rounded">@GuaraniAssistantBot</span></span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="font-bold">2.</span>
                      <span>Inicia una conversación enviando el comando <span className="font-mono bg-white px-2 py-1 rounded">/start</span></span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="font-bold">3.</span>
                      <span>El bot te proporcionará tu Chat ID único</span>
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="font-bold">4.</span>
                      <span>Copia el Chat ID y pégalo en el campo de abajo</span>
                    </li>
                  </ol>
                  <a
                    href="https://t.me/GuaraniAssistantBot"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors mt-4"
                  >
                    <span>📱</span>
                    Abrir Bot en Telegram
                  </a>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Tu Chat ID de Telegram
                  </label>
                  <input
                    type="text"
                    value={telegramConfig.chatId}
                    onChange={(e) => setTelegramConfig({ ...telegramConfig, chatId: e.target.value })}
                    placeholder="Ej: 123456789"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                  />
                  <p className="text-xs text-gray-500 mt-1">
                    El bot te proporcionará este número cuando inicies la conversación
                  </p>
                </div>

                <div className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    id="telegram-enabled"
                    checked={telegramConfig.enabled}
                    onChange={(e) => setTelegramConfig({ ...telegramConfig, enabled: e.target.checked })}
                    className="w-4 h-4 text-emerald-600 rounded focus:ring-emerald-500"
                  />
                  <label htmlFor="telegram-enabled" className="text-sm text-gray-700">
                    Habilitar notificaciones de Telegram
                  </label>
                </div>

                <button
                  type="submit"
                  className="w-full px-6 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors font-medium"
                >
                  ✅ Activar Bot de Telegram
                </button>
              </form>
            </div>

            {/* Features Card */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
                <span>✨</span>
                Funcionalidades del Asistente
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="flex items-start gap-3">
                  <span className="text-2xl">📅</span>
                  <div>
                    <h4 className="font-semibold text-gray-900">Gestión de Agenda</h4>
                    <p className="text-sm text-gray-600">Integración con Google Calendar para recordatorios</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <span className="text-2xl">📝</span>
                  <div>
                    <h4 className="font-semibold text-gray-900">Tareas y Recordatorios</h4>
                    <p className="text-sm text-gray-600">Crea y gestiona tus tareas del día</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <span className="text-2xl">💰</span>
                  <div>
                    <h4 className="font-semibold text-gray-900">Control de Gastos</h4>
                    <p className="text-sm text-gray-600">Registra y analiza tus gastos empresariales</p>
                  </div>
                </div>
                <div className="flex items-start gap-3">
                  <span className="text-2xl">🔍</span>
                  <div>
                    <h4 className="font-semibold text-gray-900">Búsquedas Web</h4>
                    <p className="text-sm text-gray-600">Búsquedas automáticas con resultados resumidos</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default AsistenteDirectivos;
