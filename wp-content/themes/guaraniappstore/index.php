<?php get_header(); ?>

<!-- Hero Section con Video Background -->
<section class="hero-section" id="inicio">
    <!-- Video Background -->
    <div class="video-background">
        <video autoplay loop muted playsinline>
            <source src="<?php echo get_template_directory_uri(); ?>/assets/videos/background.mp4" type="video/mp4">
        </video>
        <div class="video-overlay"></div>
    </div>

    <!-- Hero Content -->
    <div class="hero-content animate-fade-in-up">
        <h1 class="hero-title text-shadow-strong">
            Automatiza tu Empresa<br>
            <span class="gradient-text">con Soluciones Inteligentes</span>
        </h1>

        <p class="hero-subtitle text-shadow">
            Desde contabilizar facturas a partir de una foto o pdf, pasando por prospección de leads, hasta agentes de ventas 24/7. Transforma tu negocio con automatización avanzada.
        </p>

        <!-- Trial Banner -->
        <div class="trial-banner">
            <h3>
                <span style="font-size: 1.875rem;">🎁</span>
                ¡Trial Gratuito de 7 Días!
            </h3>
            <p>
                Prueba <strong>cualquier servicio sin tarjeta de crédito</strong>
            </p>
            <p class="trial-features">
                ✓ Sin compromiso &nbsp;|&nbsp; ✓ Cancela cuando quieras &nbsp;|&nbsp; ✓ Full acceso
            </p>
        </div>

        <!-- Crypto Banner -->
        <div class="crypto-banner">
            <h4>⚡ Servicios para inversores en criptomonedas</h4>
            <p>
                Regístrate hoy y obtén nuestro <strong>Escáner de Fraude CryptoShield IA GRATIS... para siempre</strong>
            </p>
            <p class="crypto-discount">
                🪙 25% OFF en planes anuales pagando con BTC/ETH
            </p>
        </div>

        <!-- Hero Actions -->
        <div class="hero-actions">
            <a href="#trial" class="btn-primary">
                Comenzar Trial Gratis (7 días)
            </a>
            <a href="#contact" class="btn-secondary">
                💬 Hablar con Asistente
            </a>
        </div>
    </div>
</section>

<!-- Features Section -->
<section class="features-section section">
    <div class="container">
        <h2 class="section-title text-shadow-strong">¿Por qué elegirnos?</h2>

        <div class="features-grid">
            <?php
            $features = guaraniappstore_get_services();
            foreach ($features as $feature) :
            ?>
                <div class="feature-card service-card">
                    <div class="service-icon">
                        <?php echo $feature['icon']; ?>
                    </div>
                    <h3 class="service-title"><?php echo esc_html($feature['title']); ?></h3>
                    <p class="service-description"><?php echo esc_html($feature['description']); ?></p>
                </div>
            <?php endforeach; ?>
        </div>
    </div>
</section>

