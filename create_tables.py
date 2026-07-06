from app.core.database import engine
from app.database.base import Base

# Import all models
from app.database.models import CustomerOrder, Ticket

# Create all tables
Base.metadata.create_all(bind=engine)

print("✅ Tables created successfully!")