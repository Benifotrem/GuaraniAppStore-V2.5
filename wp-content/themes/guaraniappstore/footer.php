<footer class="site-footer">
    <div class="footer-content">
        <!-- Columna 1: Sobre la Empresa -->
        <div class="footer-section">
            <div class="footer-logo">GuaraniAppStore</div>
            <p class="footer-description">
                Automatización inteligente con IA. Transforma tu negocio con tecnología de vanguardia.
            </p>
            <p style="color: rgba(255, 255, 255, 0.8); margin-top: 1rem;">
                🇵🇾 Hecho con ❤️ en Paraguay para el mundo 🌎
            </p>
            <p style="color: rgba(255, 255, 255, 0.7); margin-top: 0.5rem;">
                📍 Asunción, Paraguay
            </p>
        </div>

        <!-- Columna 2: Servicios -->
        <div class="footer-section">
            <h3>Servicios</h3>
            <ul>
                <li><a href="#servicios">🤖 Suite Completa de IA</a></li>
                <li><a href="#servicios">⚡ Automatización</a></li>
                <li><a href="#servicios">₿ Suite Crypto</a></li>
                <li><a href="#servicios">💼 Consultoría</a></li>
                <li><a href="#servicios">🎯 Agentes IA</a></li>
            </ul>
        </div>

        <!-- Columna 3: Empresa -->
        <div class="footer-section">
            <h3>Empresa</h3>
            <ul>
                <li><a href="#equipo">👥 Nuestro Equipo</a></li>
                <li><a href="#inicio">🏢 Sobre Nosotros</a></li>
                <li><a href="<?php echo esc_url(home_url('/blog')); ?>">📝 Blog</a></li>
                <li><a href="<?php echo esc_url(home_url('/faq')); ?>">❓ FAQ</a></li>
            </ul>
        </div>

        <!-- Columna 4: Legal y Contacto -->
        <div class="footer-section">
            <h3>Contacto</h3>
            <ul>
                <li>
                    <strong style="color: var(--emerald-300);">📧 Email:</strong><br>
                    <a href="mailto:admin@guaraniappstore.com">admin@guaraniappstore.com</a>
                </li>
                <li style="margin-top: 1rem;">
                    <strong style="color: var(--emerald-300);">💬 Soporte:</strong><br>
                    24/7 vía Chat IA
                </li>
            </ul>

            <div style="margin-top: 2rem;">
                <h4 style="color: var(--emerald-300); font-size: 1rem; margin-bottom: 1rem;">Síguenos</h4>
                <div class="social-links">
                    <a href="https://www.facebook.com/profile.php?id=61568205705311" target="_blank" rel="noopener noreferrer" class="social-link" aria-label="Facebook">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                        </svg>
                    </a>
                    <a href="https://www.linkedin.com/company/guaran%C3%AD-app-store" target="_blank" rel="noopener noreferrer" class="social-link" aria-label="LinkedIn">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 24 24">
                            <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
                        </svg>
                    </a>
                </div>
            </div>
        </div>
    </div>

    <!-- Footer Bottom -->
    <div class="footer-bottom">
        <p>&copy; <?php echo date('Y'); ?> GuaraniAppStore. Todos los derechos reservados.</p>
        <p style="margin-top: 0.5rem; font-size: 0.875rem;">Propiedad de César Ruzafa Alberola</p>
    </div>
</footer>

<?php wp_footer(); ?>
</body>
</html>
