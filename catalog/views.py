from database_setup import Base, Category, CatalogItem
from flask import Flask, jsonify, request, url_for, abort, g
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

engine = create_engine('sqlite:///itemcatalog.db')

Base.metadata.bind = engine
app = Flask(__name__)


def getCategoryInfo(category):
    '''
    Get the serialized information of a category and related items.
    '''
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    categories = set([c.name for c in session.query(Category).all()])
    for c in categories:
        if category == c:
            sport = session.query(Category).filter_by(name=c).first()
            items = session.query(CatalogItem).filter_by(category=sport).all()
            category_info = sport.serialize
            category_info['items'] = [i.serialize for i in items]

            return category_info


@app.route('/catalog.json', methods = ['GET', 'POST'])
@app.route('/api/catalog', methods = ['GET', 'POST'])
def showAllCatalogItems():
    '''
    Return json of full catalog.
    '''
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
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


@app.route('/catalog.json/<category>')
@app.route('/api/catalog/<category>')
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
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    category = session.query(Category).filter_by(id=category_id).first()
    return showCategoriedItems(category.name)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
