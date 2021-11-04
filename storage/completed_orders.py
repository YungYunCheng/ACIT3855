from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class CompletedOrder(Base):
    """ Completed Order """

    __tablename__ = "completed_orders"

    id = Column(Integer, primary_key=True)
    order_id = Column(String(250), nullable=False)
    completedDate = Column(String(100), nullable=False)
    device_id = Column(String(250), nullable=False)
    date_created = Column(DateTime, nullable=False)
    status = Column(String(250), nullable=False)

    def __init__(self, order_id, completedDate, device_id, status):
        """ Initializes a heart rate reading """
        self.order_id = order_id
        self.completedDate = completedDate
        self.device_id = device_id
        self.status = status
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        """ Dictionary Representation of a heart rate reading """
        dict = {}
        dict['id'] = self.id
        dict['order_id'] = self.order_id
        dict['completedDate'] = self.completedDate
        dict['device_id'] = self.device_id
        dict['status'] = self.status
        dict['date_created'] = self.date_created

        return dict
