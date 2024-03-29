from flask import Flask,request,jsonify
from flask_restx import Api,Resource,fields
from config import DevConfig
from models import Dsm,User,Store,Sku,Role
from exts import db
from flask_sqlalchemy import SQLAlchemy

 
app=Flask(__name__)

app.config.from_object(DevConfig)

db.init_app(app)

api=Api(app,doc='/docs')


@api.route('/login',methods=['GET'])
class Login(Resource):
    def get(self):
        return {'status': 'success'}



user_model = api.model(
    "User",{
        "id":fields.Integer(),
        "userid":fields.String(),
        "roleid":fields.Integer(),
        "first_name":fields.String(),
        "last_name":fields.String(),
        "address":fields.String(),
        "contact_number":fields.String(),
        "date_updated":fields.String(),
        "date_created":fields.String()
    }
)


@api.route('/users')
class UsersResource(Resource):

    @api.marshal_list_with(user_model)
    def get(self):
        """ Get all the users """
        users = User.query.all();
        return users    
 
    @api.marshal_with(user_model)
    def post(self):
        """ Create new User """
        data = request.get_json()
 
        new_user = User(
            userid=data['userid'],
            roleid=data['roleid'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            address=data['address'],
            contact_number=data['contact_number'],
            date_updated='now()',
        )

        new_user.save()
        return new_user,201
    

@api.route('/user/<string:id>')
class UsersResource(Resource):

    @api.marshal_with(user_model)
    def get(self,id):
        """ Get User info """

        user = User.query.get_or_error(id) 
        return user
    
    def put(self,id):
        """ Update User """

        # raw_user = User.query.get(id) 
        raw_user = User.query.get_or_error(id) 
        data = request.get_json()
        raw_user.update(data['roleid'],data['first_name'],data['last_name'],data['address'],data['contact_number'],data['date_updated'])
        return {
            'status':'success',
            'message': 'Successfullly updated',
            'data' : { 
                'id':raw_user.id,
                'roleid':raw_user.roleid,
                'first_name':raw_user.first_name,
                'last_name':raw_user.last_name,
                'address':raw_user.address,
                'contact_number':raw_user.contact_number,
                'date_created':raw_user.date_created.strftime('%m/%d/%Y'),
                'date_updated':raw_user.date_updated.strftime('%m/%d/%Y'),
            }
        }
 
    def delete(self,id):
        """ Delete User """
        raw_user = User.query.get_or_error(id) 
        raw_user.delete()

        return {
            'status':'success',
            'message': 'successfullly deleted', 
        }


store_model = api.model(
    "Store",{
        "id":fields.Integer(), 
        "storeid":fields.Integer(), 
        "name":fields.String(), 
        "area":fields.Integer(), 
        "channel":fields.Integer(), 
        "date_updated":fields.String(),
        "date_created":fields.String(),
    }
)


sku_model = api.model(
    "Sku",{
        "id":fields.Integer(), 
        "skuid":fields.String(), 
        "name":fields.String(), 
        "category":fields.String(), 
        "brand":fields.String(), 
        "price_piece":fields.Integer(), 
        "price_case":fields.Integer(), 
        "date_updated":fields.String(),
        "date_created":fields.String()
    }
)

role_model = api.model(
    "Role",{
        "id":fields.Integer(),
        "roleid":fields.String(), 
        "name":fields.String(), 
        "date_updated":fields.String(),
        "date_created":fields.String()
    }
)


@app.shell_context_processor
def make_shell_context():
    return {
        "db":db,
        "Dsm":Dsm,
        "User":User,
        "Store":Store,
        "Sku":Sku,
        "Role":Role,
    }

if __name__ == '__main__':
    app.run()