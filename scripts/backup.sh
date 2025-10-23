#!/bin/bash
# Backup script for PostgreSQL database

set -e

echo "💾 GuaraniAppStore - Database Backup"
echo "===================================="
echo ""

# Configuration
BACKUP_DIR="./backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="guarani_backup_${TIMESTAMP}.sql"

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Load environment variables
source .env

echo "Creating backup: $BACKUP_FILE"

# Create backup
docker-compose exec -T postgres pg_dump -U $POSTGRES_USER $POSTGRES_DB > "$BACKUP_DIR/$BACKUP_FILE"

if [ $? -eq 0 ]; then
    echo "✓ Backup created successfully: $BACKUP_DIR/$BACKUP_FILE"
    
    # Compress backup
    gzip "$BACKUP_DIR/$BACKUP_FILE"
    echo "✓ Backup compressed: $BACKUP_DIR/$BACKUP_FILE.gz"
    
    # Keep only last 7 backups
    echo "Cleaning old backups (keeping last 7)..."
    ls -t $BACKUP_DIR/*.sql.gz | tail -n +8 | xargs -r rm
    echo "✓ Old backups cleaned"
    
    echo ""
    echo "Backup complete!"
    ls -lh $BACKUP_DIR/$BACKUP_FILE.gz
else
    echo "✗ Backup failed"
    exit 1
fi