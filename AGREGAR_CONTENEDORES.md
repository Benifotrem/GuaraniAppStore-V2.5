# 🐳 Guía para Agregar Contenedores a Docker Compose

## 📋 Archivos Docker Compose

### Archivo PRINCIPAL: `docker-compose.yml`
✅ **Usar este para PRODUCCIÓN en tu VPS**
- MongoDB como base de datos
- Nginx como reverse proxy
- Optimizado para producción con Cloudflare
- Health checks completos

### Archivo Secundario: `docker-compose.dev.yml`
⚠️ **Solo para desarrollo local**
- PostgreSQL (legacy)
- Hot reload habilitado
- Sin nginx

---

## 🔧 Cómo Agregar un Nuevo Contenedor

### Template General

```yaml
services:
  # ... servicios existentes ...

  # TU NUEVO SERVICIO
  nombre_servicio:
    image: nombre-imagen:version
    container_name: guarani_nombre_servicio
    restart: always
    ports:
      - "puerto-host:puerto-contenedor"
    volumes:
      - nombre_volumen:/ruta/en/contenedor
    environment:
      - VARIABLE_1=valor1
      - VARIABLE_2=valor2
    networks:
      - guarani_network
    depends_on:
      - servicio_dependencia
    healthcheck:
      test: ["CMD", "comando-de-health-check"]
      interval: 30s
      timeout: 10s
      retries: 3

# ... al final del archivo ...

volumes:
  # ... volúmenes existentes ...
  nombre_volumen:
    driver: local
```

---

## 📦 Ejemplos de Contenedores Comunes

### 1. Redis (Cache)

```yaml
  redis:
    image: redis:7-alpine
    container_name: guarani_redis
    restart: always
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - guarani_network
    command: redis-server --appendonly yes --requirepass tu_password_redis
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
```

**Agregar al backend `.env`:**
```bash
REDIS_URL=redis://:tu_password_redis@redis:6379
```

**Actualizar backend para que dependa de Redis:**
```yaml
  backend:
    # ... config existente ...
    depends_on:
      mongodb:
        condition: service_healthy
      redis:
        condition: service_healthy
```

---

### 2. PostgreSQL (Base de datos adicional)

```yaml
  postgres:
    image: postgres:15-alpine
    container_name: guarani_postgres
    restart: always
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: guarani_user
      POSTGRES_PASSWORD: password_seguro
      POSTGRES_DB: guarani_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - guarani_network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U guarani_user"]
      interval: 10s
      timeout: 5s
      retries: 5
```

**Agregar volumen:**
```yaml
volumes:
  postgres_data:
    driver: local
```

---

### 3. RabbitMQ (Message Queue)

```yaml
  rabbitmq:
    image: rabbitmq:3-management-alpine
    container_name: guarani_rabbitmq
    restart: always
    ports:
      - "5672:5672"   # AMQP
      - "15672:15672" # Management UI
    environment:
      RABBITMQ_DEFAULT_USER: admin
      RABBITMQ_DEFAULT_PASS: password_seguro
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
    networks:
      - guarani_network
    healthcheck:
      test: rabbitmq-diagnostics -q ping
      interval: 30s
      timeout: 10s
      retries: 5
```

---

### 4. Elasticsearch (Search Engine)

```yaml
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.0
    container_name: guarani_elasticsearch
    restart: always
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ports:
      - "9200:9200"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data
    networks:
      - guarani_network
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:9200/_cluster/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 5
```

---

### 5. Minio (S3-compatible Storage)

```yaml
  minio:
    image: minio/minio:latest
    container_name: guarani_minio
    restart: always
    ports:
      - "9000:9000"   # API
      - "9001:9001"   # Console
    environment:
      MINIO_ROOT_USER: admin
      MINIO_ROOT_PASSWORD: password_seguro_minimo_8_caracteres
    volumes:
      - minio_data:/data
    networks:
      - guarani_network
    command: server /data --console-address ":9001"
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 10s
      retries: 5
```

