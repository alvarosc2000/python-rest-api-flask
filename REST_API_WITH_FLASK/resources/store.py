from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from models import StoreModel, ItemModel, TagModel
from db import db
from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get(store_id)
        if store is None:
            abort(404, message="Store not found")
        return store

    def delete(self, store_id):
        store = StoreModel.query.get(store_id)
        if store is None:
            abort(404, message="Store not found")

        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted"}

    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def put(self, store_data, store_id):
        store = StoreModel.query.get(store_id)
        if store is None:
            abort(404, message="Store not found")

        store.name = store_data["name"]
        db.session.commit()
        return store



@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        if StoreModel.query.filter_by(name=store_data["name"]).first():
            abort(400, message="Store already exists")

        items_data = store_data.pop("items", [])
        tags_data = store_data.pop("tags", [])

        store = StoreModel(name=store_data["name"])
        
        # Asignar items y tags con relación directa
        store.items = [ItemModel(name=item["name"], price=item["price"]) for item in items_data]
        store.tags = [TagModel(name=tag["name"]) for tag in tags_data]

        db.session.add(store)

        try:
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=f"An error occurred while inserting the store and its relations: {str(e)}")

        return store
