import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const AutomatizacionRedesSociales = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('calendar');
  const [posts, setPosts] = useState([]);

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
      setPosts([{
        id: 1,
        content: 'Nueva publicación automática',
        platforms: ['facebook', 'instagram', 'twitter'],
        scheduledFor: new Date().toISOString(),
        status: 'scheduled'
      }]);
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
          <p className="text-gray-600">Cargando automatización de redes sociales...</p>
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-4">
              <button onClick={() => navigate('/dashboard')} className="text-gray-600 hover:text-gray-900">← Volver</button>
              <div>
                <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
                  <span>📱</span>Automatización Redes Sociales
                </h1>
                <p className="text-sm text-gray-500 mt-1">Publicaciones automáticas multi-plataforma</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-600">👤 {user?.full_name || user?.email}</span>
              <button onClick={handleLogout} className="px-4 py-2 text-sm bg-red-500 text-white rounded-lg hover:bg-red-600">Cerrar Sesión</button>
            </div>
          </div>
        </div>
      </header>

      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8">
            <button onClick={() => setActiveTab('calendar')} className={`py-4 px-1 border-b-2 font-medium text-sm ${activeTab === 'calendar' ? 'border-emerald-500 text-emerald-600' : 'border-transparent text-gray-500'}`}>📅 Calendario</button>
            <button onClick={() => setActiveTab('create')} className={`py-4 px-1 border-b-2 font-medium text-sm ${activeTab === 'create' ? 'border-emerald-500 text-emerald-600' : 'border-transparent text-gray-500'}`}>✍️ Crear Post</button>
            <button onClick={() => setActiveTab('analytics')} className={`py-4 px-1 border-b-2 font-medium text-sm ${activeTab === 'analytics' ? 'border-emerald-500 text-emerald-600' : 'border-transparent text-gray-500'}`}>📊 Analíticas</button>
            <button onClick={() => setActiveTab('platforms')} className={`py-4 px-1 border-b-2 font-medium text-sm ${activeTab === 'platforms' ? 'border-emerald-500 text-emerald-600' : 'border-transparent text-gray-500'}`}>🔗 Plataformas</button>
          </nav>
        </div>
      </div>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'calendar' && (
          <div className="space-y-4">
            {posts.map((post) => (
              <div key={post.id} className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="flex items-start justify-between">
                  <div>
                    <p className="text-gray-900 mb-2">{post.content}</p>
                    <div className="flex items-center gap-2">
                      {post.platforms.map((platform) => (
                        <span key={platform} className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs">{platform}</span>
                      ))}
                    </div>
                  </div>
                  <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-xs">Programado</span>
                </div>
              </div>
            ))}
          </div>
        )}

        {activeTab === 'platforms' && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <div className="text-3xl mb-3">📘</div>
              <h3 className="font-bold text-gray-900 mb-2">Facebook</h3>
              <p className="text-sm text-gray-600 mb-4">Publicaciones automáticas en páginas y grupos</p>
              <button className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm">Conectar</button>
            </div>
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <div className="text-3xl mb-3">📷</div>
              <h3 className="font-bold text-gray-900 mb-2">Instagram</h3>
              <p className="text-sm text-gray-600 mb-4">Stories, posts y reels automáticos</p>
              <button className="w-full px-4 py-2 bg-pink-600 text-white rounded-lg hover:bg-pink-700 text-sm">Conectar</button>
            </div>
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <div className="text-3xl mb-3">🐦</div>
              <h3 className="font-bold text-gray-900 mb-2">Twitter/X</h3>
              <p className="text-sm text-gray-600 mb-4">Tweets programados y hilos</p>
              <button className="w-full px-4 py-2 bg-gray-900 text-white rounded-lg hover:bg-gray-800 text-sm">Conectar</button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default AutomatizacionRedesSociales;