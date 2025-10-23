# Guía de Mantenimiento - GuaraniAppStore V2.5 Pro

## 📋 Tareas de Mantenimiento Regular

### Diario

#### Monitoreo de Logs
```bash
# Ver logs recientes
docker compose logs --tail=100 backend
docker compose logs --tail=100 frontend

# Buscar errores
docker compose logs | grep -i error
docker compose logs | grep -i exception
```

#### Verificar Estado de Servicios
```bash
docker compose ps
docker stats --no-stream
```

### Semanal

#### Backup de Base de Datos
```bash
# Crear backup
./scripts/backup.sh

# Verificar backups
ls -lh backups/

# Probar restore en ambiente de testing
./scripts/restore.sh
```

#### Actualizar Dependencias
```bash
# Backend
cd backend
pip list --outdated

# Frontend
cd frontend
yarn outdated
```

#### Revisar Logs de Nginx
```bash
tail -f nginx/logs/guarani_error.log
tail -f nginx/logs/guarani_access.log
```

### Mensual

#### Actualizar Sistema Operativo
```bash
sudo apt update
sudo apt upgrade -y
sudo reboot
```

#### Rotar Logs
```bash
# Comprimir logs viejos
find nginx/logs -name "*.log" -mtime +30 -exec gzip {} \;

# Eliminar logs muy antiguos
find nginx/logs -name "*.gz" -mtime +90 -delete
```

#### Limpiar Docker
```bash
./scripts/docker-cleanup.sh
```

#### Renovar Certificados SSL
```bash
# Let's Encrypt renueva automáticamente, pero verifica:
sudo certbot certificates
sudo certbot renew --dry-run
```

### Trimestral

#### Auditoría de Seguridad
```bash
# Verificar claves expuestas
./scripts/check_security.sh

# Actualizar contraseñas críticas
# - Base de datos
# - JWT secrets
# - API keys rotables
```

#### Review de Performance
```bash
# Analizar uso de recursos
docker stats

# Analizar logs de acceso
cat nginx/logs/guarani_access.log | awk '{print $1}' | sort | uniq -c | sort -rn | head -10
```

---

## 🔧 Tareas de Actualización

### Actualizar Aplicación

```bash
# 1. Hacer backup
./scripts/backup.sh

# 2. Pull cambios
git pull origin main

# 3. Rebuild y restart
docker compose build --no-cache
docker compose up -d

# 4. Verificar
docker compose ps
docker compose logs -f
```

### Actualizar Dependencias de Backend

```bash
cd backend

# Ver dependencias desactualizadas
pip list --outdated

# Actualizar una dependencia específica
pip install --upgrade fastapi

# Actualizar requirements.txt
pip freeze > requirements.txt

# Rebuild container
cd ..
docker compose build backend --no-cache
docker compose up -d backend
```

### Actualizar Dependencias de Frontend

```bash
cd frontend

# Ver dependencias desactualizadas
yarn outdated

# Actualizar una dependencia específica
yarn upgrade react

# Actualizar package.json
# Se actualiza automáticamente con yarn upgrade

# Rebuild container
cd ..
docker compose build frontend --no-cache
docker compose up -d frontend
```

---

## 📊 Monitoreo y Alertas

### Métricas Importantes a Monitorear

#### CPU y RAM
```bash
# Uso general
docker stats

# Por servicio
docker stats guarani_backend guarani_frontend guarani_postgres
```

#### Espacio en Disco
```bash
# Uso de disco
df -h

# Tamaño de volúmenes Docker
docker system df -v

# Tamaño de backups
du -sh backups/
```

#### Base de Datos
```bash
# Tamaño de base de datos
docker compose exec postgres psql -U guarani_user -d guarani_appstore -c "SELECT pg_size_pretty(pg_database_size('guarani_appstore'));"

# Conexiones activas
docker compose exec postgres psql -U guarani_user -d guarani_appstore -c "SELECT count(*) FROM pg_stat_activity;"

# Queries lentas (si tienes pg_stat_statements)
docker compose exec postgres psql -U guarani_user -d guarani_appstore -c "SELECT query, mean_exec_time FROM pg_stat_statements ORDER BY mean_exec_time DESC LIMIT 10;"
```

### Configurar Alertas (Opcional)

#### Crear script de monitoreo
```bash
#!/bin/bash
# /root/monitor-guarani.sh

# Verificar servicios
if ! docker compose ps | grep -q "Up"; then
    echo "⚠️ Algún servicio está caído" | mail -s "Alert: GuaraniAppStore" admin@example.com
fi

# Verificar espacio en disco
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 80 ]; then
    echo "⚠️ Disco al ${DISK_USAGE}%" | mail -s "Alert: Disk Space" admin@example.com
fi
```

#### Cron job para monitoreo
```bash
# Ejecutar cada hora
0 * * * * /root/monitor-guarani.sh
```

---

## 🐛 Debugging Avanzado

### Logs Detallados

#### Backend con modo debug
```bash
# Editar backend/.env
DEBUG=True

# Reiniciar
docker compose restart backend
```

#### Ver queries SQL
```bash
# En backend/.env
SQLALCHEMY_ECHO=True
```

### Acceder a Contenedores

```bash
# Backend shell
docker compose exec backend sh

# Frontend shell
docker compose exec frontend sh

# PostgreSQL CLI
docker compose exec postgres psql -U guarani_user -d guarani_appstore
```

### Network Debugging

```bash
# Ver redes
docker network ls

# Inspeccionar red
docker network inspect guarani_guarani_network

# Ping entre servicios
docker compose exec backend ping postgres
docker compose exec backend ping frontend
```

---

## 🔄 Rollback de Versión

### Rollback con Git

```bash
# Ver commits recientes
git log --oneline -10

# Rollback a commit específico
git checkout <commit-hash>

# Rebuild
docker compose build --no-cache
docker compose up -d
```

### Restaurar desde Backup

```bash
# Listar backups disponibles
ls -lh backups/

# Restaurar
./scripts/restore.sh

# Especificar backup
# Cuando te pregunte, ingresa: guarani_backup_20250101_120000.sql.gz
```

---

## 📈 Optimización de Performance

### Base de Datos

```bash
# Vacuum y análisis
docker compose exec postgres psql -U guarani_user -d guarani_appstore -c "VACUUM ANALYZE;"

# Reindex
docker compose exec postgres psql -U guarani_user -d guarani_appstore -c "REINDEX DATABASE guarani_appstore;"
```

### Docker

```bash
# Limpiar imágenes viejas
docker image prune -a

# Limpiar build cache
docker builder prune

# Ver uso de espacio
docker system df
```

### Nginx Caching (Avanzado)

Editar `nginx/conf.d/guarani.conf` para agregar:
```nginx
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=api_cache:10m max_size=100m;

location /api {
    proxy_cache api_cache;
    proxy_cache_valid 200 5m;
    ...
}
```

---

## 📞 Contacto y Soporte

- **Issues**: GitHub Issues
- **Email**: admin@guaraniappstore.com
- **Documentación**: Ver [README.md](./README.md)

---

## 📚 Checklist de Mantenimiento

```
☐ Backups diarios automatizados
☐ Monitoreo de logs configurado
☐ Alertas de recursos críticos
☐ SSL renovación automática
☐ Actualización mensual de SO
☐ Rotación de logs configurada
☐ Plan de rollback documentado
☐ Contactos de emergencia actualizados
```
