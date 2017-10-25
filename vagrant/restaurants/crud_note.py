from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)

session = DBSession()

myRestaurant = Restaurant(name = 'Pizza Palace')

session.add(myRestaurant)
session.commit()
session.query(Restaurant).all()

myItem = MenuItem(
    name = "Chess Pizza",
    description = 'Made with all natural ingredients and fresh mozzarella',
    course = 'Entree',
    price = '$8.99',
    restaurant = myRestaurant
    )

session.add(myItem)
session.commit()
session.query(MenuItem).all()

result = session.query(Restaurant).first()
result.name

items = session.query(MenuItem).all()
for item in items:
  print item.name

items = session.query(MenuItem).filter_by(name = 'Veggie Burger')
for item in items:
  print item.id
  print item.price
  print item.restaurant.name
  print "\n"

item = session.query(MenuItem).filter_by(id = 1).one()
print item.price
item.price = '$2.99'
session.add(item)
session.commit()

items = session.query(MenuItem).filter_by(name = 'Veggie Burger')
for item in items:
  if item.price != '$2.99':
    item.price = '$2.99'
    session.add(item)
    session.commit()

item = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()
print spinach.restaurant.name
session.delete(item)
session.commit()

