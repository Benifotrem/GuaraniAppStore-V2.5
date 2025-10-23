#!/usr/bin/env python3
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import AsyncSessionLocal
from models import User
from passlib.context import CryptContext
from sqlalchemy import select

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def check_and_create_admin():
    async with AsyncSessionLocal() as session:
        # Check if admin exists
        result = await session.execute(
            select(User).where(User.email == 'admin@guaraniappstore.com')
        )
        admin = result.scalar_one_or_none()
        
        if admin:
            print(f"✅ Admin user found: {admin.email}")
            print(f"   Role: {admin.role}")
            print(f"   Active: {admin.is_active}")
            print(f"   Verified: {admin.is_verified}")
            print(f"   Password hash exists: {bool(admin.password_hash)}")
            
            # Verify password
            if pwd_context.verify("admin123", admin.password_hash):
                print("✅ Password 'admin123' is correct")
            else:
                print("❌ Password 'admin123' is incorrect")
                # Update password
                admin.password_hash = pwd_context.hash("admin123")
                await session.commit()
                print("✅ Password updated to 'admin123'")
        else:
            print("❌ Admin user not found, creating...")
            # Create admin user
            admin = User(
                email="admin@guaraniappstore.com",
                password_hash=pwd_context.hash("admin123"),
                full_name="Administrator",
                role="admin",
                is_active=True,
                is_verified=True,
                country="Paraguay",
                timezone="America/Asuncion"
            )
            session.add(admin)
            await session.commit()
            print("✅ Admin user created with password 'admin123'")

if __name__ == "__main__":
    asyncio.run(check_and_create_admin())