---

### 6. Prometheus + Grafana (Monitoring)

```yaml
  prometheus:
    image: prom/prometheus:latest
    container_name: guarani_prometheus
    restart: always
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    networks:
      - guarani_network
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'

  grafana:
    image: grafana/grafana:latest
    container_name: guarani_grafana
    restart: always
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=password_admin
    volumes:
      - grafana_data:/var/lib/grafana
    networks:
      - guarani_network
    depends_on:
      - prometheus
```

---

## 🚀 Pasos para Agregar un Contenedor

### 1. Editar docker-compose.yml

```bash
cd /opt/GuaraniAppStore-V2.5
nano docker-compose.yml
```

### 2. Agregar el servicio en la sección `services:`

Copia el template del contenedor que necesitas (Redis, PostgreSQL, etc.)

### 3. Agregar volúmenes si es necesario

En la sección `volumes:` al final del archivo:
```yaml
volumes:
  # ... volúmenes existentes ...
  nuevo_volumen_data:
    driver: local
```

### 4. Actualizar dependencias si es necesario

Si el backend o frontend necesitan el nuevo servicio:
```yaml
  backend:
    depends_on:
      mongodb:
        condition: service_healthy
      nuevo_servicio:
        condition: service_healthy
```

### 5. Actualizar variables de entorno

Editar `backend/.env`:
```bash
nano backend/.env
```

Agregar variables del nuevo servicio:
```
NUEVO_SERVICIO_URL=protocolo://nuevo_servicio:puerto
NUEVO_SERVICIO_PASSWORD=password_seguro
```

### 6. Rebuild y restart

```bash
# Detener servicios
docker-compose down

# Rebuild (si hay cambios en código)
docker-compose build

# Iniciar con nuevo servicio
docker-compose up -d

# Ver logs
docker-compose logs -f nuevo_servicio
```

---

## ✅ Verificar que Funciona

```bash
# Ver estado
docker-compose ps

# Ver logs específicos
docker-compose logs nuevo_servicio

# Testear conectividad desde backend
docker exec -it guarani_backend bash
# Dentro del contenedor:
curl http://nuevo_servicio:puerto/health
# O comando específico del servicio
exit
```

---

## 📝 Ejemplo Completo: Agregar Redis

### 1. Editar docker-compose.yml

```bash
nano docker-compose.yml
```

### 2. Agregar después de mongodb:

```yaml
  redis:
    image: redis:7-alpine
    container_name: guarani_redis
    restart: always
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - guarani_network
    command: redis-server --appendonly yes
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
```

### 3. Agregar volumen al final:

```yaml
volumes:
  # ... existentes ...
  redis_data:
    driver: local
```

### 4. Actualizar backend/.env:

```bash
echo "REDIS_URL=redis://redis:6379" >> backend/.env
```

### 5. Deploy:

```bash
docker-compose down
docker-compose up -d
docker-compose logs -f redis
```

---

## 🔒 Mejores Prácticas

1. **Siempre usar `restart: always`** para producción
2. **Agregar healthchecks** para todos los servicios
3. **Usar volumes** para persistir datos importantes
4. **Usar secretos seguros** en variables de entorno
5. **Limitar recursos** si es necesario:
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '0.5'
         memory: 512M
   ```
6. **Network isolation** - todos los servicios en `guarani_network`
7. **No exponer puertos** innecesarios (comentar la sección `ports:`)

---

## 🆘 Troubleshooting

### Servicio no inicia
```bash
docker-compose logs nombre_servicio
```

### Conflicto de puertos
```bash
# Ver puertos en uso
sudo netstat -tulpn | grep LISTEN

# Cambiar puerto en docker-compose.yml
ports:
  - "NUEVO_PUERTO:puerto_contenedor"
```

### Problema de volúmenes
```bash
# Eliminar volúmenes y recrear
docker-compose down -v
docker-compose up -d
```

---

**Dime qué contenedor específico necesitas agregar y te ayudo con la configuración exacta** 🚀
