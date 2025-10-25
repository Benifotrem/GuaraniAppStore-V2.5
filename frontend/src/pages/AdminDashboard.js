import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';
const API = `${BACKEND_URL}/api`;

const AdminDashboard = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [activeTab, setActiveTab] = useState('overview');
  const [stats, setStats] = useState(null);
  const [users, setUsers] = useState([]);
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Verificar si es admin
    if (!user || !user.is_admin) {
      navigate('/dashboard');
      return;
    }
    loadAdminData();
  }, []);

  const loadAdminData = async () => {
    try {
      const token = localStorage.getItem('token');
      
      // Cargar estadísticas
      const statsResponse = await axios.get(`${API}/admin/stats`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setStats(statsResponse.data);

      // Cargar usuarios
      const usersResponse = await axios.get(`${API}/admin/users`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setUsers(usersResponse.data);

      // Cargar servicios
      const servicesResponse = await axios.get(`${API}/services`);
      setServices(servicesResponse.data);
      
    } catch (error) {
      console.error('Error loading admin data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center">
        <div className="text-white text-xl">Cargando panel admin...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-indigo-900 to-slate-900">
      {/* Header */}
      <header className="bg-black/30 backdrop-blur-lg border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <h1 className="text-2xl font-bold text-white">🛡️ Panel Admin</h1>
            <nav className="hidden md:flex items-center gap-6">
              <button
                onClick={() => setActiveTab('overview')}
                className={`text-sm font-medium transition ${
                  activeTab === 'overview' ? 'text-emerald-400' : 'text-white/70 hover:text-white'
                }`}
              >
                Resumen
              </button>
              <button
                onClick={() => setActiveTab('users')}
                className={`text-sm font-medium transition ${
                  activeTab === 'users' ? 'text-emerald-400' : 'text-white/70 hover:text-white'
                }`}
              >
                Usuarios
              </button>
              <button
                onClick={() => setActiveTab('services')}
                className={`text-sm font-medium transition ${
                  activeTab === 'services' ? 'text-emerald-400' : 'text-white/70 hover:text-white'
                }`}
              >
                Servicios
              </button>
            </nav>
          </div>
          <div className="flex items-center gap-4">
            <button
              onClick={() => navigate('/client-dashboard')}
              className="text-white/70 hover:text-white text-sm font-medium"
            >
              Ver como Cliente
            </button>
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
        {/* Overview Tab */}
        {activeTab === 'overview' && (
          <div>
            <h2 className="text-3xl font-bold text-white mb-8">Resumen General</h2>
            
            {/* Stats Cards */}
            <div className="grid md:grid-cols-4 gap-6 mb-8">
              <div className="bg-gradient-to-br from-blue-500/20 to-cyan-500/20 backdrop-blur-lg rounded-2xl p-6 border border-blue-500/30">
                <p className="text-blue-400 text-sm mb-2">Total Usuarios</p>
                <p className="text-4xl font-bold text-white">{users.length || 0}</p>
              </div>
              <div className="bg-gradient-to-br from-green-500/20 to-emerald-500/20 backdrop-blur-lg rounded-2xl p-6 border border-green-500/30">
                <p className="text-green-400 text-sm mb-2">Servicios Activos</p>
                <p className="text-4xl font-bold text-white">{services.filter(s => s.status !== 'coming_soon').length || 0}</p>
              </div>
              <div className="bg-gradient-to-br from-purple-500/20 to-pink-500/20 backdrop-blur-lg rounded-2xl p-6 border border-purple-500/30">
                <p className="text-purple-400 text-sm mb-2">Suscripciones</p>
                <p className="text-4xl font-bold text-white">{stats?.total_subscriptions || 0}</p>
              </div>
              <div className="bg-gradient-to-br from-orange-500/20 to-yellow-500/20 backdrop-blur-lg rounded-2xl p-6 border border-orange-500/30">
                <p className="text-orange-400 text-sm mb-2">Ingresos (mes)</p>
                <p className="text-4xl font-bold text-white">Gs. {(stats?.monthly_revenue || 0).toLocaleString()}</p>
              </div>
            </div>

            {/* Recent Activity */}
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
              <h3 className="text-2xl font-bold text-white mb-6">Actividad Reciente</h3>
              <div className="space-y-4">
                <div className="flex items-center justify-between py-3 border-b border-white/10">
                  <div className="flex items-center gap-4">
                    <div className="bg-green-500/20 rounded-full p-2">
                      <span className="text-green-400">👤</span>
                    </div>
                    <div>
                      <p className="text-white font-semibold">Nuevo usuario registrado</p>
                      <p className="text-white/50 text-sm">Hace 2 horas</p>
                    </div>
                  </div>
                </div>
                <div className="flex items-center justify-between py-3 border-b border-white/10">
                  <div className="flex items-center gap-4">
                    <div className="bg-blue-500/20 rounded-full p-2">
                      <span className="text-blue-400">💳</span>
                    </div>
                    <div>
                      <p className="text-white font-semibold">Nueva suscripción a Suite Crypto</p>
                      <p className="text-white/50 text-sm">Hace 5 horas</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Users Tab */}
        {activeTab === 'users' && (
          <div>
            <h2 className="text-3xl font-bold text-white mb-8">Gestión de Usuarios</h2>
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-white/20">
                      <th className="text-left text-white/70 py-3 px-4">Usuario</th>
                      <th className="text-left text-white/70 py-3 px-4">Email</th>
                      <th className="text-left text-white/70 py-3 px-4">Servicios</th>
                      <th className="text-left text-white/70 py-3 px-4">Registro</th>
                      <th className="text-left text-white/70 py-3 px-4">Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    {users.map((u) => (
                      <tr key={u.id} className="border-b border-white/10">
                        <td className="text-white py-4 px-4">{u.full_name || 'Sin nombre'}</td>
                        <td className="text-white/70 py-4 px-4">{u.email}</td>
                        <td className="text-white py-4 px-4">{u.subscription_count || 0}</td>
                        <td className="text-white/70 py-4 px-4 text-sm">
                          {u.created_at ? new Date(u.created_at).toLocaleDateString() : 'N/A'}
                        </td>
                        <td className="py-4 px-4">
                          <button className="text-emerald-400 hover:text-emerald-300 text-sm font-medium">
                            Ver Detalles
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* Services Tab */}
        {activeTab === 'services' && (
          <div>
            <div className="flex items-center justify-between mb-8">
              <h2 className="text-3xl font-bold text-white">Gestión de Servicios</h2>
              <button className="bg-gradient-to-r from-emerald-500 to-teal-600 text-white px-6 py-3 rounded-lg hover:from-emerald-600 hover:to-teal-700 transition font-semibold">
                + Agregar Servicio
              </button>
            </div>
            <div className="grid md:grid-cols-2 gap-6">
              {services.map((service) => (
                <div
                  key={service.id}
                  className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20"
                >
                  <div className="flex items-start justify-between mb-4">
                    <h3 className="text-xl font-bold text-white">{service.name}</h3>
                    <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                      service.status === 'coming_soon' 
                        ? 'bg-yellow-500/20 text-yellow-400' 
                        : 'bg-green-500/20 text-green-400'
                    }`}>
                      {service.status === 'coming_soon' ? 'Próximamente' : 'Activo'}
                    </span>
                  </div>
                  <p className="text-white/70 text-sm mb-4">{service.short_description}</p>
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-white/50 text-xs">Precio Mensual</p>
                      <p className="text-white font-bold">
                        Gs. {service.price_monthly?.toLocaleString() || 'N/A'}
                      </p>
                    </div>
                    <button className="text-emerald-400 hover:text-emerald-300 text-sm font-medium">
                      Editar
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminDashboard;
