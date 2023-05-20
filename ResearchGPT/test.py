from sqlalchemy.orm import sessionmaker, Session
import models # Import your Base and models
from database import engine

Session = sessionmaker(bind=engine)
session: Session = Session()

# Delete url_data first
session.query(models.URLData).delete()

# Now you can delete tasks
session.query(models.Task).delete()

session.commit()
