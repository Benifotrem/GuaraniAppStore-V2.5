import React from 'react';
import './Team.css';

const Team = () => {
  const teamMembers = [
    {
      name: 'Junior Cucurella',
      role: 'Gerente de Agendas',
      description: 'Gestiona completamente citas, reservas y recordatorios 24/7',
      image: '/assets/team/junior.png',
    },
    {
      name: 'Jacinto Torrelavega',
      role: 'Asistente de Flujos de Facturación',
      description: 'Automatiza flujos contables',
      image: '/assets/team/jacinto.png',
    },
    {
      name: 'Alex Albiol',
      role: 'Experto en Soporte Instantáneo',
      description: 'Respuestas rápidas y efectivas para tus clientes',
      image: '/assets/team/alex.png',
    },
    {
      name: 'Silvia Garcia',
      role: 'Puente de Integración Operativa',
      description: 'Conecta sistemas y optimiza procesos',
      image: '/assets/team/silvia.png',
    },
    {
      name: 'Blanca Garcia',
      role: 'Servicio RPA',
      description: 'Elimina el "copiar y pegar", automatizando la transferencia de datos entre plataformas no conectadas',
      image: '/assets/team/blanca.png',
    },
    {
      name: 'Rocío Almeida',
      role: 'Moderador de Reputación Online',
      description: 'Gestiona y protege tu imagen digital',
      image: '/assets/team/rocio.png',
    },
  ];

  return (
    <section className="team" id="equipo" data-testid="team-section">
      <div className="team-container">
        <div className="team-header">
          <h2 className="team-title" data-testid="team-title">
            Nuestro Equipo de Agentes IA
          </h2>
          <p className="team-subtitle" data-testid="team-subtitle">
            Expertos en automatización disponibles 24/7 para tu empresa
          </p>
        </div>

        <div className="team-image-full" data-testid="team-group-photo">
          <img 
            src="/assets/team/group.png" 
            alt="Equipo GuaraniAppStore" 
            className="group-photo"
          />
        </div>

        <div className="team-grid">
          {teamMembers.map((member, index) => (
            <div 
              key={index} 
              className="team-member-card" 
              data-testid={`team-member-${index}`}
            >
              <div className="member-image-container">
                <img 
                  src={member.image} 
                  alt={member.name}
                  className="member-image"
                  data-testid={`member-image-${index}`}
                />
              </div>
              <div className="member-info">
                <h3 className="member-name" data-testid={`member-name-${index}`}>
                  {member.name}
                </h3>
                <h4 className="member-role" data-testid={`member-role-${index}`}>
                  {member.role}
                </h4>
                <p className="member-description" data-testid={`member-desc-${index}`}>
                  {member.description}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Team;
