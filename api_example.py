from flask import Flask
from flask_restful import Resource, Api, reqparse

# create app
app = Flask(__name__)

# create api
api = Api(app)

items = []

# create item endpoint
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    def get(self, name):
        matched_items = [item for item in items if item['name'] == name]
        if not matched_items:
            return {'item': None}
        
        return {'item': matched_items[0]}

    def post(self, name):
        matched_items = [item for item in items if item['name'] == name]
        
        if matched_items:
            return {'message': f"An item with name '{name}' already exists."}

        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}
        items.append(item)
        
        return {
            'message': 'Item created',
            'item': item
        }

    def delete(self, name):
        global items
        items = [item for item in items if item['name'] != name]
        
        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()
        
        matched_items = [item for item in items if item['name'] == name]
        if not matched_items:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            matched_items[0].update(data)
        
        return {'message': 'Item updated'}


# create items endpoinnt
class ItemList(Resource):
    def get(self):
        return {'items': items}

# register endpoints
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

if __name__ == '__main__':
    app.run(debug=True)