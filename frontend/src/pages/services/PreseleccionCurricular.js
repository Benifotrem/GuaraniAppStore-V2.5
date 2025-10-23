import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const PreseleccionCurricular = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('upload');
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [analyzing, setAnalyzing] = useState(false);
  const [candidates, setCandidates] = useState([]);
  const [filters, setFilters] = useState({
    minScore: 0,
    position: '',
    experience: ''
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
      
      // TODO: Load user's candidates from backend
      // const candidatesRes = await axios.get(`${API}/user/candidates`, {
      //   headers: { Authorization: `Bearer ${token}` }
      // });
      // setCandidates(candidatesRes.data);
      
      setLoading(false);
    } catch (e) {
      console.error('Auth error:', e);
      navigate('/');
    }
  };

  const handleFileUpload = async (e) => {
    const files = Array.from(e.target.files);
    
    if (files.length === 0) return;

    setAnalyzing(true);
    
    // TODO: Upload to backend and analyze with AI
    // const token = localStorage.getItem('token');
    // const formData = new FormData();
    // files.forEach(file => formData.append('cvs', file));
    
    // const response = await axios.post(`${API}/user/analyze-cvs`, formData, {
    //   headers: { 
    //     Authorization: `Bearer ${token}`,
    //     'Content-Type': 'multipart/form-data'
    //   }
    // });
    
    // Simulate analysis
    setTimeout(() => {
      const newCandidates = files.map((file, index) => ({
        id: Date.now() + index,
        name: file.name.replace(/\.(pdf|docx?|png|jpe?g)$/i, ''),
        email: `candidato${index + 1}@ejemplo.com`,
        phone: '+595 XXX XXX XXX',
        score: Math.floor(Math.random() * 40) + 60, // 60-100
        position: 'Desarrollador',
        experience: `${Math.floor(Math.random() * 10) + 1} años`,
        skills: ['JavaScript', 'React', 'Node.js', 'Python'],
        education: 'Ingeniería en Sistemas',
        status: 'pending',
        uploadedAt: new Date().toISOString()
      }));
      
      setCandidates([...candidates, ...newCandidates]);
      setUploadedFiles([...uploadedFiles, ...files]);
      setAnalyzing(false);
      setActiveTab('candidates');
      alert(`✅ ${files.length} CV(s) analizados correctamente!`);
    }, 2000);
  };

  const updateCandidateStatus = (candidateId, newStatus) => {
    setCandidates(candidates.map(c => 
      c.id === candidateId ? { ...c, status: newStatus } : c
    ));
    // TODO: Update in backend
    // const token = localStorage.getItem('token');
    // await axios.put(`${API}/user/candidates/${candidateId}`, { status: newStatus }, {
    //   headers: { Authorization: `Bearer ${token}` }
    // });
  };

  const exportToGoogle = () => {
    alert('📊 Exportando candidatos a Google Sheets...\n\n⏳ Esta funcionalidad se integrará próximamente.');
    // TODO: Integrate with Google Sheets API
  };

  const filteredCandidates = candidates.filter(c => {
    if (filters.minScore && c.score < filters.minScore) return false;
    if (filters.position && !c.position.toLowerCase().includes(filters.position.toLowerCase())) return false;
    if (filters.experience && !c.experience.includes(filters.experience)) return false;
    return true;
  });

  const getScoreColor = (score) => {
    if (score >= 90) return 'text-green-600 bg-green-100';
    if (score >= 75) return 'text-blue-600 bg-blue-100';
    if (score >= 60) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const getStatusBadge = (status) => {
    const badges = {
      pending: { label: 'Pendiente', color: 'bg-gray-100 text-gray-800' },
      reviewing: { label: 'Revisando', color: 'bg-blue-100 text-blue-800' },
      shortlisted: { label: 'Preseleccionado', color: 'bg-green-100 text-green-800' },
      rejected: { label: 'Descartado', color: 'bg-red-100 text-red-800' },
      interviewed: { label: 'Entrevistado', color: 'bg-purple-100 text-purple-800' }
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
          <p className="text-gray-600">Cargando sistema de preselección...</p>
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
                  <span>👥</span>
                  Agente de Preselección Curricular
                </h1>
                <p className="text-sm text-gray-500 mt-1">Análisis automático de CVs con IA</p>
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
              <div className="text-2xl font-bold text-emerald-600">{candidates.length}</div>
              <div className="text-xs text-gray-600">Total CVs</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">
                {candidates.filter(c => c.status === 'shortlisted').length}
              </div>
              <div className="text-xs text-gray-600">Preseleccionados</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">
                {candidates.filter(c => c.status === 'reviewing').length}
              </div>
              <div className="text-xs text-gray-600">En Revisión</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-600">
                {candidates.filter(c => c.score >= 80).length}
              </div>
              <div className="text-xs text-gray-600">Score &gt; 80</div>
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
              📤 Subir CVs
            </button>
            <button
              onClick={() => setActiveTab('candidates')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === 'candidates'
                  ? 'border-emerald-500 text-emerald-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              👥 Candidatos ({candidates.length})
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
              <h2 className="text-xl font-bold text-gray-900 mb-2">Subir Currículums</h2>
              <p className="text-gray-600">Sube uno o varios CVs para análisis automático con IA</p>
            </div>

            {/* Upload Area */}
            <div className="bg-white rounded-xl shadow-sm border-2 border-dashed border-gray-300 p-12 text-center hover:border-emerald-500 transition-colors">
              <input
                type="file"
                id="cv-upload"
                multiple
                accept=".pdf,.doc,.docx,.png,.jpg,.jpeg"
                onChange={handleFileUpload}
                className="hidden"
                disabled={analyzing}
              />
              <label
                htmlFor="cv-upload"
                className="cursor-pointer"
              >
                <div className="text-6xl mb-4">📄</div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {analyzing ? 'Analizando CVs...' : 'Arrastra archivos aquí o haz click para seleccionar'}
                </h3>
                <p className="text-sm text-gray-600 mb-4">
                  Formatos soportados: PDF, Word (.doc, .docx), Imágenes (.png, .jpg)
                </p>
                {analyzing && (
                  <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-500"></div>
                )}
              </label>
            </div>

            {/* Features Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="text-3xl mb-3">🤖</div>
                <h3 className="font-bold text-gray-900 mb-2">Análisis con IA</h3>
                <p className="text-sm text-gray-600">
                  Claude 3.5 Sonnet analiza experiencia, habilidades y educación automáticamente
                </p>
              </div>

              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="text-3xl mb-3">📊</div>
                <h3 className="font-bold text-gray-900 mb-2">Scoring Inteligente</h3>
                <p className="text-sm text-gray-600">
                  Sistema de puntuación de 0-100 basado en criterios configurables
                </p>
              </div>

              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="text-3xl mb-3">✅</div>
                <h3 className="font-bold text-gray-900 mb-2">Validación Automática</h3>
                <p className="text-sm text-gray-600">
                  Valida emails y perfiles de LinkedIn automáticamente
                </p>
              </div>

              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="text-3xl mb-3">📧</div>
                <h3 className="font-bold text-gray-900 mb-2">Recepción por Email</h3>
                <p className="text-sm text-gray-600">
                  Configura un email dedicado para recibir CVs automáticamente
                </p>
              </div>

              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="text-3xl mb-3">📈</div>
                <h3 className="font-bold text-gray-900 mb-2">Google Sheets</h3>
                <p className="text-sm text-gray-600">
                  Exporta candidatos directamente a Google Sheets
                </p>
              </div>

              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="text-3xl mb-3">🗂️</div>
                <h3 className="font-bold text-gray-900 mb-2">OCR Avanzado</h3>
                <p className="text-sm text-gray-600">
                  Procesa CVs en imágenes con Tesseract y Google Cloud Vision
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Candidates Tab */}
        {activeTab === 'candidates' && (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <div>
                <h2 className="text-xl font-bold text-gray-900 mb-2">Candidatos Analizados</h2>
                <p className="text-gray-600">Gestiona y filtra los candidatos preseleccionados</p>
              </div>
              <button
                onClick={exportToGoogle}
                className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 flex items-center gap-2"
              >
                <span>📊</span>
                Exportar a Sheets
              </button>
            </div>

            {/* Filters */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Score Mínimo
                  </label>
                  <input
                    type="number"
                    min="0"
                    max="100"
                    value={filters.minScore}
                    onChange={(e) => setFilters({ ...filters, minScore: parseInt(e.target.value) || 0 })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Posición
                  </label>
                  <input
                    type="text"
                    value={filters.position}
                    onChange={(e) => setFilters({ ...filters, position: e.target.value })}
                    placeholder="Ej: Desarrollador"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Experiencia
                  </label>
                  <input
                    type="text"
                    value={filters.experience}
                    onChange={(e) => setFilters({ ...filters, experience: e.target.value })}
                    placeholder="Ej: 5 años"
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                  />
                </div>
              </div>
            </div>

            {/* Candidates List */}
            {filteredCandidates.length === 0 ? (
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
                <div className="text-6xl mb-4">📋</div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">No hay candidatos</h3>
                <p className="text-gray-600 mb-6">Sube CVs para comenzar el análisis automático</p>
                <button
                  onClick={() => setActiveTab('upload')}
                  className="px-6 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700"
                >
                  Subir CVs
                </button>
              </div>
            ) : (
              <div className="space-y-4">
                {filteredCandidates.map((candidate) => (
                  <div
                    key={candidate.id}
                    className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
                  >
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex-1">
                        <h3 className="text-lg font-bold text-gray-900 mb-1">{candidate.name}</h3>
                        <div className="flex flex-wrap gap-2 text-sm text-gray-600 mb-2">
                          <span className="flex items-center gap-1">
                            <span>📧</span>
                            {candidate.email}
                          </span>
                          <span className="flex items-center gap-1">
                            <span>📱</span>
                            {candidate.phone}
                          </span>
                        </div>
                        <div className="flex flex-wrap gap-2 mb-3">
                          <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">
                            {candidate.position}
                          </span>
                          <span className="px-2 py-1 bg-purple-100 text-purple-800 text-xs rounded">
                            {candidate.experience}
                          </span>
                          <span className="px-2 py-1 bg-gray-100 text-gray-800 text-xs rounded">
                            {candidate.education}
                          </span>
                        </div>
                        <div className="flex flex-wrap gap-1">
                          {candidate.skills.map((skill, idx) => (
                            <span key={idx} className="px-2 py-1 bg-emerald-50 text-emerald-700 text-xs rounded">
                              {skill}
                            </span>
                          ))}
                        </div>
                      </div>
                      <div className="text-right ml-4">
                        <div className={`text-3xl font-bold ${getScoreColor(candidate.score)} rounded-lg px-4 py-2`}>
                          {candidate.score}
                        </div>
                        <div className="text-xs text-gray-500 mt-1">Score IA</div>
                      </div>
                    </div>

                    <div className="flex items-center justify-between pt-4 border-t border-gray-100">
                      <div className="flex items-center gap-2">
                        <span className="text-sm text-gray-600">Estado:</span>
                        <span className={`px-3 py-1 text-xs rounded-full ${getStatusBadge(candidate.status).color}`}>
                          {getStatusBadge(candidate.status).label}
                        </span>
                      </div>
                      <div className="flex gap-2">
                        <button
                          onClick={() => updateCandidateStatus(candidate.id, 'reviewing')}
                          className="px-3 py-1 text-sm bg-blue-100 text-blue-700 rounded hover:bg-blue-200"
                        >
                          👁️ Revisar
                        </button>
                        <button
                          onClick={() => updateCandidateStatus(candidate.id, 'shortlisted')}
                          className="px-3 py-1 text-sm bg-green-100 text-green-700 rounded hover:bg-green-200"
                        >
                          ✅ Preseleccionar
                        </button>
                        <button
                          onClick={() => updateCandidateStatus(candidate.id, 'rejected')}
                          className="px-3 py-1 text-sm bg-red-100 text-red-700 rounded hover:bg-red-200"
                        >
                          ❌ Descartar
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Integration Tab */}
        {activeTab === 'integration' && (
          <div className="space-y-6">
            <div>
              <h2 className="text-xl font-bold text-gray-900 mb-2">Integraciones</h2>
              <p className="text-gray-600">Conecta con tus herramientas favoritas de RRHH</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Google Sheets */}
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="flex items-start gap-4 mb-4">
                  <div className="text-4xl">📊</div>
                  <div className="flex-1">
                    <h3 className="font-bold text-gray-900 mb-1">Google Sheets</h3>
                    <p className="text-sm text-gray-600 mb-3">
                      Exporta candidatos automáticamente a una hoja de cálculo
                    </p>
                    <button className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 text-sm">
                      Conectar Google Sheets
                    </button>
                  </div>
                </div>
              </div>

              {/* LinkedIn */}
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="flex items-start gap-4 mb-4">
                  <div className="text-4xl">💼</div>
                  <div className="flex-1">
                    <h3 className="font-bold text-gray-900 mb-1">LinkedIn</h3>
                    <p className="text-sm text-gray-600 mb-3">
                      Valida perfiles y enriquece datos automáticamente
                    </p>
                    <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm">
                      Conectar LinkedIn
                    </button>
                  </div>
                </div>
              </div>

              {/* Email */}
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="flex items-start gap-4 mb-4">
                  <div className="text-4xl">📧</div>
                  <div className="flex-1">
                    <h3 className="font-bold text-gray-900 mb-1">Email Dedicado</h3>
                    <p className="text-sm text-gray-600 mb-3">
                      Recibe CVs por email y analízalos automáticamente
                    </p>
                    <div className="bg-gray-50 p-3 rounded mb-3">
                      <code className="text-sm text-gray-700">rrhh-{user?.email?.split('@')[0]}@cvs.guaraniappstore.com</code>
                    </div>
                    <button className="px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 text-sm">
                      Activar Email
                    </button>
                  </div>
                </div>
              </div>

              {/* Google Drive */}
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <div className="flex items-start gap-4 mb-4">
                  <div className="text-4xl">📂</div>
                  <div className="flex-1">
                    <h3 className="font-bold text-gray-900 mb-1">Google Drive</h3>
                    <p className="text-sm text-gray-600 mb-3">
                      Sincroniza CVs desde una carpeta de Google Drive
                    </p>
                    <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm">
                      Conectar Drive
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

export default PreseleccionCurricular;
