-- ============================================================================
-- GUARANI APP STORE V2.5 - DATABASE SCHEMA
-- Para MySQL 5.7+ / MariaDB 10.2+
-- ============================================================================
-- Instrucciones:
-- 1. Crea la base de datos en phpMyAdmin
-- 2. Selecciona la base de datos
-- 3. Importa este archivo SQL
-- ============================================================================

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

-- ============================================================================
-- TABLA: users
-- ============================================================================
CREATE TABLE `users` (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `email_verified_at` timestamp NULL DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('user','admin') DEFAULT 'user',
  `avatar` varchar(255) DEFAULT NULL,
  `phone` varchar(50) DEFAULT NULL,
  `company` varchar(255) DEFAULT NULL,
  `trial_ends_at` timestamp NULL DEFAULT NULL,
  `remember_token` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_email_unique` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Usuario admin por defecto (password: admin123)
INSERT INTO `users` (`id`, `name`, `email`, `email_verified_at`, `password`, `role`, `trial_ends_at`, `created_at`, `updated_at`) VALUES
(1, 'Administrador', 'admin@guaraniappstore.com', NOW(), '$2y$12$LQv3c1yD8hN9cMJZJ5k5KeZvTjKZ.Jx0QfXxGvZ8yZvBqZvQfXxGv', 'admin', DATE_ADD(NOW(), INTERVAL 30 DAY), NOW(), NOW());

-- ============================================================================
-- TABLA: services
-- ============================================================================
CREATE TABLE `services` (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `slug` varchar(255) NOT NULL,
  `description` text,
  `long_description` text,
  `icon` varchar(50) DEFAULT NULL,
  `category` enum('telegram','ai','automation','crypto','productivity') NOT NULL,
  `type` enum('telegram_bot','ai_service','automation') NOT NULL,
  `price_monthly` decimal(10,2) DEFAULT NULL,
  `price_yearly` decimal(10,2) DEFAULT NULL,
  `currency` varchar(10) DEFAULT 'PYG',
  `trial_days` int(11) DEFAULT 7,
  `status` enum('active','coming_soon','maintenance') DEFAULT 'active',
  `features` json DEFAULT NULL,
  `requirements` json DEFAULT NULL,
  `sort_order` int(11) DEFAULT 0,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `services_slug_unique` (`slug`),
  KEY `services_status_index` (`status`),
  KEY `services_category_index` (`category`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insertar los 11 servicios
INSERT INTO `services` (`id`, `name`, `slug`, `description`, `long_description`, `icon`, `category`, `type`, `price_monthly`, `price_yearly`, `currency`, `trial_days`, `status`, `features`, `sort_order`, `created_at`, `updated_at`) VALUES
(1, 'Ruptura del Hielo', 'ruptura-del-hielo', 'Scraping de Google Maps + IA para mensajes personalizados', 'Extrae información de negocios desde Google Maps y genera mensajes de ventas personalizados usando IA avanzada.', '🎯', 'ai', 'ai_service', 150000.00, 1500000.00, 'PYG', 7, 'active', '["Scraping de Google Maps", "Análisis con IA", "Mensajes personalizados", "Exportación a CSV/Excel", "Filtros avanzados"]', 1, NOW(), NOW()),
(2, 'Preselección Curricular', 'preseleccion-curricular', 'OCR + IA para análisis automático de CVs', 'Escanea y analiza currículums automáticamente, asigna puntajes y genera recomendaciones de contratación.', '📄', 'ai', 'ai_service', 120000.00, 1200000.00, 'PYG', 7, 'active', '["OCR de documentos", "Análisis de IA", "Sistema de scoring", "Comparación de candidatos", "Informes detallados"]', 2, NOW(), NOW()),
(3, 'Consultoría Técnica', 'consultoria-tecnica', 'Bot de Telegram con IA para soporte técnico 24/7', 'Asistente técnico con IA que responde consultas de programación y tecnología las 24 horas.', '🤖', 'telegram', 'telegram_bot', 100000.00, 1000000.00, 'PYG', 7, 'active', '["Soporte 24/7", "Múltiples lenguajes", "Ejemplos de código", "Debugging asistido", "Integración Telegram"]', 3, NOW(), NOW()),
(4, 'Asistente Personal', 'asistente-personal', 'Bot de Telegram + Google Calendar + Google Drive', 'Tu asistente personal que gestiona tu agenda, archivos y tareas desde Telegram.', '📱', 'telegram', 'telegram_bot', 80000.00, 800000.00, 'PYG', 7, 'active', '["Gestión de calendario", "Organización de archivos", "Recordatorios", "Búsqueda inteligente", "Comandos por voz"]', 4, NOW(), NOW()),
(5, 'Organizador de Facturas', 'organizador-facturas', 'OCR + Google Sheets para gestión de facturas', 'Escanea facturas automáticamente y las organiza en Google Sheets con análisis financiero.', '🧾', 'productivity', 'ai_service', 90000.00, 900000.00, 'PYG', 7, 'coming_soon', '["OCR de facturas", "Integración Google Sheets", "Categorización automática", "Reportes mensuales", "Alertas de vencimiento"]', 5, NOW(), NOW()),
(6, 'Organizador de Agenda', 'organizador-agenda', 'Bot de Telegram + Google Calendar con IA', 'Gestiona tu agenda de forma inteligente con recordatorios y sugerencias de IA.', '📅', 'telegram', 'telegram_bot', 70000.00, 700000.00, 'PYG', 7, 'coming_soon', '["Calendario inteligente", "Recordatorios personalizados", "Análisis de productividad", "Sincronización multi-plataforma"]', 6, NOW(), NOW()),
(7, 'Suite Crypto (3 Bots)', 'suite-crypto', 'CryptoShield + Pulse IA + Momentum para trading', 'Suite completa de 3 bots especializados en análisis y alertas de criptomonedas.', '🪙', 'crypto', 'telegram_bot', 200000.00, 2000000.00, 'PYG', 7, 'active', '["CryptoShield: Seguridad", "Pulse IA: Análisis de mercado", "Momentum: Señales de trading", "Alertas en tiempo real", "Portfolio tracking"]', 7, NOW(), NOW()),
(8, 'Agente de Ventas IA', 'agente-ventas-ia', 'Bot de ventas autónomo con IA avanzada', 'Agente de ventas con IA que gestiona leads, seguimientos y cierra ventas automáticamente.', '💼', 'ai', 'telegram_bot', 180000.00, 1800000.00, 'PYG', 7, 'active', '["Gestión de leads", "Seguimiento automático", "Scripts de venta IA", "CRM integrado", "Reportes de conversión"]', 8, NOW(), NOW()),
(9, 'Generador de Blogs', 'generador-blogs', 'IA para crear contenido SEO optimizado', 'Genera artículos de blog completos optimizados para SEO con IA de última generación.', '✍️', 'ai', 'ai_service', 130000.00, 1300000.00, 'PYG', 7, 'coming_soon', '["SEO optimizado", "Múltiples idiomas", "Investigación automática", "Imágenes sugeridas", "Publicación directa"]', 9, NOW(), NOW()),
(10, 'Automatización E-commerce', 'automatizacion-ecommerce', 'Suite completa para tiendas online', 'Automatiza inventario, precios, marketing y atención al cliente de tu e-commerce.', '🛒', 'automation', 'automation', 250000.00, 2500000.00, 'PYG', 7, 'coming_soon', '["Gestión de inventario", "Pricing dinámico", "Marketing automation", "Chatbot de ventas", "Analytics avanzado"]', 10, NOW(), NOW()),
(11, 'Automatización de Redes', 'automatizacion-redes', 'Gestión multi-plataforma de redes sociales', 'Automatiza publicaciones, respuestas y análisis en todas tus redes sociales.', '📱', 'automation', 'automation', 160000.00, 1600000.00, 'PYG', 7, 'coming_soon', '["Multi-plataforma", "Scheduling inteligente", "Respuestas automáticas", "Analytics unificado", "Generación de contenido"]', 11, NOW(), NOW());

-- ============================================================================
-- TABLA: subscriptions
-- ============================================================================
CREATE TABLE `subscriptions` (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) UNSIGNED NOT NULL,
  `service_id` bigint(20) UNSIGNED NOT NULL,
  `status` enum('active','cancelled','expired','pending') DEFAULT 'pending',
  `billing_cycle` enum('monthly','yearly') DEFAULT 'monthly',
  `amount` decimal(10,2) NOT NULL,
  `currency` varchar(10) DEFAULT 'PYG',
  `starts_at` timestamp NULL DEFAULT NULL,
  `ends_at` timestamp NULL DEFAULT NULL,
  `cancelled_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `subscriptions_user_id_foreign` (`user_id`),
  KEY `subscriptions_service_id_foreign` (`service_id`),
  KEY `subscriptions_status_index` (`status`),
  CONSTRAINT `subscriptions_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `subscriptions_service_id_foreign` FOREIGN KEY (`service_id`) REFERENCES `services` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLA: payments
-- ============================================================================
CREATE TABLE `payments` (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) UNSIGNED NOT NULL,
  `service_id` bigint(20) UNSIGNED NOT NULL,
  `subscription_id` bigint(20) UNSIGNED DEFAULT NULL,
  `payment_gateway_id` bigint(20) UNSIGNED DEFAULT NULL,
  `amount` decimal(10,2) NOT NULL,
  `currency` varchar(10) DEFAULT 'PYG',
  `status` enum('pending','completed','failed','refunded') DEFAULT 'pending',
  `payment_method` varchar(50) DEFAULT NULL,
  `transaction_id` varchar(255) DEFAULT NULL,
  `gateway_response` text,
  `paid_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `payments_user_id_foreign` (`user_id`),
  KEY `payments_service_id_foreign` (`service_id`),
  KEY `payments_subscription_id_foreign` (`subscription_id`),
  KEY `payments_payment_gateway_id_foreign` (`payment_gateway_id`),
  KEY `payments_status_index` (`status`),
  CONSTRAINT `payments_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `payments_service_id_foreign` FOREIGN KEY (`service_id`) REFERENCES `services` (`id`) ON DELETE CASCADE,
  CONSTRAINT `payments_subscription_id_foreign` FOREIGN KEY (`subscription_id`) REFERENCES `subscriptions` (`id`) ON DELETE SET NULL,
  CONSTRAINT `payments_payment_gateway_id_foreign` FOREIGN KEY (`payment_gateway_id`) REFERENCES `payment_gateways` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLA: payment_gateways
-- ============================================================================
CREATE TABLE `payment_gateways` (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `gateway_name` varchar(50) NOT NULL,
  `display_name` varchar(100) NOT NULL,
  `is_active` tinyint(1) DEFAULT 1,
  `commission_percentage` decimal(5,2) DEFAULT 0.00,
  `config` json DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `payment_gateways_gateway_name_unique` (`gateway_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insertar las 4 pasarelas de pago
INSERT INTO `payment_gateways` (`id`, `gateway_name`, `display_name`, `is_active`, `commission_percentage`, `created_at`, `updated_at`) VALUES
(1, 'paypal', 'PayPal', 1, 3.50, NOW(), NOW()),
(2, 'pagopar', 'PagoPar', 1, 2.90, NOW(), NOW()),
(3, 'bancard', 'Bancard', 1, 2.50, NOW(), NOW()),
(4, 'crypto', 'Criptomonedas', 1, 1.00, NOW(), NOW());

-- ============================================================================
-- TABLA: api_credentials
-- ============================================================================
CREATE TABLE `api_credentials` (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `service_id` bigint(20) UNSIGNED DEFAULT NULL,
  `api_name` varchar(100) NOT NULL,
  `api_type` enum('ai','google','payment','social','blockchain','other') NOT NULL,
  `api_key` text NOT NULL,
  `api_secret` text DEFAULT NULL,
  `config` json DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT 1,
  `rate_limit` int(11) DEFAULT NULL,
  `last_used_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `api_credentials_service_id_foreign` (`service_id`),
  KEY `api_credentials_api_type_index` (`api_type`),
  CONSTRAINT `api_credentials_service_id_foreign` FOREIGN KEY (`service_id`) REFERENCES `services` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLA: password_reset_tokens (Laravel standard)
-- ============================================================================
CREATE TABLE `password_reset_tokens` (
  `email` varchar(255) NOT NULL,
  `token` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLA: sessions (Laravel standard)
-- ============================================================================
CREATE TABLE `sessions` (
  `id` varchar(255) NOT NULL,
  `user_id` bigint(20) UNSIGNED DEFAULT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `user_agent` text,
  `payload` longtext NOT NULL,
  `last_activity` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sessions_user_id_index` (`user_id`),
  KEY `sessions_last_activity_index` (`last_activity`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLA: cache (Laravel optional - recomendada)
-- ============================================================================
CREATE TABLE `cache` (
  `key` varchar(255) NOT NULL,
  `value` mediumtext NOT NULL,
  `expiration` int(11) NOT NULL,
  PRIMARY KEY (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `cache_locks` (
  `key` varchar(255) NOT NULL,
  `owner` varchar(255) NOT NULL,
  `expiration` int(11) NOT NULL,
  PRIMARY KEY (`key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLA: jobs (Laravel queue - opcional)
-- ============================================================================
CREATE TABLE `jobs` (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `queue` varchar(255) NOT NULL,
  `payload` longtext NOT NULL,
  `attempts` tinyint(3) UNSIGNED NOT NULL,
  `reserved_at` int(10) UNSIGNED DEFAULT NULL,
  `available_at` int(10) UNSIGNED NOT NULL,
  `created_at` int(10) UNSIGNED NOT NULL,
  PRIMARY KEY (`id`),
  KEY `jobs_queue_index` (`queue`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `job_batches` (
  `id` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `total_jobs` int(11) NOT NULL,
  `pending_jobs` int(11) NOT NULL,
  `failed_jobs` int(11) NOT NULL,
  `failed_job_ids` longtext NOT NULL,
  `options` mediumtext,
  `cancelled_at` int(11) DEFAULT NULL,
  `created_at` int(11) NOT NULL,
  `finished_at` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `failed_jobs` (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `uuid` varchar(255) NOT NULL,
  `connection` text NOT NULL,
  `queue` text NOT NULL,
  `payload` longtext NOT NULL,
  `exception` longtext NOT NULL,
  `failed_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `failed_jobs_uuid_unique` (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- TABLA: telegram_logs (opcional pero útil)
-- ============================================================================
CREATE TABLE `telegram_logs` (
  `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `user_id` bigint(20) UNSIGNED DEFAULT NULL,
  `bot_name` varchar(50) NOT NULL,
  `telegram_user_id` bigint(20) DEFAULT NULL,
  `chat_id` bigint(20) DEFAULT NULL,
  `message_type` varchar(50) DEFAULT NULL,
  `message_text` text,
  `response_text` text,
  `created_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `telegram_logs_user_id_foreign` (`user_id`),
  KEY `telegram_logs_bot_name_index` (`bot_name`),
  KEY `telegram_logs_telegram_user_id_index` (`telegram_user_id`),
  CONSTRAINT `telegram_logs_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

COMMIT;

-- ============================================================================
-- FIN DEL SCRIPT
-- ============================================================================
-- CREDENCIALES POR DEFECTO:
-- Email: admin@guaraniappstore.com
-- Password: admin123
--
-- IMPORTANTE: Cambiar la contraseña del admin después del primer login
-- ============================================================================
