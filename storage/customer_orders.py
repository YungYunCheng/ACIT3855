from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class CustomerOrder(Base):
    """ Customer Orders """

    __tablename__ = "customer_orders"

    id = Column(Integer,  primary_key=True)
    order_id = Column(String(250), nullable=False)
    device_id = Column(String(250), nullable=False)
    releaseDate = Column(String(100), nullable=False)
    date_created = Column(DateTime, nullable=False)
    num_of_prduct = Column(Integer, nullable=False)
    product_name = Column(String(100), nullable=False)

    def __init__(self, order_id, device_id, releaseDate, num_of_prduct, product_name):
        """ Initializes a blood pressure reading """
        self.order_id = order_id
        self.device_id = device_id
        self.releaseDate = releaseDate
        self.date_created = datetime.datetime.now()
        self.num_of_prduct = num_of_prduct
        self.product_name = product_name

    def to_dict(self):
        """ Dictionary Representation of a blood pressure reading """
        dict = {}
        dict['id'] = self.id
        dict['order_id'] = self.order_id
        dict['device_id'] = self.device_id
        dict['product'] = {}
        dict['product']['num_of_prduct'] = self.num_of_prduct
        dict['product']['product_name'] = self.product_name
        dict['releaseDate'] = self.releaseDate
        dict['date_created'] = self.date_created

        return dict
