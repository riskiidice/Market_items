# -*- coding: utf-8 -*-
import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    @jwt_required()
    def get(self, name):
        # item = next(filter(lambda x: x['name'] == name, items), None)
        item = ItemModel.find_by_name(name)

        if item:
            return item.json()

        return {'message': 'Item not found'}, 404


    def post(self, name):

        # if next(filter(lambda x: x['name'] == name, items), None):
        #     return {'message': "มีสินค้าชื่อ '{}' แล้วในระบบ".format(name)}, 400

        if ItemModel.find_by_name(name):
             return {'message': "มีสินค้าชื่อ '{}' แล้วในระบบ".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'])
        # items.append(item)
        try:
            item.save_to_db()
        except:
            return {'message': 'An error occur inserting the item'}, 500

        return item.json(), 201


    def delete(self, name):
        # global items
        # items = list(filter(lambda x: x['name'] != name, items))
        item = Item.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    def put(self, name):

        # item = next(filter(lambda x: x['name'] == name, items), None)

        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        updated_item = ItemModel(name, data['price'])

        if item is None:
            # item = { 'name':name, 'price': data['price']}
            # items.append(item)
            item = ItemModel(name, data['price'])
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):

        return {'items' :[item.json() for item in ItemModel.query.all()] }
