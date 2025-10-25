import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
const API = `${BACKEND_URL}/api`;

const ClientDashboard = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [activeTab, setActiveTab] = useState('services');
  const [userServices, setUserServices] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadUserServices();
  }, []);

  const loadUserServices = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API}/user/subscriptions`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setUserServices(response.data);
    } catch (error) {
      console.error('Error loading services:', error);
      // Si falla, mostrar servicios de ejemplo
      setUserServices([]);
    } finally {
      setLoading(false);
    }
  };

  const handleServiceAccess = (service) => {
    if (service.slug === 'suite-crypto') {
      navigate('/dashboard/suite-crypto');
    } else {
      navigate(`/dashboard/${service.slug}`);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center">
        <div className="text-white text-xl">Cargando...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <header className="bg-black/20 backdrop-blur-lg border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <h1 className="text-2xl font-bold text-white">GuaraniAppStore</h1>
            <nav className="hidden md:flex items-center gap-6">
              <button
                onClick={() => setActiveTab('services')}
                className={`text-sm font-medium transition ${
                  activeTab === 'services' ? 'text-emerald-400' : 'text-white/70 hover:text-white'
                }`}
              >
                Mis Servicios
              </button>
              <button
                onClick={() => setActiveTab('profile')}
                className={`text-sm font-medium transition ${
                  activeTab === 'profile' ? 'text-emerald-400' : 'text-white/70 hover:text-white'
                }`}
              >
                Mi Perfil
              </button>
              <button
                onClick={() => navigate('/')}
                className="text-sm font-medium text-white/70 hover:text-white transition"
              >
                Explorar Servicios
              </button>
            </nav>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-right hidden sm:block">
              <p className="text-white font-semibold text-sm">{user?.full_name || user?.email}</p>
              <p className="text-white/50 text-xs">{user?.email}</p>
            </div>
            <button
              onClick={handleLogout}
              className="bg-red-500/20 text-red-400 px-4 py-2 rounded-lg hover:bg-red-500/30 transition text-sm font-medium"
            >
              Cerrar Sesión
            </button>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-white mb-2">
            ¡Bienvenido, {user?.full_name || 'Usuario'}!
          </h2>
          <p className="text-white/70">
            Gestiona tus servicios y configuraciones desde aquí
          </p>
        </div>

        {/* Tabs Content */}
        {activeTab === 'services' && (
          <div>
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-2xl font-bold text-white">Mis Servicios Activos</h3>
              <button
                onClick={() => navigate('/')}
                className="bg-gradient-to-r from-emerald-500 to-teal-600 text-white px-6 py-2 rounded-lg hover:from-emerald-600 hover:to-teal-700 transition font-semibold"
              >
                + Contratar Nuevo Servicio
              </button>
            </div>

            {userServices.length === 0 ? (
              <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-12 text-center border border-white/20">
                <div className="text-6xl mb-4">📦</div>
                <h3 className="text-2xl font-bold text-white mb-2">No tienes servicios contratados</h3>
                <p className="text-white/70 mb-6">
                  Explora nuestro catálogo y contrata el servicio que necesites
                </p>
                <button
                  onClick={() => navigate('/')}
                  className="bg-gradient-to-r from-emerald-500 to-teal-600 text-white px-8 py-3 rounded-lg hover:from-emerald-600 hover:to-teal-700 transition font-semibold"
                >
                  Ver Servicios Disponibles
                </button>
              </div>
            ) : (
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                {userServices.map((service) => (
                  <div
                    key={service.id}
                    className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20 hover:border-emerald-400 transition"
                  >
                    <div className="flex items-start justify-between mb-4">
                      <h4 className="text-xl font-bold text-white">{service.name}</h4>
                      <span className="bg-green-500 text-white text-xs px-3 py-1 rounded-full font-bold">
                        Activo
                      </span>
                    </div>
                    <p className="text-white/70 text-sm mb-4">{service.short_description}</p>
                    <div className="mb-4">
                      <p className="text-white/50 text-xs mb-1">Vence:</p>
                      <p className="text-white font-semibold text-sm">
                        {service.expires_at ? new Date(service.expires_at).toLocaleDateString() : 'Sin vencimiento'}
                      </p>
                    </div>
                    <button
                      onClick={() => handleServiceAccess(service)}
                      className="w-full bg-gradient-to-r from-emerald-500 to-teal-600 text-white py-3 rounded-lg hover:from-emerald-600 hover:to-teal-700 transition font-semibold"
                    >
                      Abrir Servicio
                    </button>
                  </div>
                ))}
              </div>
            )}

            {/* Quick Access to Suite Crypto (Demo) */}
            <div className="mt-8">
              <h3 className="text-2xl font-bold text-white mb-4">Acceso Rápido (Demo)</h3>
              <div className="bg-gradient-to-r from-purple-500/20 to-pink-500/20 backdrop-blur-lg rounded-2xl p-6 border-2 border-purple-500/30">
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="text-2xl font-bold text-white mb-2">Suite Crypto IA</h4>
                    <p className="text-white/70 mb-4">
                      3 servicios especializados para inversores en criptomonedas
                    </p>
                    <div className="flex items-center gap-4 text-sm text-white/80">
                      <span>🛡️ CryptoShield</span>
                      <span>📊 Pulse IA</span>
                      <span>📈 Momentum Predictor</span>
                    </div>
                  </div>
                  <button
                    onClick={() => navigate('/dashboard/suite-crypto')}
                    className="bg-gradient-to-r from-purple-500 to-pink-600 text-white px-8 py-3 rounded-xl hover:from-purple-600 hover:to-pink-700 transition font-bold text-lg"
                  >
                    Acceder →
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'profile' && (
          <div className="max-w-2xl">
            <h3 className="text-2xl font-bold text-white mb-6">Mi Perfil</h3>
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
              <div className="space-y-6">
                <div>
                  <label className="block text-white/70 text-sm mb-2">Nombre Completo</label>
                  <input
                    type="text"
                    value={user?.full_name || ''}
                    disabled
                    className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/20 text-white"
                  />
                </div>
                <div>
                  <label className="block text-white/70 text-sm mb-2">Email</label>
                  <input
                    type="email"
                    value={user?.email || ''}
                    disabled
                    className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/20 text-white"
                  />
                </div>
                <div>
                  <label className="block text-white/70 text-sm mb-2">Fecha de Registro</label>
                  <input
                    type="text"
                    value={user?.created_at ? new Date(user.created_at).toLocaleDateString() : 'N/A'}
                    disabled
                    className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/20 text-white"
                  />
                </div>
                <div className="pt-4 border-t border-white/20">
                  <button className="bg-emerald-500 text-white px-6 py-3 rounded-lg hover:bg-emerald-600 transition font-semibold">
                    Actualizar Perfil
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ClientDashboard;
