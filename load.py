from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timezone
import logging

Base = declarative_base()
logging.basicConfig(filename="pipeline.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

class local_database(Base): 
    __tablename__ = 'local_database'
    id = Column(Integer, primary_key=True, unique=True)
    transaction_id = Column(Integer)
    date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    customer_name = Column(String)
    item = Column(String)
    quantity = Column(Integer)
    unit_price = Column(Float)
    total_amount = Column(Float)
    status = Column(String)

def process(payload, session):
    for transaction in payload:
        try:
            submission = local_database(transaction_id=transaction["Transaction_ID"], date=transaction["Date"], customer_name=transaction["Customer_Name"], item=transaction["Item_Purchased"], quantity=transaction["Quantity"], unit_price=transaction["Unit_Price"], total_amount=transaction["Total_Amount"], status=transaction["Status"])
            session.add(submission)
        except SQLAlchemyError as e:
            logger.error(f"Error creating database entry for transaction {transaction['Transaction_ID']}: {e}")
            continue

def initialize_db():
    try:
        engine = create_engine('sqlite:///load_db.db')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        session = Session()
        return session
    except SQLAlchemyError as e:
        logger.error(f"Error initializing database: {e}")
        return None

