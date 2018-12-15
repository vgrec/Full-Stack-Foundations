from database_setup import Restaurant, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from restaurants.framework.database_setup import MenuItem


class RestaurantsRepository:
    def __init__(self):
        engine = create_engine('sqlite:///restaurantmenu.db')
        Base.metadata.bind = engine

        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

    def get_restaurants(self):
        return self.session.query(Restaurant).all()

    def get_restaurant_menu(self, restaurant_id):
        return self.session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()

    def get_menu_by_id(self, restaurant_id, menu_id):
        return self.session.query(MenuItem).filter_by(
            restaurant_id=restaurant_id,
            id=menu_id).one()

    def get_restaurant_by_id(self, id):
        return self.session.query(Restaurant).filter_by(id=id).first()

    def new_restaurant(self, restaurant_name):
        self.session.add(Restaurant(name=restaurant_name))
        self.session.commit()

    def new_menu_item(self, menu_item):
        self.session.add(menu_item)
        self.session.commit()

    def update_restaurant(self, id, name):
        restaurant = self.get_restaurant_by_id(id)
        restaurant.name = name
        self.session.commit()

    def update_menu_item(self, menu_item):
        old_menu = self.get_menu_by_id(menu_item.restaurant_id, menu_item.id)
        old_menu.name = menu_item.name
        old_menu.description = menu_item.description
        old_menu.price = menu_item.price
        self.session.commit()


r = RestaurantsRepository()

items = r.get_restaurant_menu(1)
for item in items:
    print(item.name)
