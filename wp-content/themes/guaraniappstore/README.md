# GuaraniAppStore WordPress Theme

**Versión:** 2.5
**Autor:** GuaraniAppStore Team
**Descripción:** Tema WordPress personalizado para GuaraniAppStore - Automatización con IA

## 📋 Descripción

Este tema WordPress es una conversión exacta del diseño original de GuaraniAppStore, manteniendo todos los elementos visuales, incluyendo:

- ✅ Video de fondo en bucle en la sección Hero
- ✅ Fotos del equipo de agentes IA
- ✅ Paleta de colores Emerald (#10b981) y Teal
- ✅ Efectos glass y animaciones suaves
- ✅ Diseño 100% responsive
- ✅ Optimizado para móviles

## 🎨 Características del Diseño

### Colores Principales
- **Emerald-500:** #10b981 (Color primario)
- **Teal-600:** #0d9488 (Color secundario)
- **Gray-700:** #374151 (Texto)

### Efectos Visuales
- **Glass Effect:** Fondo translúcido con blur
- **Animaciones:** fade-in-up, float, hover effects
- **Text Shadows:** Sombras para mejorar legibilidad
- **Smooth Scroll:** Navegación suave entre secciones

## 📁 Estructura del Tema

```
guaraniappstore/
├── assets/
│   ├── css/
│   │   ├── header.css
│   │   ├── hero.css
│   │   ├── services.css
│   │   ├── team.css
│   │   └── footer.css
│   ├── js/
│   │   └── main.js
│   ├── images/
│   │   └── favicon.png
│   ├── videos/
│   │   └── background.mp4 (14MB)
│   └── team/
│       ├── junior.png
│       ├── jacinto.png
│       ├── alex.png
│       ├── silvia.png
│       ├── blanca.png
│       ├── rocio.png
│       └── group.png
├── style.css
├── functions.php
├── header.php
├── footer.php
├── index.php
└── README.md
```

## 🚀 Instalación

1. **Subir el tema:**
   - Copia la carpeta `guaraniappstore` a `wp-content/themes/`
   - O sube el tema como ZIP desde el panel de WordPress

2. **Activar el tema:**
   - Ve a Apariencia > Temas en el panel de WordPress
   - Activa el tema "GuaraniAppStore"

3. **Configurar menús:**
   - Ve a Apariencia > Menús
   - Crea un menú y asígnalo a la ubicación "Menú Principal"

4. **Opcional - Logo personalizado:**
   - Ve a Apariencia > Personalizar > Identidad del sitio
   - Sube tu logo (tamaño recomendado: 200x60px)

## 🎯 Secciones de la Landing Page

1. **Hero Section** (con video en bucle)
   - Título principal
   - Banner de trial gratuito
   - Banner de servicios crypto
   - CTAs principales

2. **Features Section**
   - 3 características principales
   - Cards con efectos hover

3. **Services Section**
   - Grid de 6 servicios
   - Cards detalladas con precios
   - Botones de suscripción

4. **Team Section**
   - Foto grupal del equipo
   - 6 miembros del equipo con fotos individuales
   - Botones de chat

5. **CTA Final**
   - Llamado a la acción
   - Banner destacado

6. **Footer**
   - Links a servicios
   - Enlaces sociales (Facebook, LinkedIn)
   - Información de contacto

## 📱 Responsive Design

El tema está optimizado para:
- **Desktop:** 1280px+
- **Tablet:** 769px - 1024px
- **Mobile:** < 768px

### Breakpoints:
```css
/* Mobile */
@media (max-width: 768px)

/* Tablet */
@media (min-width: 769px) and (max-width: 1024px)

/* Desktop */
@media (min-width: 1025px)
```

## ⚙️ Funcionalidades JavaScript

- **Mobile Menu:** Menú hamburguesa responsive
- **Smooth Scroll:** Navegación suave entre secciones
- **Header Scroll Effect:** Sombra dinámica al hacer scroll
- **Scroll Animations:** Animaciones al entrar en viewport
- **Video Autoplay:** Reproducción automática en móviles

## 🎨 Personalización

### Cambiar Colores
Edita las variables CSS en `style.css`:
```css
:root {
  --emerald-500: #10b981;  /* Color primario */
  --teal-600: #0d9488;     /* Color secundario */
}
```

### Modificar Servicios
Edita la función en `functions.php`:
```php
function guaraniappstore_get_services()
```

### Modificar Equipo
Edita la función en `functions.php`:
```php
function guaraniappstore_get_team_members()
```

## 🔧 Requisitos

- WordPress 5.0+
- PHP 7.4+
- Navegadores modernos (Chrome, Firefox, Safari, Edge)

## 📝 Notas Importantes

1. **Video de fondo:** El archivo `background.mp4` pesa 14MB. Para mejor rendimiento, considera:
   - Comprimir el video
   - Usar un CDN
   - Implementar lazy loading

2. **Imágenes del equipo:** Las fotos están optimizadas pero se recomienda usar WebP para mejor rendimiento.

3. **Móviles:** El video se reproduce automáticamente con `playsinline` y `muted` para compatibilidad iOS.

## 🌐 Compatibilidad

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+
- ✅ iOS Safari 14+
- ✅ Chrome Mobile

## 📞 Soporte

Para soporte y consultas:
- Email: admin@guaraniappstore.com
- Web: https://guaraniappstore.com

## 📄 Licencia

© 2025 GuaraniAppStore. Todos los derechos reservados.
Propiedad de César Ruzafa Alberola

---

**Versión:** 2.5
**Fecha:** Noviembre 2025
**Desarrollado por:** GuaraniAppStore Team
