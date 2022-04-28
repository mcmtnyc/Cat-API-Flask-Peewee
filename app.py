from turtle import color
from flask import Flask, jsonify, request
from peewee import *
from playhouse.shortcuts import model_to_dict, dict_to_model

db = PostgresqlDatabase('cat', user='postgres',
                        password='', host='localhost', port=5423)


class BaseModel(Model):
    class Meta:
        database = db


class Cat(BaseModel):
    name = CharField()
    color = CharField()
    hasTail = BooleanField()


db.connect()
db.drop_tables([Cat])
db.create_tables([Cat])

Cat(name='Miau', color='black', hasTail=True).save()
Cat(name='Meow', color='white', hasTail=False).save()

app = Flask(__name__)


@app.route('/Cat/', methods=['GET', 'POST'])
@app.route('/Cat/<id>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(id=None):
    if request.method == 'GET':
        if id:
            return jsonify(model_to_dict(Cat.get(Cat.id == id)))
        else:
            catList = []
            for Cat in Cat.select():
                catList.append(model_to_dict(Cat))
            return jsonify(catList)

    if request.method == 'PUT':
        return 'PUT request'

    if request.method == 'POST':
        new_Cat = dict_to_model(Cat, request.get_json())
        new_Cat.save()
        return jsonify({"success": True})

    if request.method == 'DELETE':
        return 'DELETE request'


app.run(debug=True, port=9000)
