from flask import Flask
from flask import render_template
from restaurants_repository import RestaurantsRepository

app = Flask(__name__)


@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def home(restaurant_id):
    repository = RestaurantsRepository()
    items = repository.get_menu(restaurant_id)
    output = ""
    for item in items:
        output += item.name
        output += "<br/>"
        output += item.price
        output += "<br/>"
        output += item.description
        output += "<br/> <br/>"
    return output


@app.route('/restaurant/<int:restaurant_id>/new/')
def new_menu_item(restaurant_id):
    return "page to create a new menu item. Task 1 complete!"


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/')
def edit_menu_item(restaurant_id, menu_id):
    return "page to edit a menu item. Task 2 complete!"


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/')
def delete_menu_item(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"


@app.route('/template/')
def template():
    return render_template("menu.html", item="Pasta")


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
