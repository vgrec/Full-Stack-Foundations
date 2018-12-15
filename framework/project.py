from flask import Flask
from flask import render_template
from flask import request, url_for, redirect
from restaurants_repository import RestaurantsRepository
from database_setup import MenuItem

app = Flask(__name__)


@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def home(restaurant_id):
    repository = RestaurantsRepository()
    items = repository.get_menu(restaurant_id)
    restaurant = repository.get_restaurant_by_id(restaurant_id)
    return render_template('menu.html', restaurant=restaurant, items=items)


@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def new_menu_item(restaurant_id):
    if request.method == 'POST':
        repository = RestaurantsRepository()
        new_item = MenuItem(
            name=request.form['name'],
            description=request.form['description'],
            price=request.form['price'],
            restaurant_id=restaurant_id)
        repository.new_menu_item(new_item)
        return redirect(url_for('home', restaurant_id=restaurant_id))
    else:
        return render_template("new_menu_item.html", restaurant_id=restaurant_id)


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
