from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from models import ItemModel, StoreModel
from db import db
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get(item_id)
        if item is None:
            abort(404, message="Item not found")
        return item

    def delete(self, item_id):
        item = ItemModel.query.get(item_id)
        if item is None:
            abort(404, message="Item not found")

        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted"}

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item is None:
            abort(404, message="Item not found")

        if "name" in item_data:
            item.name = item_data["name"]
        if "price" in item_data:
            item.price = item_data["price"]

        db.session.commit()
        return item


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        store = StoreModel.query.get(item_data["store_id"])
        if store is None:
            abort(404, message="Store not found")

        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")
        return item
