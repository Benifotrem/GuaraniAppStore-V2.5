import React from 'react';
import { useNavigate } from 'react-router-dom';
import './TermsConditions.css';

const TermsConditions = () => {
  const navigate = useNavigate();

  return (
    <div className="terms-page">
      {/* Header */}
      <header className="terms-header">
        <div className="terms-header-container">
          <button onClick={() => navigate('/')} className="back-button">
            ← Volver al inicio
          </button>
          <h1 className="terms-title">Términos y Condiciones</h1>
        </div>
      </header>

      {/* Contenido */}
      <main className="terms-content">
        <div className="terms-container">
          <p className="terms-date">Última actualización: {new Date().toLocaleDateString('es-ES', { year: 'numeric', month: 'long', day: 'numeric' })}</p>
          <p className="terms-subtitle">Propiedad de: César Ruzafa Alberola</p>

          <section className="terms-section">
            <h2>1. Aceptación de los Términos</h2>
            <p>
              Bienvenido a GuaraniAppStore. Al acceder y usar nuestro sitio web y servicios, aceptas estar sujeto a estos 
              Términos y Condiciones, así como a nuestra Política de Privacidad. Si no estás de acuerdo con alguna parte 
              de estos términos, no debes usar nuestros servicios.
            </p>
          </section>

          <section className="terms-section">
            <h2>2. Descripción de los Servicios</h2>
            <p>
              GuaraniAppStore ofrece una plataforma de servicios de automatización e inteligencia artificial, incluyendo pero no limitado a:
            </p>
            <ul>
              <li>🤖 Consultoría técnica especializada en IA</li>
              <li>📝 Generación automática de contenido con IA</li>
              <li>📊 Herramientas de prospección comercial</li>
              <li>📧 Gestión inteligente de emails</li>
              <li>💼 Análisis automatizado de CVs</li>
              <li>🧾 Procesamiento de facturas con OCR</li>
              <li>📅 Sistema de agendamiento inteligente</li>
              <li>🤵 Asistente virtual para directivos</li>
              <li>📱 Análisis de redes sociales</li>
              <li>💬 Chatbots para WhatsApp y Telegram</li>
              <li>₿ Suite completa de servicios crypto</li>
            </ul>
          </section>

          <section className="terms-section">
            <h2>3. Registro y Cuenta de Usuario</h2>
            
            <h3>3.1 Requisitos</h3>
            <ul>
              <li>Debes tener al menos 18 años para crear una cuenta</li>
              <li>Debes proporcionar información precisa y completa durante el registro</li>
              <li>Eres responsable de mantener la confidencialidad de tu contraseña</li>
              <li>Debes notificar inmediatamente cualquier uso no autorizado de tu cuenta</li>
            </ul>

            <h3>3.2 Trial Gratuito</h3>
            <p>
              Ofrecemos un período de prueba gratuito de 7 días para nuevos usuarios. Al finalizar el trial, 
              se te cobrará automáticamente la tarifa de suscripción seleccionada, a menos que canceles antes 
              de que termine el período de prueba.
            </p>
          </section>

          <section className="terms-section">
            <h2>4. Planes y Pagos</h2>
            
            <h3>4.1 Suscripciones</h3>
            <ul>
              <li><strong>Plan Mensual:</strong> Pago recurrente mensual</li>
              <li><strong>Plan Anual:</strong> Pago anual con 2 meses gratis (ahorro del ~17%)</li>
              <li><strong>Plan Personalizado:</strong> Soluciones a medida para empresas</li>
            </ul>

            <h3>4.2 Métodos de Pago</h3>
            <p>Aceptamos los siguientes métodos de pago:</p>
            <ul>
              <li>💳 Tarjetas de crédito y débito (Visa, Mastercard, American Express)</li>
              <li>🏦 Transferencia bancaria (Pagopar, Bancard)</li>
              <li>🌐 PayPal, Stripe, Paymentwall</li>
              <li>₿ Criptomonedas (Bitcoin, Ethereum, USDT) - 25% OFF en planes anuales</li>
            </ul>

            <h3>4.3 Facturación</h3>
            <ul>
              <li>Los pagos se procesan de forma segura a través de pasarelas certificadas PCI-DSS</li>
              <li>Las suscripciones se renuevan automáticamente al final de cada período</li>
              <li>Recibirás un recordatorio por email 7 días antes de la renovación</li>
              <li>Todas las tarifas están sujetas a impuestos aplicables</li>
            </ul>

            <h3>4.4 Cambios de Precio</h3>
            <p>
              Nos reservamos el derecho de modificar nuestras tarifas. Te notificaremos con al menos 30 días de 
              anticipación sobre cualquier cambio de precio. Los cambios no afectarán el período de facturación actual.
            </p>
          </section>

          <section className="terms-section">
            <h2>5. Política de Cancelación y Reembolsos</h2>
            
            <h3>5.1 Cancelación</h3>
            <ul>
              <li>Puedes cancelar tu suscripción en cualquier momento desde tu panel de control</li>
              <li>La cancelación será efectiva al final del período de facturación actual</li>
              <li>No se realizan reembolsos por cancelaciones anticipadas de planes anuales</li>
            </ul>

            <h3>5.2 Garantía de Satisfacción (30 días)</h3>
            <p className="highlight-box">
              Ofrecemos una garantía de satisfacción de 30 días para nuevos clientes. Si no estás completamente 
              satisfecho con nuestros servicios durante los primeros 30 días, contáctanos en 
              <a href="mailto:privacy@guaraniappstore.com"> privacy@guaraniappstore.com</a> y procesaremos 
              un reembolso completo.
            </p>

            <h3>5.3 Reembolsos por Problemas Técnicos</h3>
            <p>
              Si experimentas interrupciones prolongadas del servicio (más de 48 horas continuas), puedes solicitar 
              un reembolso proporcional por el tiempo de inactividad.
            </p>
          </section>

          <section className="terms-section">
            <h2>6. Uso Aceptable de los Servicios</h2>
            
            <h3>6.1 Está Permitido</h3>
            <ul>
              <li>✅ Usar los servicios para fines comerciales legítimos</li>
              <li>✅ Integrar nuestras APIs en tus aplicaciones (según plan contratado)</li>
              <li>✅ Compartir contenido generado por IA, siempre que respetes derechos de terceros</li>
            </ul>

            <h3>6.2 Está Prohibido</h3>
            <ul>
              <li>❌ Realizar ingeniería inversa o intentar acceder al código fuente</li>
              <li>❌ Revender o redistribuir nuestros servicios sin autorización</li>
              <li>❌ Usar los servicios para actividades ilegales, fraudulentas o dañinas</li>
              <li>❌ Generar contenido que viole derechos de propiedad intelectual</li>
              <li>❌ Enviar spam, malware o contenido malicioso</li>
              <li>❌ Intentar sobrecargar o interrumpir nuestros servidores</li>
              <li>❌ Compartir tu cuenta con terceros no autorizados</li>
            </ul>

            <h3>6.3 Consecuencias del Mal Uso</h3>
            <p>
              El incumplimiento de estas políticas puede resultar en:
            </p>
            <ul>
              <li>Suspensión temporal de la cuenta</li>
              <li>Terminación permanente del servicio sin reembolso</li>
              <li>Acciones legales cuando corresponda</li>
            </ul>
          </section>

          <section className="terms-section">
            <h2>7. Propiedad Intelectual</h2>
            
            <h3>7.1 Derechos de GuaraniAppStore</h3>
            <p>
              Todo el contenido, diseño, código, marcas y logos de GuaraniAppStore son propiedad exclusiva de 
              César Ruzafa Alberola y están protegidos por leyes de propiedad intelectual internacionales.
            </p>

            <h3>7.2 Contenido Generado por IA</h3>
            <ul>
              <li>El contenido que generes usando nuestros servicios de IA es de tu propiedad</li>
              <li>GuaraniAppStore no reclama derechos sobre el contenido generado</li>
              <li>Eres responsable de asegurar que el contenido no infrinja derechos de terceros</li>
            </ul>

            <h3>7.3 Licencia de Uso</h3>
            <p>
              Te otorgamos una licencia limitada, no exclusiva, no transferible para usar nuestros servicios 
              según estos términos. Esta licencia termina cuando finaliza tu suscripción.
            </p>
          </section>

          <section className="terms-section">
            <h2>8. Limitación de Responsabilidad</h2>
            <p className="highlight-box">
              GuaraniAppStore proporciona los servicios "tal cual" y "según disponibilidad". No garantizamos 
              que los servicios serán ininterrumpidos o libres de errores.
            </p>

            <h3>8.1 Exclusión de Garantías</h3>
            <p>
              En la máxima medida permitida por la ley, excluimos todas las garantías, ya sean expresas o implícitas, 
              incluyendo pero no limitado a garantías de comerciabilidad o idoneidad para un propósito particular.
            </p>

            <h3>8.2 Límite de Daños</h3>
            <p>
              En ningún caso GuaraniAppStore será responsable por daños indirectos, incidentales, especiales, 
              consecuenciales o punitivos, o por pérdida de beneficios, ingresos, datos o uso.
            </p>
            <p>
              Nuestra responsabilidad total no excederá la cantidad que hayas pagado por el servicio en los 
              últimos 12 meses.
            </p>
          </section>

          <section className="terms-section">
            <h2>9. Privacidad y Protección de Datos</h2>
            <p>
              El uso de nuestros servicios también está regido por nuestra 
              <button onClick={() => navigate('/privacy')} className="inline-link"> Política de Privacidad</button>, 
              que describe cómo recopilamos, usamos y protegemos tu información personal.
            </p>
            <p>
              Al usar GuaraniAppStore, consientes la recopilación y uso de tu información según lo descrito 
              en nuestra Política de Privacidad.
            </p>
          </section>

          <section className="terms-section">
            <h2>10. Modificaciones a los Términos</h2>
            <p>
              Nos reservamos el derecho de modificar estos Términos y Condiciones en cualquier momento. 
              Las modificaciones serán efectivas inmediatamente después de su publicación en nuestro sitio web.
            </p>
            <p>
              Te notificaremos sobre cambios significativos por email o mediante un aviso prominente en el sitio. 
              El uso continuado de los servicios después de las modificaciones constituye tu aceptación de los nuevos términos.
            </p>
          </section>

          <section className="terms-section">
            <h2>11. Terminación</h2>
            
            <h3>11.1 Terminación por tu Parte</h3>
            <p>
              Puedes terminar tu cuenta en cualquier momento cancelando tu suscripción desde tu panel de control.
            </p>

            <h3>11.2 Terminación por Nuestra Parte</h3>
            <p>
              Podemos suspender o terminar tu acceso a los servicios inmediatamente, sin previo aviso, si:
            </p>
            <ul>
              <li>Violas estos Términos y Condiciones</li>
              <li>Tu pago es rechazado o fraudulento</li>
              <li>Usas los servicios de manera que cause daño a otros usuarios o a nosotros</li>
              <li>Lo requiera la ley o una orden judicial</li>
            </ul>

            <h3>11.3 Efectos de la Terminación</h3>
            <ul>
              <li>Perderás acceso inmediato a todos los servicios</li>
              <li>Tus datos serán eliminados según nuestra Política de Retención de Datos (30 días para mensajes)</li>
              <li>No se realizarán reembolsos por terminaciones por incumplimiento</li>
            </ul>
          </section>

          <section className="terms-section">
            <h2>12. Indemnización</h2>
            <p>
              Aceptas indemnizar y mantener indemne a GuaraniAppStore, sus directores, empleados y afiliados, 
              de cualquier reclamo, daño, pérdida, responsabilidad y gastos (incluyendo honorarios de abogados) 
              que surjan de:
            </p>
            <ul>
              <li>Tu uso de los servicios</li>
              <li>Tu violación de estos términos</li>
              <li>Tu violación de cualquier ley o derechos de terceros</li>
            </ul>
          </section>

          <section className="terms-section">
            <h2>13. Ley Aplicable y Jurisdicción</h2>
            <p>
              Estos Términos y Condiciones se regirán e interpretarán de acuerdo con las leyes de Paraguay, 
              sin considerar sus disposiciones sobre conflictos de leyes.
            </p>
            <p>
              Cualquier disputa que surja de o relacionada con estos términos será sometida a la jurisdicción 
              exclusiva de los tribunales de Paraguay.
            </p>
          </section>

          <section className="terms-section">
            <h2>14. Resolución de Disputas</h2>
            
            <h3>14.1 Negociación Informal</h3>
            <p>
              En caso de disputa, ambas partes acuerdan primero intentar resolver el problema mediante negociación 
              informal durante un período de al menos 30 días.
            </p>

            <h3>14.2 Mediación</h3>
            <p>
              Si la negociación informal no resuelve la disputa, las partes acuerdan someterse a mediación antes 
              de iniciar cualquier procedimiento legal.
            </p>
          </section>

          <section className="terms-section">
            <h2>15. Disposiciones Generales</h2>
            
            <h3>15.1 Acuerdo Completo</h3>
            <p>
              Estos Términos y Condiciones, junto con nuestra Política de Privacidad, constituyen el acuerdo 
              completo entre tú y GuaraniAppStore con respecto al uso de nuestros servicios.
            </p>

            <h3>15.2 Divisibilidad</h3>
            <p>
              Si alguna disposición de estos términos se considera inválida o inaplicable, las demás disposiciones 
              seguirán en pleno vigor y efecto.
            </p>

            <h3>15.3 Renuncia</h3>
            <p>
              La falta de ejercicio de cualquier derecho o disposición de estos términos no constituirá una renuncia 
              a dicho derecho o disposición.
            </p>

            <h3>15.4 Cesión</h3>
            <p>
              No puedes ceder o transferir estos términos o tu cuenta sin nuestro consentimiento previo por escrito. 
              Podemos ceder estos términos sin restricciones.
            </p>
          </section>

          <section className="terms-section">
            <h2>16. Contacto</h2>
            <p>Si tienes preguntas sobre estos Términos y Condiciones, puedes contactarnos:</p>
            <div className="contact-info">
              <p>📧 <strong>Email:</strong> <a href="mailto:privacy@guaraniappstore.com">privacy@guaraniappstore.com</a></p>
              <p>🏢 <strong>Propietario:</strong> César Ruzafa Alberola</p>
              <p>🌐 <strong>Sitio web:</strong> <a href="https://guaraniappstore.com">https://guaraniappstore.com</a></p>
              <p>🌎 <strong>País:</strong> Paraguay</p>
            </div>
          </section>

          <section className="terms-section">
            <p className="highlight-box">
              <strong>Al usar GuaraniAppStore, confirmas que has leído, entendido y aceptado estos Términos y Condiciones 
              en su totalidad.</strong>
            </p>
          </section>
        </div>
      </main>

      {/* Footer */}
      <footer className="terms-footer">
        <div className="terms-footer-container">
          <p>© {new Date().getFullYear()} GuaraniAppStore. Todos los derechos reservados.</p>
          <div className="footer-links">
            <button onClick={() => navigate('/privacy')} className="footer-link">Política de Privacidad</button>
            <span className="separator">•</span>
            <button onClick={() => navigate('/')} className="footer-link">Inicio</button>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default TermsConditions;
