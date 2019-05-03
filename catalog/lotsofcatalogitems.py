from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, CatalogItem


def create_session():
    engine = create_engine('sqlite:///itemcatalog.db')
    # Bind the engine to the metadata of the Base class so that the
    # declaratives can be accessed through a DBSession instance
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    # A DBSession() instance establishes all conversations with the database
    # Any change made against the objects in the session won't be persisted
    # into the database until you call session.commit().
    # Can revert all of them back to the last commit with session.rollback()
    session = DBSession()

    return session


def add_commit(session, entry):
    # Stage the entry
    session.add(entry)
    # Commit the entry
    session.commit()
    return


def create_category(session, cat_name):
    # Create a new category
    category = Category(name=cat_name)
    # Add and commit the category
    add_commit(session, category)
    return category


def create_item(session, item_name, desc, cat_name):
    # Create a new item
    catalogItem = CatalogItem(name=item_name, description=desc,
                              category=cat_name)
    # Add and commit the item
    add_commit(session, catalogItem)
    return


# Items for Soccer
def create_soccer(session):
    # Parallel lists to hold names & descriptions
    items = [
        "Soccer ball",
        "Soccer jerseys",
        "Soccer shorts",
        "Soccer socks",
        "Shin guards",
        "Soccer cleats",
        "Soccer goalie gloves"
        ]
    descriptions = [
        "A classic soccer ball with black and white hexagon and pentagons.",
        "A soccer jersey with a number on the back.",
        "A pair of black shorts.",
        "A pair of colorful socks.",
        "A comfortable pair of shin guards to protest your shins.",
        "A pair of black soccer cleats.",
        "A pair of goalie gloves, in various colors."
        ]

    # Create the category, add and commit
    category = create_category(session, "Soccer")

    # Create category items, add and commit
    for i in range(len(items)):
        create_item(session, items[i], descriptions[i], category)

    return


# Items for Football
def create_football(session):
    # Parallel lists to hold names & descriptions
    items = [
        "Football",
        "Shoulder pads",
        "Football jersey",
        "Football pants",
        "Pants pads",
        "Football cleats",
        "Football socks",
        "Football helmet"
        ]
    descriptions = [
        "A classic leather football.",
        "Shoulder pads for fitting under a football jersey.",
        "A football jersey with a number on the back.",
        "A pair of white football pants.",
        "Pads to fit into football pants",
        "A pair of black football cleats.",
        "A pair of colorful socks.",
        "A white football helmet."
        ]

    # Create the category, add and commit
    category = create_category(session, "Football")

    # Create category items, add and commit
    for i in range(len(items)):
        create_item(session, items[i], descriptions[i], category)

    return


# Items for Baseball
def create_baseball(session):
    # Parallel lists to hold names & descriptions
    items = [
        "Bat",
        "Glove",
        "Baseball",
        "Baseball jersey",
        "Baseball pants",
        "Baseball cleats",
        "Baseball socks"
        ]
    descriptions = [
        "A metal baseball bat.",
        "A leather baseball glove.",
        "A classic baseball with red seams.",
        "A baseball jersey with a number on the back.",
        "A pair of white baseball pants.",
        "A pair of black baseball cleats.",
        "A pair of colorful socks."
        ]

    # Create the category, add and commit
    category = create_category(session, "Baseball")

    # Create category items, add and commit
    for i in range(len(items)):
        create_item(session, items[i], descriptions[i], category)

    return


# Items for Basketball
def create_basketball(session):
    # Parallel lists to hold names & descriptions
    items = [
        "Basketball",
        "Basketball jersey",
        "Basketball shorts",
        "Basketball socks",
        "Basketball shoes"
        ]
    descriptions = [
        "A classic brown basketball with black seams.",
        "A jersey with a number on the back.",
        "A pair of colorful shorts.",
        "A pair of colorful socks.",
        "A pair of colorful basketball shoes."
        ]

    # Create the category, add and commit
    category = create_category(session, "Basketball")

    # Create category items, add and commit
    for i in range(len(items)):
        create_item(session, items[i], descriptions[i], category)

    return


# Items for Hockey
def create_hockey(session):
    # Parallel lists to hold names & descriptions
    items = [
        "Skates",
        "Hockey helmet",
        "Hockey pads",
        "Hockey jersey",
        "Hockey pants",
        "Hockey socks",
        "Hockey stick",
        "Hockey goalie pads",
        "Hockey goalie glove"
        ]
    descriptions = [
        "A pair of hockey skates.",
        "A white hockey helmet.",
        "Shoulder and pants pads for a hockey player.",
        "A dark-colored hockey jersey.",
        "A light-colored pair of hockey pants.",
        "A colorful pair of hockey socks.",
        "A hockey stick.",
        "Large pads for a hockey goalie.",
        "A large glove for a hockey goalie."
        ]

    # Create the category, add and commit
    category = create_category(session, "Hockey")

    # Create category items, add and commit
    for i in range(len(items)):
        create_item(session, items[i], descriptions[i], category)

    return


def main():
    session = create_session()
    create_soccer(session)
    create_football(session)
    create_baseball(session)
    create_basketball(session)
    create_hockey(session)

    print "Added catalog items!"
    return


if __name__ == "__main__":
    main()
