import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Dashboard.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Dashboard = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [orders, setOrders] = useState([]);
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview'); // 'overview', 'orders', 'services', 'profile'

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
      // Get user info
      const userResponse = await axios.get(`${API}/auth/me`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setUser(userResponse.data);

      // Get orders
      const ordersResponse = await axios.get(`${API}/orders/my-orders`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setOrders(ordersResponse.data);

      // Get services
      const servicesResponse = await axios.get(`${API}/services`);
      setServices(servicesResponse.data);

      setLoading(false);
    } catch (e) {
      console.error('Auth error:', e);
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      navigate('/');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/');
  };

  const formatPrice = (price) => {
    return 'Gs. ' + new Intl.NumberFormat('es-PY', {
      minimumFractionDigits: 0
    }).format(price);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('es-PY', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const getOrderStatusBadge = (status) => {
    const badges = {
      pending: { color: 'yellow', text: 'Pendiente' },
      completed: { color: 'green', text: 'Completado' },
      failed: { color: 'red', text: 'Fallido' },
      expired: { color: 'gray', text: 'Expirado' }
    };
    const badge = badges[status] || badges.pending;
    
    return (
      <span className={`px-3 py-1 rounded-full text-xs font-semibold bg-${badge.color}-100 text-${badge.color}-800`}>
        {badge.text}
      </span>
    );
  };

  const getServiceById = (serviceId) => {
    return services.find(s => s.id === serviceId);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-emerald-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Cargando...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      {/* Sidebar */}
      <aside className="dashboard-sidebar">
        <div className="sidebar-header">
          <h2 className="text-2xl font-bold text-emerald-700">GuaraniAppStore</h2>
          <p className="text-sm text-gray-600">Panel de Usuario</p>
        </div>

        <nav className="sidebar-nav">
          <button
            onClick={() => setActiveTab('overview')}
            className={`nav-item ${activeTab === 'overview' ? 'active' : ''}`}
            data-testid="nav-overview"
          >
            <span className="text-xl">📊</span>
            <span>Resumen</span>
          </button>

          <button
            onClick={() => setActiveTab('orders')}
            className={`nav-item ${activeTab === 'orders' ? 'active' : ''}`}
            data-testid="nav-orders"
          >
            <span className="text-xl">🛒</span>
            <span>Mis Órdenes</span>
          </button>

          <button
            onClick={() => setActiveTab('services')}
            className={`nav-item ${activeTab === 'services' ? 'active' : ''}`}
            data-testid="nav-services"
          >
            <span className="text-xl">⚡</span>
            <span>Servicios Activos</span>
          </button>

          <button
            onClick={() => setActiveTab('profile')}
            className={`nav-item ${activeTab === 'profile' ? 'active' : ''}`}
            data-testid="nav-profile"
          >
            <span className="text-xl">👤</span>
            <span>Mi Perfil</span>
          </button>
        </nav>

        <div className="sidebar-footer">
          <button
            onClick={() => navigate('/')}
            className="w-full px-4 py-2 text-emerald-600 hover:bg-emerald-50 rounded-lg font-semibold mb-2"
          >
            ← Volver al Inicio
          </button>
          <button
            onClick={handleLogout}
            className="w-full px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-lg font-semibold"
          >
            Cerrar Sesión
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="dashboard-main">
        {/* Header */}
        <div className="dashboard-header">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              {activeTab === 'overview' && 'Resumen General'}
              {activeTab === 'orders' && 'Mis Órdenes'}
              {activeTab === 'services' && 'Servicios Activos'}
              {activeTab === 'profile' && 'Mi Perfil'}
            </h1>
            <p className="text-gray-600 mt-1">Bienvenido, {user.full_name}</p>
          </div>

          <div className="flex items-center gap-4">
            <div className="text-right">
              <p className="text-sm text-gray-600">País</p>
              <p className="font-semibold text-gray-900">{user.country}</p>
            </div>
            <div className="w-12 h-12 bg-emerald-500 rounded-full flex items-center justify-center">
              {user.profile_picture ? (
                <img src={user.profile_picture} alt={user.full_name} className="w-full h-full rounded-full object-cover" />
              ) : (
                <span className="text-white text-xl font-bold">{user.full_name[0]}</span>
              )}
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="dashboard-content">
          {/* Overview Tab */}
          {activeTab === 'overview' && (
            <div className="space-y-6">
              {/* Stats Cards */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="stat-card">
                  <div className="stat-icon bg-emerald-100">
                    <span className="text-3xl">🛒</span>
                  </div>
                  <div>
                    <p className="stat-label">Total Órdenes</p>
                    <p className="stat-value">{orders.length}</p>
                  </div>
                </div>

                <div className="stat-card">
                  <div className="stat-icon bg-green-100">
                    <span className="text-3xl">✅</span>
                  </div>
                  <div>
                    <p className="stat-label">Pagos Completados</p>
                    <p className="stat-value">{orders.filter(o => o.payment_status === 'completed').length}</p>
                  </div>
                </div>

                <div className="stat-card">
                  <div className="stat-icon bg-yellow-100">
                    <span className="text-3xl">⏳</span>
                  </div>
                  <div>
                    <p className="stat-label">Pagos Pendientes</p>
                    <p className="stat-value">{orders.filter(o => o.payment_status === 'pending').length}</p>
                  </div>
                </div>
              </div>

              {/* Recent Orders */}
              <div className="card">
                <h3 className="text-xl font-bold text-gray-900 mb-4">Órdenes Recientes</h3>
                {orders.length === 0 ? (
                  <div className="text-center py-8">
                    <p className="text-gray-500 mb-4">No tienes órdenes todavía</p>
                    <button
                      onClick={() => navigate('/')}
                      className="px-6 py-2 bg-emerald-500 text-white rounded-lg hover:bg-emerald-600 font-semibold"
                    >
                      Explorar Servicios
                    </button>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {orders.slice(0, 5).map(order => {
                      const service = getServiceById(order.service_id);
                      return (
                        <div key={order.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition">
                          <div className="flex-1">
                            <p className="font-semibold text-gray-900">{service?.name || 'Servicio'}</p>
                            <p className="text-sm text-gray-600">Orden #{order.order_number}</p>
                            <p className="text-xs text-gray-500">{formatDate(order.created_at)}</p>
                          </div>
                          <div className="text-right mr-4">
                            <p className="font-bold text-emerald-700">{formatPrice(order.final_price)}</p>
                            <p className="text-xs text-gray-500 uppercase">{order.payment_method}</p>
                          </div>
                          {getOrderStatusBadge(order.payment_status)}
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Orders Tab */}
          {activeTab === 'orders' && (
            <div className="space-y-4">
              {orders.length === 0 ? (
                <div className="card text-center py-12">
                  <div className="text-6xl mb-4">🛒</div>
                  <h3 className="text-xl font-bold text-gray-900 mb-2">No tienes órdenes</h3>
                  <p className="text-gray-600 mb-6">Comienza a usar nuestros servicios de automatización</p>
                  <button
                    onClick={() => navigate('/')}
                    className="px-6 py-3 bg-emerald-500 text-white rounded-lg hover:bg-emerald-600 font-semibold"
                  >
                    Ver Servicios Disponibles
                  </button>
                </div>
              ) : (
                orders.map(order => {
                  const service = getServiceById(order.service_id);
                  return (
                    <div key={order.id} className="card">
                      <div className="flex items-start justify-between mb-4">
                        <div>
                          <h4 className="text-xl font-bold text-gray-900">{service?.name || 'Servicio'}</h4>
                          <p className="text-sm text-gray-600">Orden #{order.order_number}</p>
                        </div>
                        {getOrderStatusBadge(order.payment_status)}
                      </div>

                      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4 p-4 bg-gray-50 rounded-lg">
                        <div>
                          <p className="text-xs text-gray-600 mb-1">Plan</p>
                          <p className="font-semibold text-gray-900 capitalize">{order.plan_type === 'one_time' ? 'Pago Único' : order.plan_type === 'monthly' ? 'Mensual' : 'Anual'}</p>
                        </div>
                        {order.platform && (
                          <div>
                            <p className="text-xs text-gray-600 mb-1">Plataforma</p>
                            <p className="font-semibold text-gray-900 capitalize">{order.platform}</p>
                          </div>
                        )}
                        <div>
                          <p className="text-xs text-gray-600 mb-1">Método de Pago</p>
                          <p className="font-semibold text-gray-900 uppercase">{order.payment_method}</p>
                        </div>
                        <div>
                          <p className="text-xs text-gray-600 mb-1">Total</p>
                          <p className="font-bold text-emerald-700">{formatPrice(order.final_price)}</p>
                          {order.discount_percentage > 0 && (
                            <p className="text-xs text-green-600">-{order.discount_percentage}% descuento</p>
                          )}
                        </div>
                      </div>

                      <div className="flex items-center justify-between">
                        <p className="text-sm text-gray-600">
                          Creado: {formatDate(order.created_at)}
                          {order.completed_at && ` • Completado: ${formatDate(order.completed_at)}`}
                        </p>
                        {order.payment_status === 'pending' && order.payment_url && (
                          <a
                            href={order.payment_url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="px-4 py-2 bg-emerald-500 text-white rounded-lg hover:bg-emerald-600 font-semibold text-sm"
                          >
                            Completar Pago
                          </a>
                        )}
                        {order.payment_status === 'pending' && order.crypto_address && (
                          <button
                            onClick={() => navigate(`/checkout/${order.service_id}`)}
                            className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 font-semibold text-sm"
                          >
                            Ver Instrucciones Crypto
                          </button>
                        )}
                      </div>
                    </div>
                  );
                })
              )}
            </div>
          )}

          {/* Services Tab */}
          {activeTab === 'services' && (
            <div className="card text-center py-12">
              <div className="text-6xl mb-4">⚡</div>
              <h3 className="text-xl font-bold text-gray-900 mb-2">Servicios Activos</h3>
              <p className="text-gray-600 mb-6">
                Una vez que completes un pago, tus servicios activos aparecerán aquí con las credenciales de acceso.
              </p>
              <p className="text-sm text-gray-500">
                {orders.filter(o => o.payment_status === 'completed').length} pago(s) completado(s) • Activación en proceso
              </p>
            </div>
          )}

          {/* Profile Tab */}
          {activeTab === 'profile' && (
            <div className="space-y-6">
              <div className="card">
                <h3 className="text-xl font-bold text-gray-900 mb-6">Información Personal</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Nombre Completo</label>
                    <p className="p-3 bg-gray-50 rounded-lg text-gray-900">{user.full_name}</p>
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Email</label>
                    <p className="p-3 bg-gray-50 rounded-lg text-gray-900">{user.email}</p>
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">País</label>
                    <p className="p-3 bg-gray-50 rounded-lg text-gray-900">{user.country}</p>
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Zona Horaria</label>
                    <p className="p-3 bg-gray-50 rounded-lg text-gray-900">{user.timezone}</p>
                  </div>

                  {user.phone && (
                    <div>
                      <label className="block text-sm font-semibold text-gray-700 mb-2">Teléfono</label>
                      <p className="p-3 bg-gray-50 rounded-lg text-gray-900">{user.phone}</p>
                    </div>
                  )}

                  {user.company && (
                    <div>
                      <label className="block text-sm font-semibold text-gray-700 mb-2">Empresa</label>
                      <p className="p-3 bg-gray-50 rounded-lg text-gray-900">{user.company}</p>
                    </div>
                  )}

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Cuenta Creada</label>
                    <p className="p-3 bg-gray-50 rounded-lg text-gray-900">{formatDate(user.created_at)}</p>
                  </div>

                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">Estado</label>
                    <p className="p-3 bg-gray-50 rounded-lg">
                      <span className={`px-3 py-1 rounded-full text-xs font-semibold ${user.is_verified ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
                        {user.is_verified ? '✓ Verificado' : '⏳ Pendiente verificación'}
                      </span>
                    </p>
                  </div>
                </div>
              </div>

              <div className="card">
                <h3 className="text-xl font-bold text-gray-900 mb-4">Seguridad</h3>
                <div className="space-y-3">
                  <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div>
                      <p className="font-semibold text-gray-900">Autenticación de Dos Factores (2FA)</p>
                      <p className="text-sm text-gray-600">
                        {user.two_factor_enabled ? 'Activado ✓' : 'Desactivado - Recomendamos activarlo'}
                      </p>
                    </div>
                    <button className="px-4 py-2 bg-emerald-500 text-white rounded-lg hover:bg-emerald-600 font-semibold text-sm">
                      {user.two_factor_enabled ? 'Desactivar' : 'Activar'}
                    </button>
                  </div>

                  <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                    <div>
                      <p className="font-semibold text-gray-900">Cambiar Contraseña</p>
                      <p className="text-sm text-gray-600">Actualiza tu contraseña periódicamente</p>
                    </div>
                    <button className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 font-semibold text-sm">
                      Cambiar
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
