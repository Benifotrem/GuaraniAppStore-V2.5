import React from 'react';
import './Hero.css';

const Hero = () => {
  return (
    <section className="hero" id="inicio" data-testid="hero-section">
      <div className="hero-background">
        <video 
          autoPlay 
          loop 
          muted 
          playsInline 
          className="hero-video"
          data-testid="hero-video"
        >
          <source src="/assets/videos/background.mp4" type="video/mp4" />
        </video>
        <div className="hero-overlay"></div>
      </div>

      <div className="hero-content">
        <h1 className="hero-title" data-testid="hero-title">
          Automatiza tu Negocio con <span className="gradient-text">Inteligencia Artificial</span>
        </h1>
        
        <p className="hero-subtitle" data-testid="hero-subtitle">
          Soluciones empresariales potenciadas por IA para aumentar tu productividad.
          <br />
          Bots de WhatsApp, Telegram, análisis de datos y más.
        </p>

        <div className="hero-actions">
          <button className="btn-hero-primary" data-testid="hero-cta-primary">
            Comenzar Trial Gratis (7 días)
          </button>
          <button className="btn-hero-secondary" data-testid="hero-cta-secondary">
            Ver Demo en Vivo
          </button>
        </div>

        <div className="hero-stats">
          <div className="stat-item" data-testid="stat-clients">
            <div className="stat-number">500+</div>
            <div className="stat-label">Clientes Activos</div>
          </div>
          <div className="stat-item" data-testid="stat-automation">
            <div className="stat-number">95%</div>
            <div className="stat-label">Automatización</div>
          </div>
          <div className="stat-item" data-testid="stat-support">
            <div className="stat-number">24/7</div>
            <div className="stat-label">Soporte IA</div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
