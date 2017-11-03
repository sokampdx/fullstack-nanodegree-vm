from flask import Flask, render_template, request, redirect, url_for
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

# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
  if request.method == 'POST':
    new_item = MenuItem(name=request.form['name'], restaurant_id=restaurant_id)
    session.add(new_item)
    session.commit()
    return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
  else:
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    return render_template('newmenuitem.html', restaurant=restaurant)

# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
  edit_item = session.query(MenuItem).filter_by(id=menu_id).one()
  if request.method == 'POST':
    item_name = request.form['name']
    if item_name:
      edit_item.name = item_name
      session.add(edit_item)
      session.commit()
    return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
  else:
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    return render_template('editmenuitem.html', restaurant=restaurant, edit_item=edit_item)

# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
  return "page to delete a menu item. Task 3 complete!"

if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0', port=5000)