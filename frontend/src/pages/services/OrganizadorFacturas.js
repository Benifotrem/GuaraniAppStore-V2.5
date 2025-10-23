import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const OrganizadorFacturas = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('upload');
  const [invoices, setInvoices] = useState([]);
  const [processing, setProcessing] = useState(false);
  const [stats, setStats] = useState({
    total: 0,
    pending: 0,
    validated: 0,
    totalAmount: 0
  });
  const [filters, setFilters] = useState({
    dateFrom: '',
    dateTo: '',
    status: 'all',
    minAmount: '',
    maxAmount: ''
  });

  useEffect(() => {
    checkAuth();
  }, []);

  useEffect(() => {
    if (invoices.length > 0) {
      calculateStats();
    }
  }, [invoices]);

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

  const calculateStats = () => {
    setStats({
      total: invoices.length,
      pending: invoices.filter(i => i.status === 'pending').length,
      validated: invoices.filter(i => i.status === 'validated').length,
      totalAmount: invoices.reduce((sum, i) => sum + i.amount, 0)
    });
  };

  const handleFileUpload = async (e) => {
    const files = Array.from(e.target.files);
    if (files.length === 0) return;

    setProcessing(true);

    // Simulate OCR processing
    setTimeout(() => {
      const newInvoices = files.map((file, index) => ({
        id: Date.now() + index,
        fileName: file.name,
        date: new Date().toISOString().split('T')[0],
        issuer: `Proveedor ${Math.floor(Math.random() * 100)}`,
        ruc: `${Math.floor(Math.random() * 9000000) + 1000000}-${Math.floor(Math.random() * 9)}`,
        amount: Math.floor(Math.random() * 5000000) + 100000,
        taxAmount: Math.floor(Math.random() * 500000) + 10000,
        description: 'Productos y servicios varios',
        status: 'pending',
        extractedData: {
          confidence: Math.floor(Math.random() * 20) + 80,
          ocr: true
        },
        uploadedAt: new Date().toISOString()
      }));

      setInvoices([...invoices, ...newInvoices]);
      setProcessing(false);
      setActiveTab('invoices');
      alert(`✅ ${files.length} factura(s) procesadas correctamente!`);
    }, 2000);
  };

  const validateInvoice = (invoiceId) => {
    setInvoices(invoices.map(inv => 
      inv.id === invoiceId ? { ...inv, status: 'validated' } : inv
    ));
  };

  const rejectInvoice = (invoiceId) => {
    setInvoices(invoices.map(inv => 
      inv.id === invoiceId ? { ...inv, status: 'rejected' } : inv
    ));
  };

  const exportToExcel = () => {
    alert('📊 Exportando facturas a Excel...\n\n⏳ Funcionalidad en desarrollo.');
  };

  const exportToContable = () => {
    alert('💼 Exportando a sistema contable...\n\n⏳ Funcionalidad en desarrollo.');
  };

  const filteredInvoices = invoices.filter(inv => {
    if (filters.status !== 'all' && inv.status !== filters.status) return false;
    if (filters.dateFrom && inv.date < filters.dateFrom) return false;
    if (filters.dateTo && inv.date > filters.dateTo) return false;
    if (filters.minAmount && inv.amount < parseFloat(filters.minAmount)) return false;
    if (filters.maxAmount && inv.amount > parseFloat(filters.maxAmount)) return false;
    return true;
  });

  const formatCurrency = (amount) => {
    return 'Gs. ' + new Intl.NumberFormat('es-PY').format(amount);
  };

  const getStatusBadge = (status) => {
    const badges = {
      pending: { label: 'Pendiente', color: 'bg-yellow-100 text-yellow-800' },
      validated: { label: 'Validado', color: 'bg-green-100 text-green-800' },
      rejected: { label: 'Rechazado', color: 'bg-red-100 text-red-800' }
    };
    return badges[status] || badges.pending;
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
          <p className="text-gray-600">Cargando organizador de facturas...</p>
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
            <div className="flex items-center gap-4">
              <button
                onClick={() => navigate('/dashboard')}
                className="text-gray-600 hover:text-gray-900"
              >
                ← Volver
              </button>
              <div>
                <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
                  <span>🧾</span>
                  Organizador de Facturas para Contadores
                </h1>
                <p className="text-sm text-gray-500 mt-1">Digitalización y organización automática con OCR</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-600">
                👤 {user?.full_name || user?.email}
              </span>
              <button
                onClick={handleLogout}
                className="px-4 py-2 text-sm bg-red-500 text-white rounded-lg hover:bg-red-600"
              >
                Cerrar Sesión
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Stats Bar */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">{stats.total}</div>
              <div className="text-xs text-gray-600">Total Facturas</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-yellow-600">{stats.pending}</div>
              <div className="text-xs text-gray-600">Pendientes</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">{stats.validated}</div>
              <div className="text-xs text-gray-600">Validadas</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-emerald-600">{formatCurrency(stats.totalAmount)}</div>
              <div className="text-xs text-gray-600">Monto Total</div>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8">
            <button
              onClick={() => setActiveTab('upload')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === 'upload'
                  ? 'border-emerald-500 text-emerald-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              📤 Subir Facturas
            </button>
            <button
              onClick={() => setActiveTab('invoices')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === 'invoices'
                  ? 'border-emerald-500 text-emerald-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              🧾 Facturas ({invoices.length})
            </button>
            <button
              onClick={() => setActiveTab('reports')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === 'reports'
                  ? 'border-emerald-500 text-emerald-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              📊 Reportes
            </button>
            <button
              onClick={() => setActiveTab('integration')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === 'integration'
                  ? 'border-emerald-500 text-emerald-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              🔗 Integraciones
            </button>
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Upload Tab */}
        {activeTab === 'upload' && (
          <div className="space-y-6">
            <div>
              <h2 className="text-xl font-bold text-gray-900 mb-2">Subir Facturas</h2>
              <p className="text-gray-600">Digitaliza facturas físicas con OCR avanzado (Tesseract + Google Cloud Vision)</p>
            </div>

            {/* Upload Area */}
            <div className="bg-white rounded-xl shadow-sm border-2 border-dashed border-gray-300 p-12 text-center hover:border-emerald-500 transition-colors">
              <input
                type="file"
                id="invoice-upload"
                multiple
                accept=".pdf,.png,.jpg,.jpeg"
                onChange={handleFileUpload}
                className="hidden"
                disabled={processing}
              />
              <label htmlFor="invoice-upload" className="cursor-pointer">
                <div className="text-6xl mb-4">🧾</div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {processing ? 'Procesando facturas con OCR...' : 'Arrastra facturas aquí o haz click'}
                </h3>
                <p className="text-sm text-gray-600 mb-4">
                  PDF, imágenes (PNG, JPG) - OCR automático con IA
                </p>
                {processing && (
                  <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-500"></div>
                )}
              </label>
            </div>

            {/* Features Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="text-3xl mb-3">🔍</div>
                <h3 className="font-bold text-gray-900 mb-2">OCR Avanzado</h3>
                <p className="text-sm text-gray-600">
                  Tesseract + Google Cloud Vision para máxima precisión
                </p>
              </div>

              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="text-3xl mb-3">🤖</div>
                <h3 className="font-bold text-gray-900 mb-2">Extracción con IA</h3>
                <p className="text-sm text-gray-600">
                  RUC, monto, IVA, fecha y descripción automáticos
                </p>
              </div>

              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="text-3xl mb-3">📁</div>
                <h3 className="font-bold text-gray-900 mb-2">Almacenamiento</h3>
                <p className="text-sm text-gray-600">
                  Organización automática por fecha y proveedor
                </p>
              </div>

              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="text-3xl mb-3">✅</div>
                <h3 className="font-bold text-gray-900 mb-2">Validación SET</h3>
                <p className="text-sm text-gray-600">
                  Verifica validez de RUC y facturas con SET Paraguay
                </p>
              </div>

              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="text-3xl mb-3">📊</div>
                <h3 className="font-bold text-gray-900 mb-2">Reportes</h3>
                <p className="text-sm text-gray-600">
                  Genera reportes mensuales y anuales automáticamente
                </p>
              </div>

              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="text-3xl mb-3">💼</div>
                <h3 className="font-bold text-gray-900 mb-2">Integración</h3>
                <p className="text-sm text-gray-600">
                  Exporta a Excel, sistemas contables y Google Drive
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Invoices Tab */}
        {activeTab === 'invoices' && (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <div>
                <h2 className="text-xl font-bold text-gray-900 mb-2">Facturas Procesadas</h2>
                <p className="text-gray-600">Revisa y valida las facturas digitalizadas</p>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={exportToExcel}
                  className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 text-sm flex items-center gap-2"
                >
                  <span>📊</span>
                  Excel
                </button>
                <button
                  onClick={exportToContable}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm flex items-center gap-2"
                >
                  <span>💼</span>
                  Exportar
                </button>
              </div>
            </div>

            {/* Filters */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
              <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Desde</label>
                  <input
                    type="date"
                    value={filters.dateFrom}
                    onChange={(e) => setFilters({ ...filters, dateFrom: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Hasta</label>
                  <input
                    type="date"
                    value={filters.dateTo}
                    onChange={(e) => setFilters({ ...filters, dateTo: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Estado</label>
                  <select
                    value={filters.status}
                    onChange={(e) => setFilters({ ...filters, status: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 text-sm"
                  >
                    <option value="all">Todos</option>
                    <option value="pending">Pendiente</option>
                    <option value="validated">Validado</option>
                    <option value="rejected">Rechazado</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Monto Mín</label>
                  <input
                    type="number"
                    value={filters.minAmount}
                    onChange={(e) => setFilters({ ...filters, minAmount: e.target.value })}
                    placeholder="Gs."
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 text-sm"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Monto Máx</label>
                  <input
                    type="number"
                    value={filters.maxAmount}
                    onChange={(e) => setFilters({ ...filters, maxAmount: e.target.value })}
                    placeholder="Gs."
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 text-sm"
                  />
                </div>
              </div>
            </div>

            {/* Invoices List */}
            {filteredInvoices.length === 0 ? (
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
                <div className="text-6xl mb-4">🧾</div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">No hay facturas</h3>
                <p className="text-gray-600 mb-6">Sube facturas para comenzar la digitalización</p>
                <button
                  onClick={() => setActiveTab('upload')}
                  className="px-6 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700"
                >
                  Subir Facturas
                </button>
              </div>
            ) : (
              <div className="space-y-4">
                {filteredInvoices.map((invoice) => (
                  <div
                    key={invoice.id}
                    className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
                  >
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <h3 className="text-lg font-bold text-gray-900">{invoice.issuer}</h3>
                          <span className={`px-3 py-1 text-xs rounded-full ${getStatusBadge(invoice.status).color}`}>
                            {getStatusBadge(invoice.status).label}
                          </span>
                          {invoice.extractedData.ocr && (
                            <span className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded flex items-center gap-1">
                              <span>🔍</span>
                              OCR {invoice.extractedData.confidence}%
                            </span>
                          )}
                        </div>
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                          <div>
                            <span className="text-gray-500">RUC:</span>
                            <div className="font-mono text-gray-900">{invoice.ruc}</div>
                          </div>
                          <div>
                            <span className="text-gray-500">Fecha:</span>
                            <div className="text-gray-900">{invoice.date}</div>
                          </div>
                          <div>
                            <span className="text-gray-500">Monto:</span>
                            <div className="font-semibold text-emerald-600">{formatCurrency(invoice.amount)}</div>
                          </div>
                          <div>
                            <span className="text-gray-500">IVA:</span>
                            <div className="text-gray-900">{formatCurrency(invoice.taxAmount)}</div>
                          </div>
                        </div>
                        <div className="mt-3">
                          <span className="text-sm text-gray-500">Descripción: </span>
                          <span className="text-sm text-gray-700">{invoice.description}</span>
                        </div>
                      </div>
                    </div>

                    {invoice.status === 'pending' && (
                      <div className="flex gap-2 pt-4 border-t border-gray-100">
                        <button
                          onClick={() => validateInvoice(invoice.id)}
                          className="flex-1 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 text-sm"
                        >
                          ✅ Validar
                        </button>
                        <button
                          onClick={() => rejectInvoice(invoice.id)}
                          className="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 text-sm"
                        >
                          ❌ Rechazar
                        </button>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Reports Tab */}
        {activeTab === 'reports' && (
          <div className="space-y-6">
            <div>
              <h2 className="text-xl font-bold text-gray-900 mb-2">Reportes y Análisis</h2>
              <p className="text-gray-600">Genera reportes contables automáticamente</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <h3 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
                  <span>📊</span>
                  Reporte Mensual
                </h3>
                <p className="text-sm text-gray-600 mb-4">
                  Resumen de facturas y totales del mes actual
                </p>
                <button className="w-full px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700">
                  Generar Reporte
                </button>
              </div>

              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <h3 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
                  <span>📈</span>
                  Reporte Anual
                </h3>
                <p className="text-sm text-gray-600 mb-4">
                  Resumen completo del año fiscal
                </p>
                <button className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                  Generar Reporte
                </button>
              </div>

              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <h3 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
                  <span>💰</span>
                  Reporte de IVA
                </h3>
                <p className="text-sm text-gray-600 mb-4">
                  Cálculo de IVA crédito y débito fiscal
                </p>
                <button className="w-full px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700">
                  Generar Reporte
                </button>
              </div>

              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <h3 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
                  <span>🏢</span>
                  Por Proveedor
                </h3>
                <p className="text-sm text-gray-600 mb-4">
                  Análisis de gastos por proveedor
                </p>
                <button className="w-full px-4 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700">
                  Generar Reporte
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Integration Tab */}
        {activeTab === 'integration' && (
          <div className="space-y-6">
            <div>
              <h2 className="text-xl font-bold text-gray-900 mb-2">Integraciones</h2>
              <p className="text-gray-600">Conecta con tus herramientas contables</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="flex items-start gap-4">
                  <div className="text-4xl">📊</div>
                  <div className="flex-1">
                    <h3 className="font-bold text-gray-900 mb-1">Excel / Google Sheets</h3>
                    <p className="text-sm text-gray-600 mb-3">
                      Exporta facturas a hojas de cálculo
                    </p>
                    <button className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 text-sm">
                      Conectar
                    </button>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="flex items-start gap-4">
                  <div className="text-4xl">💼</div>
                  <div className="flex-1">
                    <h3 className="font-bold text-gray-900 mb-1">Sistema Contable</h3>
                    <p className="text-sm text-gray-600 mb-3">
                      Integración con ERP/software contable
                    </p>
                    <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm">
                      Configurar
                    </button>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="flex items-start gap-4">
                  <div className="text-4xl">📂</div>
                  <div className="flex-1">
                    <h3 className="font-bold text-gray-900 mb-1">Google Drive</h3>
                    <p className="text-sm text-gray-600 mb-3">
                      Almacena facturas automáticamente
                    </p>
                    <button className="px-4 py-2 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 text-sm">
                      Conectar Drive
                    </button>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="flex items-start gap-4">
                  <div className="text-4xl">🏛️</div>
                  <div className="flex-1">
                    <h3 className="font-bold text-gray-900 mb-1">SET Paraguay</h3>
                    <p className="text-sm text-gray-600 mb-3">
                      Validación automática de RUC y facturas
                    </p>
                    <button className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 text-sm">
                      Conectar SET
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default OrganizadorFacturas;
