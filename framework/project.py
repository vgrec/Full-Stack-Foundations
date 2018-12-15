from flask import Flask
from flask import render_template
from flask import request, url_for, redirect, flash
from restaurants_repository import RestaurantsRepository
from database_setup import MenuItem

app = Flask(__name__)


@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def home(restaurant_id):
    repository = RestaurantsRepository()
    items = repository.get_restaurant_menu(restaurant_id)
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
        flash("New menu item created!")
        return redirect(url_for('home', restaurant_id=restaurant_id))
    else:
        return render_template("new_menu_item.html", restaurant_id=restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def edit_menu_item(restaurant_id, menu_id):
    repository = RestaurantsRepository()
    menu = repository.get_menu_by_id(restaurant_id, menu_id)
    if request.method == 'POST':
        edited_item = MenuItem(
            id=menu_id,
            name=request.form['name'],
            description=request.form['description'],
            price=request.form['price'],
            restaurant_id=restaurant_id)
        repository.update_menu_item(edited_item)
        return redirect(url_for('home', restaurant_id=restaurant_id))
    else:
        return render_template('edit_menu_item.html', restaurant_id=restaurant_id, menu=menu)


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/')
def delete_menu_item(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"


@app.route('/template/')
def template():
    return render_template("menu.html", item="Pasta")


if __name__ == '__main__':
    app.secret_key = "test_key"
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
