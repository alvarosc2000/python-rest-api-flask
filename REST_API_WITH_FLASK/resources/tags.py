from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import TagSchema, TagUpdateSchema
from models.tags import TagModel
from models.store import StoreModel
from db import db

blp = Blueprint("tags", __name__, description="Operations on tags")


@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        print(f"DEBUG: GET /tag/{tag_id} llamado")
        tag = TagModel.query.get(tag_id)
        if not tag:
            print(f"DEBUG: Tag con id {tag_id} no encontrado")
            abort(404, message="Tag not found")
        return tag

    def delete(self, tag_id):
        print(f"DEBUG: DELETE /tag/{tag_id} llamado")
        tag = TagModel.query.get(tag_id)
        if not tag:
            print(f"DEBUG: Tag con id {tag_id} no encontrado para borrar")
            abort(404, message="Tag not found")
        db.session.delete(tag)
        db.session.commit()
        return {"message": "Tag deleted"}

    @blp.arguments(TagUpdateSchema)
    @blp.response(200, TagSchema)
    def put(self, tag_data, tag_id):
        print(f"DEBUG: PUT /tag/{tag_id} llamado con datos {tag_data}")
        tag = TagModel.query.get(tag_id)
        if not tag:
            print(f"DEBUG: Tag con id {tag_id} no encontrado para actualizar")
            abort(404, message="Tag not found")

        if "name" in tag_data:
            tag.name = tag_data["name"]

        db.session.commit()
        return tag


@blp.route("/tag")
class TagList(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self):
        print("DEBUG: GET /tag llamado")
        return TagModel.query.all()

    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data):
        print(f"DEBUG: POST /tag llamado con datos {tag_data}")

        store = StoreModel.query.get(tag_data["store_id"])
        if not store:
            print(f"DEBUG: Store con id {tag_data['store_id']} no encontrada")
            abort(404, message="Store not found")

        existing_tag = TagModel.query.filter_by(
            name=tag_data["name"], 
            store_id=tag_data["store_id"]
        ).first()

        if existing_tag:
            print(f"DEBUG: Tag '{tag_data['name']}' ya existe en la tienda")
            abort(400, message=f"Tag '{tag_data['name']}' already exists in this store.")

        tag = TagModel(**tag_data)
        db.session.add(tag)
        db.session.commit()

        print(f"DEBUG: Tag creado con id {tag.id}")
        return tag
