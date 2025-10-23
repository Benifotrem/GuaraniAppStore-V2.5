import React from 'react';
import './Benefits.css';

const Benefits = () => {
  const benefits = [
    {
      icon: '⚡',
      title: 'Automatización 24/7',
      description: 'Bots que trabajan por ti mientras duermes. Respuestas instantáneas a clientes.',
    },
    {
      icon: '🛡️',
      title: 'Datos Seguros',
      description: 'Encriptación end-to-end. Cumplimiento GDPR.',
    },
    {
      icon: '📈',
      title: 'Crece sin Límites',
      description: 'Infraestructura que crece contigo. Sin costos ocultos.',
    },
  ];

  return (
    <section className="benefits" data-testid="benefits-section">
      <div className="benefits-container">
        <div className="benefits-grid">
          {benefits.map((benefit, index) => (
            <div 
              key={index} 
              className="benefit-card" 
              data-testid={`benefit-card-${index}`}
            >
              <div className="benefit-icon" data-testid={`benefit-icon-${index}`}>
                {benefit.icon}
              </div>
              <h3 className="benefit-title" data-testid={`benefit-title-${index}`}>
                {benefit.title}
              </h3>
              <p className="benefit-description" data-testid={`benefit-description-${index}`}>
                {benefit.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Benefits;
