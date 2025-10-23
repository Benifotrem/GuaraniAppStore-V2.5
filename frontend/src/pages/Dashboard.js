import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Dashboard.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Dashboard = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [stats, setStats] = useState(null);
  const [orders, setOrders] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');
  const [editingProfile, setEditingProfile] = useState(false);
  const [profileData, setProfileData] = useState({});
  const [show2FAModal, setShow2FAModal] = useState(false);
  const [qrCode, setQrCode] = useState(null);
  const [twoFACode, setTwoFACode] = useState('');

  useEffect(() => {
    loadDashboardData();
  }, []);

  useEffect(() => {
    if (user && activeTab === 'transactions') {
      loadTransactions();
    }
  }, [activeTab, user]);

  const loadDashboardData = async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/');
      return;
    }

    try {
      const [userRes, statsRes, ordersRes, servicesRes] = await Promise.all([
        axios.get(`${API}/auth/me`, { headers: { Authorization: `Bearer ${token}` } }),
        axios.get(`${API}/user/dashboard/stats`, { headers: { Authorization: `Bearer ${token}` } }),
        axios.get(`${API}/orders/my-orders`, { headers: { Authorization: `Bearer ${token}` } }),
        axios.get(`${API}/services`)
      ]);

      setUser(userRes.data);
      setStats(statsRes.data);
      setOrders(ordersRes.data);
      setServices(servicesRes.data);
      setProfileData({
        full_name: userRes.data.full_name || '',
        phone: userRes.data.phone || '',
        company: userRes.data.company || '',
        country: userRes.data.country || '',
        timezone: userRes.data.timezone || ''
      });
      setLoading(false);
    } catch (e) {
      console.error('Error loading dashboard:', e);
      localStorage.removeItem('token');
      navigate('/');
    }
  };

  const loadTransactions = async () => {
    const token = localStorage.getItem('token');
    try {
      const res = await axios.get(`${API}/user/transactions`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setTransactions(res.data);
    } catch (e) {
      console.error('Error loading transactions:', e);
    }
  };

  const handleUpdateProfile = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem('token');
    
    try {
      await axios.put(`${API}/user/profile`, profileData, {
        headers: { Authorization: `Bearer ${token}` }
      });
      alert('✅ Perfil actualizado exitosamente');
      setEditingProfile(false);
      loadDashboardData();
    } catch (e) {
      alert('❌ Error al actualizar perfil');
    }
  };

  const handleEnable2FA = async () => {
    const token = localStorage.getItem('token');
    
    try {
      const res = await axios.post(`${API}/user/2fa/enable`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setQrCode(res.data.qr_code);
      setShow2FAModal(true);
    } catch (e) {
      alert('❌ Error al generar 2FA');
    }
  };

  const handleVerify2FA = async () => {
    const token = localStorage.getItem('token');
    
    try {
      await axios.post(`${API}/user/2fa/verify-enable`, 
        { token: twoFACode },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      alert('✅ 2FA activado exitosamente');
      setShow2FAModal(false);
      setTwoFACode('');
      loadDashboardData();
    } catch (e) {
      alert('❌ Código 2FA inválido');
    }
  };

  const handleDisable2FA = async () => {
    const code = prompt('Ingresa tu código 2FA para desactivar:');
    if (!code) return;

    const token = localStorage.getItem('token');
    
    try {
      await axios.post(`${API}/user/2fa/disable`,
        { token: code },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      alert('✅ 2FA desactivado');
      loadDashboardData();
    } catch (e) {
      alert('❌ Código 2FA inválido');
    }
  };


  const handleInitializeService = async (serviceId, serviceTitle) => {
    const token = localStorage.getItem('token');
    
    // Create slug from title
    const serviceSlug = serviceTitle.toLowerCase()
      .normalize('NFD').replace(/[\u0300-\u036f]/g, '') // Remove accents
      .replace(/\s+/g, '-')
      .replace(/[^a-z0-9-]/g, '');
    
    try {
      const response = await axios.post(
        `${API}/services/${serviceSlug}/initialize`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      );
      
      if (response.data.success) {
        // Show initialization result
        const result = response.data;
        
        let message = `✅ Servicio "${serviceTitle}" inicializado correctamente!\n\n`;
        
        if (result.bot_link) {
          message += `🤖 Bot: ${result.bot_link}\n\n`;
        }
        
        if (result.bots) {
          message += `🤖 Bots disponibles:\n`;
          Object.entries(result.bots).forEach(([key, link]) => {
            message += `- ${key}: ${link}\n`;
          });
          message += `\n`;
        }
        
        if (result.dashboard_url) {
          message += `📊 Dashboard: ${result.dashboard_url}\n\n`;
        }
        
        if (result.instructions) {
          if (Array.isArray(result.instructions)) {
            message += `📋 Instrucciones:\n${result.instructions.map((i, idx) => `${idx + 1}. ${i}`).join('\n')}\n\n`;
          } else if (typeof result.instructions === 'object') {
            message += `📋 Bots configurados:\n`;
            Object.entries(result.instructions).forEach(([botKey, botInfo]) => {
              message += `\n${botInfo.name}:\n`;
              if (botInfo.commands) {
                botInfo.commands.forEach(cmd => message += `  ${cmd}\n`);
              }
            });
          }
        }
        
        alert(message);
      } else {
        if (result.status === 'coming_soon') {
          alert(`⏳ El servicio "${serviceTitle}" estará disponible próximamente.\n\nMientras tanto, tu suscripción está activa y podrás acceder cuando esté listo.`);
        } else {
          alert(`❌ Error al inicializar: ${result.error || 'Error desconocido'}`);
        }
      }
    } catch (e) {
      console.error('Error initializing service:', e);
      alert('❌ Error al inicializar el servicio. Intenta nuevamente.');
    }
  };


  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/');
  };

  const handleDeleteAccount = async () => {
    try {
      const token = localStorage.getItem('token');
      await axios.delete(`${API}/user/account`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      alert('Tu cuenta ha sido eliminada exitosamente.');
      
      // Limpiar sesión y redirigir
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      navigate('/');
    } catch (error) {
      console.error('Error eliminando cuenta:', error);
      alert('Error al eliminar la cuenta: ' + (error.response?.data?.detail || 'Intenta de nuevo'));
    }
  };

  const handleCancelSubscription = async (subscriptionId, orderId) => {
    if (!window.confirm('¿Estás seguro de que deseas cancelar esta suscripción?\n\nSe cancelarán todos los cobros futuros, pero podrás seguir usando el servicio hasta el final del período actual.')) {
      return;
    }

    try {
      const token = localStorage.getItem('token');
      await axios.post(
        `${API}/subscription/cancel`,
        { subscription_id: subscriptionId, order_id: orderId },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      
      alert('Suscripción cancelada exitosamente. Podrás seguir usando el servicio hasta el final del período actual.');
      
      // Recargar transacciones
      fetchTransactions();
    } catch (error) {
      console.error('Error cancelando suscripción:', error);
      alert('Error al cancelar la suscripción: ' + (error.response?.data?.detail || 'Intenta de nuevo'));
    }
  };

  const formatPrice = (price) => {
    return 'Gs. ' + new Intl.NumberFormat('es-PY', { minimumFractionDigits: 0 }).format(price);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString('es-PY', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getStatusBadge = (status) => {
    const styles = {
      pending: 'bg-yellow-100 text-yellow-800',
      completed: 'bg-green-100 text-green-800',
      failed: 'bg-red-100 text-red-800',
      expired: 'bg-gray-100 text-gray-800'
    };
    const labels = {
      pending: 'Pendiente',
      completed: 'Completado',
      failed: 'Fallido',
      expired: 'Expirado'
    };
    return { style: styles[status] || 'bg-gray-100 text-gray-800', label: labels[status] || status };
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-emerald-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Cargando tu dashboard...</p>
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
              <h1 className="text-2xl font-bold text-gray-900">Mi Panel</h1>
              <p className="text-sm text-gray-500 mt-1">Bienvenido, {user?.full_name || user?.email}</p>
            </div>
            <div className="flex items-center gap-4">
              <button
                onClick={() => navigate('/')}
                className="px-4 py-2 text-sm text-gray-700 hover:text-emerald-600 transition-colors"
              >
                🏠 Inicio
              </button>
              {user?.role === 'admin' && (
                <button
                  onClick={() => navigate('/admin')}
                  className="px-4 py-2 text-sm bg-purple-500 text-white rounded-lg hover:bg-purple-600 transition-colors"
                >
                  👑 Admin Panel
                </button>
              )}
              <button
                onClick={handleLogout}
                className="px-4 py-2 text-sm bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
              >
                Cerrar Sesión
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Tabs */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8 overflow-x-auto">
            {[
              { id: 'overview', label: '📊 Resumen', icon: '📊' },
              { id: 'services', label: '⚙️ Mis Servicios', icon: '⚙️' },
              { id: 'orders', label: '🛒 Mis Órdenes', icon: '🛒' },
              { id: 'transactions', label: '💳 Transacciones', icon: '💳' },
              { id: 'profile', label: '👤 Perfil', icon: '👤' }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-4 px-1 border-b-2 font-medium text-sm whitespace-nowrap transition-colors ${
                  activeTab === tab.id
                    ? 'border-emerald-500 text-emerald-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Overview Tab */}
        {activeTab === 'overview' && stats && (
          <div className="space-y-6">
            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Total Órdenes</p>
                    <p className="text-3xl font-bold text-gray-900 mt-2">{stats.total_orders}</p>
                  </div>
                  <div className="text-4xl">🛒</div>
                </div>
              </div>

              <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Suscripciones Activas</p>
                    <p className="text-3xl font-bold text-gray-900 mt-2">{stats.active_subscriptions}</p>
                  </div>
                  <div className="text-4xl">✅</div>
                </div>
              </div>

              <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Órdenes Pendientes</p>
                    <p className="text-3xl font-bold text-gray-900 mt-2">{stats.pending_orders}</p>
                  </div>
                  <div className="text-4xl">⏳</div>
                </div>
              </div>

              <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Total Gastado</p>
                    <p className="text-2xl font-bold text-gray-900 mt-2">{formatPrice(stats.total_spent)}</p>
                  </div>
                  <div className="text-4xl">💰</div>
                </div>
              </div>
            </div>

            {/* Recent Orders */}
            {stats.recent_orders && stats.recent_orders.length > 0 && (
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Órdenes Recientes</h3>
                <div className="space-y-3">
                  {stats.recent_orders.map((order) => {
                    const badge = getStatusBadge(order.payment_status);
                    return (
                      <div key={order.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                        <div className="flex-1">
                          <p className="text-sm font-medium text-gray-900">
                            Orden #{order.order_number}
                          </p>
                          <p className="text-xs text-gray-500 mt-1">
                            {formatDate(order.created_at)}
                          </p>
                        </div>
                        <div className="flex items-center gap-4">
                          <span className="text-lg font-bold text-emerald-600">
                            {formatPrice(order.final_price)}
                          </span>
                          <span className={`px-3 py-1 text-xs rounded-full ${badge.style}`}>
                            {badge.label}
                          </span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* Quick Actions */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Acciones Rápidas</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <button
                  onClick={() => navigate('/')}
                  className="p-4 border-2 border-emerald-500 text-emerald-600 rounded-lg hover:bg-emerald-50 transition-colors text-center"
                >
                  <div className="text-3xl mb-2">🛍️</div>
                  <p className="font-medium">Ver Servicios</p>
                </button>
                <button
                  onClick={() => setActiveTab('orders')}
                  className="p-4 border-2 border-blue-500 text-blue-600 rounded-lg hover:bg-blue-50 transition-colors text-center"
                >
                  <div className="text-3xl mb-2">📦</div>
                  <p className="font-medium">Mis Órdenes</p>
                </button>
                <button
                  onClick={() => setActiveTab('profile')}
                  className="p-4 border-2 border-purple-500 text-purple-600 rounded-lg hover:bg-purple-50 transition-colors text-center"
                >
                  <div className="text-3xl mb-2">⚙️</div>
                  <p className="font-medium">Configuración</p>
                </button>
              </div>
            </div>
          </div>
        )}


        {/* My Services Tab */}
        {activeTab === 'services' && (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-bold text-gray-900">Mis Servicios Activos</h2>
              <button
                onClick={() => navigate('/')}
                className="px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700"
              >
                ➕ Contratar Más Servicios
              </button>
            </div>

            {orders.filter(o => o.payment_status === 'completed').length === 0 ? (
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
                <div className="text-6xl mb-4">⚙️</div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">No tienes servicios activos</h3>
                <p className="text-gray-600 mb-6">Contrata un servicio para comenzar a usar nuestras herramientas</p>
                <button
                  onClick={() => navigate('/')}
                  className="px-6 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700"
                >
                  Ver Servicios Disponibles
                </button>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {services
                  .filter(service => {
                    // Check if user has active subscription for this service
                    return orders.some(order => 
                      order.service_id === service.id && order.payment_status === 'completed'
                    );
                  })
                  .map(service => (
                    <div key={service.id} className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-lg transition-shadow">
                      <div className="flex justify-between items-start mb-4">
                        <h3 className="text-lg font-bold text-gray-900">{service.title}</h3>
                        <span className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">
                          Activo
                        </span>
                      </div>
                      
                      <p className="text-sm text-gray-600 mb-4 line-clamp-2">{service.description}</p>
                      
                      <div className="space-y-2 mb-4">
                        <div className="flex items-center gap-2 text-sm text-gray-600">
                          <span>📅</span>
                          <span>Plan: {orders.find(o => o.service_id === service.id && o.payment_status === 'completed')?.plan_type || 'N/A'}</span>
                        </div>
                        <div className="flex items-center gap-2 text-sm text-gray-600">
                          <span>💰</span>
                          <span>Pagado: {formatPrice(orders.find(o => o.service_id === service.id && o.payment_status === 'completed')?.final_price || 0)}</span>
                        </div>
                      </div>

                      {/* Service Access Buttons */}
                      {(service.title.toLowerCase().includes('suite crypto') || service.title.toLowerCase().includes('cryptoshield')) ? (
                        <div className="space-y-3">
                          <button
                            onClick={() => navigate('/services/crypto-suite')}
                            className="w-full px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors flex items-center justify-center gap-2"
                          >
                            <span>🚀</span>
                            <span>Panel Suite Crypto</span>
                          </button>
                          <div className="bg-purple-50 rounded-lg p-3 text-xs">
                            <p className="font-semibold text-purple-900 mb-2">🤖 Bots de Telegram incluidos:</p>
                            <div className="space-y-1.5 text-purple-700">
                              <div className="flex items-center gap-2">
                                <span>📊</span>
                                <a href="https://t.me/Rojiverdebot" target="_blank" rel="noopener noreferrer" className="hover:underline">
                                  Pulse IA (@Rojiverdebot)
                                </a>
                              </div>
                              <div className="flex items-center gap-2">
                                <span>🛡️</span>
                                <a href="https://t.me/stopfraudebot" target="_blank" rel="noopener noreferrer" className="hover:underline">
                                  CryptoShield IA (@stopfraudebot)
                                </a>
                              </div>
                              <div className="flex items-center gap-2">
                                <span>🚀</span>
                                <a href="https://t.me/Mejormomentobot" target="_blank" rel="noopener noreferrer" className="hover:underline">
                                  Momentum IA (@Mejormomentobot)
                                </a>
                              </div>
                            </div>
                          </div>
                        </div>
                      ) : service.title.toLowerCase().includes('asistente') && service.title.toLowerCase().includes('directivos') ? (
                        <div className="space-y-3">
                          <button
                            onClick={() => navigate('/services/asistente-directivos')}
                            className="w-full px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors flex items-center justify-center gap-2"
                          >
                            <span>👔</span>
                            <span>Configurar Asistente</span>
                          </button>
                          <div className="bg-blue-50 rounded-lg p-3 text-xs">
                            <p className="font-semibold text-blue-900 mb-2">📱 Acceso por Telegram:</p>
                            <div className="text-blue-700">
                              <a 
                                href="https://t.me/GuaraniAssistantBot" 
                                target="_blank" 
                                rel="noopener noreferrer" 
                                className="hover:underline flex items-center gap-2"
                              >
                                <span>🤖</span>
                                <span>GuaraniAppStore Assistant (@GuaraniAssistantBot)</span>
                              </a>
                            </div>
                            <p className="text-blue-600 mt-2">Gestiona servicios que usan Telegram</p>
                          </div>
                        </div>
                      ) : service.title.toLowerCase().includes('preselección') || service.title.toLowerCase().includes('curricular') ? (
                        <button
                          onClick={() => navigate('/services/preseleccion-curricular')}
                          className="w-full px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors flex items-center justify-center gap-2"
                        >
                          <span>👥</span>
                          <span>Panel de Preselección</span>
                        </button>
                      ) : service.title.toLowerCase().includes('facturas') || service.title.toLowerCase().includes('contador') ? (
                        <button
                          onClick={() => navigate('/services/organizador-facturas')}
                          className="w-full px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors flex items-center justify-center gap-2"
                        >
                          <span>🧾</span>
                          <span>Organizador de Facturas</span>
                        </button>
                      ) : service.title.toLowerCase().includes('agenda') ? (
                        <button
                          onClick={() => navigate('/services/organizador-agenda')}
                          className="w-full px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors flex items-center justify-center gap-2"
                        >
                          <span>📅</span>
                          <span>Organizador de Agenda</span>
                        </button>
                      ) : (
                        <button
                          onClick={() => handleInitializeService(service.id, service.title)}
                          className="w-full px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors flex items-center justify-center gap-2"
                        >
                          <span>🚀</span>
                          <span>Acceder al Servicio</span>
                        </button>
                      )}
                    </div>
                  ))}
              </div>
            )}
          </div>
        )}

        {/* Orders Tab */}
        {activeTab === 'orders' && (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-bold text-gray-900">Mis Órdenes</h2>
              <button
                onClick={() => navigate('/')}
                className="px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700"
              >
                ➕ Nueva Orden
              </button>
            </div>

            {orders.length === 0 ? (
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
                <div className="text-6xl mb-4">📦</div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">No tienes órdenes aún</h3>
                <p className="text-gray-600 mb-6">Explora nuestros servicios y realiza tu primera compra</p>
                <button
                  onClick={() => navigate('/')}
                  className="px-6 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700"
                >
                  Ver Servicios
                </button>
              </div>
            ) : (
              <div className="grid grid-cols-1 gap-6">
                {orders.map((order) => {
                  const badge = getStatusBadge(order.payment_status);
                  return (
                    <div key={order.id} className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                      <div className="flex justify-between items-start mb-4">
                        <div>
                          <h3 className="text-lg font-semibold text-gray-900">
                            Orden #{order.order_number}
                          </h3>
                          <p className="text-sm text-gray-600 mt-1">{formatDate(order.created_at)}</p>
                        </div>
                        <span className={`px-3 py-1 text-xs rounded-full ${badge.style}`}>
                          {badge.label}
                        </span>
                      </div>

                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-4">
                        <div>
                          <p className="text-xs text-gray-600">Plan</p>
                          <p className="text-sm font-medium text-gray-900 capitalize">{order.plan_type}</p>
                        </div>
                        <div>
                          <p className="text-xs text-gray-600">Método de Pago</p>
                          <p className="text-sm font-medium text-gray-900 uppercase">{order.payment_method}</p>
                        </div>
                        <div>
                          <p className="text-xs text-gray-600">Descuento</p>
                          <p className="text-sm font-medium text-gray-900">{order.discount_percentage || 0}%</p>
                        </div>
                        <div>
                          <p className="text-xs text-gray-600">Total</p>
                          <p className="text-lg font-bold text-emerald-600">{formatPrice(order.final_price)}</p>
                        </div>
                      </div>

                      {order.payment_status === 'pending' && order.payment_url && (
                        <div className="mt-4 pt-4 border-t border-gray-200">
                          <a
                            href={order.payment_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-block px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700"
                          >
                            💳 Completar Pago
                          </a>
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        )}

        {/* Transactions Tab */}
        {activeTab === 'transactions' && (
          <div className="space-y-6">
            <h2 className="text-xl font-bold text-gray-900">Historial de Transacciones</h2>

            {transactions.length === 0 ? (
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
                <div className="text-6xl mb-4">💳</div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">No hay transacciones</h3>
                <p className="text-gray-600">Tus transacciones aparecerán aquí</p>
              </div>
            ) : (
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
                <div className="overflow-x-auto">
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Orden</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Monto</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Método</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Gateway</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Fecha</th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Acciones</th>
                      </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                      {transactions.map((tx) => {
                        const badge = getStatusBadge(tx.status);
                        return (
                          <tr key={tx.id} className="hover:bg-gray-50">
                            <td className="px-6 py-4 text-sm text-gray-900">
                              {tx.id.substring(0, 8)}...
                            </td>
                            <td className="px-6 py-4 text-sm text-gray-900">
                              {tx.order_id.substring(0, 8)}...
                            </td>
                            <td className="px-6 py-4 text-sm font-semibold text-gray-900">
                              {formatPrice(tx.amount)}
                            </td>
                            <td className="px-6 py-4 text-sm">
                              <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded uppercase text-xs">
                                {tx.payment_method}
                              </span>
                            </td>
                            <td className="px-6 py-4 text-sm text-gray-600 uppercase">
                              {tx.gateway}
                            </td>
                            <td className="px-6 py-4">
                              <span className={`px-2 py-1 text-xs rounded-full ${badge.style}`}>
                                {badge.label}
                              </span>
                            </td>
                            <td className="px-6 py-4 text-sm text-gray-500">
                              {formatDate(tx.created_at)}
                            </td>
                            <td className="px-6 py-4">
                              {tx.subscription_id && tx.status === 'completed' ? (
                                <button
                                  onClick={() => handleCancelSubscription(tx.subscription_id, tx.order_id)}
                                  className="px-3 py-1 bg-red-100 text-red-700 text-xs font-semibold rounded-lg hover:bg-red-200 transition-colors"
                                >
                                  ❌ Cancelar Suscripción
                                </button>
                              ) : (
                                <span className="text-xs text-gray-400">-</span>
                              )}
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Profile Tab */}
        {activeTab === 'profile' && (
          <div className="space-y-6">
            <h2 className="text-xl font-bold text-gray-900">Mi Perfil y Configuración</h2>

            {/* Profile Info */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <div className="flex justify-between items-center mb-6">
                <h3 className="text-lg font-semibold text-gray-900">Información Personal</h3>
                <button
                  onClick={() => setEditingProfile(!editingProfile)}
                  className="px-4 py-2 text-sm bg-blue-500 text-white rounded-lg hover:bg-blue-600"
                >
                  {editingProfile ? 'Cancelar' : '✏️ Editar'}
                </button>
              </div>

              {editingProfile ? (
                <form onSubmit={handleUpdateProfile} className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Nombre Completo</label>
                      <input
                        type="text"
                        value={profileData.full_name}
                        onChange={(e) => setProfileData({...profileData, full_name: e.target.value})}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Teléfono</label>
                      <input
                        type="tel"
                        value={profileData.phone}
                        onChange={(e) => setProfileData({...profileData, phone: e.target.value})}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">Empresa</label>
                      <input
                        type="text"
                        value={profileData.company}
                        onChange={(e) => setProfileData({...profileData, company: e.target.value})}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">País</label>
                      <input
                        type="text"
                        value={profileData.country}
                        onChange={(e) => setProfileData({...profileData, country: e.target.value})}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                      />
                    </div>
                  </div>
                  <button
                    type="submit"
                    className="px-6 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700"
                  >
                    💾 Guardar Cambios
                  </button>
                </form>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <p className="text-sm text-gray-600">Email</p>
                    <p className="text-base font-medium text-gray-900 mt-1">{user?.email}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Nombre Completo</p>
                    <p className="text-base font-medium text-gray-900 mt-1">{user?.full_name || 'No configurado'}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Teléfono</p>
                    <p className="text-base font-medium text-gray-900 mt-1">{user?.phone || 'No configurado'}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Empresa</p>
                    <p className="text-base font-medium text-gray-900 mt-1">{user?.company || 'No configurado'}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">País</p>
                    <p className="text-base font-medium text-gray-900 mt-1">{user?.country}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Zona Horaria</p>
                    <p className="text-base font-medium text-gray-900 mt-1">{user?.timezone}</p>
                  </div>
                </div>
              )}
            </div>

            {/* 2FA Settings */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Autenticación de Dos Factores (2FA)</h3>
              
              <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div>
                  <p className="font-medium text-gray-900">Estado de 2FA</p>
                  <p className="text-sm text-gray-600 mt-1">
                    {user?.two_factor_enabled ? 
                      '✅ Activado - Tu cuenta está protegida' : 
                      '⚠️ Desactivado - Activa 2FA para mayor seguridad'
                    }
                  </p>
                </div>
                {user?.two_factor_enabled ? (
                  <button
                    onClick={handleDisable2FA}
                    className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
                  >
                    Desactivar 2FA
                  </button>
                ) : (
                  <button
                    onClick={handleEnable2FA}
                    className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600"
                  >
                    Activar 2FA
                  </button>
                )}
              </div>
            </div>

            {/* Account Info */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Información de Cuenta</h3>
              <div className="space-y-3">
                <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                  <span className="text-sm text-gray-600">Rol</span>
                  <span className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full capitalize">
                    {user?.role}
                  </span>
                </div>
                <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                  <span className="text-sm text-gray-600">Estado</span>
                  <span className={`px-3 py-1 text-sm rounded-full ${
                    user?.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                  }`}>
                    {user?.is_active ? 'Activa' : 'Inactiva'}
                  </span>
                </div>
                <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                  <span className="text-sm text-gray-600">Email Verificado</span>
                  <span className={`px-3 py-1 text-sm rounded-full ${
                    user?.is_verified ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                  }`}>
                    {user?.is_verified ? '✓ Verificado' : 'Pendiente'}
                  </span>
                </div>
                <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                  <span className="text-sm text-gray-600">Miembro desde</span>
                  <span className="text-sm font-medium text-gray-900">
                    {formatDate(user?.created_at)}
                  </span>
                </div>
              </div>
            </div>


            {/* Danger Zone - Eliminar Cuenta */}
            <div className="bg-red-50 border-2 border-red-200 rounded-xl shadow-sm p-6">
              <h3 className="text-lg font-semibold text-red-800 mb-4">⚠️ Zona de Peligro</h3>
              <p className="text-sm text-red-700 mb-4">
                Una vez que elimines tu cuenta, no hay vuelta atrás. Por favor, asegúrate de que realmente deseas hacerlo.
              </p>
              <button
                onClick={() => {
                  if (window.confirm('¿Estás absolutamente seguro de que deseas eliminar tu cuenta? Esta acción NO se puede deshacer.\n\nSe eliminarán:\n- Todos tus datos personales\n- Tus servicios contratados\n- Tu historial de transacciones\n- Tus conversaciones\n\n¿Continuar?')) {
                    handleDeleteAccount();
                  }
                }}
                className="px-6 py-3 bg-red-600 text-white font-semibold rounded-lg hover:bg-red-700 transition-colors"
              >
                🗑️ Eliminar Mi Cuenta Permanentemente
              </button>
            </div>

          </div>
        )}
      </main>

      {/* 2FA Modal */}
      {show2FAModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-xl max-w-md w-full p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Configurar 2FA</h2>
            
            <div className="mb-6">
              <p className="text-sm text-gray-600 mb-4">
                Escanea este código QR con tu aplicación de autenticación (Google Authenticator, Authy, etc.)
              </p>
              {qrCode && (
                <div className="flex justify-center mb-4">
                  <img src={qrCode} alt="QR Code" className="w-64 h-64" />
                </div>
              )}
            </div>

            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Ingresa el código de 6 dígitos
              </label>
              <input
                type="text"
                value={twoFACode}
                onChange={(e) => setTwoFACode(e.target.value)}
                maxLength={6}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg text-center text-2xl tracking-widest focus:ring-2 focus:ring-emerald-500"
                placeholder="000000"
              />
            </div>

            <div className="flex gap-3">
              <button
                onClick={() => {
                  setShow2FAModal(false);
                  setTwoFACode('');
                  setQrCode(null);
                }}
                className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50"
              >
                Cancelar
              </button>
              <button
                onClick={handleVerify2FA}
                disabled={twoFACode.length !== 6}
                className="flex-1 px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 disabled:bg-gray-300 disabled:cursor-not-allowed"
              >
                Verificar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