<!-- Services Section -->
<section class="services-section section" id="servicios">
    <div class="container">
        <h2 class="section-title text-shadow-strong">Servicios de Automatización</h2>
        <p class="section-subtitle text-shadow">Comienza desde Gs. 99.000/mes</p>

        <div class="services-grid">
            <!-- Agente de Ventas IA -->
            <div class="service-card">
                <div class="service-icon">🤖</div>
                <h3 class="service-title">Agente de Ventas IA</h3>
                <p class="service-description">
                    Cierra ventas 24/7 vía WhatsApp o Telegram con respuestas personalizadas y seguimiento automático.
                </p>
                <ul class="service-features">
                    <li>Respuestas personalizadas automáticas</li>
                    <li>Seguimiento inteligente de leads</li>
                    <li>Integración con CRM</li>
                    <li>Análisis de conversaciones</li>
                </ul>
                <button class="service-btn">Suscribirse</button>
            </div>

            <!-- Organizador de Facturas -->
            <div class="service-card">
                <div class="service-icon">📊</div>
                <h3 class="service-title">Organizador de Facturas</h3>
                <p class="service-description">
                    Sube fotos o PDFs de facturas y automatiza tu contabilidad completamente.
                </p>
                <ul class="service-features">
                    <li>Extracción automática de datos</li>
                    <li>Categorización inteligente</li>
                    <li>Reportes automáticos</li>
                    <li>Integración contable</li>
                </ul>
                <button class="service-btn">Suscribirse</button>
            </div>

            <!-- Prospección Comercial -->
            <div class="service-card">
                <div class="service-icon">🎯</div>
                <h3 class="service-title">Prospección Comercial</h3>
                <p class="service-description">
                    Encuentra leads calificados en Google Maps con datos completos y mensajes personalizados.
                </p>
                <ul class="service-features">
                    <li>Búsqueda automática de leads</li>
                    <li>Datos de contacto verificados</li>
                    <li>Mensajes Ice Breaker</li>
                    <li>5 leads gratis de prueba</li>
                </ul>
                <button class="service-btn">Suscribirse</button>
            </div>

            <!-- Asistente para Directivos -->
            <div class="service-card">
                <div class="service-icon">💼</div>
                <h3 class="service-title">Asistente para Directivos</h3>
                <p class="service-description">
                    IA ejecutiva que analiza datos, genera informes y te ayuda en decisiones estratégicas.
                </p>
                <ul class="service-features">
                    <li>Análisis de KPIs en tiempo real</li>
                    <li>Informes ejecutivos automáticos</li>
                    <li>Predicciones y recomendaciones</li>
                    <li>Dashboard personalizado</li>
                </ul>
                <button class="service-btn">Suscribirse</button>
            </div>

            <!-- Suite Crypto -->
            <div class="service-card">
                <div class="service-icon">₿</div>
                <h3 class="service-title">Suite Crypto</h3>
                <p class="service-description">
                    3 herramientas para inversores: Escáner de fraude, Análisis técnico y Análisis de sentimiento.
                </p>
                <ul class="service-features">
                    <li>CryptoShield - Detector de fraudes (GRATIS)</li>
                    <li>Momentum - Análisis técnico avanzado</li>
                    <li>Pulse - Análisis de sentimiento</li>
                    <li>25% OFF pagando con BTC/ETH</li>
                </ul>
                <button class="service-btn">Suscribirse</button>
            </div>

            <!-- Generador de Blogs -->
            <div class="service-card">
                <div class="service-icon">✍️</div>
                <h3 class="service-title">Generador de Blogs</h3>
                <p class="service-description">
                    Crea artículos optimizados para SEO automáticamente con IA de última generación.
                </p>
                <ul class="service-features">
                    <li>Artículos SEO-optimizados</li>
                    <li>Publicación automática</li>
                    <li>Múltiples idiomas</li>
                    <li>Análisis de keywords</li>
                </ul>
                <button class="service-btn">Suscribirse</button>
            </div>
        </div>
    </div>
</section>

<!-- Team Section -->
<section class="team-section section" id="equipo">
    <div class="container">
        <h2 class="section-title text-shadow-strong">Nuestro Equipo de Agentes IA</h2>
        <p class="section-subtitle text-shadow">
            Conoce a los agentes especializados que trabajarán 24/7 para automatizar tu negocio
        </p>

        <!-- Group Photo -->
        <div class="team-group-photo">
            <div class="team-group-photo-container">
                <img
                    src="<?php echo get_template_directory_uri(); ?>/assets/team/group.png"
                    alt="Equipo GuaraniAppStore"
                >
            </div>
        </div>

        <!-- Team Grid -->
        <div class="team-grid">
            <?php
            $team_members = guaraniappstore_get_team_members();
            foreach ($team_members as $member) :
            ?>
                <div class="team-card">
                    <div class="team-member-photo">
                        <div class="team-member-photo-container">
                            <img
                                src="<?php echo esc_url($member['image']); ?>"
                                alt="<?php echo esc_attr($member['name']); ?>"
                            >
                        </div>
                    </div>
                    <h3 class="team-member-name"><?php echo esc_html($member['name']); ?></h3>
                    <h4 class="team-member-role"><?php echo esc_html($member['role']); ?></h4>
                    <p class="team-member-description"><?php echo esc_html($member['description']); ?></p>
                    <button class="team-member-btn">
                        💬 Chatear con <?php echo esc_html(explode(' ', $member['name'])[0]); ?>
                    </button>
                </div>
            <?php endforeach; ?>
        </div>
    </div>
</section>

<!-- CTA Section -->
<section class="section" style="padding: 6rem 1.5rem;">
    <div class="container">
        <div class="glass-dark" style="max-width: 56rem; margin: 0 auto; text-align: center; border-radius: 1.5rem; padding: 3rem; border: 2px solid rgba(255, 255, 255, 0.3);">
            <h2 style="font-size: 2.5rem; font-weight: 700; margin-bottom: 1.5rem; color: white;">
                ¿Listo para automatizar?
            </h2>
            <p style="font-size: 1.25rem; margin-bottom: 2.5rem; color: var(--emerald-100);">
                Prueba gratis por 7 días. Sin tarjeta de crédito.
            </p>
            <a href="#trial" style="background: white; color: var(--emerald-600); padding: 1.5rem 2.5rem; font-size: 1.25rem; border-radius: 9999px; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3); font-weight: 600; display: inline-block; transition: all 0.3s ease;">
                Iniciar Trial Gratuito
            </a>
        </div>
    </div>
</section>

<?php get_footer(); ?>
