from database_setup import Restaurant, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class RestaurantsRepository:
    def __init__(self):
        engine = create_engine('sqlite:///restaurantmenu.db')
        Base.metadata.bind = engine

        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def get_restaurants(self):
        return self.session.query(Restaurant).all()

    def new_restaurant(self, restaurant_name):
        self.session.add(Restaurant(name=restaurant_name))
        self.session.commit()


r = RestaurantsRepository()
r.new_restaurant("Alibaba")
