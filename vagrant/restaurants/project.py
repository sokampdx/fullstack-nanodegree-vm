from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

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
    new_item = MenuItem(name=request.form['name'], restaurant_id=restaurant_id)
    session.add(new_item)
    session.commit()
    flash("New menu item " + new_item.name + " created!")
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
    if item_name:
      item.name = item_name
      session.add(item)
      session.commit()
      flash(item_name + " has been edited!")
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

  return "page to delete a menu item. Task 3 complete!"

if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host='0.0.0.0', port=5000)
