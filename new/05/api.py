from flask import Blueprint, request, abort, jsonify
import sqlalchemy.orm                       # ajax

from models import Category, Product

api = Blueprint('api', __name__)


@api.route('/product')
def products_for_category():
    try:
        category_id = int(request.args.get('category_id'))
        category = Category.query.filter(Category.id == category_id).one()
    except ValueError:
        # category_id not a number
        abort(404)
    except sqlalchemy.orm.exc.NoResultFound:
        # No category found for this id
        abort(404)

    products = Product.query.filter(Product.category_id == category_id).all()
    return jsonify([product.as_dict() for product in products])