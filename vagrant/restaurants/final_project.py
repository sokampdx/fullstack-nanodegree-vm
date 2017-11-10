from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/restaurants')
def show_restaurants():
  restaurants = session.query(Restaurant)
  return render_template('restaurants.html', restaurants=restaurants)

@app.route('/restaurants/JSON')
def restaurant_json():
  restaurants = session.query(Restaurant)
  return jsonify(Restaurant=[r.serialize for r in restaurants])

@app.route('/restaurants/new', methods=['GET', 'POST'])
def newRestaurant():
  if request.method == 'POST':
    restaurant = Restaurant(name=request.form['name'])
    session.add(restaurant)
    session.commit()
    flash("New restaurant " + restaurant.name + " created!")
    return redirect(url_for('show_restaurants'))
  else:
    return render_template('newrestaurant.html')

@app.route('/restaurants/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
  restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
  if request.method == 'POST':
    restaurant_old_name = restaurant.name
    restaurant_name = request.form['name']
    if restaurant_name:
      restaurant.name = restaurant_name
      session.add(restaurant)
      session.commit()
      flash(restaurant_old_name + " is now " + restaurant_name)
    return redirect(url_for('show_restaurants'))
  else:
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    return render_template('editrestaurant.html', restaurant=restaurant)

@app.route('/restaurants/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
  restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
  restaurant_name = restaurant.name
  if request.method == 'POST':
    session.delete(restaurant)
    session.commit()
    flash(restaurant_name + " has been deleted!")
    return redirect(url_for('show_restaurants'))
  else:
    return render_template('deleterestaurant.html', restaurant=restaurant)

@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu')
def restaurant_menu(restaurant_id):
  restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
  items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
  return render_template('menu.html', restaurant=restaurant, items=items)

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurant_menu_json(restaurant_id):
  restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
  items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
  return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menu_item_json(restaurant_id, menu_id):
  item = session.query(MenuItem).filter_by(id=menu_id).one()
  return jsonify(MenuItem=item.serialize)

# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
  if request.method == 'POST':
    item = MenuItem(name=request.form['name'], restaurant_id=restaurant_id)
    item.description = request.form['description']
    item.price = request.form['price']
    session.add(item)
    session.commit()
    flash("New menu item " + item.name + " created!")
    return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
  else:
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    return render_template('newmenuitem.html', restaurant=restaurant)

# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
  item = session.query(MenuItem).filter_by(id=menu_id).one()
  if request.method == 'POST':
    item_old_name = item.name
    item_name = request.form['name']
    item_description = request.form['description']
    item_price = request.form['price']
    if item_name or item_description or item_price:
      if item_name:
        item.name = item_name
        flash(item_old_name + " has been renamed to " + item.name)
      if item_description:
        item.description = item_description
        flash(item_old_name + " description has changed")
      if item_price:
        item.price = item_price
        flash(item_old_name + " has changed its price to " + item.price)
      session.add(item)
      session.commit()
    return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
  else:
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    return render_template('editmenuitem.html', restaurant=restaurant, item=item)

# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
  item = session.query(MenuItem).filter_by(id=menu_id).one()
  item_name = item.name
  if request.method == 'POST':
    session.delete(item)
    session.commit()
    flash(item_name + " has been deleted!")
    return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
  else:
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
  return render_template('deletemenuitem.html', restaurant=restaurant, item=item)

if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host='0.0.0.0', port=5000)
