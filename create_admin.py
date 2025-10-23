#!/usr/bin/env python3
"""
Create admin user for testing
"""

import asyncio
import sys
import os
sys.path.append('/app/backend')

from database import get_db, engine, Base
from models import User, UserRole
from auth import hash_password
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def create_admin_user():
    """Create admin user if it doesn't exist"""
    
    # Create database session
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async for db in get_db():
        try:
            # Check if admin user exists
            result = await db.execute(select(User).filter(User.email == "admin@guaraniappstore.com"))
            existing_user = result.scalar_one_or_none()
            
            if existing_user:
                print("✅ Admin user already exists")
                print(f"   Email: {existing_user.email}")
                print(f"   Role: {existing_user.role}")
                return
            
            # Create admin user
            admin_user = User(
                email="admin@guaraniappstore.com",
                password_hash=hash_password("admin123"),
                full_name="Admin User",
                role=UserRole.ADMIN,
                is_active=True,
                is_verified=True,
                country="Paraguay",
                timezone="America/Asuncion"
            )
            
            db.add(admin_user)
            await db.commit()
            await db.refresh(admin_user)
            
            print("✅ Admin user created successfully")
            print(f"   Email: {admin_user.email}")
            print(f"   Role: {admin_user.role}")
            print(f"   ID: {admin_user.id}")
            
        except Exception as e:
            print(f"❌ Error creating admin user: {str(e)}")
            await db.rollback()
        finally:
            break

if __name__ == "__main__":
    asyncio.run(create_admin_user())