from database_setup import Base, Category, CatalogItem
from flask import Flask, render_template, jsonify, request 
from flask import redirect, url_for, abort, g
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

engine = create_engine('sqlite:///itemcatalog.db')

Base.metadata.bind = engine
app = Flask(__name__)


def getSession():
    '''
    Open a database session.
    '''
    DBSession = sessionmaker(bind=engine)
    return DBSession()


def getAllCategories(session):
    '''
    Show all categories in the Catalog.
    '''
    return session.query(Category).all()


'''
HTTP request functions.
'''
@app.route('/')
@app.route('/catalog/')
def fullCatalog():
    '''
    Show the all catalog categories, and newest 10 items added.
    '''
    session = getSession()
    categories = getAllCategories(session)
    last_ten_items = session.query(CatalogItem) \
        .order_by(CatalogItem.id.desc()).limit(10).all()
    return render_template('catalog.html', categories=categories, 
        items=last_ten_items)


@app.route('/catalog/<category>/')
def catalogCategory(category):
    '''
    Show items in a catalog, and links to descriptions.
    '''
    session = getSession()
    cat = session.query(Category).filter_by(name=category).one()
    items = session.query(CatalogItem).filter_by(category_id=cat.id)
    categories = getAllCategories(session)
    return render_template('category.html', category=cat, items=items,
        categories=categories)


@app.route('/catalog/<category>/<item_name>/')
def categoryItem(category, item_name):
    '''
    Show name and description of a catalog item, and links to edit/delete.
    '''
    session = getSession()
    item = session.query(CatalogItem).filter_by(name=item_name).one()
    categories = getAllCategories(session)
    return render_template('catalogitem.html', category=category, item=item,
        categories=categories)


@app.route('/catalog/<category>/new/', methods=['GET', 'POST'])
def newCatalogItem(category):
    '''
    Add a new catalog item.
    '''
    session = getSession()
    cat = session.query(Category).filter_by(name=category).first()
    cat_id = cat.id
    if request.method == 'POST':
        newItem = CatalogItem(
            name=request.form['name'], category_id=cat_id,
            description=request.form['description'])
        session.add(newItem)
        session.commit()
        return redirect(url_for('catalogCategory', category=category))
    else:
        return render_template('newcatalogitem.html', category=category)


@app.route('/catalog/<category>/<item_name>/edit/', methods=['GET', 'POST'])
def editCatalogItem(category, item_name):
    '''
    Edit a catalog item.
    '''
    session = getSession()
    item = session.query(CatalogItem).filter_by(name=item_name).one()
    if request.method == 'POST':
        new_name = request.form['new_name']
        new_desc = request.form['new_description']
        if new_name:
            item.name = new_name
        if new_desc:
            item.description = new_desc
        session.add(item)
        session.commit()
        return redirect(url_for('categoryItem', category=category, 
            item_name=item.name))
    else:
        return render_template('editcatalogitem.html', category=category, 
            name=item_name, description=item.description)


@app.route('/catalog/<category>/<item_name>/delete/', methods=['GET', 'POST'])
def deleteCatalogItem(category, item_name):
    '''
    Delete a catalog item.
    '''
    session = getSession()
    item = session.query(CatalogItem).filter_by(name=item_name).one()
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        return redirect(url_for('catalogCategory', category=category))
    else:
        return render_template('deletecatalogitem.html', category=category, 
            item=item_name)


'''
API request functions.
'''
def getCategoryInfo(category):
    '''
    Get the serialized information of a category and related items.
    '''
    session = getSession()
    categories = set([c.name for c in session.query(Category).all()])
    for c in categories:
        if category == c:
            sport = session.query(Category).filter_by(name=c).first()
            items = session.query(CatalogItem).filter_by(category=sport).all()
            category_info = sport.serialize
            category_info['items'] = [i.serialize for i in items]

            return category_info


@app.route('/catalog.json/', methods = ['GET', 'POST'])
@app.route('/api/catalog/', methods = ['GET', 'POST'])
def showAllCatalogItems():
    '''
    Return json of full catalog.
    '''
    session = getSession()
    if request.method == 'GET':
        all_items = []
        categories = set([c.name for c in session.query(Category).all()])
        for c in categories:
            all_items.append(getCategoryInfo(c))
        return jsonify(categories = all_items)
    if request.method == 'POST':
        name = request.json.get('name')
        category = request.json.get('category')
        description = request.json.get('description')
        newItem = CatalogItem(name=name, category=category, 
            description=description)
        session.add(newItem)
        session.commit()
        return jsonify(newItem.serialize)


@app.route('/catalog.json/<category>/')
@app.route('/api/catalog/<category>/')
def showCategoriedItems(category):
    '''
    Return json of a category based on category name.
    '''
    category_info = getCategoryInfo(category)
    return jsonify(category = [category_info])


@app.route('/catalog.json/<int:category_id>/')
@app.route('/api/catalog/<int:category_id>/')
def showCategoriedIDItems(category_id):
    '''
    Return json of a category based on category id.
    '''
    session = getSession()
    category = session.query(Category).filter_by(id=category_id).first()
    return showCategoriedItems(category.name)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
