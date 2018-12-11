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

    def get_restaurant_by_id(self, id):
        return self.session.query(Restaurant).filter_by(id=id).first()

    def update_restaurant(self, id, name):
        restaurant = self.get_restaurant_by_id(id)
        restaurant.name = name
        self.session.commit()

r = RestaurantsRepository()

r.update_restaurant(3, "Hola")

print(r.get_restaurant_by_id(3).name)
