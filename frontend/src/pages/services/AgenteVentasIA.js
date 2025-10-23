import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const AgenteVentasIA = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('bot');
  const [conversations, setConversations] = useState([]);

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
      
      // Demo conversations
      setConversations([
        {
          id: 1,
          client: 'Cliente Potencial 1',
          date: new Date().toISOString().split('T')[0],
          status: 'active',
          messages: 15,
          interest: 'high'
        }
      ]);
      
      setLoading(false);
    } catch (e) {
      console.error('Auth error:', e);
      navigate('/');
    }
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
          <p className="text-gray-600">Cargando agente de ventas...</p>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-4">
              <button onClick={() => navigate('/dashboard')} className="text-gray-600 hover:text-gray-900">
                ← Volver
              </button>
              <div>
                <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
                  <span>👩‍💼</span>
                  Agente de Ventas IA
                </h1>
                <p className="text-sm text-gray-500 mt-1">Rocío Almeida - Bot autónomo en Telegram</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <a
                href="https://t.me/RocioAlmeidaBot"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm"
              >
                <span>📱</span>
                Abrir en Telegram
              </a>
              <span className="text-sm text-gray-600">👤 {user?.full_name || user?.email}</span>
              <button onClick={handleLogout} className="px-4 py-2 text-sm bg-red-500 text-white rounded-lg hover:bg-red-600">
                Cerrar Sesión
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Info Banner */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="bg-gradient-to-r from-purple-50 to-pink-50 border border-purple-200 rounded-lg p-6">
          <div className="flex items-start gap-4">
            <span className="text-4xl">👩‍💼</span>
            <div className="flex-1">
              <h3 className="font-bold text-gray-900 mb-2 text-lg">Rocío Almeida - Tu Agente de Ventas IA</h3>
              <p className="text-sm text-gray-700 mb-3">
                Bot autónomo en Telegram que busca clientes potenciales en grupos, responde consultas 24/7 
                y genera conversaciones de ventas de forma natural.
              </p>
              <div className="flex items-center gap-4">
                <a
                  href="https://t.me/RocioAlmeidaBot"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 text-sm font-medium"
                >
                  <span>🚀</span>
                  Interactuar con Rocío
                </a>
                <span className="text-sm text-purple-700">
                  <strong>@RocioAlmeidaBot</strong> en Telegram
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="grid grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-600">{conversations.length}</div>
              <div className="text-xs text-gray-600">Conversaciones Activas</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">
                {conversations.filter(c => c.interest === 'high').length}
              </div>
              <div className="text-xs text-gray-600">Alto Interés</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">24/7</div>
              <div className="text-xs text-gray-600">Disponibilidad</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-emerald-600">95%</div>
              <div className="text-xs text-gray-600">Tasa de Respuesta</div>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8">
            <button
              onClick={() => setActiveTab('bot')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === 'bot' ? 'border-emerald-500 text-emerald-600' : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              🤖 Bot Info
            </button>
            <button
              onClick={() => setActiveTab('conversations')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === 'conversations' ? 'border-emerald-500 text-emerald-600' : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              💬 Conversaciones ({conversations.length})
            </button>
            <button
              onClick={() => setActiveTab('config')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === 'config' ? 'border-emerald-500 text-emerald-600' : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              ⚙️ Configuración
            </button>
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Bot Info Tab */}
        {activeTab === 'bot' && (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="text-3xl mb-3">🤖</div>
                <h3 className="font-bold text-gray-900 mb-2">IA Conversacional</h3>
                <p className="text-sm text-gray-600">
                  Respuestas naturales y contextuales usando Claude 3.5 Sonnet
                </p>
              </div>

              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="text-3xl mb-3">🎯</div>
                <h3 className="font-bold text-gray-900 mb-2">Prospección Activa</h3>
                <p className="text-sm text-gray-600">
                  Busca clientes potenciales en grupos de Telegram automáticamente
                </p>
              </div>

              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="text-3xl mb-3">📊</div>
                <h3 className="font-bold text-gray-900 mb-2">Análisis de Leads</h3>
                <p className="text-sm text-gray-600">
                  Califica automáticamente el interés y prioridad de cada lead
                </p>
              </div>

              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="text-3xl mb-3">💼</div>
                <h3 className="font-bold text-gray-900 mb-2">Base de Productos</h3>
                <p className="text-sm text-gray-600">
                  Conocimiento completo de tu catálogo con base vectorizada
                </p>
              </div>

              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="text-3xl mb-3">⏰</div>
                <h3 className="font-bold text-gray-900 mb-2">Disponibilidad 24/7</h3>
                <p className="text-sm text-gray-600">
                  Atiende consultas y genera ventas las 24 horas del día
                </p>
              </div>

              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="text-3xl mb-3">📈</div>
                <h3 className="font-bold text-gray-900 mb-2">Seguimiento</h3>
                <p className="text-sm text-gray-600">
                  Hace follow-up automático a leads con alto potencial
                </p>
              </div>
            </div>

            <div className="bg-gradient-to-br from-purple-50 to-pink-100 rounded-xl p-8">
              <div className="flex items-center gap-6">
                <div className="text-6xl">👩‍💼</div>
                <div>
                  <h3 className="text-2xl font-bold text-gray-900 mb-2">Rocío Almeida</h3>
                  <p className="text-gray-700 mb-4">
                    Agente de ventas IA especializada en generar conversaciones naturales, 
                    identificar necesidades y cerrar ventas de forma autónoma en Telegram.
                  </p>
                  <div className="flex items-center gap-3">
                    <span className="px-3 py-1 bg-purple-600 text-white rounded-full text-sm font-medium">
                      IA Avanzada
                    </span>
                    <span className="px-3 py-1 bg-pink-600 text-white rounded-full text-sm font-medium">
                      Autónomo
                    </span>
                    <span className="px-3 py-1 bg-blue-600 text-white rounded-full text-sm font-medium">
                      Telegram
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Conversations Tab */}
        {activeTab === 'conversations' && (
          <div className="space-y-4">
            {conversations.length === 0 ? (
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
                <div className="text-6xl mb-4">💬</div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">No hay conversaciones activas</h3>
                <p className="text-gray-600">Rocío comenzará a generar conversaciones automáticamente</p>
              </div>
            ) : (
              conversations.map((conv) => (
                <div
                  key={conv.id}
                  className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <h3 className="text-lg font-bold text-gray-900 mb-2">{conv.client}</h3>
                      <div className="flex items-center gap-4 text-sm text-gray-600">
                        <span>📅 {conv.date}</span>
                        <span>💬 {conv.messages} mensajes</span>
                        <span className={`px-2 py-1 rounded text-xs ${
                          conv.interest === 'high' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                        }`}>
                          {conv.interest === 'high' ? 'Alto Interés' : 'Interés Medio'}
                        </span>
                      </div>
                    </div>
                    <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-xs">
                      Activo
                    </span>
                  </div>
                </div>
              ))
            )}
          </div>
        )}

        {/* Config Tab */}
        {activeTab === 'config' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
                <span>📝</span>
                Personalización del Bot
              </h3>
              <p className="text-sm text-gray-600 mb-4">
                Personaliza el tono, estilo de comunicación y productos de Rocío
              </p>
              <button className="w-full px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700">
                Configurar
              </button>
            </div>

            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
                <span>🎯</span>
                Grupos Objetivo
              </h3>
              <p className="text-sm text-gray-600 mb-4">
                Configura los grupos de Telegram donde Rocío buscará clientes
              </p>
              <button className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                Gestionar Grupos
              </button>
            </div>

            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
                <span>💼</span>
                Catálogo de Productos
              </h3>
              <p className="text-sm text-gray-600 mb-4">
                Actualiza la base de conocimiento de productos y servicios
              </p>
              <button className="w-full px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700">
                Editar Catálogo
              </button>
            </div>

            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
                <span>📊</span>
                Reportes y Métricas
              </h3>
              <p className="text-sm text-gray-600 mb-4">
                Analiza el rendimiento y conversiones de Rocío
              </p>
              <button className="w-full px-4 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700">
                Ver Reportes
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default AgenteVentasIA;
