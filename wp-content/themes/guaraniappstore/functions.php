<?php
/**
 * GuaraniAppStore Theme Functions
 *
 * @package GuaraniAppStore
 * @version 2.5
 */

// Evitar acceso directo
if (!defined('ABSPATH')) {
    exit;
}

/**
 * Configuración del tema
 */
function guaraniappstore_setup() {
    // Soporte para título del sitio
    add_theme_support('title-tag');

    // Soporte para imágenes destacadas
    add_theme_support('post-thumbnails');

    // Soporte para logo personalizado
    add_theme_support('custom-logo', array(
        'height'      => 60,
        'width'       => 200,
        'flex-height' => true,
        'flex-width'  => true,
    ));

    // Registro de menús
    register_nav_menus(array(
        'primary' => __('Menú Principal', 'guaraniappstore'),
        'footer'  => __('Menú Footer', 'guaraniappstore'),
    ));

    // Soporte HTML5
    add_theme_support('html5', array(
        'search-form',
        'comment-form',
        'comment-list',
        'gallery',
        'caption',
    ));
}
add_action('after_setup_theme', 'guaraniappstore_setup');

/**
 * Registrar y encolar estilos
 */
function guaraniappstore_enqueue_styles() {
    // Estilo principal
    wp_enqueue_style('guaraniappstore-style', get_stylesheet_uri(), array(), '2.5');

    // Estilos de componentes
    wp_enqueue_style('guaraniappstore-header', get_template_directory_uri() . '/assets/css/header.css', array(), '2.5');
    wp_enqueue_style('guaraniappstore-hero', get_template_directory_uri() . '/assets/css/hero.css', array(), '2.5');
    wp_enqueue_style('guaraniappstore-services', get_template_directory_uri() . '/assets/css/services.css', array(), '2.5');
    wp_enqueue_style('guaraniappstore-team', get_template_directory_uri() . '/assets/css/team.css', array(), '2.5');
    wp_enqueue_style('guaraniappstore-footer', get_template_directory_uri() . '/assets/css/footer.css', array(), '2.5');
}
add_action('wp_enqueue_scripts', 'guaraniappstore_enqueue_styles');

/**
 * Registrar y encolar scripts
 */
function guaraniappstore_enqueue_scripts() {
    // Script principal
    wp_enqueue_script('guaraniappstore-main', get_template_directory_uri() . '/assets/js/main.js', array(), '2.5', true);
}
add_action('wp_enqueue_scripts', 'guaraniappstore_enqueue_scripts');

/**
 * Obtener datos de los servicios
 */
function guaraniappstore_get_services() {
    return array(
        array(
            'icon' => '⚡',
            'title' => 'Autoconfigurable',
            'description' => 'Sin necesidad de desarrolladores. Configura y activa tus servicios en minutos sin conocimientos técnicos'
        ),
        array(
            'icon' => '🛡️',
            'title' => 'Seguro y Confiable',
            'description' => 'Tus datos protegidos con encriptación de nivel empresarial'
        ),
        array(
            'icon' => '📈',
            'title' => 'Escalable',
            'description' => 'Crece desde 10 hasta 10,000 conversaciones sin límites'
        ),
    );
}

/**
 * Obtener datos del equipo
 */
function guaraniappstore_get_team_members() {
    return array(
        array(
            'name' => 'Junior Cucurella',
            'role' => 'Gerente de Agendas',
            'description' => 'Gestiona completamente citas, reservas y recordatorios 24/7',
            'image' => get_template_directory_uri() . '/assets/team/junior.png'
        ),
        array(
            'name' => 'Jacinto Torrelavega',
            'role' => 'Asistente de Facturación',
            'description' => 'Automatiza flujos contables',
            'image' => get_template_directory_uri() . '/assets/team/jacinto.png'
        ),
        array(
            'name' => 'Alex Albiol',
            'role' => 'Soporte Instantáneo',
            'description' => 'Respuestas rápidas y efectivas para tus clientes',
            'image' => get_template_directory_uri() . '/assets/team/alex.png'
        ),
        array(
            'name' => 'Silvia Garcia',
            'role' => 'Integración Operativa',
            'description' => 'Conecta sistemas y optimiza procesos',
            'image' => get_template_directory_uri() . '/assets/team/silvia.png'
        ),
        array(
            'name' => 'Blanca Garcia',
            'role' => 'Servicio RPA',
            'description' => 'Elimina el "copiar y pegar", automatizando la transferencia de datos',
            'image' => get_template_directory_uri() . '/assets/team/blanca.png'
        ),
        array(
            'name' => 'Rocío Almeida',
            'role' => 'Moderador de Reputación',
            'description' => 'Gestiona y protege tu imagen digital',
            'image' => get_template_directory_uri() . '/assets/team/rocio.png'
        ),
    );
}

/**
 * Agregar favicon
 */
function guaraniappstore_add_favicon() {
    echo '<link rel="icon" type="image/png" href="' . get_template_directory_uri() . '/assets/images/favicon.png">';
}
add_action('wp_head', 'guaraniappstore_add_favicon');

/**
 * Personalizar excerpt length
 */
function guaraniappstore_excerpt_length($length) {
    return 30;
}
add_filter('excerpt_length', 'guaraniappstore_excerpt_length');

/**
 * Personalizar excerpt more
 */
function guaraniappstore_excerpt_more($more) {
    return '...';
}
add_filter('excerpt_more', 'guaraniappstore_excerpt_more');
