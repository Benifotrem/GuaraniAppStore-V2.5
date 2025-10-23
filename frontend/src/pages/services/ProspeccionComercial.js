import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const ProspeccionComercial = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('search');
  const [leads, setLeads] = useState([]);
  const [searching, setSearching] = useState(false);
  const [searchParams, setSearchParams] = useState({
    industry: '',
    location: '',
    size: ''
  });

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

  const handleSearch = async (e) => {
    e.preventDefault();
    setSearching(true);
    
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(`${API}/user/llm/find-leads`, {
        industry: searchParams.industry,
        location: searchParams.location,
        size: searchParams.size
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });

      if (response.data.success) {
        // Demo leads with AI strategy
        const demoLeads = [
          {
            id: 1,
            company: 'Tech Solutions SRL',
            contact: 'Juan Pérez',
            email: 'juan@techsolutions.com',
            phone: '+595 XXX XXX',
            score: 85,
            status: 'new',
            aiStrategy: response.data.response
          }
        ];
        setLeads(demoLeads);
        setActiveTab('leads');
        alert('✅ Estrategia de prospección generada!');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('❌ Error al buscar leads.');
    } finally {
      setSearching(false);
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
          <p className="text-gray-600">Cargando prospección comercial...</p>
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
                  <span>🎯</span>Prospección Comercial
                </h1>
                <p className="text-sm text-gray-500 mt-1">Búsqueda inteligente de clientes potenciales</p>
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
            <button onClick={() => setActiveTab('search')} className={`py-4 px-1 border-b-2 font-medium text-sm ${activeTab === 'search' ? 'border-emerald-500 text-emerald-600' : 'border-transparent text-gray-500'}`}>🔍 Buscar Leads</button>
            <button onClick={() => setActiveTab('leads')} className={`py-4 px-1 border-b-2 font-medium text-sm ${activeTab === 'leads' ? 'border-emerald-500 text-emerald-600' : 'border-transparent text-gray-500'}`}>📋 Leads ({leads.length})</button>
            <button onClick={() => setActiveTab('campaigns')} className={`py-4 px-1 border-b-2 font-medium text-sm ${activeTab === 'campaigns' ? 'border-emerald-500 text-emerald-600' : 'border-transparent text-gray-500'}`}>📧 Campañas</button>
            <button onClick={() => setActiveTab('sources')} className={`py-4 px-1 border-b-2 font-medium text-sm ${activeTab === 'sources' ? 'border-emerald-500 text-emerald-600' : 'border-transparent text-gray-500'}`}>🌐 Fuentes</button>
          </nav>
        </div>
      </div>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'search' && (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2">
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <h2 className="text-xl font-bold text-gray-900 mb-6">Buscar Clientes Potenciales</h2>
                <form onSubmit={handleSearch} className="space-y-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Industria</label>
                    <input type="text" value={searchParams.industry} onChange={(e) => setSearchParams({...searchParams, industry: e.target.value})} className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500" placeholder="Ej: Tecnología, Retail" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Ubicación</label>
                    <input type="text" value={searchParams.location} onChange={(e) => setSearchParams({...searchParams, location: e.target.value})} className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500" placeholder="Ciudad, País" />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Tamaño de Empresa</label>
                    <select value={searchParams.size} onChange={(e) => setSearchParams({...searchParams, size: e.target.value})} className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500">
                      <option value="">Todos</option>
                      <option value="small">1-50 empleados</option>
                      <option value="medium">51-200 empleados</option>
                      <option value="large">200+ empleados</option>
                    </select>
                  </div>
                  <button type="submit" disabled={searching} className="w-full px-6 py-4 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 disabled:opacity-50 font-medium flex items-center justify-center gap-2">
                    {searching ? (
                      <><div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div> Buscando...</>
                    ) : (
                      <>🔍 Buscar Leads</>
                    )}
                  </button>
                </form>
              </div>
            </div>
            <div className="space-y-6">
              <div className="bg-gradient-to-br from-blue-50 to-purple-100 rounded-xl p-6">
                <h3 className="font-bold text-gray-900 mb-2">🤖 IA + Scraping</h3>
                <p className="text-sm text-gray-700">Outscraper + Apify para búsqueda masiva de leads</p>
              </div>
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <h3 className="font-bold text-gray-900 mb-4">🌐 Fuentes</h3>
                <div className="space-y-2 text-sm">
                  <div>✅ Google Maps</div>
                  <div>✅ LinkedIn</div>
                  <div>✅ Redes Sociales</div>
                  <div>✅ Directorios</div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'leads' && (
          <div className="space-y-4">
            {leads.length === 0 ? (
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
                <div className="text-6xl mb-4">🎯</div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">No hay leads</h3>
                <button onClick={() => setActiveTab('search')} className="px-6 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700">Buscar Leads</button>
              </div>
            ) : (
              leads.map((lead) => (
                <div key={lead.id} className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                  <div className="flex items-start justify-between">
                    <div>
                      <h3 className="text-lg font-bold text-gray-900">{lead.company}</h3>
                      <div className="flex items-center gap-4 text-sm text-gray-600 mt-2">
                        <span>👤 {lead.contact}</span>
                        <span>📧 {lead.email}</span>
                        <span>📱 {lead.phone}</span>
                      </div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-emerald-600">{lead.score}</div>
                      <div className="text-xs text-gray-500">Score</div>
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        )}

        {activeTab === 'sources' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 className="font-bold text-gray-900 mb-4 flex items-center gap-2"><span>🗺️</span>Google Maps</h3>
              <p className="text-sm text-gray-600 mb-4">Extrae negocios locales por categoría y ubicación</p>
              <button className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm">Configurar</button>
            </div>
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 className="font-bold text-gray-900 mb-4 flex items-center gap-2"><span>💼</span>LinkedIn</h3>
              <p className="text-sm text-gray-600 mb-4">Búsqueda de empresas y contactos profesionales</p>
              <button className="w-full px-4 py-2 bg-blue-700 text-white rounded-lg hover:bg-blue-800 text-sm">Configurar</button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default ProspeccionComercial;