<?php

namespace Database\Seeders;

use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;

class ServicesTableSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        $services = [
            // SERVICIOS DE PAGO ÚNICO
            [
                'name' => 'Ruptura del Hielo y Prospección Comercial',
                'slug' => 'ruptura-del-hielo',
                'description' => 'Encuentra leads en Google Maps, extrae datos de contacto y genera mensajes personalizados de primer contacto con IA.',
                'type' => 'one_time',
                'price' => 150000, // Gs. 150,000
                'trial_days' => 0,
                'status' => 'active',
                'features' => [
                    'Búsqueda de leads en Google Maps',
                    'Extracción automática de datos',
                    'Mensajes Ice Breaker generados por IA',
                    'Export a Google Sheets',
                    'Prueba gratis: 5 leads'
                ],
                'icon' => '🎯',
                'sort_order' => 1
            ],
            [
                'name' => 'Agente de Preselección Curricular',
                'slug' => 'preseleccion-curricular',
                'description' => 'Análisis automático de CVs con scoring inteligente, extracción de datos y validación.',
                'type' => 'one_time',
                'price' => 200000, // Gs. 200,000
                'trial_days' => 0,
                'status' => 'active',
                'features' => [
                    'OCR avanzado de CVs',
                    'Scoring 0-100 con IA',
                    'Extracción de datos estructurados',
                    'Validación de email y teléfono',
                    'Export a Google Sheets'
                ],
                'icon' => '📄',
                'sort_order' => 6
            ],
            [
                'name' => 'Consultoría Técnica',
                'slug' => 'consultoria-tecnica',
                'description' => 'Análisis profundo empresarial y estrategia de automatización personalizada.',
                'type' => 'one_time',
                'price' => 500000, // Gs. 500,000
                'trial_days' => 0,
                'status' => 'active',
                'features' => [
                    'Análisis completo de procesos',
                    'Roadmap de automatización',
                    'Recomendaciones de stack tecnológico',
                    'Documento estratégico 20-30 páginas',
                    'Sesión Q&A de 60 minutos'
                ],
                'icon' => '🔍',
                'sort_order' => 11
            ],

            // SERVICIOS DE SUSCRIPCIÓN CON TRIAL 7 DÍAS
            [
                'name' => 'Asistente Personal para Directivos',
                'slug' => 'asistente-personal',
                'description' => 'Asistente ejecutivo 24/7 vía Telegram que gestiona agenda, tareas, finanzas y búsquedas automatizadas.',
                'type' => 'subscription',
                'price' => 300000, // Gs. 300,000/mes
                'trial_days' => 7,
                'status' => 'active',
                'features' => [
                    'Gestión de Google Calendar',
                    'Control de ingresos y gastos',
                    'Búsquedas web automatizadas',
                    'Notificaciones vía Telegram',
                    'Trial 7 días GRATIS'
                ],
                'icon' => '🤵',
                'sort_order' => 3
            ],
            [
                'name' => 'Organizador de Facturas (OCR)',
                'slug' => 'organizador-facturas',
                'description' => 'OCR avanzado para extraer datos estructurados de facturas, contratos y formularios.',
                'type' => 'subscription',
                'price' => 250000, // Gs. 250,000/mes
                'trial_days' => 7,
                'status' => 'active',
                'features' => [
                    'OCR con Tesseract + IA',
                    'Extracción automática de datos',
                    'Validación de cálculos',
                    'Export a Google Sheets/Excel',
                    'Trial 7 días GRATIS'
                ],
                'icon' => '🧾',
                'sort_order' => 8
            ],
            [
                'name' => 'Organizador de Agenda',
                'slug' => 'organizador-agenda',
                'description' => 'Sistema de agendamiento de citas con sincronización Google Calendar y recordatorios automáticos vía Telegram.',
                'type' => 'subscription',
                'price' => 200000, // Gs. 200,000/mes
                'trial_days' => 7,
                'status' => 'active',
                'features' => [
                    'Calendario propio + sincronización Google',
                    'Recordatorios vía Telegram',
                    'Confirmación automática de citas',
                    'Panel de personalización',
                    'Trial 7 días GRATIS'
                ],
                'icon' => '📅',
                'sort_order' => 9
            ],
            [
                'name' => 'Suite Crypto (3 Bots Telegram)',
                'slug' => 'suite-crypto',
                'description' => '3 bots especializados para trading de criptomonedas: CryptoShield (fraude), Pulse IA (sentimiento) y Momentum Predictor (señales).',
                'type' => 'subscription',
                'price' => 400000, // Gs. 400,000/mes
                'trial_days' => 7,
                'status' => 'active',
                'features' => [
                    'CryptoShield: Detección de fraudes',
                    'Pulse IA: Análisis de sentimiento',
                    'Momentum Predictor: Señales de trading',
                    'Alertas vía Telegram',
                    'Trial 7 días GRATIS'
                ],
                'icon' => '🪙',
                'sort_order' => 10
            ],

            // SERVICIOS PRÓXIMAMENTE
            [
                'name' => 'Agente de Ventas IA',
                'slug' => 'agente-ventas-ia',
                'description' => 'Chatbot conversacional avanzado vía Telegram que funciona como vendedor virtual 24/7.',
                'type' => 'subscription',
                'price' => 350000, // Gs. 350,000/mes
                'trial_days' => 7,
                'status' => 'coming_soon',
                'features' => [
                    'Bot Telegram 24/7',
                    'Catálogo hasta 200 productos',
                    'Sistema de scoring de clientes',
                    'Seguimientos automáticos',
                    'Trial 7 días GRATIS'
                ],
                'icon' => '🤖',
                'sort_order' => 2
            ],
            [
                'name' => 'Generador de Blogs Automatizado',
                'slug' => 'generador-blogs',
                'description' => 'Genera 1 artículo diario SEO-optimizado (800-1500 palabras) con imágenes profesionales.',
                'type' => 'subscription',
                'price' => 280000, // Gs. 280,000/mes
                'trial_days' => 7,
                'status' => 'coming_soon',
                'features' => [
                    'Artículo diario automatizado',
                    'SEO optimizado con IA',
                    'Imágenes generadas con Gemini',
                    'Publicación automática',
                    'Trial 7 días GRATIS'
                ],
                'icon' => '📝',
                'sort_order' => 4
            ],
            [
                'name' => 'Automatización de E-commerce',
                'slug' => 'automatizacion-ecommerce',
                'description' => 'Gestión automatizada de tiendas online (Shopify, WooCommerce, BigCommerce).',
                'type' => 'subscription',
                'price' => 320000, // Gs. 320,000/mes
                'trial_days' => 7,
                'status' => 'coming_soon',
                'features' => [
                    'Gestión automática de inventario',
                    'Procesamiento de pedidos',
                    'Búsqueda de proveedores con IA',
                    'Sincronización multi-plataforma',
                    'Trial 7 días GRATIS'
                ],
                'icon' => '🛒',
                'sort_order' => 5
            ],
            [
                'name' => 'Automatización de Contenidos en Redes',
                'slug' => 'automatizacion-redes',
                'description' => 'Generación de contenido desde fuentes y optimización para cada red social (LinkedIn, Twitter, Instagram, Facebook).',
                'type' => 'subscription',
                'price' => 300000, // Gs. 300,000/mes
                'trial_days' => 7,
                'status' => 'coming_soon',
                'features' => [
                    'Conversión multi-formato con IA',
                    'Optimización por red social',
                    'Programación automática',
                    'Analytics y reportes',
                    'Trial 7 días GRATIS'
                ],
                'icon' => '📱',
                'sort_order' => 7
            ],
        ];

        foreach ($services as $service) {
            \App\Models\Service::create($service);
        }
    }
}
