import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import VideoBackground from '../components/VideoBackground';
import Header from '../components/Header';
import Footer from '../components/Footer';
import './LandingPage.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const LandingPage = ({ services }) => {
  const navigate = useNavigate();
  const [showAuth, setShowAuth] = useState(false);
  const [isLogin, setIsLogin] = useState(true);
  const [chatOpen, setChatOpen] = useState(false);
  const [chatMessages, setChatMessages] = useState([]);
  const [chatInput, setChatInput] = useState('');
  const [chatLoading, setChatLoading] = useState(false);
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    name: '',
    country: 'Paraguay'
  });
  const [errorMsg, setErrorMsg] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [showForgotPassword, setShowForgotPassword] = useState(false);
  const [forgotPasswordEmail, setForgotPasswordEmail] = useState('');
  const [countries, setCountries] = useState([]);

  // Función para verificar si está logueado
  const isLoggedIn = localStorage.getItem('token') !== null;

  useEffect(() => {
    fetchCountries();
    
    // Manejar callback de Google OAuth
    const urlParams = new URLSearchParams(window.location.search);
    const tokenParam = urlParams.get('token');
    const oauth = urlParams.get('oauth');
    const error = urlParams.get('error');
    
    if (tokenParam && oauth === 'google') {
      // Guardar token y redirigir al dashboard
      localStorage.setItem('token', tokenParam);
      window.location.href = '/dashboard';
    } else if (error) {
      const message = urlParams.get('message') || 'Error en la autenticación con Google';
      alert(message);
      // Limpiar la URL
      window.history.replaceState({}, document.title, window.location.pathname);
    }
  }, []);

  const fetchCountries = async () => {
    try {
      const response = await axios.get(`${API}/countries`);
      setCountries(response.data.countries);
    } catch (e) {
      console.error('Failed to fetch countries', e);
    }
  };

  const handleAuth = async (e) => {
    e.preventDefault();
    setErrorMsg('');

    try {
      const endpoint = isLogin ? '/auth/login' : '/auth/register';
      const response = await axios.post(`${API}${endpoint}`, formData);

      if (!isLogin) {
        alert('¡Cuenta creada! Por favor verifica tu email antes de iniciar sesión.');
        setShowAuth(false);
        return;
      }

      // Store token and user
      localStorage.setItem('token', response.data.access_token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
      
      setShowAuth(false);
      navigate('/dashboard');
    } catch (e) {
      const error = e.response?.data?.detail || (isLogin ? 'Error de autenticación' : 'Error en el registro');
      setErrorMsg(error);
    }
  };

  const handleGoogleLogin = () => {
    // Redirigir al endpoint de Google OAuth en el backend
    const redirect_after = encodeURIComponent(window.location.origin + '/dashboard');
    window.location.href = `${API}/auth/google/login?redirect_after=${redirect_after}`;
  };

  const handleChat = async () => {
    if (!chatInput.trim() || chatLoading) return;

    const userMsg = { role: 'user', content: chatInput };
    setChatMessages(prev => [...prev, userMsg]);
    setChatInput('');
    setChatLoading(true);

    try {
      const response = await axios.post(`${API}/chat`, {
        message: chatInput,
        agent_name: 'Rocío'
      });

      const aiMsg = { role: 'assistant', content: response.data.response };
      setChatMessages(prev => [...prev, aiMsg]);
    } catch (e) {
      console.error('Chat error:', e);
      const errorMsg = { role: 'assistant', content: 'Lo siento, estoy experimentando dificultades técnicas.' };
      setChatMessages(prev => [...prev, errorMsg]);
    } finally {
      setChatLoading(false);
    }
  };

  const formatPrice = (price) => {
    if (price === 0) return 'GRATIS';
    return 'Gs. ' + new Intl.NumberFormat('es-PY', {
      minimumFractionDigits: 0
    }).format(price);
  };

  const formatPriceWithDiscount = (price) => {
    if (price === 0) return 'GRATIS';
    const discounted = price * 0.75; // 25% off
    return 'Gs. ' + new Intl.NumberFormat('es-PY', {
      minimumFractionDigits: 0
    }).format(discounted);
  };

  return (
    <VideoBackground>
      {/* Header */}
      <Header 
        onLoginClick={() => setShowAuth(true)}
        onTrialClick={() => setShowAuth(true)}
      />

      {/* Hero Section */}
      <section className="pt-32 pb-12 px-6">
        <div className="max-w-7xl mx-auto text-center">
          <div className="animate-fade-in-up">
            <h2 className="text-5xl sm:text-6xl lg:text-7xl font-bold mb-6 leading-tight text-white text-shadow-strong">
              Automatiza tu Empresa
              <br />
              <span className="text-emerald-300">con Soluciones Inteligentes</span>
            </h2>
            <p className="text-xl text-white text-shadow mb-4 max-w-3xl mx-auto">
              Desde contabilizar facturas a partir de una foto o pdf, pasando por prospección de leads, hasta agentes de ventas 24/7. Transforma tu negocio con automatización avanzada.
            </p>
            
            {/* Banner Trial Gratuito */}
            <div className="glass-strong rounded-2xl p-6 max-w-2xl mx-auto mb-4 border-4 border-green-400 bg-gradient-to-r from-green-50 to-emerald-50">
              <div className="flex items-center justify-center mb-2">
                <span className="text-3xl mr-2">🎁</span>
                <p className="text-emerald-900 font-bold text-2xl">
                  ¡Trial Gratuito de 7 Días!
                </p>
              </div>
              <p className="text-gray-800 text-base">
                Prueba <strong>cualquier servicio sin tarjeta de crédito</strong>
              </p>
              <p className="text-green-700 text-sm mt-2 font-semibold">
                ✓ Sin compromiso &nbsp;|&nbsp; ✓ Cancela cuando quieras &nbsp;|&nbsp; ✓ Full acceso
              </p>
            </div>
            
            {/* Banner Crypto */}
            <div className="glass-strong rounded-2xl p-4 max-w-2xl mx-auto mb-8 border-2 border-yellow-400 bg-yellow-50">
              <p className="text-emerald-900 font-semibold text-lg">
                ⚡ Servicios para inversores en criptomonedas
              </p>
              <p className="text-gray-700 text-sm mt-1">
                Regístrate hoy y obtén nuestro <strong>Escáner de Fraude CryptoShield IA GRATIS... para siempre</strong>
              </p>
              <p className="text-orange-600 text-xs mt-2 font-semibold">
                🪙 25% OFF en planes anuales pagando con BTC/ETH
              </p>
            </div>

            {!isLoggedIn && (
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <button
                  onClick={() => setShowAuth(true)}
                  className="bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white px-8 py-6 text-lg rounded-full btn-primary shadow-xl font-semibold"
                >
                  Comenzar Trial Gratis (7 días)
                </button>
                <button
                  onClick={() => setChatOpen(true)}
                  className="glass-strong border-2 border-white/50 text-emerald-900 hover:bg-white/90 px-8 py-6 text-lg rounded-full font-semibold"
                >
                  💬 Hablar con Asistente
                </button>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-12 px-6">
        <div className="max-w-7xl mx-auto">
          <h3 className="text-4xl font-bold text-center mb-16 text-white text-shadow-strong">¿Por qué elegirnos?</h3>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              { icon: '⚡', title: 'Autoconfigurable', desc: 'Sin necesidad de desarrolladores. Configura y activa tus servicios en minutos sin conocimientos técnicos' },
              { icon: '🛡️', title: 'Seguro y Confiable', desc: 'Tus datos protegidos con encriptación de nivel empresarial' },
              { icon: '📈', title: 'Escalable', desc: 'Crece desde 10 hasta 10,000 conversaciones sin límites' }
            ].map((feature, idx) => (
              <div key={idx} className="service-card glass-strong border-2 border-white/40 hover:border-emerald-300 rounded-2xl p-8">
                <div className="w-16 h-16 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-2xl flex items-center justify-center mb-4 text-white shadow-lg text-3xl">
                  {feature.icon}
                </div>
                <h4 className="text-2xl text-emerald-900 font-bold mb-4">{feature.title}</h4>
                <p className="text-gray-700">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Services */}
      <section className="py-20 px-6" id="servicios">
        <div className="max-w-7xl mx-auto">
          <h3 className="text-4xl font-bold text-center mb-6 text-white text-shadow-strong">Servicios de Automatización</h3>
          <p className="text-center text-white text-shadow mb-8 text-lg">Comienza desde Gs. 99.000/mes</p>

          {services.length === 0 ? (
            <div className="text-center py-12">
              <p className="text-white text-shadow text-lg">Cargando servicios...</p>
            </div>
          ) : (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
              {services.map((service, idx) => (
                <div key={service.id} className={`service-card glass-strong border-2 border-white/40 hover:border-emerald-400 rounded-2xl p-6 relative overflow-hidden ${service.status === 'coming_soon' ? 'opacity-75' : ''}`}>
                  {service.status === 'coming_soon' && (
                    <div className="absolute top-12 -right-12 bg-yellow-400 text-black px-16 py-2 transform rotate-45 shadow-lg z-10">
                      <span className="font-bold text-sm">PRÓXIMAMENTE</span>
                    </div>
                  )}
                  
                  <h4 className="text-2xl text-emerald-700 font-bold mb-3">{service.name}</h4>
                  <p className="text-base text-gray-700 mb-4">{service.short_description || service.description}</p>
                  
                  {/* Suite Crypto - Incluye servicios */}
                  {service.included_services && service.included_services.length > 0 && (
                    <div className="mb-4 space-y-2">
                      {service.included_services.map((inc, iidx) => (
                        <div key={iidx} className="flex items-center justify-between bg-white/50 rounded-lg p-2">
                          <span className="text-sm font-semibold text-gray-700">{inc.name}</span>
                          {inc.status === 'GRATIS' && (
                            <span className="bg-green-500 text-white text-xs px-2 py-1 rounded-full font-bold">GRATIS</span>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                  
                  <div className="mb-6">
                    {/* Si es freemium con packs */}
                    {service.billing_type === 'freemium_packs' ? (
                      <div className="mb-4">
                        {/* Trial Gratuito */}
                        <div className="bg-gradient-to-r from-green-100 to-emerald-100 p-4 rounded-xl border-2 border-green-400 mb-3">
                          <p className="text-xs text-green-800 mb-2 uppercase font-bold">🎁 Prueba Gratis</p>
                          <div className="text-center mb-2">
                            <span className="text-3xl font-bold text-green-700">5 Leads Incluidos</span>
                          </div>
                          <div className="space-y-1 text-xs text-gray-700 mb-3">
                            <p>✅ Sin tarjeta de crédito</p>
                            <p>✅ 5 leads con datos completos</p>
                            <p>✅ Mensajes Ice Breaker personalizados</p>
                          </div>
                          <p className="text-xs text-gray-600 text-center">
                            Crea tu primera campaña GRATIS y descubre cómo obtenemos leads reales de Google Maps
                          </p>
                        </div>
                      </div>
                    ) : service.billing_type === 'one_time' ? (
                      /* Pago único (Consultoría) */
                      <div className="mb-4">
                        <div className="bg-gradient-to-r from-purple-100 to-pink-100 p-4 rounded-xl border-2 border-purple-300">
                          <p className="text-xs text-purple-700 mb-2 uppercase font-bold">💎 Pago Único - No Suscripción</p>
                          <div className="mb-3">
                            <p className="text-sm text-gray-600 mb-1">Precio Regular:</p>
                            <span className="text-3xl font-bold text-purple-700">{formatPrice(service.price_monthly)}</span>
                          </div>
                          {service.price_crypto && service.price_crypto < service.price_monthly && (
                            <div className="mt-3 p-3 bg-gradient-to-r from-orange-100 to-yellow-100 rounded-lg border-2 border-orange-300">
                              <p className="text-xs text-orange-800 font-bold mb-1">🪙 Paga con BTC/ETH:</p>
                              <div className="flex items-baseline gap-2">
                                <span className="text-2xl font-bold text-orange-700">{formatPrice(service.price_crypto)}</span>
                                <span className="bg-orange-500 text-white px-2 py-0.5 rounded-full text-xs font-bold">-25%</span>
                              </div>
                            </div>
                          )}
                          {service.no_expiration && (
                            <div className="mt-3 p-3 bg-white/80 rounded-lg">
                              <p className="text-xs text-purple-700 font-bold mb-1">⏰ No Caduca</p>
                              <p className="text-xs text-gray-700">Usa bajo demanda cuando lo necesites</p>
                            </div>
                          )}
                        </div>
                      </div>
                    ) : (
                      <>
                        {/* Suite Crypto - Plan anual únicamente */}
                        {service.billing_period === 'annual_only' && (
                          <div className="mb-4">
                            <div className="bg-white p-4 rounded-lg">
                              <div className="text-center mb-3">
                                <span className="text-3xl font-bold text-emerald-700">{formatPrice(service.price_annual)}</span>
                                <span className="text-gray-600 ml-2">/año</span>
                              </div>
                              <p className="text-xs text-gray-600 text-center mb-3">Plan anual - Acceso a los 3 servicios</p>
                              {service.included_services && service.included_services.length > 0 && (
                                <div className="mb-3 space-y-2">
                                  {service.included_services.map((inc, iidx) => (
                                    <div key={iidx} className="flex items-center justify-between bg-gray-50 rounded-lg p-2">
                                      <span className="text-sm font-semibold text-gray-700">{inc.name}</span>
                                      {inc.status === 'GRATIS' && (
                                        <span className="bg-green-500 text-white text-xs px-2 py-1 rounded-full font-bold">GRATIS</span>
                                      )}
                                    </div>
                                  ))}
                                </div>
                              )}
                              {service.price_annual_crypto && (
                                <div className="p-3 bg-gradient-to-r from-orange-100 to-yellow-100 rounded-lg border-2 border-orange-300">
                                  <div className="text-center">
                                    <span className="text-2xl font-bold text-orange-700">{formatPrice(service.price_annual_crypto)}</span>
                                    <span className="text-gray-600 ml-1 text-sm">con BTC/ETH</span>
                                    <span className="text-orange-600 ml-2 text-sm font-semibold">(25% OFF)</span>
                                  </div>
                                </div>
                              )}
                            </div>
                          </div>
                        )}
                        
                        {/* Servicios CON mensajería (WhatsApp/Telegram) */}
                        {service.requires_messaging && service.billing_period !== 'annual_only' && (
                          <div className="mb-4 p-3 bg-gradient-to-r from-blue-50 to-cyan-50 rounded-lg border-2 border-blue-300">
                            <p className="text-xs text-blue-800 font-bold mb-2">📱 Precios por Plataforma</p>
                            
                            {/* WhatsApp - Precio Base */}
                            <div className="bg-white p-3 rounded-lg mb-3">
                              <div className="flex items-center gap-2 mb-3">
                                <span className="text-lg">💚</span>
                                <span className="font-bold text-green-700">WhatsApp</span>
                              </div>
                              <div className="grid grid-cols-2 gap-4">
                                <div className="text-center p-3 bg-green-50 rounded-lg">
                                  <p className="text-xs text-gray-600 mb-2 font-semibold">Mensual</p>
                                  <p className="text-lg font-bold text-green-700 mb-1">{formatPrice(service.price_monthly)}</p>
                                  <p className="text-sm text-gray-500">/mes</p>
                                </div>
                                <div className="text-center p-3 bg-green-50 rounded-lg">
                                  <p className="text-xs text-gray-600 mb-2 font-semibold">Anual (10 meses)</p>
                                  <p className="text-lg font-bold text-green-700 mb-1">{formatPrice(service.price_annual)}</p>
                                  <p className="text-sm text-gray-500">/año</p>
                                  <p className="text-xs text-emerald-600 font-semibold mt-2">✓ Ahorras 2 meses</p>
                                </div>
                              </div>
                              {service.price_annual_crypto && (
                                <div className="mt-3 p-3 bg-gradient-to-r from-orange-100 to-yellow-100 rounded-lg border-2 border-orange-300">
                                  <p className="text-xs text-orange-800 font-bold mb-2">🪙 Anual con BTC/ETH:</p>
                                  <div className="flex flex-col items-center gap-2">
                                    <div className="flex items-baseline gap-2">
                                      <span className="text-xl font-bold text-orange-700">{formatPrice(service.price_annual_crypto)}</span>
                                      <span className="text-sm text-gray-500">/año</span>
                                    </div>
                                    <span className="bg-orange-500 text-white px-3 py-1 rounded-full text-xs font-bold">AHORRA 25%</span>
                                  </div>
                                </div>
                              )}
                            </div>

                            {/* Telegram con descuento 20% */}
                            <div className="bg-white p-3 rounded-lg border-2 border-blue-400">
                              <div className="flex items-center justify-between mb-3">
                                <div className="flex items-center gap-2">
                                  <span className="text-lg">✈️</span>
                                  <span className="font-bold text-blue-700">Telegram</span>
                                </div>
                                <span className="bg-blue-500 text-white px-2 py-0.5 rounded-full text-xs font-bold">-20%</span>
                              </div>
                              <div className="grid grid-cols-2 gap-4">
                                <div className="text-center p-3 bg-blue-50 rounded-lg">
                                  <p className="text-xs text-gray-600 mb-2 font-semibold">Mensual</p>
                                  <p className="text-lg font-bold text-blue-700 mb-1">{formatPrice(service.price_monthly_telegram || Math.round(service.price_monthly * 0.8))}</p>
                                  <p className="text-sm text-gray-500">/mes</p>
                                </div>
                                <div className="text-center p-3 bg-blue-50 rounded-lg">
                                  <p className="text-xs text-gray-600 mb-2 font-semibold">Anual (10 meses)</p>
                                  <p className="text-lg font-bold text-blue-700 mb-1">{formatPrice(service.price_annual_telegram || Math.round(service.price_annual * 0.8))}</p>
                                  <p className="text-sm text-gray-500">/año</p>
                                  <p className="text-xs text-emerald-600 font-semibold mt-2">✓ Ahorras 2 meses</p>
                                </div>
                              </div>
                              {service.price_annual_crypto_telegram && (
                                <div className="mt-3 p-2 bg-gradient-to-r from-orange-100 to-yellow-100 rounded-lg border-2 border-orange-300">
                                  <p className="text-xs text-orange-800 font-bold mb-1">🪙 Anual con BTC/ETH:</p>
                                  <div className="flex items-baseline justify-center gap-2">
                                    <span className="text-xl font-bold text-orange-700">{formatPrice(service.price_annual_crypto_telegram)}/año</span>
                                    <span className="bg-orange-500 text-white px-2 py-0.5 rounded-full text-xs font-bold">-25%</span>
                                  </div>
                                </div>
                              )}
                              <div className="mt-2 p-2 bg-blue-50 rounded text-xs text-blue-800">
                                <strong>⚡ Más estable:</strong> Telegram ofrece mayor fiabilidad en la entrega
                              </div>
                            </div>
                          </div>
                        )}
                        
                        {/* Servicios SIN mensajería (solo Panel Web) */}
                        {!service.requires_messaging && service.billing_period !== 'annual_only' && service.billing_type !== 'one_time' && service.billing_type !== 'freemium_packs' && (
                          <div className="mb-4 p-3 bg-gradient-to-r from-indigo-50 to-purple-50 rounded-lg border-2 border-indigo-300">
                            <div className="flex items-center gap-2 mb-3">
                              <span className="text-lg">🖥️</span>
                              <p className="text-xs text-indigo-800 font-bold">ACCESO VÍA PANEL WEB</p>
                            </div>
                            
                            <div className="bg-white p-4 rounded-lg">
                              <div className="grid grid-cols-2 gap-4 mb-4">
                                <div className="text-center p-3 bg-gray-50 rounded-lg">
                                  <p className="text-xs text-gray-600 mb-2 font-semibold">Plan Mensual</p>
                                  <p className="text-xl font-bold text-indigo-700 mb-1">{formatPrice(service.price_monthly)}</p>
                                  <p className="text-sm text-gray-500">/mes</p>
                                </div>
                                <div className="text-center p-3 bg-gray-50 rounded-lg">
                                  <p className="text-xs text-gray-600 mb-2 font-semibold">Plan Anual (10 meses)</p>
                                  <p className="text-xl font-bold text-indigo-700 mb-1">{formatPrice(service.price_annual)}</p>
                                  <p className="text-sm text-gray-500">/año</p>
                                  <p className="text-xs text-emerald-600 font-semibold mt-2">✓ Ahorras 2 meses</p>
                                </div>
                              </div>
                              {service.price_annual_crypto && (
                                <div className="mb-3 p-3 bg-gradient-to-r from-orange-100 to-yellow-100 rounded-lg border-2 border-orange-300">
                                  <p className="text-xs text-orange-800 font-bold mb-2">🪙 Anual con BTC/ETH:</p>
                                  <div className="flex flex-col items-center gap-2">
                                    <div className="flex items-baseline gap-2">
                                      <span className="text-2xl font-bold text-orange-700">{formatPrice(service.price_annual_crypto)}</span>
                                      <span className="text-sm text-gray-500">/año</span>
                                    </div>
                                    <span className="bg-orange-500 text-white px-3 py-1 rounded-full text-xs font-bold">AHORRA 25%</span>
                                  </div>
                                </div>
                              )}
                              {service.multi_purchase && (
                                <div className="mt-3 p-3 bg-indigo-50 rounded-lg text-xs text-indigo-800 leading-relaxed">
                                  <strong className="block mb-1">🔢 Múltiples instancias:</strong>
                                  <span>Puedes contratar varias para diferentes proyectos</span>
                                </div>
                              )}
                              <div className="mt-3 p-3 bg-indigo-50 rounded-lg text-xs text-indigo-800 leading-relaxed">
                                <strong className="block mb-1">✨ Dashboard Personalizado:</strong>
                                <span>Gestiona todo desde tu área de cliente</span>
                              </div>
                            </div>
                          </div>
                        )}
                      </>
                    )}
                  </div>
                  </div>
                  
                  {/* Features */}
                  {service.features && service.features.length > 0 && (
                    <ul className="space-y-2 mb-6">
                      {service.features.map((feature, fidx) => (
                        <li key={fidx} className="flex items-start gap-2 text-gray-700 text-sm">
                          <span className="text-emerald-500 flex-shrink-0 mt-0.5">✓</span>
                          <span>{feature}</span>
                        </li>
                      ))}
                    </ul>
                  )}
                  
                  {/* Button */}
                  <button 
                    onClick={() => service.status !== 'coming_soon' && (isLoggedIn ? navigate('/dashboard') : setShowAuth(true))}
                    disabled={service.status === 'coming_soon'}
                    className={`w-full py-3 px-4 rounded-xl font-bold transition ${
                      service.status === 'coming_soon' 
                        ? 'bg-gray-400 text-gray-200 cursor-not-allowed'
                        : 'bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white'
                    }`}
                  >
                    {service.status === 'coming_soon' ? 'Próximamente' : 'Suscribirse'}
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Team */}
      <section className="py-24 px-6" id="equipo">
        <div className="max-w-7xl mx-auto">
          <h3 className="text-4xl font-bold text-center mb-6 text-white text-shadow-strong">Nuestro Equipo de Agentes IA</h3>
          <p className="text-center text-white text-shadow mb-12 text-lg max-w-3xl mx-auto">
            Conoce a los agentes especializados que trabajarán 24/7 para automatizar tu negocio
          </p>

          <div className="mb-16 flex justify-center">
            <div className="glass-strong rounded-2xl overflow-hidden border-4 border-white/40 shadow-2xl max-w-4xl">
              <img
                src="/assets/team/group.png"
                alt="Equipo GuaraniAppStore"
                className="w-full h-auto"
              />
            </div>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              { name: 'Junior Cucurella', role: 'Gerente de Agendas', desc: 'Gestiona completamente citas, reservas y recordatorios 24/7', img: '/assets/team/junior.png' },
              { name: 'Jacinto Torrelavega', role: 'Asistente de Facturación', desc: 'Automatiza flujos contables', img: '/assets/team/jacinto.png' },
              { name: 'Alex Albiol', role: 'Soporte Instantáneo', desc: 'Respuestas rápidas y efectivas para tus clientes', img: '/assets/team/alex.png' },
              { name: 'Silvia Garcia', role: 'Integración Operativa', desc: 'Conecta sistemas y optimiza procesos', img: '/assets/team/silvia.png' },
              { name: 'Blanca Garcia', role: 'Servicio RPA', desc: 'Elimina el "copiar y pegar", automatizando la transferencia de datos', img: '/assets/team/blanca.png' },
              { name: 'Rocío Almeida', role: 'Moderador de Reputación', desc: 'Gestiona y protege tu imagen digital', img: '/assets/team/rocio.png' }
            ].map((member, idx) => (
              <div key={idx} className="glass-strong border-2 border-white/40 hover:border-emerald-400 service-card rounded-2xl p-6">
                <div className="flex justify-center mb-4">
                  <div className="w-32 h-32 rounded-full overflow-hidden border-4 border-emerald-500 shadow-lg">
                    <img
                      src={member.img}
                      alt={member.name}
                      className="w-full h-full object-cover"
                    />
                  </div>
                </div>
                <h4 className="text-xl text-center text-emerald-900 font-bold mb-2">{member.name}</h4>
                <p className="text-center text-emerald-700 font-semibold text-sm mb-4">{member.role}</p>
                <p className="text-gray-700 text-sm text-center mb-4">{member.desc}</p>
                <button
                  onClick={() => {
                    setChatOpen(true);
                    setChatMessages([{
                      role: 'assistant',
                      content: `¡Hola! Soy ${member.name}, ${member.role}. ${member.desc}. ¿En qué puedo ayudarte hoy?`
                    }]);
                  }}
                  className="w-full bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white py-2 rounded-xl btn-primary font-semibold"
                >
                  💬 Chatear con {member.name.split(' ')[0]}
                </button>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-24 px-6">
        <div className="max-w-4xl mx-auto text-center glass-dark rounded-3xl p-12 border-2 border-white/30">
          <h3 className="text-4xl sm:text-5xl font-bold mb-6 text-white">¿Listo para automatizar?</h3>
          <p className="text-xl mb-10 text-emerald-100">Prueba gratis por 7 días. Sin tarjeta de crédito.</p>
          {!isLoggedIn && (
            <button
              onClick={() => setShowAuth(true)}
              className="bg-white text-emerald-600 hover:bg-emerald-50 px-10 py-6 text-xl rounded-full shadow-2xl font-semibold"
            >
              Iniciar Trial Gratuito
            </button>
          )}
        </div>
      </section>

      {/* Auth Modal */}
      {showAuth && (
        <div className="fixed inset-0 z-[9999] flex items-center justify-center bg-black/50 backdrop-blur-sm" onClick={() => setShowAuth(false)}>
          <div className="glass-strong rounded-2xl p-8 max-w-md w-full mx-4 border-2 border-white/30" onClick={(e) => e.stopPropagation()}>
            <h2 className="text-2xl font-bold text-emerald-900 mb-2">{isLogin ? 'Iniciar Sesión' : 'Crear Cuenta'}</h2>
            <p className="text-gray-600 mb-6">{isLogin ? '¡Bienvenido de vuelta!' : 'Comienza tu trial gratuito de 7 días'}</p>
            
            <form onSubmit={handleAuth} className="space-y-4">
              {!isLogin && (
                <>
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-1">Nombre completo</label>
                    <input
                      type="text"
                      value={formData.name}
                      onChange={(e) => setFormData({...formData, name: e.target.value})}
                      required
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-1">País</label>
                    <select
                      value={formData.country}
                      onChange={(e) => setFormData({...formData, country: e.target.value})}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
                    >
                      {countries.map((c) => (
                        <option key={c.name} value={c.name}>{c.name} ({c.timezone})</option>
                      ))}
                    </select>
                  </div>
                </>
              )}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-1">Email</label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({...formData, email: e.target.value})}
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
                />
              </div>
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-1">Contraseña</label>
                <div className="relative">
                  <input
                    type={showPassword ? "text" : "password"}
                    value={formData.password}
                    onChange={(e) => setFormData({...formData, password: e.target.value})}
                    required
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent pr-10"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-2 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-700"
                  >
                    {showPassword ? '🙈' : '👁️'}
                  </button>
                </div>
                {isLogin && (
                  <div className="text-right mt-1">
                    <button
                      type="button"
                      onClick={() => {
                        setShowAuth(false);
                        setShowForgotPassword(true);
                      }}
                      className="text-sm text-emerald-600 hover:text-emerald-700 hover:underline"
                    >
                      ¿Olvidaste tu contraseña?
                    </button>
                  </div>
                )}
              </div>
              {errorMsg && (
                <div className="text-red-500 text-sm bg-red-50 p-3 rounded-lg">
                  {errorMsg}
                </div>
              )}
              <button type="submit" className="w-full bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white py-3 rounded-xl btn-primary font-semibold">
                {isLogin ? 'Iniciar Sesión' : 'Crear Cuenta'}
              </button>
              
              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-gray-300"></div>
                </div>
                <div className="relative flex justify-center text-sm">
                  <span className="px-2 bg-white text-gray-500">o continúa con</span>
                </div>
              </div>

              <button
                type="button"
                onClick={handleGoogleLogin}
                className="w-full border-2 border-gray-300 hover:border-emerald-500 text-gray-700 py-3 rounded-xl font-semibold flex items-center justify-center gap-2"
              >
                <svg className="w-5 h-5" viewBox="0 0 24 24">
                  <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                  <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                  <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                  <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                </svg>
                Google
              </button>
            </form>
            
            <div className="text-center mt-6">
              <button
                onClick={() => setIsLogin(!isLogin)}
                className="text-emerald-600 hover:underline text-sm font-semibold"
              >
                {isLogin ? '¿No tienes cuenta? Regístrate' : '¿Ya tienes cuenta? Inicia sesión'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Chat Widget */}
      {chatOpen && (
        <div className="fixed bottom-6 right-6 w-96 h-[500px] glass-strong rounded-2xl shadow-2xl flex flex-col z-[9999] border-2 border-white/30">
          <div className="bg-gradient-to-r from-emerald-500 to-teal-600 p-4 rounded-t-2xl flex justify-between items-center">
            <h4 className="text-white font-semibold">💬 Asistente Virtual</h4>
            <button onClick={() => setChatOpen(false)} className="text-white hover:bg-white/20 p-1 rounded">
              ✕
            </button>
          </div>
          <div className="flex-1 overflow-y-auto p-4 space-y-3 bg-white/50">
            {chatMessages.length === 0 && (
              <div className="text-center text-gray-700 mt-8">
                <p>¡Hola! ¿En qué puedo ayudarte hoy?</p>
              </div>
            )}
            {chatMessages.map((msg, idx) => (
              <div key={idx} className={`flex gap-2 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[80%] p-3 rounded-2xl ${
                  msg.role === 'user'
                    ? 'bg-gradient-to-r from-emerald-500 to-teal-600 text-white'
                    : 'bg-white text-gray-800 shadow-sm'
                }`}>
                  {msg.content}
                </div>
              </div>
            ))}
            {chatLoading && (
              <div className="flex justify-start">
                <div className="bg-gray-100 p-3 rounded-2xl">
                  <div className="flex gap-1">
                    <div className="w-2 h-2 bg-emerald-500 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-emerald-500 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                    <div className="w-2 h-2 bg-emerald-500 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                  </div>
                </div>
              </div>
            )}
          </div>
          <div className="p-4 border-t border-emerald-100">
            <div className="flex gap-2">
              <input
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleChat()}
                placeholder="Escribe tu mensaje..."
                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
              />
              <button
                onClick={handleChat}
                className="bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-600 hover:to-teal-700 text-white px-6 py-2 rounded-lg btn-primary font-semibold"
              >
                Enviar
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Floating Chat Button */}
      {!chatOpen && (
        <button
          onClick={() => setChatOpen(true)}
          className="fixed bottom-6 right-6 w-16 h-16 rounded-full shadow-2xl flex items-center justify-center animate-float z-50 overflow-hidden border-4 border-white hover:scale-110 transition-transform"
        >
          <img src="/assets/rocio-chat.png" alt="Chat con Rocío" className="w-full h-full object-cover" />
        </button>
      )}

      {/* Footer */}
      <Footer />
    </VideoBackground>
  );
};

export default LandingPage;
