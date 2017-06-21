from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# # Making an API Endpoint (GET Request)
# @app.route('/restaurants/<int:restaurant_id>/menu/JSON')
# def restaurantMenuJSON(restaurant_id):
#     restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
#     items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
#     return jsonify(MenuItems=[i.serialize for i in items])
#
# @app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
# def restaurantMenuItemJSON(restaurant_id, menu_id):
#     menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
#     return jsonify(MenuItem=[menuItem.serialize])

# List restaurants
@app.route('/')
@app.route('/restaurants/')
def restaurantList():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', items=restaurants)

# New restaurant
@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'])
        session.add(newRestaurant)
        session.commit()
        flash("new restaurant created!")
        return redirect(url_for('restaurantList'))
    else:
        return render_template('newRestaurant.html')

# Edit Restaurant Name
@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurantName(restaurant_id):
    editedItem = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        flash("restaurant name edited")
        return redirect(url_for('restaurantList'))
    else:
        return render_template('editRestaurantName.html', restaurant_id=restaurant_id, item=editedItem)

# Delete Restaurant
@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    deletedItem = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        flash("yucky restaurant deleted")
        return redirect(url_for('restaurantList'))
    else:
        return render_template('deleteRestaurant.html', restaurant_id=restaurant_id, item=deletedItem)

# # New Menu Item
# @app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET', 'POST'])
# def newMenuItem(restaurant_id):
#     if request.method == 'POST':
#         newItem = MenuItem(name=request.form['name'], restaurant_id=restaurant_id)
#         session.add(newItem)
#         session.commit()
#         flash("new menu item created!")
#         return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
#     else:
#         return render_template('newMenuItem.html', restaurant_id=restaurant_id)
#
# # Edit Menu Item
# @app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
# def editMenuItem(restaurant_id, menu_id):
#     editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
#     if request.method == 'POST':
#         if request.form['name']:
#             editedItem.name = request.form['name']
#         session.add(editedItem)
#         session.commit()
#         flash("menu name edited")
#         return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
#     else:
#         return render_template('editMenuItem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)
#
# # Delete Menu Item
# @app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
# def deleteMenuItem(restaurant_id, menu_id):
#     deletedItem = session.query(MenuItem).filter_by(id=menu_id).one()
#     if request.method == 'POST':
#         session.delete(deletedItem)
#         session.commit()
#         flash("yucky menu item deleted")
#         return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
#     else:
#         return render_template('deleteMenuItem.html', restaurant_id=restaurant_id, item=deletedItem)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
