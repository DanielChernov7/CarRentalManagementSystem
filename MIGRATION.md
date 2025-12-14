# MySQL → PostgreSQL Migration Guide

This document describes the migration from MySQL to PostgreSQL completed for the Car Rental Management System.

## Changes Made

### 1. Database Layer

**Replaced:**
- MySQL → PostgreSQL 16
- PyMySQL → psycopg2-binary

**Added:**
- Alembic for database migrations
- docker-compose.yml for local PostgreSQL instance

**Removed:**
- schema.sql (replaced by Alembic migrations)
- seed_data.sql (replaced by Python seed script)

### 2. New Files

```
docker-compose.yml                                    # PostgreSQL container
backend/
├── alembic.ini                                       # Alembic configuration
├── alembic/
│   ├── env.py                                        # Migration environment
│   ├── script.py.mako                                # Migration template
│   └── versions/
│       └── 20251214_0000_initial_schema.py          # Initial migration
└── seed.py                                           # Python seed script
```

### 3. Updated Files

**backend/requirements.txt**
- Replaced: `pymysql==1.1.1` → `psycopg2-binary==2.9.10`

**backend/.env.example**
- Updated DATABASE_URL from MySQL to PostgreSQL format
- `postgresql://admin:admin123@localhost:5432/car_rental_db`

**backend/README.md**
- Added PostgreSQL setup instructions
- Added Alembic migration commands
- Added database management commands

**README.md (root)**
- Updated tech stack references
- Updated setup instructions
- Added Docker prerequisite

### 4. Code Changes

**No changes to application code required!**

The beauty of SQLAlchemy is that the same models and queries work with both MySQL and PostgreSQL. All existing code in:
- `app/models/*` - No changes
- `app/routers/*` - No changes
- `app/services/*` - No changes
- `app/schemas/*` - No changes

## Migration Steps (For New Developers)

### First Time Setup

1. **Start PostgreSQL:**
   ```bash
   docker-compose up -d
   ```

2. **Install dependencies:**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   ```

4. **Run migrations:**
   ```bash
   alembic upgrade head
   ```

5. **Seed database:**
   ```bash
   python seed.py
   ```

6. **Start server:**
   ```bash
   uvicorn app.main:app --reload
   ```

### Database Management

**Create new migration after model changes:**
```bash
alembic revision --autogenerate -m "description"
```

**Apply pending migrations:**
```bash
alembic upgrade head
```

**Rollback last migration:**
```bash
alembic downgrade -1
```

**Reset database (WARNING: deletes all data):**
```bash
docker-compose down -v
docker-compose up -d
alembic upgrade head
python seed.py
```

## Key Differences: MySQL vs PostgreSQL

### What Changed

1. **Connection String Format:**
   - MySQL: `mysql+pymysql://user:pass@host:port/db`
   - PostgreSQL: `postgresql://user:pass@host:port/db`

2. **Database Driver:**
   - MySQL: PyMySQL
   - PostgreSQL: psycopg2

3. **Enum Types:**
   - PostgreSQL creates native ENUM types (more strict)
   - MySQL uses string-based ENUMs

### What Stayed the Same

- All SQLAlchemy models
- All API endpoints
- All business logic
- All Pydantic schemas
- JWT authentication
- CORS configuration

## Testing Checklist

After migration, verify these scenarios:

- [ ] User registration and login
- [ ] Create/read/update/delete operations for all entities
- [ ] Search and filter operations
- [ ] Date-based vehicle availability
- [ ] Reservation creation with price calculation
- [ ] Payment processing
- [ ] Reservation state transitions (pending → confirmed → active → completed)
- [ ] Foreign key constraints (e.g., can't delete location with vehicles)
- [ ] Unique constraints (e.g., duplicate email/license plate)

## Rollback Plan

If PostgreSQL causes issues, you can rollback to MySQL:

1. Stop PostgreSQL: `docker-compose down`
2. Revert `requirements.txt`: change `psycopg2-binary` → `pymysql`
3. Revert `.env`: change DATABASE_URL to MySQL format
4. Set up MySQL: run `schema.sql` and `seed_data.sql`
5. Reinstall: `pip install -r requirements.txt`

However, this should not be necessary as no breaking changes were made to application code.

## Notes

- PostgreSQL is more strict with data types and constraints (this is good!)
- The migration maintains backward compatibility with existing API contracts
- All timestamps use UTC (PostgreSQL handles this natively)
- Connection pooling settings remain the same in `database.py`
