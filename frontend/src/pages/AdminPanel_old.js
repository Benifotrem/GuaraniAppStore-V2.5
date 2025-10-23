import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
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
  const [searchType, setSearchType] = useState('users');
  const [searchResults, setSearchResults] = useState([]);
  const [editingService, setEditingService] = useState(null);
  const [showServiceModal, setShowServiceModal] = useState(false);

  useEffect(() => {
    checkAdminAuth();
  }, []);

  useEffect(() => {
    if (user && user.role === 'admin') {
      loadData();
    }
  }, [activeTab, filterStatus]);

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
        const statsResponse = await axios.get(`${API}/admin/stats`, { headers });
        setStats(statsResponse.data);
      } else if (activeTab === 'users') {
        const usersResponse = await axios.get(`${API}/admin/users`, { headers });
        setUsers(usersResponse.data);
      } else if (activeTab === 'orders') {
        const ordersResponse = await axios.get(`${API}/admin/orders${filterStatus !== 'all' ? `?payment_status=${filterStatus}` : ''}`, { headers });
        setOrders(ordersResponse.data);
      } else if (activeTab === 'services') {
        const servicesResponse = await axios.get(`${API}/admin/services/manage`, { headers });
        setServices(servicesResponse.data);
      }
    } catch (e) {
      console.error('Error loading data:', e);
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
      alert('Rol actualizado exitosamente');
      loadData();
    } catch (e) {
      alert('Error al actualizar rol');
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
      alert('Estado actualizado exitosamente');
      loadData();
    } catch (e) {
      alert('Error al actualizar estado');
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
      alert('Estado de orden actualizado');
      loadData();
    } catch (e) {
      alert('Error al actualizar orden');
    }
  };

  const formatPrice = (price) => {
    return 'Gs. ' + new Intl.NumberFormat('es-PY', {
      minimumFractionDigits: 0
    }).format(price);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString('es-PY');
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-emerald-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Cargando panel de administración...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="admin-panel-container">
      {/* Sidebar */}
      <aside className="admin-sidebar">
        <div className="sidebar-header">
          <h2 className="text-2xl font-bold text-emerald-700">🛡️ Admin Panel</h2>
          <p className="text-sm text-gray-600">GuaraniAppStore</p>
        </div>

        <nav className="sidebar-nav">
          <button
            onClick={() => setActiveTab('dashboard')}
            className={`nav-item ${activeTab === 'dashboard' ? 'active' : ''}`}
          >
            <span className="text-xl">📊</span>
            <span>Dashboard</span>
          </button>

          <button
            onClick={() => setActiveTab('users')}
            className={`nav-item ${activeTab === 'users' ? 'active' : ''}`}
          >
            <span className="text-xl">👥</span>
            <span>Usuarios</span>
          </button>

          <button
            onClick={() => setActiveTab('orders')}
            className={`nav-item ${activeTab === 'orders' ? 'active' : ''}`}
          >
            <span className="text-xl">🛒</span>
            <span>Órdenes</span>
          </button>

          <button
            onClick={() => setActiveTab('services')}
            className={`nav-item ${activeTab === 'services' ? 'active' : ''}`}
          >
            <span className="text-xl">⚡</span>
            <span>Servicios</span>
          </button>
        </nav>

        <div className="sidebar-footer">
          <button
            onClick={() => navigate('/dashboard')}
            className="w-full px-4 py-2 text-emerald-600 hover:bg-emerald-50 rounded-lg font-semibold mb-2"
          >
            ← Panel Usuario
          </button>
          <button
            onClick={() => navigate('/')}
            className="w-full px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg font-semibold"
          >
            Volver al Inicio
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="admin-main">
        <div className="admin-header">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              {activeTab === 'dashboard' && 'Dashboard General'}
              {activeTab === 'users' && 'Gestión de Usuarios'}
              {activeTab === 'orders' && 'Gestión de Órdenes'}
              {activeTab === 'services' && 'Gestión de Servicios'}
            </h1>
            <p className="text-gray-600 mt-1">Panel de Administración</p>
          </div>

          <div className="flex items-center gap-3">
            <div className="px-4 py-2 bg-red-100 text-red-800 rounded-lg font-semibold text-sm">
              🛡️ ADMIN
            </div>
          </div>
        </div>

        <div className="admin-content">
          {/* Dashboard Tab */}
          {activeTab === 'dashboard' && stats && (
            <div className="space-y-6">
              {/* Stats Grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <div className="stat-card bg-gradient-to-br from-blue-50 to-blue-100">
                  <div className="text-4xl mb-2">👥</div>
                  <div className="stat-value text-blue-700">{stats.users.total}</div>
                  <div className="stat-label">Total Usuarios</div>
                  <div className="text-xs text-blue-600 mt-2">
                    {stats.users.verified} verificados • {stats.users.with_2fa} con 2FA
                  </div>
                </div>

                <div className="stat-card bg-gradient-to-br from-green-50 to-green-100">
                  <div className="text-4xl mb-2">🛒</div>
                  <div className="stat-value text-green-700">{stats.orders.total}</div>
                  <div className="stat-label">Total Órdenes</div>
                  <div className="text-xs text-green-600 mt-2">
                    {stats.orders.completed} completadas • {stats.orders.pending} pendientes
                  </div>
                </div>

                <div className="stat-card bg-gradient-to-br from-emerald-50 to-emerald-100">
                  <div className="text-4xl mb-2">💰</div>
                  <div className="stat-value text-emerald-700">{formatPrice(stats.revenue.total)}</div>
                  <div className="stat-label">Ingresos Totales</div>
                  <div className="text-xs text-emerald-600 mt-2">
                    {stats.orders.completed} pagos completados
                  </div>
                </div>

                <div className="stat-card bg-gradient-to-br from-purple-50 to-purple-100">
                  <div className="text-4xl mb-2">⚡</div>
                  <div className="stat-value text-purple-700">{stats.services.total}</div>
                  <div className="stat-label">Servicios</div>
                  <div className="text-xs text-purple-600 mt-2">
                    Activos y próximamente
                  </div>
                </div>
              </div>

              {/* Revenue by Payment Method */}
              <div className="card">
                <h3 className="text-xl font-bold text-gray-900 mb-4">Ingresos por Método de Pago</h3>
                <div className="space-y-3">
                  {Object.entries(stats.revenue.by_method).map(([method, amount]) => (
                    <div key={method} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                      <div className="flex items-center gap-3">
                        <span className="text-2xl">
                          {method === 'pagopar' && '💳'}
                          {method === 'btc' && '₿'}
                          {method === 'eth' && '⟠'}
                          {method === 'usdt' && '₮'}
                        </span>
                        <span className="font-semibold text-gray-900 uppercase">{method}</span>
                      </div>
                      <div className="text-right">
                        <p className="font-bold text-emerald-700">{formatPrice(amount)}</p>
                        <p className="text-xs text-gray-500">
                          {((amount / stats.revenue.total) * 100).toFixed(1)}%
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* Users Tab */}
          {activeTab === 'users' && (
            <div className="card overflow-x-auto">
              <table className="admin-table">
                <thead>
                  <tr>
                    <th>Usuario</th>
                    <th>Email</th>
                    <th>País</th>
                    <th>Rol</th>
                    <th>Estado</th>
                    <th>Verificado</th>
                    <th>Fecha Registro</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {users.map(u => (
                    <tr key={u.id}>
                      <td>
                        <div className="font-semibold">{u.full_name}</div>
                        {u.company && <div className="text-xs text-gray-500">{u.company}</div>}
                      </td>
                      <td>{u.email}</td>
                      <td>{u.country}</td>
                      <td>
                        <select
                          value={u.role}
                          onChange={(e) => handleUpdateUserRole(u.id, e.target.value)}
                          className="px-3 py-1 border rounded text-sm"
                        >
                          <option value="user">User</option>
                          <option value="admin">Admin</option>
                          <option value="guest">Guest</option>
                        </select>
                      </td>
                      <td>
                        <span className={`px-2 py-1 rounded text-xs font-semibold ${u.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                          {u.is_active ? 'Activo' : 'Inactivo'}
                        </span>
                      </td>
                      <td>
                        <span className={`px-2 py-1 rounded text-xs font-semibold ${u.is_verified ? 'bg-blue-100 text-blue-800' : 'bg-yellow-100 text-yellow-800'}`}>
                          {u.is_verified ? '✓' : '⏳'}
                        </span>
                      </td>
                      <td className="text-sm">{new Date(u.created_at).toLocaleDateString('es-PY')}</td>
                      <td>
                        <button
                          onClick={() => handleToggleUserStatus(u.id, u.is_active)}
                          className="px-3 py-1 bg-gray-200 hover:bg-gray-300 rounded text-xs font-semibold"
                        >
                          {u.is_active ? 'Desactivar' : 'Activar'}
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {/* Orders Tab */}
          {activeTab === 'orders' && (
            <div className="space-y-4">
              {/* Filter */}
              <div className="card">
                <div className="flex items-center gap-4">
                  <span className="font-semibold text-gray-700">Filtrar por estado:</span>
                  <select
                    value={filterStatus}
                    onChange={(e) => setFilterStatus(e.target.value)}
                    className="px-4 py-2 border border-gray-300 rounded-lg"
                  >
                    <option value="all">Todos</option>
                    <option value="pending">Pendientes</option>
                    <option value="completed">Completados</option>
                    <option value="failed">Fallidos</option>
                    <option value="expired">Expirados</option>
                  </select>
                  <span className="text-sm text-gray-600">{orders.length} órdenes</span>
                </div>
              </div>

              {/* Orders List */}
              <div className="card overflow-x-auto">
                <table className="admin-table">
                  <thead>
                    <tr>
                      <th>Orden #</th>
                      <th>Usuario</th>
                      <th>Servicio</th>
                      <th>Plan</th>
                      <th>Método</th>
                      <th>Total</th>
                      <th>Estado</th>
                      <th>Fecha</th>
                      <th>Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    {orders.map(order => (
                      <tr key={order.id}>
                        <td className="font-mono text-sm">{order.order_number}</td>
                        <td className="text-sm">{order.user_id.substring(0, 8)}...</td>
                        <td className="text-sm">{order.service_id.substring(0, 8)}...</td>
                        <td className="text-sm capitalize">{order.plan_type}</td>
                        <td className="text-sm uppercase">{order.payment_method}</td>
                        <td className="font-semibold">{formatPrice(order.final_price)}</td>
                        <td>
                          <select
                            value={order.payment_status}
                            onChange={(e) => handleUpdateOrderStatus(order.id, e.target.value)}
                            className={`px-2 py-1 rounded text-xs font-semibold border-2 ${
                              order.payment_status === 'completed' ? 'border-green-300 bg-green-50 text-green-800' :
                              order.payment_status === 'pending' ? 'border-yellow-300 bg-yellow-50 text-yellow-800' :
                              order.payment_status === 'failed' ? 'border-red-300 bg-red-50 text-red-800' :
                              'border-gray-300 bg-gray-50 text-gray-800'
                            }`}
                          >
                            <option value="pending">Pendiente</option>
                            <option value="completed">Completado</option>
                            <option value="failed">Fallido</option>
                            <option value="expired">Expirado</option>
                          </select>
                        </td>
                        <td className="text-xs">{new Date(order.created_at).toLocaleDateString('es-PY')}</td>
                        <td>
                          <button className="px-3 py-1 bg-blue-100 hover:bg-blue-200 text-blue-800 rounded text-xs font-semibold">
                            Ver Detalles
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* Services Tab */}
          {activeTab === 'services' && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {services.map(service => (
                <div key={service.id} className="card">
                  <div className="flex items-start justify-between mb-4">
                    <h3 className="text-lg font-bold text-gray-900">{service.name}</h3>
                    <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                      service.status === 'active' ? 'bg-green-100 text-green-800' :
                      service.status === 'coming_soon' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-gray-100 text-gray-800'
                    }`}>
                      {service.status === 'active' ? 'Activo' : service.status === 'coming_soon' ? 'Próximamente' : 'Inactivo'}
                    </span>
                  </div>

                  <p className="text-sm text-gray-600 mb-4 line-clamp-2">{service.description}</p>

                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Mensual:</span>
                      <span className="font-semibold">{formatPrice(service.price_monthly)}</span>
                    </div>
                    {service.price_annual > 0 && (
                      <div className="flex justify-between">
                        <span className="text-gray-600">Anual:</span>
                        <span className="font-semibold">{formatPrice(service.price_annual)}</span>
                      </div>
                    )}
                    <div className="flex justify-between">
                      <span className="text-gray-600">Categoría:</span>
                      <span className="font-semibold capitalize">{service.category}</span>
                    </div>
                  </div>

                  <button className="w-full mt-4 px-4 py-2 bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg font-semibold text-sm">
                    Editar Servicio
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default AdminPanel;
