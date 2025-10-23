import React from 'react';
import { useNavigate } from 'react-router-dom';
import './PrivacyPolicy.css';

const PrivacyPolicy = () => {
  const navigate = useNavigate();

  return (
    <div className="privacy-policy-page">
      {/* Header simple */}
      <header className="privacy-header">
        <div className="privacy-header-container">
          <button onClick={() => navigate('/')} className="back-button">
            ← Volver al inicio
          </button>
          <h1 className="privacy-title">Política de Privacidad</h1>
        </div>
      </header>

      {/* Contenido */}
      <main className="privacy-content">
        <div className="privacy-container">
          <p className="privacy-date">Última actualización: {new Date().toLocaleDateString('es-ES', { year: 'numeric', month: 'long', day: 'numeric' })}</p>

          <section className="privacy-section">
            <h2>1. Introducción</h2>
            <p>
              En GuaraniAppStore ("nosotros", "nuestro" o "la empresa"), nos comprometemos a proteger y respetar tu privacidad. 
              Esta Política de Privacidad explica cómo recopilamos, usamos, compartimos y protegemos tu información personal 
              cuando utilizas nuestros servicios de automatización e inteligencia artificial.
            </p>
            <p>
              Al usar nuestros servicios, aceptas la recopilación y el uso de información de acuerdo con esta política.
            </p>
          </section>

          <section className="privacy-section">
            <h2>2. Información que Recopilamos</h2>
            
            <h3>2.1 Información que proporcionas directamente</h3>
            <ul>
              <li><strong>Datos de registro:</strong> Nombre completo, correo electrónico, país, contraseña (encriptada)</li>
              <li><strong>Información de pago:</strong> Datos de facturación procesados de manera segura a través de pasarelas de pago certificadas (PCI-DSS)</li>
              <li><strong>Contenido del usuario:</strong> Datos que compartes al usar nuestros servicios de IA (consultas, documentos, imágenes)</li>
              <li><strong>Comunicaciones:</strong> Mensajes que envías a través de chat, email o soporte técnico</li>
            </ul>

            <h3>2.2 Información recopilada automáticamente</h3>
            <ul>
              <li><strong>Datos de uso:</strong> Interacciones con nuestros servicios, funciones utilizadas, tiempo de uso</li>
              <li><strong>Información técnica:</strong> Dirección IP, tipo de navegador, sistema operativo, identificadores de dispositivo</li>
              <li><strong>Cookies y tecnologías similares:</strong> Para mejorar la experiencia del usuario y analizar el uso del servicio</li>
            </ul>

            <h3>2.3 Integraciones de terceros</h3>
            <p>
              Si conectas servicios de terceros (Google Calendar, Google Sheets, etc.), podemos acceder a la información 
              necesaria para proporcionar la funcionalidad solicitada, siempre con tu autorización explícita.
            </p>
          </section>

          <section className="privacy-section">
            <h2>3. Cómo Usamos tu Información</h2>
            <p>Utilizamos la información recopilada para:</p>
            <ul>
              <li>✅ Proporcionar, mantener y mejorar nuestros servicios de IA</li>
              <li>✅ Procesar pagos y gestionar suscripciones</li>
              <li>✅ Personalizar tu experiencia y ofrecer contenido relevante</li>
              <li>✅ Enviar notificaciones importantes sobre tu cuenta y servicios</li>
              <li>✅ Proporcionar soporte técnico y responder a tus consultas</li>
              <li>✅ Detectar, prevenir y abordar problemas técnicos y de seguridad</li>
              <li>✅ Cumplir con obligaciones legales y regulatorias</li>
              <li>✅ Realizar análisis internos para mejorar nuestros productos</li>
            </ul>
          </section>

          <section className="privacy-section">
            <h2>4. Base Legal para el Procesamiento</h2>
            <p>Procesamos tus datos personales bajo las siguientes bases legales:</p>
            <ul>
              <li><strong>Ejecución de contrato:</strong> Para proporcionar los servicios que has solicitado</li>
              <li><strong>Consentimiento:</strong> Cuando has dado tu consentimiento explícito</li>
              <li><strong>Interés legítimo:</strong> Para mejorar nuestros servicios y detectar fraudes</li>
              <li><strong>Cumplimiento legal:</strong> Cuando la ley lo requiera</li>
            </ul>
          </section>

          <section className="privacy-section">
            <h2>5. Compartir Información</h2>
            <p>No vendemos tu información personal. Podemos compartir información con:</p>
            
            <h3>5.1 Proveedores de servicios</h3>
            <p>
              Compartimos datos con proveedores que nos ayudan a operar nuestro negocio:
            </p>
            <ul>
              <li>🔒 Proveedores de infraestructura en la nube (AWS, Google Cloud)</li>
              <li>🔒 Procesadores de pagos (Pagopar, PayPal, Stripe)</li>
              <li>🔒 Servicios de IA y machine learning (OpenAI, Anthropic)</li>
              <li>🔒 Herramientas de análisis y monitoreo</li>
            </ul>
            <p className="highlight-box">
              Todos nuestros proveedores están obligados contractualmente a proteger tu información y solo pueden usarla 
              para los propósitos específicos que les autorizamos.
            </p>

            <h3>5.2 Cumplimiento legal</h3>
            <p>
              Podemos divulgar tu información si es requerido por ley o en respuesta a solicitudes válidas de autoridades públicas.
            </p>

            <h3>5.3 Transferencias empresariales</h3>
            <p>
              En caso de fusión, adquisición o venta de activos, tu información puede ser transferida al nuevo propietario.
            </p>
          </section>

          <section className="privacy-section">
            <h2>6. Seguridad de los Datos</h2>
            <p>Implementamos medidas de seguridad técnicas y organizativas para proteger tu información:</p>
            <ul>
              <li>🔐 Encriptación de datos en tránsito (TLS/SSL) y en reposo</li>
              <li>🔐 Autenticación de dos factores (2FA) disponible</li>
              <li>🔐 Acceso restringido a datos personales (principio de necesidad de conocer)</li>
              <li>🔐 Auditorías de seguridad regulares</li>
              <li>🔐 Monitoreo continuo de amenazas</li>
              <li>🔐 Copias de seguridad cifradas y redundantes</li>
            </ul>
            <p className="highlight-box">
              Ningún sistema es 100% seguro. Si detectas alguna vulnerabilidad, por favor contáctanos inmediatamente 
              en <a href="mailto:privacy@guaraniappstore.com">privacy@guaraniappstore.com</a>
            </p>
          </section>

          <section className="privacy-section">
            <h2>7. Retención de Datos</h2>
            <p>
              Conservamos tu información personal solo durante el tiempo necesario para cumplir con los propósitos descritos 
              en esta política:
            </p>
            <ul>
              <li><strong>Datos de cuenta activa:</strong> Mientras tu cuenta esté activa</li>
              <li><strong>Datos de conversación:</strong> 30 días después de la última interacción</li>
              <li><strong>Datos de facturación:</strong> Según lo requiera la legislación fiscal (generalmente 5-10 años)</li>
              <li><strong>Logs técnicos:</strong> 90 días para seguridad y troubleshooting</li>
            </ul>
            <p>
              Después de estos períodos, eliminamos o anonimizamos tu información de manera segura.
            </p>
          </section>

          <section className="privacy-section">
            <h2>8. Tus Derechos</h2>
            <p>Tienes los siguientes derechos sobre tu información personal:</p>
            <ul>
              <li>📋 <strong>Acceso:</strong> Solicitar una copia de tus datos personales</li>
              <li>✏️ <strong>Rectificación:</strong> Corregir datos inexactos o incompletos</li>
              <li>🗑️ <strong>Eliminación:</strong> Solicitar la eliminación de tus datos ("derecho al olvido")</li>
              <li>🔒 <strong>Restricción:</strong> Limitar el procesamiento de tus datos</li>
              <li>📤 <strong>Portabilidad:</strong> Recibir tus datos en formato estructurado y portable</li>
              <li>🚫 <strong>Oposición:</strong> Oponerte al procesamiento de tus datos en ciertas circunstancias</li>
              <li>⚖️ <strong>Retirar consentimiento:</strong> Cuando el procesamiento se base en tu consentimiento</li>
            </ul>
            <p className="highlight-box">
              Para ejercer cualquiera de estos derechos, contáctanos en <a href="mailto:privacy@guaraniappstore.com">privacy@guaraniappstore.com</a>. 
              Responderemos a tu solicitud dentro de 30 días.
            </p>
          </section>

          <section className="privacy-section">
            <h2>9. Cookies y Tecnologías de Rastreo</h2>
            <p>Utilizamos cookies y tecnologías similares para:</p>
            <ul>
              <li>🍪 Mantener tu sesión iniciada</li>
              <li>🍪 Recordar tus preferencias</li>
              <li>🍪 Analizar el uso de nuestros servicios</li>
              <li>🍪 Mejorar la seguridad</li>
            </ul>
            <p>
              Puedes controlar las cookies a través de la configuración de tu navegador. Sin embargo, deshabilitar cookies 
              puede afectar la funcionalidad de nuestros servicios.
            </p>
          </section>

          <section className="privacy-section">
            <h2>10. Privacidad de Menores</h2>
            <p>
              Nuestros servicios no están dirigidos a menores de 18 años. No recopilamos intencionalmente información 
              personal de menores. Si descubrimos que hemos recopilado datos de un menor sin el consentimiento parental 
              verificable, eliminaremos esa información de inmediato.
            </p>
          </section>

          <section className="privacy-section">
            <h2>11. Transferencias Internacionales</h2>
            <p>
              Tu información puede ser transferida y procesada en países fuera de tu país de residencia. Cuando transferimos 
              datos internacionalmente, implementamos salvaguardas apropiadas, incluyendo:
            </p>
            <ul>
              <li>Cláusulas contractuales estándar aprobadas</li>
              <li>Certificaciones de Privacy Shield (cuando aplique)</li>
              <li>Medidas de seguridad adicionales</li>
            </ul>
          </section>

          <section className="privacy-section">
            <h2>12. Cambios a esta Política</h2>
            <p>
              Podemos actualizar esta Política de Privacidad periódicamente. Te notificaremos sobre cambios significativos 
              publicando la nueva política en esta página y actualizando la fecha de "Última actualización".
            </p>
            <p>
              Te recomendamos revisar esta política regularmente para estar informado sobre cómo protegemos tu información.
            </p>
          </section>

          <section className="privacy-section">
            <h2>13. Contacto</h2>
            <p>Si tienes preguntas, comentarios o inquietudes sobre esta Política de Privacidad, puedes contactarnos:</p>
            <div className="contact-info">
              <p>📧 <strong>Email:</strong> <a href="mailto:privacy@guaraniappstore.com">privacy@guaraniappstore.com</a></p>
              <p>🏢 <strong>Empresa:</strong> GuaraniAppStore</p>
              <p>🌎 <strong>País:</strong> Paraguay</p>
            </div>
          </section>

          <section className="privacy-section">
            <h2>14. Autoridad de Protección de Datos</h2>
            <p>
              Si consideras que no hemos manejado tu información personal de acuerdo con esta política o la ley aplicable, 
              tienes derecho a presentar una queja ante la autoridad de protección de datos de tu jurisdicción.
            </p>
          </section>
        </div>
      </main>

      {/* Footer simple */}
      <footer className="privacy-footer">
        <div className="privacy-footer-container">
          <p>© {new Date().getFullYear()} GuaraniAppStore. Todos los derechos reservados.</p>
          <div className="footer-links">
            <button onClick={() => navigate('/terms')} className="footer-link">Términos y Condiciones</button>
            <span className="separator">•</span>
            <button onClick={() => navigate('/')} className="footer-link">Inicio</button>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default PrivacyPolicy;
