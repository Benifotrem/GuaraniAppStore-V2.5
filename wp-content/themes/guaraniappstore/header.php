<!DOCTYPE html>
<html <?php language_attributes(); ?>>
<head>
    <meta charset="<?php bloginfo('charset'); ?>">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#10b981">
    <?php wp_head(); ?>
</head>
<body <?php body_class(); ?>>
<?php wp_body_open(); ?>

<header class="site-header" id="site-header">
    <div class="header-container">
        <!-- Logo -->
        <div class="site-logo">
            <?php if (has_custom_logo()) : ?>
                <?php the_custom_logo(); ?>
            <?php else : ?>
                <a href="<?php echo esc_url(home_url('/')); ?>">
                    GuaraniAppStore
                </a>
            <?php endif; ?>
        </div>

        <!-- Mobile Menu Toggle -->
        <button class="mobile-menu-toggle" id="mobile-menu-toggle" aria-label="Menú">
            ☰
        </button>

        <!-- Navigation -->
        <nav class="main-nav" id="main-nav">
            <?php
            wp_nav_menu(array(
                'theme_location' => 'primary',
                'menu_class'     => 'nav-menu',
                'container'      => false,
                'fallback_cb'    => 'guaraniappstore_fallback_menu',
            ));
            ?>

            <div class="header-cta">
                <a href="#contact" class="btn-login">Iniciar Sesión</a>
                <a href="#trial" class="btn-trial">Comenzar Prueba</a>
            </div>
        </nav>
    </div>
</header>

<?php
// Menú de respaldo si no hay menú configurado
function guaraniappstore_fallback_menu() {
    echo '<ul class="nav-menu">';
    echo '<li><a href="#inicio">Inicio</a></li>';
    echo '<li><a href="#servicios">Servicios</a></li>';
    echo '<li><a href="#equipo">Equipo</a></li>';
    echo '<li><a href="#faq">FAQ</a></li>';
    echo '<li><a href="#blog">Blog</a></li>';
    echo '</ul>';
}
?>
