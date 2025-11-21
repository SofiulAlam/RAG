#!/usr/bin/env python3
"""
Seed script to populate the database with initial data
"""
import asyncio
from app.db.session import AsyncSessionLocal
from app.db.seed_templates import seed_templates


async def main():
    """Main seed function"""
    async with AsyncSessionLocal() as db:
        print("Seeding database...")
        await seed_templates(db)
        print("Database seeded successfully!")


if __name__ == "__main__":
    asyncio.run(main())
