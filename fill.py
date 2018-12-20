import sys
from item_catalog import create_app, db
from item_catalog.models import Item, User

app = create_app()


if __name__ == '__main__':
    if '--setup' in sys.argv:
        with app.app_context():
            db.create_all()
            db.session.commit()
    u = User(username='exampleuser', email='example@example.com', name='John Doe')
    db.session.add(u)
    db.session.commit()
    print('Example user added to the database.')
    user = User.query.first()
    item_list = []
    item_list.append(Item(name='Basketball',
                          sport='Basketball',
                          category='Equipment',
                          description='An orange ball with black stripes.',
                          private=False,
                          user_id=user.id))
    item_list.append(Item(name='Baseball',
                          sport='Baseball',
                          category='Equipment',
                          description='A white ball with red stitches.',
                          private=False,
                          user_id=user.id))
    item_list.append(Item(name='Bowling Ball',
                          sport='Bowling',
                          category='Equipment',
                          description='It looks like a giant marble, and you throw it at pins.',
                          private=False,
                          user_id=user.id))
    item_list.append(Item(name='Jersey',
                          sport='Basketball',
                          category='Apparel',
                          description='A thin piece of material that smells funny.',
                          private=False,
                          user_id=user.id))
    item_list.append(Item(name='Baseball Bat',
                          sport='Baseball',
                          category='Equipment',
                          description='A long piece of aluminum that you swing.',
                          private=False,
                          user_id=user.id))
    item_list.append(Item(name='Set of Pins',
                          sport='Bowling',
                          category='Equipment',
                          description='Oddly shaped white things that are easy to tip over.',
                          private=False,
                          user_id=user.id))
    item_list.append(Item(name='Autographed Basketball',
                          sport='Basketball',
                          category='Fan Gear',
                          description='An orange ball with black stripes, like the others, but this one has ink on it.',
                          private=False,
                          user_id=user.id))
    item_list.append(Item(name='Baseball Cap',
                          sport='Baseball',
                          category='Apparel',
                          description='A nice little hat with a duckbill coming off of it.',
                          private=False,
                          user_id=user.id))
    item_list.append(Item(name='Pizza',
                          sport='Bowling',
                          category='Equipment',
                          description='An absolute necessity when playing the game. Best when shared with nobody.',
                          private=False,
                          user_id=user.id))
    item_list.append(Item(name='Football',
                          sport='Football',
                          category='Equipment',
                          description='A brown piece of leather that can\'t really be called a "ball".',
                          private=False,
                          user_id=user.id))
    item_list.append(Item(name='Soccer Ball',
                          sport='Soccer',
                          category='Equipment',
                          description='A white ball with black spots.',
                          private=False,
                          user_id=user.id))
    item_list.append(Item(name='Tennis Ball',
                          sport='Tennis',
                          category='Equipment',
                          description='A small ball that may be yellow or may be green, depending on who you ask.',
                          private=False,
                          user_id=user.id))
    item_list.append(Item(name='Shorts',
                          sport='Boxing',
                          category='Apparel',
                          description='Super tiny pants that are sure to be tight in bad places.',
                          private=False,
                          user_id=user.id))
    item_list.append(Item(name='Golf Ball',
                          sport='Golf',
                          category='Equipment',
                          description='A white ball that was raised by angry woodpeckers.',
                          private=False,
                          user_id=user.id))
    item_list.append(Item(name='Dentures',
                          sport='Hockey',
                          category='Accessories',
                          description='You don\'t need them yet, but you will.',
                          private=False,
                          user_id=user.id))
    item_list.append(Item(name='Helmet',
                          sport='Football',
                          category='Equipment',
                          description='A second skull to protect the smaller skull underneath.',
                          private=False,
                          user_id=user.id))
    item_list.append(Item(name='Pointed Stick',
                          sport='Other',
                          category='Equipment',
                          description='Great for fighting off an adversary wielding an unlicensed banana.',
                          private=False,
                          user_id=user.id))
    item_list.append(Item(name='Net',
                          sport='Tennis',
                          category='Equipment',
                          description='The barrier that protects players from having a good time.',
                          private=False,
                          user_id=user.id))
    item_list.append(Item(name='Hockey Stick',
                          sport='Hockey',
                          category='Equipment',
                          description='A poor substitute for the push-broom you really need.',
                          private=False,
                          user_id=user.id))
    item_list.append(Item(name='Ring',
                          sport='Football',
                          category='Accessories',
                          description='A chunk of metal bigger than your fist that you show off to everyone.',
                          private=False,
                          user_id=user.id))
    item_list.append(Item(name='Gloves',
                          sport='Boxing',
                          category='Equipment',
                          description='Basically the training wheels that keep competitors from finishing the job.',
                          private=False,
                          user_id=user.id))
    item_list.append(Item(name='Golf Cart',
                          sport='Golf',
                          category='Accessories',
                          description='A little car for those who have forgotten how to walk.',
                          private=False,
                          user_id=user.id))
    item_list.append(Item(name='Shoes',
                          sport='Soccer',
                          category='Apparel',
                          description='Spiky kicks that impale, rather than crush, the cockroaches in your home.',
                          private=False,
                          user_id=user.id))
    item_list.append(Item(name='Visor',
                          sport='Tennis',
                          category='Apparel',
                          description='The duckbill part of the baseball cap, isolated so your hair stays nice.',
                          private=False,
                          user_id=user.id))
    for item in item_list:
        db.session.add(item)
    db.session.commit()
    print('Database populated with items.')
