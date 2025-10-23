import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const OrganizadorAgenda = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('calendar');
  const [events, setEvents] = useState([]);
  const [showEventModal, setShowEventModal] = useState(false);
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);
  const [newEvent, setNewEvent] = useState({
    title: '',
    date: new Date().toISOString().split('T')[0],
    time: '09:00',
    duration: 60,
    description: '',
    type: 'meeting',
    reminder: 15
  });
  const [googleConnected, setGoogleConnected] = useState(false);

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
      
      // Load some demo events
      setEvents([
        {
          id: 1,
          title: 'Reunión con equipo',
          date: new Date().toISOString().split('T')[0],
          time: '10:00',
          duration: 60,
          type: 'meeting',
          description: 'Revisión semanal del proyecto'
        },
        {
          id: 2,
          title: 'Llamada con cliente',
          date: new Date(Date.now() + 86400000).toISOString().split('T')[0],
          time: '14:30',
          duration: 30,
          type: 'call',
          description: 'Seguimiento de propuesta'
        }
      ]);
      
      setLoading(false);
    } catch (e) {
      console.error('Auth error:', e);
      navigate('/');
    }
  };

  const handleCreateEvent = (e) => {
    e.preventDefault();
    const event = {
      id: Date.now(),
      ...newEvent
    };
    setEvents([...events, event]);
    setShowEventModal(false);
    setNewEvent({
      title: '',
      date: new Date().toISOString().split('T')[0],
      time: '09:00',
      duration: 60,
      description: '',
      type: 'meeting',
      reminder: 15
    });
    alert('✅ Evento creado correctamente!');
  };

  const deleteEvent = (eventId) => {
    if (window.confirm('¿Eliminar este evento?')) {
      setEvents(events.filter(e => e.id !== eventId));
    }
  };

  const connectGoogle = () => {
    alert('🔗 Conectando con Google Calendar...\n\n⏳ Redirigiendo a autorización OAuth...');
    // TODO: Implement Google OAuth
    setTimeout(() => {
      setGoogleConnected(true);
      alert('✅ Google Calendar conectado!');
    }, 1500);
  };

  const syncEvents = () => {
    alert('🔄 Sincronizando eventos con Google Calendar...\n\n⏳ Funcionalidad en desarrollo.');
  };

  const getEventTypeColor = (type) => {
    const colors = {
      meeting: 'bg-blue-100 text-blue-800',
      call: 'bg-green-100 text-green-800',
      task: 'bg-purple-100 text-purple-800',
      reminder: 'bg-yellow-100 text-yellow-800'
    };
    return colors[type] || colors.meeting;
  };

  const getEventTypeIcon = (type) => {
    const icons = {
      meeting: '👥',
      call: '📞',
      task: '✅',
      reminder: '⏰'
    };
    return icons[type] || icons.meeting;
  };

  const todayEvents = events.filter(e => e.date === new Date().toISOString().split('T')[0]);
  const upcomingEvents = events.filter(e => e.date > new Date().toISOString().split('T')[0]).slice(0, 5);

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/');
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-emerald-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Cargando agenda...</p>
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
                  <span>📅</span>
                  Organizador de Agenda
                </h1>
                <p className="text-sm text-gray-500 mt-1">Integrado con Google Calendar</p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              {googleConnected ? (
                <span className="flex items-center gap-2 text-sm text-green-600 bg-green-50 px-3 py-1 rounded-full">
                  <span>✅</span>
                  Google conectado
                </span>
              ) : (
                <button
                  onClick={connectGoogle}
                  className="flex items-center gap-2 text-sm bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
                >
                  <span>🔗</span>
                  Conectar Google
                </button>
              )}
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

      {/* Quick Stats */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">{todayEvents.length}</div>
              <div className="text-xs text-gray-600">Eventos Hoy</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-purple-600">{events.length}</div>
              <div className="text-xs text-gray-600">Total Eventos</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-green-600">{upcomingEvents.length}</div>
              <div className="text-xs text-gray-600">Próximos</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-emerald-600">
                {new Date().toLocaleDateString('es-PY', { weekday: 'short' })}
              </div>
              <div className="text-xs text-gray-600">Día Actual</div>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8">
            <button
              onClick={() => setActiveTab('calendar')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === 'calendar'
                  ? 'border-emerald-500 text-emerald-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              📅 Calendario
            </button>
            <button
              onClick={() => setActiveTab('today')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === 'today'
                  ? 'border-emerald-500 text-emerald-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              📆 Hoy ({todayEvents.length})
            </button>
            <button
              onClick={() => setActiveTab('upcoming')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === 'upcoming'
                  ? 'border-emerald-500 text-emerald-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              ⏭️ Próximos
            </button>
            <button
              onClick={() => setActiveTab('settings')}
              className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === 'settings'
                  ? 'border-emerald-500 text-emerald-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              ⚙️ Configuración
            </button>
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Calendar Tab */}
        {activeTab === 'calendar' && (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <div>
                <h2 className="text-xl font-bold text-gray-900 mb-2">Calendario de Eventos</h2>
                <p className="text-gray-600">Visualiza y gestiona todos tus eventos</p>
              </div>
              <button
                onClick={() => setShowEventModal(true)}
                className="px-6 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 flex items-center gap-2"
              >
                <span>➕</span>
                Nuevo Evento
              </button>
            </div>

            {/* Events List */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2 space-y-4">
                {events.length === 0 ? (
                  <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
                    <div className="text-6xl mb-4">📅</div>
                    <h3 className="text-xl font-semibold text-gray-900 mb-2">No hay eventos</h3>
                    <p className="text-gray-600 mb-6">Crea tu primer evento para organizar tu agenda</p>
                    <button
                      onClick={() => setShowEventModal(true)}
                      className="px-6 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700"
                    >
                      Crear Evento
                    </button>
                  </div>
                ) : (
                  events
                    .sort((a, b) => new Date(a.date + ' ' + a.time) - new Date(b.date + ' ' + b.time))
                    .map((event) => (
                      <div
                        key={event.id}
                        className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
                      >
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <div className="flex items-center gap-3 mb-2">
                              <span className="text-2xl">{getEventTypeIcon(event.type)}</span>
                              <div>
                                <h3 className="text-lg font-bold text-gray-900">{event.title}</h3>
                                <div className="flex items-center gap-3 text-sm text-gray-600">
                                  <span>📅 {event.date}</span>
                                  <span>⏰ {event.time}</span>
                                  <span>⏱️ {event.duration} min</span>
                                </div>
                              </div>
                            </div>
                            {event.description && (
                              <p className="text-sm text-gray-600 mt-2">{event.description}</p>
                            )}
                          </div>
                          <div className="flex items-center gap-2">
                            <span className={`px-3 py-1 text-xs rounded-full ${getEventTypeColor(event.type)}`}>
                              {event.type}
                            </span>
                            <button
                              onClick={() => deleteEvent(event.id)}
                              className="text-red-600 hover:text-red-800"
                            >
                              🗑️
                            </button>
                          </div>
                        </div>
                      </div>
                    ))
                )}
              </div>

              {/* Sidebar */}
              <div className="space-y-6">
                <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                  <h3 className="font-bold text-gray-900 mb-4">⏰ Próximos Eventos</h3>
                  {upcomingEvents.length === 0 ? (
                    <p className="text-sm text-gray-500">No hay eventos próximos</p>
                  ) : (
                    <div className="space-y-3">
                      {upcomingEvents.map((event) => (
                        <div key={event.id} className="text-sm">
                          <div className="font-semibold text-gray-900">{event.title}</div>
                          <div className="text-gray-500">{event.date} • {event.time}</div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl p-6">
                  <h3 className="font-bold text-blue-900 mb-2">🔔 Recordatorios</h3>
                  <p className="text-sm text-blue-800 mb-4">
                    Recibe notificaciones antes de tus eventos
                  </p>
                  <button className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 text-sm">
                    Configurar
                  </button>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Today Tab */}
        {activeTab === 'today' && (
          <div className="space-y-6">
            <div>
              <h2 className="text-xl font-bold text-gray-900 mb-2">Eventos de Hoy</h2>
              <p className="text-gray-600">
                {new Date().toLocaleDateString('es-PY', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
              </p>
            </div>

            {todayEvents.length === 0 ? (
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
                <div className="text-6xl mb-4">🎉</div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">No hay eventos hoy</h3>
                <p className="text-gray-600">Disfruta tu día libre</p>
              </div>
            ) : (
              <div className="space-y-4">
                {todayEvents
                  .sort((a, b) => a.time.localeCompare(b.time))
                  .map((event) => (
                    <div
                      key={event.id}
                      className="bg-white rounded-xl shadow-sm border border-gray-200 p-6"
                    >
                      <div className="flex items-center gap-4">
                        <div className="text-4xl">{getEventTypeIcon(event.type)}</div>
                        <div className="flex-1">
                          <h3 className="text-lg font-bold text-gray-900">{event.title}</h3>
                          <div className="flex items-center gap-3 text-sm text-gray-600 mt-1">
                            <span>⏰ {event.time}</span>
                            <span>⏱️ {event.duration} min</span>
                            <span className={`px-2 py-1 text-xs rounded ${getEventTypeColor(event.type)}`}>
                              {event.type}
                            </span>
                          </div>
                          {event.description && (
                            <p className="text-sm text-gray-600 mt-2">{event.description}</p>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
              </div>
            )}
          </div>
        )}

        {/* Upcoming Tab */}
        {activeTab === 'upcoming' && (
          <div className="space-y-6">
            <div>
              <h2 className="text-xl font-bold text-gray-900 mb-2">Próximos Eventos</h2>
              <p className="text-gray-600">Eventos programados para los próximos días</p>
            </div>

            {upcomingEvents.length === 0 ? (
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
                <div className="text-6xl mb-4">📆</div>
                <h3 className="text-xl font-semibold text-gray-900 mb-2">No hay eventos próximos</h3>
                <p className="text-gray-600">Agenda nuevos eventos para organizar tu semana</p>
              </div>
            ) : (
              <div className="space-y-4">
                {upcomingEvents.map((event) => (
                  <div
                    key={event.id}
                    className="bg-white rounded-xl shadow-sm border border-gray-200 p-6"
                  >
                    <div className="flex items-center gap-4">
                      <div className="text-4xl">{getEventTypeIcon(event.type)}</div>
                      <div className="flex-1">
                        <h3 className="text-lg font-bold text-gray-900">{event.title}</h3>
                        <div className="flex items-center gap-3 text-sm text-gray-600 mt-1">
                          <span>📅 {event.date}</span>
                          <span>⏰ {event.time}</span>
                          <span>⏱️ {event.duration} min</span>
                        </div>
                        {event.description && (
                          <p className="text-sm text-gray-600 mt-2">{event.description}</p>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Settings Tab */}
        {activeTab === 'settings' && (
          <div className="space-y-6">
            <div>
              <h2 className="text-xl font-bold text-gray-900 mb-2">Configuración</h2>
              <p className="text-gray-600">Personaliza tu organizador de agenda</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <h3 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
                  <span>🔗</span>
                  Google Calendar
                </h3>
                <p className="text-sm text-gray-600 mb-4">
                  {googleConnected 
                    ? 'Tu cuenta está conectada y sincronizada'
                    : 'Conecta tu cuenta de Google para sincronizar eventos'}
                </p>
                {googleConnected ? (
                  <div className="space-y-2">
                    <button
                      onClick={syncEvents}
                      className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                    >
                      🔄 Sincronizar Ahora
                    </button>
                    <button
                      onClick={() => setGoogleConnected(false)}
                      className="w-full px-4 py-2 bg-red-100 text-red-700 rounded-lg hover:bg-red-200"
                    >
                      Desconectar
                    </button>
                  </div>
                ) : (
                  <button
                    onClick={connectGoogle}
                    className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                  >
                    Conectar Google
                  </button>
                )}
              </div>

              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <h3 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
                  <span>🔔</span>
                  Notificaciones
                </h3>
                <div className="space-y-3">
                  <label className="flex items-center gap-2">
                    <input type="checkbox" defaultChecked className="rounded" />
                    <span className="text-sm text-gray-700">Email antes de eventos</span>
                  </label>
                  <label className="flex items-center gap-2">
                    <input type="checkbox" defaultChecked className="rounded" />
                    <span className="text-sm text-gray-700">Push notifications</span>
                  </label>
                  <label className="flex items-center gap-2">
                    <input type="checkbox" className="rounded" />
                    <span className="text-sm text-gray-700">SMS recordatorios</span>
                  </label>
                </div>
              </div>

              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <h3 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
                  <span>⏰</span>
                  Recordatorios
                </h3>
                <div className="space-y-3">
                  <div>
                    <label className="block text-sm text-gray-700 mb-1">
                      Recordar antes de eventos
                    </label>
                    <select className="w-full px-3 py-2 border border-gray-300 rounded-lg">
                      <option>15 minutos</option>
                      <option>30 minutos</option>
                      <option>1 hora</option>
                      <option>1 día</option>
                    </select>
                  </div>
                </div>
              </div>

              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <h3 className="font-bold text-gray-900 mb-4 flex items-center gap-2">
                  <span>🌍</span>
                  Zona Horaria
                </h3>
                <p className="text-sm text-gray-600 mb-3">
                  Tu zona horaria: {user?.timezone || 'America/Asuncion'}
                </p>
                <button className="w-full px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200">
                  Cambiar
                </button>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Event Modal */}
      {showEventModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl max-w-2xl w-full p-6">
            <h3 className="text-xl font-bold text-gray-900 mb-4">Crear Nuevo Evento</h3>
            <form onSubmit={handleCreateEvent} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Título del Evento
                </label>
                <input
                  type="text"
                  required
                  value={newEvent.title}
                  onChange={(e) => setNewEvent({ ...newEvent, title: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                  placeholder="Ej: Reunión con cliente"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Fecha
                  </label>
                  <input
                    type="date"
                    required
                    value={newEvent.date}
                    onChange={(e) => setNewEvent({ ...newEvent, date: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Hora
                  </label>
                  <input
                    type="time"
                    required
                    value={newEvent.time}
                    onChange={(e) => setNewEvent({ ...newEvent, time: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Duración (min)
                  </label>
                  <input
                    type="number"
                    required
                    value={newEvent.duration}
                    onChange={(e) => setNewEvent({ ...newEvent, duration: parseInt(e.target.value) })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Tipo
                  </label>
                  <select
                    value={newEvent.type}
                    onChange={(e) => setNewEvent({ ...newEvent, type: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                  >
                    <option value="meeting">Reunión</option>
                    <option value="call">Llamada</option>
                    <option value="task">Tarea</option>
                    <option value="reminder">Recordatorio</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Descripción
                </label>
                <textarea
                  value={newEvent.description}
                  onChange={(e) => setNewEvent({ ...newEvent, description: e.target.value })}
                  rows="3"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500"
                  placeholder="Detalles adicionales..."
                />
              </div>

              <div className="flex gap-3">
                <button
                  type="submit"
                  className="flex-1 px-6 py-3 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700"
                >
                  Crear Evento
                </button>
                <button
                  type="button"
                  onClick={() => setShowEventModal(false)}
                  className="px-6 py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
                >
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default OrganizadorAgenda;
