import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const ConsultoriaTecnica = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('chat');
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [consulting, setConsulting] = useState(false);
  const [consultations, setConsultations] = useState([]);

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
      
      // Demo consultations
      setConsultations([
        {
          id: 1,
          date: new Date().toISOString().split('T')[0],
          topic: 'Migración a Microservicios',
          status: 'resolved',
          messages: 12
        },
        {
          id: 2,
          date: new Date(Date.now() - 86400000).toISOString().split('T')[0],
          topic: 'Optimización de Base de Datos',
          status: 'ongoing',
          messages: 8
        }
      ]);
      
      setLoading(false);
    } catch (e) {
      console.error('Auth error:', e);
      navigate('/');
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim()) return;

    const userMessage = {
      id: Date.now(),
      text: inputMessage,
      sender: 'user',
      timestamp: new Date().toISOString()
    };

    setMessages([...messages, userMessage]);
    setInputMessage('');
    setConsulting(true);

    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(`${API}/user/llm/technical-consultation`, {
        question: inputMessage,
        session_id: `tech_${user.id}_${Date.now()}`
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });

      if (response.data.success) {
        const aiMessage = {
          id: Date.now() + 1,
          text: response.data.response,
          sender: 'ai',
          timestamp: new Date().toISOString()
        };
        setMessages(prev => [...prev, aiMessage]);
      } else {
        throw new Error(response.data.error);
      }
    } catch (error) {
      console.error('Error:', error);
      const errorMessage = {
        id: Date.now() + 1,
        text: '❌ Error al procesar la consulta. Por favor intenta de nuevo.',
        sender: 'ai',
        timestamp: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setConsulting(false);
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
          <p className="text-gray-600">Cargando consultoría técnica...</p>
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
                  <span>💡</span>
                  Consultoría Técnica con IA
                </h1>
                <p className="text-sm text-gray-500 mt-1">Asistente técnico especializado 24/7</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-600">👤 {user?.full_name || user?.email}</span>
              <button onClick={handleLogout} className="px-4 py-2 text-sm bg-red-500 text-white rounded-lg hover:bg-red-600">
                Cerrar Sesión
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Tabs */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8">
            <button
              onClick={() => setActiveTab('chat')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === 'chat' ? 'border-emerald-500 text-emerald-600' : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              💬 Chat Técnico
            </button>
            <button
              onClick={() => setActiveTab('history')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === 'history' ? 'border-emerald-500 text-emerald-600' : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              📋 Historial ({consultations.length})
            </button>
            <button
              onClick={() => setActiveTab('topics')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === 'topics' ? 'border-emerald-500 text-emerald-600' : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              🎯 Temas Especializados
            </button>
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Chat Tab */}
        {activeTab === 'chat' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 h-[600px] flex flex-col">
                {/* Chat Messages */}
                <div className="flex-1 p-6 overflow-y-auto space-y-4">
                  {messages.length === 0 ? (
                    <div className="text-center py-12">
                      <div className="text-6xl mb-4">🤖</div>
                      <h3 className="text-xl font-semibold text-gray-900 mb-2">Consultoría Técnica con IA</h3>
                      <p className="text-gray-600">Pregunta sobre arquitectura, código, DevOps, cloud, bases de datos...</p>
                    </div>
                  ) : (
                    messages.map((msg) => (
                      <div key={msg.id} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-[80%] rounded-lg p-4 ${
                          msg.sender === 'user' ? 'bg-emerald-600 text-white' : 'bg-gray-100 text-gray-900'
                        }`}>
                          <p className="text-sm whitespace-pre-wrap">{msg.text}</p>
                          <p className={`text-xs mt-2 ${
                            msg.sender === 'user' ? 'text-emerald-100' : 'text-gray-500'
                          }`}>
                            {new Date(msg.timestamp).toLocaleTimeString('es-PY', { hour: '2-digit', minute: '2-digit' })}
                          </p>
                        </div>
                      </div>
                    ))
                  )}
                  {consulting && (
                    <div className="flex justify-start">
                      <div className="bg-gray-100 rounded-lg p-4">
                        <div className="flex items-center gap-2">
                          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-emerald-500"></div>
                          <p className="text-sm text-gray-600">Analizando consulta...</p>
                        </div>
                      </div>
                    </div>
                  )}
                </div>

                {/* Input */}
                <div className="border-t border-gray-200 p-4">
                  <form onSubmit={handleSendMessage} className="flex gap-3">
                    <input
                      type="text"
                      value={inputMessage}
                      onChange={(e) => setInputMessage(e.target.value)}
                      placeholder="Escribe tu consulta técnica..."
                      className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                      disabled={consulting}
                    />
                    <button
                      type="submit"
                      disabled={consulting || !inputMessage.trim()}
                      className="px-6 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 disabled:opacity-50"
                    >
                      Enviar
                    </button>
                  </form>
                </div>
              </div>
            </div>

            {/* Sidebar */}
            <div className="space-y-6">
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <h3 className="font-bold text-gray-900 mb-4">🎯 Especializaciones</h3>
                <div className="space-y-2 text-sm">
                  <div className="flex items-center gap-2"><span>☁️</span>Cloud & DevOps</div>
                  <div className="flex items-center gap-2"><span>🏗️</span>Arquitectura Software</div>
                  <div className="flex items-center gap-2"><span>💾</span>Bases de Datos</div>
                  <div className="flex items-center gap-2"><span>🔐</span>Seguridad</div>
                  <div className="flex items-center gap-2"><span>📱</span>Mobile & Web</div>
                  <div className="flex items-center gap-2"><span>🤖</span>IA & Machine Learning</div>
                </div>
              </div>

              <div className="bg-gradient-to-br from-blue-50 to-purple-100 rounded-xl p-6">
                <h3 className="font-bold text-gray-900 mb-2">💎 Powered by Claude</h3>
                <p className="text-sm text-gray-700">Consultoría técnica impulsada por Claude 3.5 Sonnet con conocimiento actualizado</p>
              </div>
            </div>
          </div>
        )}

        {/* History Tab */}
        {activeTab === 'history' && (
          <div className="space-y-4">
            {consultations.map((consult) => (
              <div key={consult.id} className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="font-bold text-gray-900">{consult.topic}</h3>
                    <div className="flex items-center gap-3 text-sm text-gray-600 mt-1">
                      <span>📅 {consult.date}</span>
                      <span>💬 {consult.messages} mensajes</span>
                    </div>
                  </div>
                  <span className={`px-3 py-1 text-xs rounded-full ${
                    consult.status === 'resolved' ? 'bg-green-100 text-green-800' : 'bg-blue-100 text-blue-800'
                  }`}>
                    {consult.status === 'resolved' ? 'Resuelto' : 'En curso'}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Topics Tab */}
        {activeTab === 'topics' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <div className="text-3xl mb-3">☁️</div>
              <h3 className="font-bold text-gray-900 mb-2">Cloud & DevOps</h3>
              <p className="text-sm text-gray-600">AWS, Azure, GCP, Docker, Kubernetes, CI/CD</p>
            </div>
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <div className="text-3xl mb-3">🏗️</div>
              <h3 className="font-bold text-gray-900 mb-2">Arquitectura</h3>
              <p className="text-sm text-gray-600">Microservicios, Monolitos, Event-Driven, Serverless</p>
            </div>
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <div className="text-3xl mb-3">💾</div>
              <h3 className="font-bold text-gray-900 mb-2">Bases de Datos</h3>
              <p className="text-sm text-gray-600">SQL, NoSQL, PostgreSQL, MongoDB, Redis</p>
            </div>
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <div className="text-3xl mb-3">🔐</div>
              <h3 className="font-bold text-gray-900 mb-2">Seguridad</h3>
              <p className="text-sm text-gray-600">OAuth, JWT, Encryption, Penetration Testing</p>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default ConsultoriaTecnica;