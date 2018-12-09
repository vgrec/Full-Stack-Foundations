from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem


class RestaurantsRepository:
    def __init__(self):
        engine = create_engine('sqlite:///restaurantmenu.db')
        Base.metadata.bind = engine

        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def get_restaurants(self):
        return self.session.query(Restaurant).all()


r = RestaurantsRepository()
print(r.get_restaurants())