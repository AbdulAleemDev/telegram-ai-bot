from app.database.base import Base
from app.core.database import engine
from app.database.models import CustomerOrder, Order, Ticket

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Done.")