import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const AutomatizacionEcommerce = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [products, setProducts] = useState([]);
  const [orders, setOrders] = useState([]);

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
          <p className="text-gray-600">Cargando automatización e-commerce...</p>
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
                  <span>🛒</span>Automatización E-commerce
                </h1>
                <p className="text-sm text-gray-500 mt-1">Gestión inteligente de tienda online</p>
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
            <button onClick={() => setActiveTab('dashboard')} className={`py-4 px-1 border-b-2 font-medium text-sm ${activeTab === 'dashboard' ? 'border-emerald-500 text-emerald-600' : 'border-transparent text-gray-500'}`}>📊 Dashboard</button>
            <button onClick={() => setActiveTab('products')} className={`py-4 px-1 border-b-2 font-medium text-sm ${activeTab === 'products' ? 'border-emerald-500 text-emerald-600' : 'border-transparent text-gray-500'}`}>📦 Productos</button>
            <button onClick={() => setActiveTab('orders')} className={`py-4 px-1 border-b-2 font-medium text-sm ${activeTab === 'orders' ? 'border-emerald-500 text-emerald-600' : 'border-transparent text-gray-500'}`}>🛍️ Pedidos</button>
            <button onClick={() => setActiveTab('automation')} className={`py-4 px-1 border-b-2 font-medium text-sm ${activeTab === 'automation' ? 'border-emerald-500 text-emerald-600' : 'border-transparent text-gray-500'}`}>🤖 Automatizaciones</button>
          </nav>
        </div>
      </div>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'dashboard' && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <div className="text-3xl mb-3">📦</div>
              <h3 className="font-bold text-gray-900 mb-2">Gestión de Inventario</h3>
              <p className="text-sm text-gray-600">Control automático de stock y alertas</p>
            </div>
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <div className="text-3xl mb-3">💰</div>
              <h3 className="font-bold text-gray-900 mb-2">Precios Dinámicos</h3>
              <p className="text-sm text-gray-600">Ajustes inteligentes según demanda</p>
            </div>
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <div className="text-3xl mb-3">📧</div>
              <h3 className="font-bold text-gray-900 mb-2">Email Marketing</h3>
              <p className="text-sm text-gray-600">Campañas automáticas personalizadas</p>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default AutomatizacionEcommerce;