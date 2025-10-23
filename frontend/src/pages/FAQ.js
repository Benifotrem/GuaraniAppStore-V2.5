import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import Footer from '../components/Footer';
import './FAQ.css';

const FAQ = () => {
  const navigate = useNavigate();
  const [openCategory, setOpenCategory] = useState('servicios');
  const [openQuestion, setOpenQuestion] = useState(null);

  const toggleQuestion = (questionId) => {
    setOpenQuestion(openQuestion === questionId ? null : questionId);
  };

  const faqData = {
    servicios: {
      title: '📦 Servicios Disponibles',
      icon: '📦',
      questions: [
        {
          id: 'servicios-disponibles',
          question: '¿Qué servicios están actualmente disponibles?',
          answer: (
            <div>
              <p className="mb-3">Tenemos <strong>11 servicios de IA</strong> diseñados para automatizar tu negocio:</p>
              
              <h4 className="font-semibold mb-2 text-emerald-600">✅ Servicios Activos:</h4>
              <ul className="list-disc pl-6 mb-4 space-y-1">
                <li><strong>Suite Crypto</strong> - 3 bots de Telegram para inversores (CryptoShield GRATIS + Pulse + Momentum)</li>
                <li><strong>Asistente Personal para Directivos</strong> - Asistente ejecutivo 24/7 con Google Calendar</li>
                <li><strong>Agente de Preselección Curricular</strong> - Análisis automático de CVs con IA</li>
                <li><strong>Organizador de Facturas</strong> - OCR inteligente para contadores</li>
                <li><strong>Organizador de Agenda</strong> - Gestión automatizada de calendario</li>
                <li><strong>Consultoría Técnica Personalizada</strong> - Asesoría experta con IA</li>
              </ul>

              <h4 className="font-semibold mb-2 text-blue-600">🔜 Próximamente:</h4>
              <ul className="list-disc pl-6 space-y-1">
                <li><strong>Generador de Blogs Automatizado</strong> - Contenido SEO con IA</li>
                <li><strong>Automatización de E-commerce</strong> - Gestión completa de tienda online</li>
                <li><strong>Automatización de Redes Sociales</strong> - Contenido viral para LinkedIn, Twitter, Instagram, Facebook</li>
                <li><strong>Prospección Comercial</strong> - Búsqueda automática de leads en Google Maps (5 leads GRATIS)</li>
                <li><strong>Agente de Ventas IA</strong> - Vendedor conversacional 24/7</li>
              </ul>
            </div>
          )
        },
        {
          id: 'organizador-agenda',
          question: '📅 ¿Qué es el Organizador de Agenda?',
          answer: (
            <div>
              <p className="mb-3">Un asistente inteligente que gestiona tu calendario automáticamente:</p>
              <ul className="list-disc pl-6 space-y-2">
                <li>✅ Integración completa con <strong>Google Calendar</strong></li>
                <li>✅ Creación de eventos por voz o texto</li>
                <li>✅ Recordatorios automáticos inteligentes</li>
                <li>✅ Resolución de conflictos de horarios</li>
                <li>✅ Acceso vía WhatsApp o Telegram 24/7</li>
                <li>✅ Sincronización en tiempo real</li>
              </ul>
              <p className="mt-3"><strong>Precio:</strong> Gs. 99.000/mes</p>
            </div>
          )
        },
        {
          id: 'asistente-directivos',
          question: '💼 ¿Qué es el Asistente Personal para Directivos?',
          answer: (
            <div>
              <p className="mb-3">Tu secretaria ejecutiva virtual disponible 24/7:</p>
              <ul className="list-disc pl-6 space-y-2">
                <li>✅ Gestión completa de agenda (Google Calendar integrado)</li>
                <li>✅ Organización de tareas y recordatorios</li>
                <li>✅ Control de ingresos y gastos empresariales</li>
                <li>✅ Búsquedas web automatizadas</li>
                <li>✅ Enriquecimiento de contactos con LinkedIn</li>
                <li>✅ Disponible por WhatsApp y Telegram</li>
              </ul>
              <p className="mt-3"><strong>Precio:</strong> Gs. 299.000/mes (20% más barato por Telegram)</p>
            </div>
          )
        },
        {
          id: 'preseleccion-curricular',
          question: '📄 ¿Qué es el Agente de Preselección Curricular?',
          answer: (
            <div>
              <p className="mb-3">Automatiza completamente tu proceso de RRHH con IA:</p>
              <ul className="list-disc pl-6 space-y-2">
                <li>✅ Análisis automático de CVs (PDF, Word, imágenes)</li>
                <li>✅ Sistema de <strong>scoring inteligente</strong> de candidatos</li>
                <li>✅ Validación automática de emails y LinkedIn</li>
                <li>✅ Integración directa con Google Drive y Sheets</li>
                <li>✅ Recepción automática por email</li>
                <li>✅ Informes detallados de candidatos</li>
              </ul>
              <p className="mt-3"><strong>Precio:</strong> Gs. 249.000/mes</p>
            </div>
          )
        },
        {
          id: 'organizador-facturas',
          question: '🧾 ¿Qué es el Organizador de Facturas para Contadores?',
          answer: (
            <div>
              <p className="mb-3">OCR inteligente que digitaliza y organiza todas tus facturas:</p>
              <ul className="list-disc pl-6 space-y-2">
                <li>✅ <strong>OCR con IA</strong> (Mistral Pixtral + Google Vision)</li>
                <li>✅ Extracción automática de: fecha, RUC, nombre, importe, concepto</li>
                <li>✅ Categorización inteligente de gastos</li>
                <li>✅ Exportación a Google Sheets y Excel</li>
                <li>✅ Búsqueda instantánea por cualquier campo</li>
                <li>✅ Compatible con facturas paraguayas</li>
              </ul>
              <p className="mt-3"><strong>Precio:</strong> Gs. 199.000/mes</p>
            </div>
          )
        }
      ]
    },
    crypto: {
      title: <><img src="/assets/payment/bitcoin-logo.png" alt="Bitcoin" style={{width: '20px', height: '20px', display: 'inline-block', marginRight: '8px'}} /> Servicios Crypto</>,
      icon: <img src="/assets/payment/bitcoin-logo.png" alt="Bitcoin" style={{width: '20px', height: '20px'}} />,
      questions: [
        {
          id: 'cryptoshield-gratis',
          question: '🛡️ ¿CryptoShield IA es realmente gratis para siempre?',
          answer: (
            <div>
              <p className="mb-3">¡SÍ! <strong>CryptoShield IA es 100% GRATIS y lo será siempre.</strong></p>
              <p className="mb-3">CryptoShield es nuestro detector de fraude en criptomonedas que te ayuda a:</p>
              <ul className="list-disc pl-6 space-y-2">
                <li>✅ Escanear proyectos crypto sospechosos</li>
                <li>✅ Detectar red flags en contratos inteligentes</li>
                <li>✅ Analizar wallets y transacciones</li>
                <li>✅ Verificar legitimidad de exchanges</li>
                <li>✅ Alertas de scams conocidos</li>
              </ul>
              <p className="mt-3 text-emerald-600 font-semibold">
                🎁 Sin límites de uso. Sin tarjeta de crédito. Solo descarga el bot en Telegram: @stopfraudebot
              </p>
            </div>
          )
        },
        {
          id: 'pulse-ia',
          question: '📊 ¿Qué es Pulse IA?',
          answer: (
            <div>
              <p className="mb-3"><strong>Pulse IA</strong> es tu indicador de sentimiento del mercado crypto en tiempo real.</p>
              <ul className="list-disc pl-6 space-y-2">
                <li>✅ Análisis de sentimiento de redes sociales (Twitter, Reddit, Telegram)</li>
                <li>✅ Indicador visual: 🔴 Bearish / 🟡 Neutral / 🟢 Bullish</li>
                <li>✅ Alertas de cambios bruscos de sentimiento</li>
                <li>✅ Análisis de menciones de las top 50 cryptos</li>
                <li>✅ Detección de FOMO y FUD</li>
              </ul>
              <p className="mt-3">
                <strong>Bot:</strong> @Rojiverdebot<br/>
                <strong>Precio:</strong> Incluido en Suite Crypto (Gs. 0/mes individual, Gs. 600.000/año completo)
              </p>
            </div>
          )
        },
        {
          id: 'momentum-ia',
          question: '📈 ¿Qué es Momentum Predictor IA?',
          answer: (
            <div>
              <p className="mb-3"><strong>Momentum Predictor IA</strong> te da señales de trading diarias basadas en Machine Learning.</p>
              <ul className="list-disc pl-6 space-y-2">
                <li>✅ Señales diarias de BUY/SELL/HOLD</li>
                <li>✅ Predicción de movimientos de precio a 24h, 7d, 30d</li>
                <li>✅ Análisis técnico automatizado</li>
                <li>✅ Backtesting de estrategias</li>
                <li>✅ Alertas de oportunidades de alta probabilidad</li>
              </ul>
              <p className="mt-3">
                <strong>Bot:</strong> @Mejormomentobot<br/>
                <strong>Precio:</strong> Incluido en Suite Crypto
              </p>
            </div>
          )
        },
        {
          id: 'suite-crypto-anual',
          question: '💎 ¿Qué incluye la suscripción anual de Suite Crypto?',
          answer: (
            <div>
              <p className="mb-3">La <strong>Suite Crypto completa</strong> incluye acceso ilimitado a los 3 bots de Telegram:</p>
              <ul className="list-disc pl-6 space-y-2 mb-4">
                <li>🛡️ <strong>CryptoShield IA</strong> - Detector de fraude (GRATIS siempre)</li>
                <li>📊 <strong>Pulse IA</strong> - Análisis de sentimiento</li>
                <li>📈 <strong>Momentum Predictor IA</strong> - Señales de trading</li>
              </ul>
              <div className="bg-emerald-50 border border-emerald-200 rounded-lg p-4">
                <p className="font-semibold text-emerald-800 mb-2">💰 Precios:</p>
                <ul className="space-y-1">
                  <li>• Mensual: <strong>Gs. 0/mes</strong> (promoción lanzamiento)</li>
                  <li>• Anual: <strong>Gs. 600.000/año</strong></li>
                  <li>• Pago con BTC/ETH: <strong>Gs. 450.000/año</strong> (25% OFF)</li>
                </ul>
              </div>
            </div>
          )
        },
        {
          id: 'vincular-telegram',
          question: '🔗 ¿Cómo vinculo mi Telegram a los bots?',
          answer: (
            <div>
              <p className="mb-3">Es muy simple:</p>
              <ol className="list-decimal pl-6 space-y-2">
                <li>Busca el bot en Telegram (ej: @stopfraudebot)</li>
                <li>Presiona "START" o "/start"</li>
                <li>El bot te pedirá tu email registrado en GuaraniAppStore</li>
                <li>Ingresa tu email y ¡listo! Ya estás vinculado</li>
              </ol>
              <p className="mt-3 text-amber-600">
                ⚠️ Usa el mismo email con el que te registraste en guaraniappstore.com
              </p>
            </div>
          )
        },
        {
          id: 'analisis-guardados',
          question: '💾 ¿Los análisis se guardan? ¿Por cuánto tiempo?',
          answer: (
            <div>
              <p className="mb-3">Sí, todos tus análisis se guardan automáticamente:</p>
              <ul className="list-disc pl-6 space-y-2">
                <li>✅ Análisis de CryptoShield: <strong>30 días</strong></li>
                <li>✅ Datos de Pulse IA: <strong>90 días</strong></li>
                <li>✅ Señales de Momentum: <strong>180 días</strong></li>
              </ul>
              <p className="mt-3">
                Puedes acceder a tu historial completo desde tu <strong>Dashboard en guaraniappstore.com</strong>
              </p>
            </div>
          )
        },
        {
          id: 'usar-sin-registro',
          question: '👤 ¿Puedo usar los bots sin registrarme?',
          answer: (
            <div>
              <p className="mb-3">Sí y no, depende del bot:</p>
              <ul className="list-disc pl-6 space-y-2">
                <li>🛡️ <strong>CryptoShield IA</strong>: Puedes usarlo sin registro con funcionalidad limitada (5 análisis/día)</li>
                <li>📊 <strong>Pulse IA</strong>: Requiere registro (gratis durante promoción)</li>
                <li>📈 <strong>Momentum Predictor IA</strong>: Requiere registro</li>
              </ul>
              <p className="mt-3 text-emerald-600">
                💡 Te recomendamos registrarte para acceso ilimitado y guardar tu historial
              </p>
            </div>
          )
        }
      ]
    },
    automatizaciones: {
      title: '⚙️ Automatizaciones a Medida',
      icon: '⚙️',
      questions: [
        {
          id: 'automatizacion-personalizada',
          question: '🛠️ ¿Puedo solicitar una automatización personalizada?',
          answer: (
            <div>
              <p className="mb-3">¡Por supuesto! Nuestro equipo de 6 especialistas está listo para ayudarte:</p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 my-4">
                <div className="bg-blue-50 p-3 rounded-lg">
                  <p className="font-semibold">👨‍💼 Junior Cucurella</p>
                  <p className="text-sm text-gray-600">Automatizaciones empresariales</p>
                </div>
                <div className="bg-blue-50 p-3 rounded-lg">
                  <p className="font-semibold">👨‍💼 Jacinto Torrelavega</p>
                  <p className="text-sm text-gray-600">Automatizaciones de marketing</p>
                </div>
                <div className="bg-blue-50 p-3 rounded-lg">
                  <p className="font-semibold">👨‍💼 Alex Albiol</p>
                  <p className="text-sm text-gray-600">Automatizaciones de ventas</p>
                </div>
                <div className="bg-purple-50 p-3 rounded-lg">
                  <p className="font-semibold">👩‍💼 Silvia García</p>
                  <p className="text-sm text-gray-600">Automatizaciones de RRHH</p>
                </div>
                <div className="bg-purple-50 p-3 rounded-lg">
                  <p className="font-semibold">👩‍💼 Blanca García</p>
                  <p className="text-sm text-gray-600">Automatizaciones financieras</p>
                </div>
                <div className="bg-emerald-50 p-3 rounded-lg">
                  <p className="font-semibold">👩‍💼 Rocío Almeida</p>
                  <p className="text-sm text-gray-600">Chat general + ventas</p>
                </div>
              </div>
              <button 
                onClick={() => navigate('/dashboard')}
                className="w-full bg-emerald-600 text-white px-6 py-3 rounded-lg hover:bg-emerald-700 transition-colors font-semibold"
              >
                Hablar con un Agente
              </button>
            </div>
          )
        },
        {
          id: 'preconsultoria-gratis',
          question: '💬 ¿Cómo funciona la pre-consultoría gratuita?',
          answer: (
            <div>
              <p className="mb-3">Nuestra pre-consultoría es 100% gratuita y sin compromiso:</p>
              <ol className="list-decimal pl-6 space-y-2">
                <li>Chateas con uno de nuestros agentes (chat disponible desde tu dashboard)</li>
                <li>Explicas qué necesitas automatizar</li>
                <li>El agente evalúa la viabilidad y complejidad</li>
                <li>Recibes una estimación de tiempo y costo</li>
                <li>Decides si proceder o no</li>
              </ol>
              <p className="mt-3 text-emerald-600">
                ✅ Sin costo. Sin compromiso. Solo claridad sobre tu proyecto.
              </p>
            </div>
          )
        },
        {
          id: 'consultoria-pago',
          question: '💵 ¿Cuándo necesito una consultoría de pago?',
          answer: (
            <div>
              <p className="mb-3">La consultoría de pago (Gs. 750.000/mes) es necesaria cuando:</p>
              <ul className="list-disc pl-6 space-y-2">
                <li>✅ Tu proyecto requiere análisis técnico profundo (más de 2 horas)</li>
                <li>✅ Necesitas un plan de automatización detallado</li>
                <li>✅ Requieres arquitectura de sistemas complejos</li>
                <li>✅ Quieres sesiones de mentoría técnica continua</li>
                <li>✅ Necesitas auditoría de sistemas existentes</li>
              </ul>
              <p className="mt-3">
                💡 La pre-consultoría gratuita te ayudará a determinar si necesitas el servicio completo de consultoría.
              </p>
            </div>
          )
        },
        {
          id: 'info-automatizacion',
          question: '📋 ¿Qué información necesitan para mi automatización?',
          answer: (
            <div>
              <p className="mb-3">Para darte una propuesta precisa, necesitamos:</p>
              <ul className="list-disc pl-6 space-y-2">
                <li>✅ Descripción del proceso actual (manual)</li>
                <li>✅ Qué quieres automatizar específicamente</li>
                <li>✅ Volumen de operaciones (ej: 100 facturas/mes)</li>
                <li>✅ Sistemas actuales que usas (ej: Google Sheets, CRM, etc.)</li>
                <li>✅ Presupuesto aproximado (opcional)</li>
                <li>✅ Timeframe deseado</li>
              </ul>
              <p className="mt-3 text-gray-600">
                No te preocupes si no tienes toda la información. El agente te guiará en el proceso.
              </p>
            </div>
          )
        },
        {
          id: 'contacto-postconsultoria',
          question: '📞 ¿Cómo me contactan después de la pre-consultoría?',
          answer: (
            <div>
              <p className="mb-3">Después de la pre-consultoría, te contactamos por:</p>
              <ul className="list-disc pl-6 space-y-2">
                <li>✅ Email (admin@guaraniappstore.com)</li>
                <li>✅ WhatsApp (si proporcionaste tu número)</li>
                <li>✅ Telegram (si vinculaste tu cuenta)</li>
                <li>✅ Dashboard (notificaciones internas)</li>
              </ul>
              <p className="mt-3">
                <strong>Tiempo de respuesta:</strong> Máximo 24 horas hábiles
              </p>
            </div>
          )
        }
      ]
    },
    cuenta: {
      title: '👤 Cuenta y Suscripción',
      icon: '👤',
      questions: [
        {
          id: 'crear-cuenta',
          question: '📝 ¿Cómo creo una cuenta?',
          answer: (
            <div>
              <ol className="list-decimal pl-6 space-y-2">
                <li>Ve a <strong>guaraniappstore.com</strong></li>
                <li>Click en "Registrarse" o "Crear Cuenta"</li>
                <li>Completa el formulario (email, contraseña, nombre completo)</li>
                <li>Verifica tu email (revisa spam si no llega)</li>
                <li>¡Listo! Accede a tu dashboard</li>
              </ol>
              <p className="mt-3 text-emerald-600">
                🎁 Al registrarte, obtienes acceso GRATIS a CryptoShield IA inmediatamente
              </p>
            </div>
          )
        },
        {
          id: 'cambiar-cancelar-plan',
          question: '🔄 ¿Puedo cambiar de plan o cancelar?',
          answer: (
            <div>
              <p className="mb-3">Sí, tienes total flexibilidad:</p>
              <ul className="list-disc pl-6 space-y-2">
                <li>✅ <strong>Cambiar de plan:</strong> Desde tu dashboard, tab "Mis Servicios", botón "Cambiar Plan"</li>
                <li>✅ <strong>Upgrade:</strong> Efecto inmediato con prorrateo del pago</li>
                <li>✅ <strong>Downgrade:</strong> Toma efecto al final del período actual</li>
                <li>✅ <strong>Cancelar:</strong> Sin penalidades. Acceso hasta fin del período pagado</li>
              </ul>
              <p className="mt-3 text-amber-600">
                ⚠️ No hay reembolsos por períodos no utilizados, pero puedes usar el servicio hasta el final
              </p>
            </div>
          )
        },
        {
          id: 'metodos-pago',
          question: '💳 ¿Qué métodos de pago aceptan?',
          answer: (
            <div>
              <p className="mb-3">Aceptamos múltiples métodos de pago:</p>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div className="bg-blue-50 p-3 rounded-lg">
                  <p className="font-semibold mb-1">🇵🇾 Paraguay:</p>
                  <ul className="text-sm space-y-1">
                    <li>• Pagopar (tarjetas PYG)</li>
                    <li>• Bancard (débito/crédito)</li>
                  </ul>
                </div>
                <div className="bg-green-50 p-3 rounded-lg">
                  <p className="font-semibold mb-1">🌍 Internacional:</p>
                  <ul className="text-sm space-y-1">
                    <li>• PayPal</li>
                    <li>• 2Checkout</li>
                    <li>• Paymentwall</li>
                  </ul>
                </div>
                <div className="bg-amber-50 p-3 rounded-lg md:col-span-2">
                  <p className="font-semibold mb-1">
                    <img src="/assets/payment/bitcoin-logo.png" alt="Bitcoin" style={{width: '18px', height: '18px', display: 'inline-block', marginRight: '5px', verticalAlign: 'middle'}} />
                    Criptomonedas (25% OFF en planes anuales):
                  </p>
                  <ul className="text-sm space-y-1">
                    <li>• Bitcoin (BTC)</li>
                    <li>• Ethereum (ETH)</li>
                    <li>• USDT (Tether)</li>
                    <li>• Vía Leemon Squid</li>
                  </ul>
                </div>
              </div>
            </div>
          )
        },
        {
          id: 'descuentos',
          question: '🎁 ¿Hay descuentos disponibles?',
          answer: (
            <div>
              <p className="mb-3">¡Sí! Tenemos varios descuentos:</p>
              <ul className="list-disc pl-6 space-y-2">
                <li>💎 <strong>Plan Anual:</strong> 2 meses GRATIS (ahorra ~17%)</li>
                <li>
                  <img src="/assets/payment/bitcoin-logo.png" alt="Bitcoin" style={{width: '16px', height: '16px', display: 'inline-block', marginRight: '5px', verticalAlign: 'middle'}} />
                  <strong>Pago con Crypto:</strong> 25% OFF adicional en planes anuales
                </li>
                <li>📱 <strong>Telegram vs WhatsApp:</strong> 20% más barato si usas Telegram</li>
                <li>🎓 <strong>Estudiantes:</strong> 30% OFF (verificación requerida)</li>
                <li>🚀 <strong>Startups:</strong> 40% OFF primeros 3 meses (verificación requerida)</li>
              </ul>
              <p className="mt-3 text-emerald-600">
                💡 Los descuentos no son acumulables, se aplica el mayor
              </p>
            </div>
          )
        }
      ]
    },
    tecnico: {
      title: '🔧 Técnico',
      icon: '🔧',
      questions: [
        {
          id: 'bots-seguros',
          question: '🔒 ¿Los bots de Telegram son seguros?',
          answer: (
            <div>
              <p className="mb-3">¡Absolutamente! Seguridad es nuestra prioridad #1:</p>
              <ul className="list-disc pl-6 space-y-2">
                <li>✅ <strong>Encriptación end-to-end</strong> de Telegram</li>
                <li>✅ <strong>No guardamos tu contraseña</strong>, solo tu email de registro</li>
                <li>✅ <strong>Datos sensibles cifrados</strong> en nuestros servidores (AES-256)</li>
                <li>✅ <strong>Servidores en USA y Europa</strong> con certificaciones ISO 27001</li>
                <li>✅ <strong>Auditorías de seguridad</strong> trimestrales</li>
                <li>✅ <strong>No vendemos ni compartimos</strong> tus datos con terceros</li>
              </ul>
              <p className="mt-3 text-blue-600">
                🛡️ Los bots solo pueden leer mensajes que tú les envías directamente
              </p>
            </div>
          )
        },
        {
          id: 'uso-movil',
          question: '📱 ¿Puedo usar los servicios desde mi celular?',
          answer: (
            <div>
              <p className="mb-3">¡Sí! Todos nuestros servicios están optimizados para móvil:</p>
              <ul className="list-disc pl-6 space-y-2">
                <li>✅ <strong>Dashboard responsive</strong> - Se adapta a cualquier pantalla</li>
                <li>✅ <strong>Bots de Telegram</strong> - Nativamente móvil</li>
                <li>✅ <strong>WhatsApp Business</strong> - Disponible en celular</li>
                <li>✅ <strong>PWA (Progressive Web App)</strong> - Instala guaraniappstore.com como app</li>
              </ul>
              <p className="mt-3 text-gray-600">
                💡 Para mejor experiencia, recomendamos usar los bots de Telegram desde tu celular
              </p>
            </div>
          )
        },
        {
          id: 'limite-uso',
          question: '⚡ ¿Hay límite de uso en los servicios premium?',
          answer: (
            <div>
              <p className="mb-3">Depende del servicio:</p>
              <div className="space-y-3">
                <div className="bg-emerald-50 p-3 rounded-lg">
                  <p className="font-semibold mb-2">✅ Uso Ilimitado:</p>
                  <ul className="text-sm space-y-1">
                    <li>• CryptoShield IA (GRATIS)</li>
                    <li>• Pulse IA</li>
                    <li>• Momentum Predictor IA</li>
                    <li>• Asistente Personal</li>
                    <li>• Organizador de Agenda</li>
                  </ul>
                </div>
                <div className="bg-amber-50 p-3 rounded-lg">
                  <p className="font-semibold mb-2">📊 Límites Fair Use:</p>
                  <ul className="text-sm space-y-1">
                    <li>• Organizador de Facturas: 500 facturas/mes</li>
                    <li>• Preselección Curricular: 200 CVs/mes</li>
                    <li>• Generador de Blogs: 100 artículos/mes</li>
                  </ul>
                  <p className="text-xs mt-2 text-amber-800">
                    Si necesitas más, contáctanos para plan empresarial
                  </p>
                </div>
              </div>
            </div>
          )
        },
        {
          id: 'eliminar-datos',
          question: '🗑️ ¿Qué pasa con mis datos al eliminar mi cuenta?',
          answer: (
            <div>
              <p className="mb-3">Respetamos tu privacidad y derecho al olvido:</p>
              <ul className="list-disc pl-6 space-y-2">
                <li>✅ <strong>Eliminación inmediata:</strong> Tu cuenta se desactiva al instante</li>
                <li>✅ <strong>30 días de gracia:</strong> Puedes recuperar tu cuenta en este período</li>
                <li>✅ <strong>Eliminación permanente:</strong> Después de 30 días, todos tus datos se borran</li>
                <li>✅ <strong>Backups cifrados:</strong> Eliminados de nuestros backups en 90 días</li>
                <li>✅ <strong>Datos anónimos:</strong> Estadísticas agregadas (sin identificación) se conservan</li>
              </ul>
              <p className="mt-3 text-red-600">
                ⚠️ La eliminación es irreversible después de 30 días. Tus suscripciones se cancelan automáticamente.
              </p>
            </div>
          )
        }
      ]
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-emerald-600 via-emerald-700 to-teal-800 text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-5xl font-bold mb-6">
            ❓ Preguntas Frecuentes
          </h1>
          <p className="text-xl text-emerald-100 max-w-3xl mx-auto">
            Encuentra respuestas rápidas a las dudas más comunes sobre GuaraniAppStore
          </p>
        </div>
      </section>

      {/* Categories Navigation */}
      <section className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex overflow-x-auto space-x-4">
            {Object.keys(faqData).map((categoryKey) => (
              <button
                key={categoryKey}
                onClick={() => setOpenCategory(categoryKey)}
                className={`whitespace-nowrap px-6 py-3 rounded-lg font-medium transition-all ${
                  openCategory === categoryKey
                    ? 'bg-emerald-600 text-white shadow-lg'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {faqData[categoryKey].icon} {faqData[categoryKey].title}
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ Content */}
      <section className="py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="space-y-4">
            {faqData[openCategory].questions.map((item) => (
              <div
                key={item.id}
                className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden"
              >
                <button
                  onClick={() => toggleQuestion(item.id)}
                  className="w-full px-6 py-4 text-left flex justify-between items-center hover:bg-gray-50 transition-colors"
                >
                  <h3 className="text-lg font-semibold text-gray-900 pr-4">
                    {item.question}
                  </h3>
                  <span className="text-2xl text-emerald-600 flex-shrink-0">
                    {openQuestion === item.id ? '−' : '+'}
                  </span>
                </button>
                
                {openQuestion === item.id && (
                  <div className="px-6 py-4 border-t border-gray-100 bg-gray-50">
                    <div className="prose max-w-none text-gray-700">
                      {item.answer}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section className="bg-gradient-to-br from-emerald-600 to-teal-700 text-white py-16">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl font-bold mb-4">¿Aún tienes preguntas?</h2>
          <p className="text-xl text-emerald-100 mb-8">
            Chatea con nuestros agentes desde tu dashboard o contáctanos por email
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              onClick={() => navigate('/dashboard')}
              className="bg-white text-emerald-600 px-8 py-4 rounded-lg font-semibold hover:bg-emerald-50 transition-colors"
            >
              💬 Hablar con un Agente
            </button>
            <a
              href="mailto:admin@guaraniappstore.com"
              className="bg-emerald-700 text-white px-8 py-4 rounded-lg font-semibold hover:bg-emerald-800 transition-colors border-2 border-white"
            >
              📧 Enviar Email
            </a>
          </div>
          <p className="mt-6 text-emerald-100">
            admin@guaraniappstore.com
          </p>
        </div>
      </section>

      <Footer />
    </div>
  );
};

export default FAQ;
