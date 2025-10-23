#!/bin/bash
# Restore script for PostgreSQL database

set -e

echo "🔄 GuaraniAppStore - Database Restore"
echo "====================================="
echo ""

BACKUP_DIR="./backups"

# Check if backup directory exists
if [ ! -d "$BACKUP_DIR" ]; then
    echo "Error: Backup directory not found"
    exit 1
fi

# List available backups
echo "Available backups:"
ls -lh $BACKUP_DIR/*.sql.gz 2>/dev/null || {
    echo "No backups found"
    exit 1
}

echo ""
read -p "Enter backup filename to restore: " BACKUP_FILE

if [ ! -f "$BACKUP_DIR/$BACKUP_FILE" ]; then
    echo "Error: Backup file not found"
    exit 1
fi

# Load environment variables
source .env

echo ""
read -p "⚠️  This will REPLACE the current database. Continue? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Restore cancelled"
    exit 0
fi

echo ""
echo "Decompressing backup..."
gunzip -c "$BACKUP_DIR/$BACKUP_FILE" > /tmp/restore.sql

echo "Stopping backend service..."
docker-compose stop backend

echo "Restoring database..."
docker-compose exec -T postgres psql -U $POSTGRES_USER -d $POSTGRES_DB < /tmp/restore.sql

rm /tmp/restore.sql

echo "Starting backend service..."
docker-compose start backend

echo ""
echo "✓ Database restored successfully!"
echo "✓ Backend service restarted"