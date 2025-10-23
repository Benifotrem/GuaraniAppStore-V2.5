import React from 'react';
import './Services.css';

const Services = ({ services }) => {
  return (
    <section className="services" id="servicios" data-testid="services-section">
      <div className="services-container">
        <div className="services-header">
          <h2 className="services-title" data-testid="services-title">
            Nuestros Servicios
          </h2>
          <p className="services-subtitle" data-testid="services-subtitle">
            Soluciones personalizadas para cada necesidad empresarial
          </p>
        </div>

        <div className="services-grid">
          {services && services.length > 0 ? (
            services.map((service, index) => (
              <div 
                key={service.id} 
                className="service-card" 
                data-testid={`service-card-${index}`}
              >
                {service.status === 'COMING_SOON' && (
                  <div className="coming-soon-badge" data-testid={`badge-${index}`}>
                    PRÓXIMAMENTE
                  </div>
                )}
                
                <div className="service-icon" data-testid={`service-icon-${index}`}>
                  {service.icon}
                </div>
                
                <h3 className="service-name" data-testid={`service-name-${index}`}>
                  {service.name}
                </h3>
                
                <p className="service-short-desc" data-testid={`service-desc-${index}`}>
                  {service.short_description || service.description}
                </p>
                
                <div className="service-pricing" data-testid={`service-pricing-${index}`}>
                  <span className="price">${service.price_monthly}</span>
                  <span className="period">/mes</span>
                </div>
                
                {service.features && (
                  <ul className="service-features">
                    {service.features.slice(0, 3).map((feature, idx) => (
                      <li key={idx} data-testid={`service-feature-${index}-${idx}`}>
                        ✓ {feature}
                      </li>
                    ))}
                  </ul>
                )}
                
                <button 
                  className="btn-service" 
                  disabled={service.status === 'COMING_SOON'}
                  data-testid={`service-btn-${index}`}
                >
                  {service.status === 'COMING_SOON' ? 'Próximamente' : 'Más información'}
                </button>
              </div>
            ))
          ) : (
            <div className="services-loading" data-testid="services-loading">
              Cargando servicios...
            </div>
          )}
        </div>
      </div>
    </section>
  );
};

export default Services;
