import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import BlogAdminPanel from './BlogAdminPanel';
import './AdminPanel.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const AdminPanel = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [stats, setStats] = useState(null);
  const [users, setUsers] = useState([]);
  const [orders, setOrders] = useState([]);
  const [services, setServices] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [filterStatus, setFilterStatus] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [editingService, setEditingService] = useState(null);
  const [showServiceModal, setShowServiceModal] = useState(false);
  const [bots, setBots] = useState([]);
  const [botsLoading, setBotsLoading] = useState(false);
  const [paymentGateways, setPaymentGateways] = useState([]);
  const [editingGateway, setEditingGateway] = useState(null);
  const [showGatewayModal, setShowGatewayModal] = useState(false);

  useEffect(() => {
    checkAdminAuth();
  }, []);

  useEffect(() => {
    if (user && user.role === 'admin') {
      loadData();
    }
  }, [activeTab, filterStatus, user]);

  const checkAdminAuth = async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/');
      return;
    }

    try {
      const userResponse = await axios.get(`${API}/auth/me`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      if (userResponse.data.role !== 'admin') {
        alert('Acceso denegado: Solo administradores');
        navigate('/dashboard');
        return;
      }

      setUser(userResponse.data);
      setLoading(false);
    } catch (e) {
      console.error('Auth error:', e);
      localStorage.removeItem('token');
      navigate('/');
    }
  };

  const loadData = async () => {
    const token = localStorage.getItem('token');
    const headers = { Authorization: `Bearer ${token}` };

    try {
      if (activeTab === 'dashboard') {
        const [statsRes, analyticsRes] = await Promise.all([
          axios.get(`${API}/admin/stats`, { headers }),
          axios.get(`${API}/admin/analytics?days=30`, { headers })
        ]);
        setStats(statsRes.data);
        setAnalytics(analyticsRes.data);
      } else if (activeTab === 'users') {
        const usersResponse = await axios.get(`${API}/admin/users`, { headers });
        setUsers(usersResponse.data);
      } else if (activeTab === 'orders') {
        const url = `${API}/admin/orders${filterStatus !== 'all' ? `?payment_status=${filterStatus}` : ''}`;
        const ordersResponse = await axios.get(url, { headers });
        setOrders(ordersResponse.data);
      } else if (activeTab === 'services') {
        const servicesResponse = await axios.get(`${API}/admin/services/manage`, { headers });
        setServices(servicesResponse.data);
      } else if (activeTab === 'transactions') {
        const transactionsResponse = await axios.get(`${API}/admin/transactions`, { headers });
        setTransactions(transactionsResponse.data);
      } else if (activeTab === 'bots') {
        await loadBots();
      } else if (activeTab === 'payments') {
        await loadPaymentGateways();
      }
    } catch (e) {
      console.error('Error loading data:', e);
    }
  };

  const loadPaymentGateways = async () => {
    const token = localStorage.getItem('token');
    try {
      const response = await axios.get(`${API}/admin/payment-gateways`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setPaymentGateways(response.data);
    } catch (e) {
      console.error('Error loading payment gateways:', e);
    }
  };

  const saveGateway = async (gatewayData) => {
    const token = localStorage.getItem('token');
    try {
      await axios.post(`${API}/admin/payment-gateways`, gatewayData, {
        headers: { Authorization: `Bearer ${token}` }
      });
      await loadPaymentGateways();
      setShowGatewayModal(false);
      setEditingGateway(null);
      alert('✅ Pasarela guardada correctamente');
    } catch (e) {
      console.error('Error saving gateway:', e);
      alert('❌ Error al guardar la pasarela');
    }
  };

  const loadBots = async () => {
    const token = localStorage.getItem('token');
    setBotsLoading(true);
    try {
      const response = await axios.get(`${API}/admin/bots/status`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      if (response.data.success) {
        // Convert bots object to array for easier rendering with correct info
        const botsArray = [
          { 
            id: 'asistente', 
            name: 'GuaraniAppStore Assistant', 
            username: '@GuaraniAssistantBot',
            description: 'Gestiona servicios que usan Telegram (NO crypto)', 
            icon: '🤖', 
            category: 'General',
            ...response.data.bots['Asistente Directivos'] 
          },
          { 
            id: 'pulse', 
            name: 'Pulse IA', 
            username: '@Rojiverdebot',
            description: 'Análisis de Sentimiento de las 50 cryptos más relevantes', 
            icon: '📊', 
            category: 'Crypto',
            ...response.data.bots['Pulse IA'] 
          },
          { 
            id: 'cryptoshield', 
            name: 'CryptoShield IA', 
            username: '@stopfraudebot',
            description: 'Analiza Criptomonedas y evalúa potencial de fraude', 
            icon: '🛡️', 
            category: 'Crypto',
            ...response.data.bots['CryptoShield IA'] 
          },
          { 
            id: 'momentum', 
            name: 'Momentum Predictor IA', 
            username: '@Mejormomentobot',
            description: 'Evalúa el mejor momento para entrar o salir del mercado', 
            icon: '🚀', 
            category: 'Crypto',
            ...response.data.bots['Momentum Predictor IA'] 
          },
          { 
            id: 'agente_ventas', 
            name: 'Rocío Almeida - GuaraniAppStore', 
            username: '@RocioAlmeidaBot',
            description: 'Agente de ventas autónomo en Telegram para buscar clientes', 
            icon: '👩‍💼', 
            category: 'Sales',
            ...response.data.bots['Agente Ventas IA'] 
          }
        ];
        setBots(botsArray);
      }
    } catch (e) {
      console.error('Error loading bots:', e);
    } finally {
      setBotsLoading(false);
    }
  };

  const handleStartBot = async (botId) => {
    const token = localStorage.getItem('token');
    setBotsLoading(true);
    try {
      await axios.post(`${API}/admin/bots/start/${botId}`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      await loadBots();
      alert(`Bot ${botId} iniciado correctamente`);
    } catch (e) {
      console.error('Error starting bot:', e);
      alert('Error al iniciar el bot');
    } finally {
      setBotsLoading(false);
    }
  };

  const handleStopBot = async (botId) => {
    const token = localStorage.getItem('token');
    setBotsLoading(true);
    try {
      await axios.post(`${API}/admin/bots/stop/${botId}`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      await loadBots();
      alert(`Bot ${botId} detenido correctamente`);
    } catch (e) {
      console.error('Error stopping bot:', e);
      alert('Error al detener el bot');
    } finally {
      setBotsLoading(false);
    }
  };

  const handleStartAllBots = async () => {
    const token = localStorage.getItem('token');
    setBotsLoading(true);
    try {
      await axios.post(`${API}/admin/bots/start-all`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      await loadBots();
      alert('Todos los bots han sido iniciados');
    } catch (e) {
      console.error('Error starting all bots:', e);
      alert('Error al iniciar los bots');
    } finally {
      setBotsLoading(false);
    }
  };

  const handleStopAllBots = async () => {
    const token = localStorage.getItem('token');
    setBotsLoading(true);
    try {
      await axios.post(`${API}/admin/bots/stop-all`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
      await loadBots();
      alert('Todos los bots han sido detenidos');
    } catch (e) {
      console.error('Error stopping all bots:', e);
      alert('Error al detener los bots');
    } finally {
      setBotsLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;
    
    const token = localStorage.getItem('token');
    try {
      const response = await axios.get(
        `${API}/admin/search?q=${searchQuery}&type=${activeTab === 'users' ? 'users' : activeTab === 'orders' ? 'orders' : 'services'}`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      
      if (activeTab === 'users') {
        setUsers(response.data);
      } else if (activeTab === 'orders') {
        setOrders(response.data);
      } else if (activeTab === 'services') {
        setServices(response.data);
      }
    } catch (e) {
      console.error('Search error:', e);
    }
  };

  const handleUpdateUserRole = async (userId, newRole) => {
    const token = localStorage.getItem('token');
    try {
      await axios.put(
        `${API}/admin/users/${userId}/role`,
        { role: newRole },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      alert('✅ Rol actualizado exitosamente');
      loadData();
    } catch (e) {
      alert('❌ Error al actualizar rol');
    }
  };

  const handleToggleUserStatus = async (userId, isActive) => {
    const token = localStorage.getItem('token');
    try {
      await axios.put(
        `${API}/admin/users/${userId}/status`,
        { is_active: !isActive },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      alert('✅ Estado actualizado exitosamente');
      loadData();
    } catch (e) {
      alert('❌ Error al actualizar estado');
    }
  };

  const handleUpdateOrderStatus = async (orderId, newStatus) => {
    const token = localStorage.getItem('token');
    try {
      await axios.put(
        `${API}/admin/orders/${orderId}/status`,
        { status: newStatus },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      alert('✅ Estado de orden actualizado');
      loadData();
    } catch (e) {
      alert('❌ Error al actualizar orden');
    }
  };

  const handleUpdateService = async (serviceData) => {
    const token = localStorage.getItem('token');
    try {
      if (editingService) {
        await axios.put(
          `${API}/admin/services/${editingService.id}`,
          serviceData,
          { headers: { Authorization: `Bearer ${token}` } }
        );
        alert('✅ Servicio actualizado');
      } else {
        await axios.post(
          `${API}/admin/services`,
          serviceData,
          { headers: { Authorization: `Bearer ${token}` } }
        );
        alert('✅ Servicio creado');
      }
      setShowServiceModal(false);
      setEditingService(null);
      loadData();
    } catch (e) {
      alert('❌ Error al guardar servicio');
    }
  };

  const handleDeleteService = async (serviceId) => {
    if (!window.confirm('¿Estás seguro de eliminar este servicio?')) return;
    
    const token = localStorage.getItem('token');
    try {
      await axios.delete(
        `${API}/admin/services/${serviceId}`,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      alert('✅ Servicio eliminado');
      loadData();
    } catch (e) {
      alert('❌ Error al eliminar servicio');
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

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/');
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-emerald-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Cargando panel de administración...</p>
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
              <h1 className="text-2xl font-bold text-gray-900">Panel de Administración</h1>
              <p className="text-sm text-gray-500 mt-1">GuaraniAppStore V2.5 Pro</p>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-600">
                👤 {user?.full_name || user?.email}
              </span>
              <button
                onClick={() => navigate('/dashboard')}
                className="px-4 py-2 text-sm text-gray-700 hover:text-emerald-600 transition-colors"
              >
                Mi Panel
              </button>
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

      {/* Tabs Navigation */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8 overflow-x-auto">
            {[
              { id: 'dashboard', label: '📊 Dashboard', icon: '📊' },
              { id: 'users', label: '👥 Usuarios', icon: '👥' },
              { id: 'orders', label: '🛒 Órdenes', icon: '🛒' },
              { id: 'services', label: '⚙️ Servicios', icon: '⚙️' },
              { id: 'blog', label: '📝 Blog', icon: '📝' },
              { id: 'bots', label: '🤖 Telegram Bots', icon: '🤖' },
              { id: 'payments', label: '💳 Pasarelas de Pago', icon: '💳' },
              { id: 'transactions', label: '💰 Transacciones', icon: '💰' }
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
        {/* Dashboard Tab */}
        {activeTab === 'dashboard' && stats && (
          <div className="space-y-6">
            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Total Usuarios</p>
                    <p className="text-3xl font-bold text-gray-900 mt-2">{stats.users.total}</p>
                    <p className="text-xs text-green-600 mt-1">
                      ✓ {stats.users.verified} verificados
                    </p>
                  </div>
                  <div className="text-4xl">👥</div>
                </div>
              </div>

              <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Total Órdenes</p>
                    <p className="text-3xl font-bold text-gray-900 mt-2">{stats.orders.total}</p>
                    <p className="text-xs text-green-600 mt-1">
                      ✓ {stats.orders.completed} completadas
                    </p>
                  </div>
                  <div className="text-4xl">🛒</div>
                </div>
              </div>

              <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Ingresos Totales</p>
                    <p className="text-2xl font-bold text-gray-900 mt-2">
                      {formatPrice(stats.revenue.total)}
                    </p>
                    <p className="text-xs text-gray-500 mt-1">
                      De órdenes completadas
                    </p>
                  </div>
                  <div className="text-4xl">💰</div>
                </div>
              </div>

              <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-600">Servicios Activos</p>
                    <p className="text-3xl font-bold text-gray-900 mt-2">{stats.services.total}</p>
                    <p className="text-xs text-gray-500 mt-1">
                      Disponibles
                    </p>
                  </div>
                  <div className="text-4xl">⚙️</div>
                </div>
              </div>
            </div>

            {/* Order Status Distribution */}
            <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Estado de Órdenes</h3>
              <div className="grid grid-cols-3 gap-4">
                <div className="text-center p-4 bg-yellow-50 rounded-lg">
                  <p className="text-2xl font-bold text-yellow-600">{stats.orders.pending}</p>
                  <p className="text-sm text-gray-600 mt-1">Pendientes</p>
                </div>
                <div className="text-center p-4 bg-green-50 rounded-lg">
                  <p className="text-2xl font-bold text-green-600">{stats.orders.completed}</p>
                  <p className="text-sm text-gray-600 mt-1">Completadas</p>
                </div>
                <div className="text-center p-4 bg-red-50 rounded-lg">
                  <p className="text-2xl font-bold text-red-600">{stats.orders.failed}</p>
                  <p className="text-sm text-gray-600 mt-1">Fallidas</p>
                </div>
              </div>
            </div>

            {/* Revenue by Payment Method */}
            {stats.revenue.by_method && Object.keys(stats.revenue.by_method).length > 0 && (
              <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  Ingresos por Método de Pago
                </h3>
                <div className="space-y-3">
                  {Object.entries(stats.revenue.by_method).map(([method, amount]) => (
                    <div key={method} className="flex items-center justify-between">
                      <span className="text-sm font-medium text-gray-700 uppercase">{method}</span>
                      <span className="text-lg font-bold text-emerald-600">{formatPrice(amount)}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Popular Services */}
            {analytics && analytics.popular_services && analytics.popular_services.length > 0 && (
              <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">
                  Servicios Más Populares (Últimos 30 días)
                </h3>
                <div className="space-y-3">
                  {analytics.popular_services.map((item, index) => (
                    <div key={index} className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <span className="text-2xl">{index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : '🏅'}</span>
                        <span className="text-sm font-medium text-gray-700">{item.service}</span>
                      </div>
                      <span className="text-sm font-bold text-emerald-600">{item.orders} órdenes</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Users Tab */}
        {activeTab === 'users' && (
          <div className="space-y-6">
            {/* Search */}
            <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-200">
              <div className="flex gap-3">
                <input
                  type="text"
                  placeholder="Buscar usuarios por email o nombre..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
                />
                <button
                  onClick={handleSearch}
                  className="px-6 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition-colors"
                >
                  🔍 Buscar
                </button>
                <button
                  onClick={loadData}
                  className="px-6 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
                >
                  🔄 Recargar
                </button>
              </div>
            </div>

            {/* Users Table */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Usuario
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Email
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Rol
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Estado
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Registro
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Acciones
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {users.map((u) => (
                      <tr key={u.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="flex items-center">
                            <div className="h-10 w-10 flex-shrink-0 bg-emerald-100 rounded-full flex items-center justify-center">
                              <span className="text-emerald-600 font-semibold">
                                {u.full_name?.charAt(0) || u.email.charAt(0).toUpperCase()}
                              </span>
                            </div>
                            <div className="ml-4">
                              <div className="text-sm font-medium text-gray-900">
                                {u.full_name || 'Sin nombre'}
                              </div>
                              {u.two_factor_enabled && (
                                <span className="text-xs text-green-600">🔐 2FA</span>
                              )}
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <div className="text-sm text-gray-900">{u.email}</div>
                          {u.is_verified && (
                            <span className="text-xs text-green-600">✓ Verificado</span>
                          )}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <select
                            value={u.role}
                            onChange={(e) => handleUpdateUserRole(u.id, e.target.value)}
                            className="text-sm border border-gray-300 rounded px-2 py-1"
                          >
                            <option value="user">Usuario</option>
                            <option value="admin">Admin</option>
                            <option value="guest">Invitado</option>
                          </select>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`px-2 py-1 text-xs rounded-full ${
                            u.is_active
                              ? 'bg-green-100 text-green-800'
                              : 'bg-red-100 text-red-800'
                          }`}>
                            {u.is_active ? 'Activo' : 'Suspendido'}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {formatDate(u.created_at)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm">
                          <button
                            onClick={() => handleToggleUserStatus(u.id, u.is_active)}
                            className={`px-3 py-1 rounded ${
                              u.is_active
                                ? 'bg-red-500 text-white hover:bg-red-600'
                                : 'bg-green-500 text-white hover:bg-green-600'
                            }`}
                          >
                            {u.is_active ? 'Suspender' : 'Activar'}
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              {users.length === 0 && (
                <div className="text-center py-12">
                  <p className="text-gray-500">No se encontraron usuarios</p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Orders Tab */}
        {activeTab === 'orders' && (
          <div className="space-y-6">
            {/* Filters */}
            <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-200">
              <div className="flex gap-3 items-center">
                <label className="text-sm font-medium text-gray-700">Filtrar por estado:</label>
                <select
                  value={filterStatus}
                  onChange={(e) => setFilterStatus(e.target.value)}
                  className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                >
                  <option value="all">Todos</option>
                  <option value="pending">Pendiente</option>
                  <option value="completed">Completado</option>
                  <option value="failed">Fallido</option>
                  <option value="expired">Expirado</option>
                </select>
                <button
                  onClick={loadData}
                  className="ml-auto px-6 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700"
                >
                  🔄 Recargar
                </button>
              </div>
            </div>

            {/* Orders Table */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Usuario</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Servicio</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Monto</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Método</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Fecha</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Acciones</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {orders.map((order) => (
                      <tr key={order.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 text-sm text-gray-900">
                          {order.id.substring(0, 8)}...
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-900">
                          {order.user_id.substring(0, 8)}...
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-900">
                          {order.service_id.substring(0, 8)}...
                        </td>
                        <td className="px-6 py-4 text-sm font-semibold text-gray-900">
                          {formatPrice(order.final_price)}
                        </td>
                        <td className="px-6 py-4 text-sm">
                          <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded uppercase text-xs">
                            {order.payment_method}
                          </span>
                        </td>
                        <td className="px-6 py-4">
                          <select
                            value={order.payment_status}
                            onChange={(e) => handleUpdateOrderStatus(order.id, e.target.value)}
                            className={`text-xs px-2 py-1 rounded ${
                              order.payment_status === 'completed'
                                ? 'bg-green-100 text-green-800'
                                : order.payment_status === 'pending'
                                ? 'bg-yellow-100 text-yellow-800'
                                : order.payment_status === 'failed'
                                ? 'bg-red-100 text-red-800'
                                : 'bg-gray-100 text-gray-800'
                            }`}
                          >
                            <option value="pending">Pendiente</option>
                            <option value="completed">Completado</option>
                            <option value="failed">Fallido</option>
                            <option value="expired">Expirado</option>
                          </select>
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-500">
                          {formatDate(order.created_at)}
                        </td>
                        <td className="px-6 py-4 text-sm">
                          <button
                            onClick={() => alert(`Detalles de orden: ${order.id}`)}
                            className="text-emerald-600 hover:text-emerald-800"
                          >
                            Ver detalles
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              {orders.length === 0 && (
                <div className="text-center py-12">
                  <p className="text-gray-500">No se encontraron órdenes</p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Services Tab */}
        {activeTab === 'services' && (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-bold text-gray-900">Gestión de Servicios</h2>
              <button
                onClick={() => {
                  setEditingService(null);
                  setShowServiceModal(true);
                }}
                className="px-6 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700"
              >
                ➕ Crear Servicio
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {services.map((service) => (
                <div key={service.id} className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
                  <div className="flex justify-between items-start mb-4">
                    <h3 className="text-lg font-bold text-gray-900">{service.title}</h3>
                    <span className={`px-2 py-1 text-xs rounded ${
                      service.status === 'DISPONIBLE'
                        ? 'bg-green-100 text-green-800'
                        : 'bg-yellow-100 text-yellow-800'
                    }`}>
                      {service.status}
                    </span>
                  </div>
                  <p className="text-sm text-gray-600 mb-4 line-clamp-3">{service.description}</p>
                  <div className="space-y-2 mb-4">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">PYG:</span>
                      <span className="font-semibold">{formatPrice(service.price_pyg)}</span>
                    </div>
                    {service.price_btc > 0 && (
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-600">BTC:</span>
                        <span className="font-semibold">{service.price_btc}</span>
                      </div>
                    )}
                  </div>
                  <div className="flex gap-2">
                    <button
                      onClick={() => {
                        setEditingService(service);
                        setShowServiceModal(true);
                      }}
                      className="flex-1 px-3 py-2 bg-blue-500 text-white text-sm rounded hover:bg-blue-600"
                    >
                      ✏️ Editar
                    </button>
                    <button
                      onClick={() => handleDeleteService(service.id)}
                      className="flex-1 px-3 py-2 bg-red-500 text-white text-sm rounded hover:bg-red-600"
                    >
                      🗑️ Eliminar
                    </button>
                  </div>
                </div>
              ))}
            </div>

            {services.length === 0 && (
              <div className="text-center py-12 bg-white rounded-xl">
                <p className="text-gray-500">No hay servicios disponibles</p>
              </div>
            )}
          </div>
        )}

        {/* Transactions Tab */}
        {activeTab === 'transactions' && (
          <div className="space-y-6">
            <h2 className="text-xl font-bold text-gray-900">Transacciones</h2>

            <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">ID</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Orden</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Usuario</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Monto</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Método</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Gateway</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Estado</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Fecha</th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {transactions.map((tx) => (
                      <tr key={tx.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 text-sm text-gray-900">
                          {tx.id.substring(0, 8)}...
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-900">
                          {tx.order_id.substring(0, 8)}...
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-900">
                          {tx.user_id.substring(0, 8)}...
                        </td>
                        <td className="px-6 py-4 text-sm font-semibold">
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
                          <span className={`px-2 py-1 text-xs rounded ${
                            tx.status === 'completed'
                              ? 'bg-green-100 text-green-800'
                              : tx.status === 'pending'
                              ? 'bg-yellow-100 text-yellow-800'
                              : 'bg-red-100 text-red-800'
                          }`}>
                            {tx.status}
                          </span>
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-500">
                          {formatDate(tx.created_at)}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              {transactions.length === 0 && (
                <div className="text-center py-12">
                  <p className="text-gray-500">No se encontraron transacciones</p>
                </div>
              )}
            </div>
          </div>
        )}


        {/* Blog Tab */}
        {activeTab === 'blog' && (
          <div className="bg-white rounded-lg shadow-sm">
            <BlogAdminPanel />
          </div>
        )}

        {/* Telegram Bots Tab */}
        {activeTab === 'bots' && (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-bold text-gray-900">Gestión de Telegram Bots</h2>
              <div className="flex gap-3">
                <button
                  onClick={handleStartAllBots}
                  disabled={botsLoading}
                  className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
                >
                  <span>▶️</span>
                  Iniciar Todos
                </button>
                <button
                  onClick={handleStopAllBots}
                  disabled={botsLoading}
                  className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
                >
                  <span>⏹️</span>
                  Detener Todos
                </button>
                <button
                  onClick={loadBots}
                  disabled={botsLoading}
                  className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
                >
                  <span>🔄</span>
                  Actualizar
                </button>
              </div>
            </div>

            {/* Info Banner */}
            <div className="bg-gradient-to-r from-blue-50 to-purple-50 border border-blue-200 rounded-lg p-5">
              <div className="flex items-start gap-3">
                <span className="text-3xl">🤖</span>
                <div className="flex-1">
                  <h3 className="font-bold text-gray-900 mb-2 text-lg">Gestión de Bots de Telegram</h3>
                  <p className="text-sm text-gray-700 mb-3">
                    Sistema de gestión para los 5 bots activos de GuaraniAppStore. Estos bots operan de forma autónoma en Telegram 
                    y están organizados por categorías.
                  </p>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
                    <div className="bg-white/70 rounded p-2">
                      <span className="font-semibold text-purple-700">🔮 Crypto (3 bots):</span>
                      <p className="text-gray-600 mt-1">Pulse, CryptoShield, Momentum</p>
                    </div>
                    <div className="bg-white/70 rounded p-2">
                      <span className="font-semibold text-blue-700">🤖 General (1 bot):</span>
                      <p className="text-gray-600 mt-1">GuaraniAppStore Assistant</p>
                    </div>
                    <div className="bg-white/70 rounded p-2">
                      <span className="font-semibold text-orange-700">💼 Sales (1 bot):</span>
                      <p className="text-gray-600 mt-1">Rocío Almeida</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {botsLoading && (
              <div className="flex justify-center py-8">
                <div className="animate-spin rounded-full h-12 w-12 border-b-4 border-emerald-500"></div>
              </div>
            )}

            {!botsLoading && (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {bots.map((bot) => (
                  <div
                    key={bot.id}
                    className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
                  >
                    {/* Header with Icon and Name */}
                    <div className="flex items-start gap-3 mb-3">
                      <span className="text-4xl">{bot.icon}</span>
                      <div className="flex-1">
                        <h3 className="font-bold text-gray-900 text-lg">{bot.name}</h3>
                        <a 
                          href={`https://t.me/${bot.username.replace('@', '')}`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-sm text-blue-600 hover:underline"
                        >
                          {bot.username}
                        </a>
                      </div>
                      <span className={`px-2 py-1 text-xs rounded-full font-semibold ${
                        bot.category === 'Crypto' ? 'bg-purple-100 text-purple-800' :
                        bot.category === 'Sales' ? 'bg-orange-100 text-orange-800' :
                        'bg-blue-100 text-blue-800'
                      }`}>
                        {bot.category}
                      </span>
                    </div>

                    {/* Description */}
                    <p className="text-sm text-gray-600 mb-4 leading-relaxed">{bot.description}</p>

                    {/* Status Badge */}
                    <div className="mb-4">
                      {bot.running ? (
                        <div className="flex items-center gap-2 flex-wrap">
                          <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-xs font-semibold flex items-center gap-1">
                            <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                            En Ejecución
                          </span>
                          {bot.pid && (
                            <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">PID: {bot.pid}</span>
                          )}
                        </div>
                      ) : (
                        <span className="px-3 py-1 bg-gray-100 text-gray-600 rounded-full text-xs font-semibold">
                          ⏸️ Detenido
                        </span>
                      )}
                    </div>

                    {/* Action Buttons */}
                    <div className="flex gap-2">
                      {!bot.running ? (
                        <button
                          onClick={() => handleStartBot(bot.id)}
                          disabled={botsLoading}
                          className="flex-1 px-4 py-2 bg-emerald-500 text-white rounded-lg hover:bg-emerald-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-sm font-medium"
                        >
                          ▶️ Iniciar
                        </button>
                      ) : (
                        <button
                          onClick={() => handleStopBot(bot.id)}
                          disabled={botsLoading}
                          className="flex-1 px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-sm font-medium"
                        >
                          ⏹️ Detener
                        </button>
                      )}
                    </div>

                    {/* Bot Info */}
                    <div className="mt-4 pt-4 border-t border-gray-100">
                      <div className="text-xs text-gray-500 space-y-1">
                        <div className="flex justify-between">
                          <span>ID del Bot:</span>
                          <span className="font-mono text-gray-700">{bot.id}</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Estado Sistema:</span>
                          <span className={bot.running ? 'text-green-600 font-semibold' : 'text-gray-600'}>
                            {bot.running ? 'Activo ✓' : 'Inactivo'}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}

            {!botsLoading && bots.length === 0 && (
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
                <span className="text-6xl mb-4 block">🤖</span>
                <h3 className="text-xl font-bold text-gray-900 mb-2">No hay bots configurados</h3>
                <p className="text-gray-500">
                  Los bots de Telegram aparecerán aquí una vez que estén configurados en el backend.
                </p>
              </div>
            )}
          </div>
        )}


        {/* Payment Gateways Tab */}
        {activeTab === 'payments' && (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <div>
                <h2 className="text-xl font-bold text-gray-900 mb-2">Pasarelas de Pago</h2>
                <p className="text-gray-600">Configura las pasarelas de pago disponibles</p>
              </div>
              <button
                onClick={() => {
                  setEditingGateway(null);
                  setShowGatewayModal(true);
                }}
                className="px-6 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 flex items-center gap-2"
              >
                <span>➕</span>
                Nueva Pasarela
              </button>
            </div>

            {/* Gateway Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {/* PayPal */}
              <GatewayCard
                name="PayPal"
                icon="💙"
                gateway={paymentGateways.find(g => g.gateway_name === 'paypal')}
                onEdit={() => {
                  const gw = paymentGateways.find(g => g.gateway_name === 'paypal');
                  setEditingGateway(gw || { gateway_name: 'paypal', config: {} });
                  setShowGatewayModal(true);
                }}
                onToggle={async (enabled) => {
                  const gw = paymentGateways.find(g => g.gateway_name === 'paypal');
                  if (gw) {
                    await saveGateway({ ...gw, is_enabled: enabled });
                  }
                }}
              />

              {/* Bancard */}
              <GatewayCard
                name="Bancard"
                icon="🇵🇾"
                gateway={paymentGateways.find(g => g.gateway_name === 'bancard')}
                onEdit={() => {
                  const gw = paymentGateways.find(g => g.gateway_name === 'bancard');
                  setEditingGateway(gw || { gateway_name: 'bancard', config: {} });
                  setShowGatewayModal(true);
                }}
                onToggle={async (enabled) => {
                  const gw = paymentGateways.find(g => g.gateway_name === 'bancard');
                  if (gw) {
                    await saveGateway({ ...gw, is_enabled: enabled });
                  }
                }}
              />

              {/* 2Checkout */}
              <GatewayCard
                name="2Checkout"
                icon="💳"
                gateway={paymentGateways.find(g => g.gateway_name === '2checkout')}
                onEdit={() => {
                  const gw = paymentGateways.find(g => g.gateway_name === '2checkout');
                  setEditingGateway(gw || { gateway_name: '2checkout', config: {} });
                  setShowGatewayModal(true);
                }}
                onToggle={async (enabled) => {
                  const gw = paymentGateways.find(g => g.gateway_name === '2checkout');
                  if (gw) {
                    await saveGateway({ ...gw, is_enabled: enabled });
                  }
                }}
              />

              {/* Paymentwall */}
              <GatewayCard
                name="Paymentwall"
                icon="🌐"
                gateway={paymentGateways.find(g => g.gateway_name === 'paymentwall')}
                onEdit={() => {
                  const gw = paymentGateways.find(g => g.gateway_name === 'paymentwall');
                  setEditingGateway(gw || { gateway_name: 'paymentwall', config: {} });
                  setShowGatewayModal(true);
                }}
                onToggle={async (enabled) => {
                  const gw = paymentGateways.find(g => g.gateway_name === 'paymentwall');
                  if (gw) {
                    await saveGateway({ ...gw, is_enabled: enabled });
                  }
                }}
              />

              {/* Leemon Squid */}
              <GatewayCard
                name="Leemon Squid"
                icon="🦑"
                gateway={paymentGateways.find(g => g.gateway_name === 'leemon_squid')}
                onEdit={() => {
                  const gw = paymentGateways.find(g => g.gateway_name === 'leemon_squid');
                  setEditingGateway(gw || { gateway_name: 'leemon_squid', config: {} });
                  setShowGatewayModal(true);
                }}
                onToggle={async (enabled) => {
                  const gw = paymentGateways.find(g => g.gateway_name === 'leemon_squid');
                  if (gw) {
                    await saveGateway({ ...gw, is_enabled: enabled });
                  }
                }}
              />

              {/* Pagopar (Existing) */}
              <GatewayCard
                name="Pagopar"
                icon="🇵🇾"
                gateway={paymentGateways.find(g => g.gateway_name === 'pagopar') || { is_enabled: true }}
                onEdit={() => {
                  const gw = paymentGateways.find(g => g.gateway_name === 'pagopar');
                  setEditingGateway(gw || { gateway_name: 'pagopar', config: {} });
                  setShowGatewayModal(true);
                }}
                onToggle={async (enabled) => {
                  const gw = paymentGateways.find(g => g.gateway_name === 'pagopar');
                  if (gw) {
                    await saveGateway({ ...gw, is_enabled: enabled });
                  }
                }}
              />
            </div>
          </div>
        )}



      {/* Gateway Configuration Modal */}
      {showGatewayModal && (
        <GatewayConfigModal
          gateway={editingGateway}
          onClose={() => {
            setShowGatewayModal(false);
            setEditingGateway(null);
          }}
          onSave={saveGateway}
        />
      )}
      </main>
    </div>
  );
};

// Gateway Card Component
const GatewayCard = ({ name, icon, gateway, onEdit, onToggle }) => {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-3">
          <span className="text-4xl">{icon}</span>
          <div>
            <h3 className="font-bold text-gray-900">{name}</h3>
            <span className={`text-xs px-2 py-1 rounded-full ${
              gateway?.is_enabled ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'
            }`}>
              {gateway?.is_enabled ? 'Activo' : 'Inactivo'}
            </span>
          </div>
        </div>
      </div>

      <div className="space-y-2">
        {gateway && (
          <div className="text-xs text-gray-500">
            {Object.keys(gateway.config || {}).length} campos configurados
          </div>
        )}
      </div>

      <div className="flex gap-2 mt-4">
        <button
          onClick={onEdit}
          className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm"
        >
          ⚙️ Configurar
        </button>
        {gateway && (
          <button
            onClick={() => onToggle(!gateway.is_enabled)}
            className={`px-4 py-2 rounded-lg text-sm ${
              gateway.is_enabled
                ? 'bg-red-100 text-red-700 hover:bg-red-200'
                : 'bg-green-100 text-green-700 hover:bg-green-200'
            }`}
          >
            {gateway.is_enabled ? 'Desactivar' : 'Activar'}
          </button>
        )}
      </div>
    </div>
  );
};

// Gateway Config Modal Component
const GatewayConfigModal = ({ gateway, onClose, onSave }) => {
  const [formData, setFormData] = useState(gateway || { gateway_name: '', config: {} });
  const [configFields, setConfigFields] = useState(gateway?.config || {});

  const getFieldsForGateway = (gatewayName) => {
    const fields = {
      paypal: [
        { key: 'client_id', label: 'Client ID', type: 'text', required: true },
        { key: 'secret', label: 'Secret Key', type: 'password', required: true },
        { key: 'mode', label: 'Mode', type: 'select', options: ['sandbox', 'live'], required: true },
        { key: 'webhook_id', label: 'Webhook ID', type: 'text', required: false }
      ],
      bancard: [
        { key: 'public_key', label: 'Public Key', type: 'text', required: true },
        { key: 'private_key', label: 'Private Key', type: 'password', required: true },
        { key: 'commerce_code', label: 'Commerce Code', type: 'text', required: true },
        { key: 'environment', label: 'Environment', type: 'select', options: ['staging', 'production'], required: true }
      ],
      '2checkout': [
        { key: 'merchant_code', label: 'Merchant Code', type: 'text', required: true },
        { key: 'secret_key', label: 'Secret Key', type: 'password', required: true },
        { key: 'publishable_key', label: 'Publishable Key', type: 'text', required: true },
        { key: 'environment', label: 'Environment', type: 'select', options: ['sandbox', 'production'], required: true }
      ],
      paymentwall: [
        { key: 'project_key', label: 'Project Key', type: 'text', required: true },
        { key: 'secret_key', label: 'Secret Key', type: 'password', required: true },
        { key: 'widget_code', label: 'Widget Code', type: 'text', required: true },
        { key: 'api_type', label: 'API Type', type: 'select', options: ['vc', 'pw'], required: true }
      ],
      leemon_squid: [
        { key: 'api_key', label: 'API Key', type: 'password', required: true },
        { key: 'merchant_id', label: 'Merchant ID', type: 'text', required: true },
        { key: 'webhook_secret', label: 'Webhook Secret', type: 'password', required: true },
        { key: 'environment', label: 'Environment', type: 'select', options: ['test', 'production'], required: true }
      ],
      pagopar: [
        { key: 'public_key', label: 'Public Key', type: 'text', required: true },
        { key: 'private_key', label: 'Private Key', type: 'password', required: true },
        { key: 'environment', label: 'Environment', type: 'select', options: ['sandbox', 'production'], required: true }
      ]
    };

    return fields[gatewayName] || [];
  };

  const fields = getFieldsForGateway(formData.gateway_name);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave({
      gateway_name: formData.gateway_name,
      config: configFields,
      is_enabled: formData.is_enabled || false
    });
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6">
        <div className="flex justify-between items-center mb-6">
          <h3 className="text-xl font-bold text-gray-900">
            Configurar {formData.gateway_name ? formData.gateway_name.replace('_', ' ').toUpperCase() : 'Pasarela'}
          </h3>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700 text-2xl">
            ×
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          {fields.map((field) => (
            <div key={field.key}>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                {field.label} {field.required && <span className="text-red-500">*</span>}
              </label>
              {field.type === 'select' ? (
                <select
                  value={configFields[field.key] || ''}
                  onChange={(e) => setConfigFields({ ...configFields, [field.key]: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                  required={field.required}
                >
                  <option value="">Seleccionar...</option>
                  {field.options.map((opt) => (
                    <option key={opt} value={opt}>{opt}</option>
                  ))}
                </select>
              ) : (
                <input
                  type={field.type}
                  value={configFields[field.key] || ''}
                  onChange={(e) => setConfigFields({ ...configFields, [field.key]: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                  required={field.required}
                  placeholder={`Ingresa ${field.label.toLowerCase()}`}
                />
              )}
            </div>
          ))}

          <div className="flex items-center gap-2 pt-4">
            <input
              type="checkbox"
              id="enable-gateway"
              checked={formData.is_enabled || false}
              onChange={(e) => setFormData({ ...formData, is_enabled: e.target.checked })}
              className="w-4 h-4 text-emerald-600 rounded focus:ring-emerald-500"
            />
            <label htmlFor="enable-gateway" className="text-sm text-gray-700">
              Activar esta pasarela de pago
            </label>
          </div>

          <div className="flex gap-3 pt-4">
            <button
              type="submit"
              className="flex-1 px-6 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700"
            >
              💾 Guardar Configuración
            </button>
            <button
              type="button"
              onClick={onClose}
              className="px-6 py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
            >
              Cancelar
            </button>
          </div>
        </form>

        <div className="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
          <div className="flex items-start gap-2">
            <span className="text-yellow-600">⚠️</span>
            <div className="text-sm text-yellow-800">
              <p className="font-semibold mb-1">Importante:</p>
              <p>
                Las credenciales se almacenan de forma segura en la base de datos. 
                Asegúrate de usar las credenciales correctas según el ambiente (sandbox/production).
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// Service Modal Component
const ServiceModal = ({ service, onClose, onSave }) => {
  const [formData, setFormData] = useState(service || {
    title: '',
    description: '',
    features: [],
    price_pyg: 0,
    price_btc: 0,
    price_eth: 0,
    price_usdt: 0,
    discount_crypto: 0,
    status: 'DISPONIBLE',
    category: 'General',
    delivery_time: '',
    order: 0
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(formData);
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto p-6">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-gray-900">
            {service ? 'Editar Servicio' : 'Crear Servicio'}
          </h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 text-2xl"
          >
            ×
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Título</label>
            <input
              type="text"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Descripción</label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({ ...formData, description: e.target.value })}
              rows="3"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
              required
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Precio PYG</label>
              <input
                type="number"
                value={formData.price_pyg}
                onChange={(e) => setFormData({ ...formData, price_pyg: parseFloat(e.target.value) })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Precio BTC</label>
              <input
                type="number"
                step="0.00000001"
                value={formData.price_btc}
                onChange={(e) => setFormData({ ...formData, price_btc: parseFloat(e.target.value) })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Precio ETH</label>
              <input
                type="number"
                step="0.00000001"
                value={formData.price_eth}
                onChange={(e) => setFormData({ ...formData, price_eth: parseFloat(e.target.value) })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Precio USDT</label>
              <input
                type="number"
                step="0.01"
                value={formData.price_usdt}
                onChange={(e) => setFormData({ ...formData, price_usdt: parseFloat(e.target.value) })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Descuento Crypto (%)</label>
              <input
                type="number"
                value={formData.discount_crypto}
                onChange={(e) => setFormData({ ...formData, discount_crypto: parseInt(e.target.value) })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Estado</label>
              <select
                value={formData.status}
                onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
              >
                <option value="DISPONIBLE">Disponible</option>
                <option value="PRÓXIMAMENTE">Próximamente</option>
              </select>
            </div>
          </div>

          <div className="flex gap-3 mt-6">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50"
            >
              Cancelar
            </button>
            <button
              type="submit"
              className="flex-1 px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700"
            >
              Guardar
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default AdminPanel;
