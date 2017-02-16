#!/usr/bin/python
"""
Add docstring here
"""
from flask.ext.restful_swagger_2 import Resource, swagger
from flask_restful import reqparse
from qube.src.api.swagger_models.parameters \
    import header_ex, path_ex, query_ex
from qube.src.api.swagger_models.response_messages \
    import response_msgs
from qube.src.commons.log import Log as LOG
from flask import  request
from qube.src.models.hello import Hello
from mongoalchemy.exceptions import DocumentException, MissingValueException, ExtraValueException, FieldNotRetrieved, BadFieldSpecification



params = [header_ex, path_ex, query_ex]


class HelloItemResource(Resource):
    @swagger.doc(
        {
            'tags': ['Hello World'],
            'description': 'hello world get operation',
            'parameters': params,
            'responses': response_msgs
        }
    )
    
  
    def get(self, id):
        LOG.debug("hello world")

        parser = reqparse.RequestParser()
        #parser.add_argument('id')
        args = parser.parse_args()
        data = Hello.query.get(id)
        if data is None:
            return 'not found', 404
            
        hello_data = data.wrap()
        #normalize the name for 'id'
        if '_id' in hello_data:
            hello_data['id'] = str(hello_data['_id'])
            del hello_data['_id']

        return hello_data
        
    @swagger.doc(
        {
            'tags': ['Hello World'],
            'description': 'hello world update operation',
            'responses': response_msgs
        }
    ) 
    def put(self, id):
        """
        Update.
        """
        # Validate request body with schema model
        hello_data = None


        try:
            #data = Hello(**request.get_json())
            data = request.get_json()
            #hello_data = Hello(data)
            old_hello = Hello.query.get(id)
            
            if old_hello is None:
                return 'not found', 404
            
            #old_hello.update(data)
            old_hello_dic = old_hello.wrap()
            old_hello_dic.update(data)
            hello = old_hello.unwrap(old_hello_dic)
            hello.save()
            return '', 204, {'Location': request.path + '/' + str(old_hello.mongo_id)}

        except e:
            return e.args[0], 400

     
        return 'unexpected error', 500
    
    def delete(self, id):
        """
        Delete.
        """
        try:
            #data = Hello(**request.get_json())
            data = request.get_json()
            #hello_data = Hello(data)
            hello = Hello.query.get(id)
            if hello is None:
                return 'not found', 404
            
            hello.remove()
            return '', 204

        except e:
            return e.args[0], 400

     
        return 'unexpected error', 500

class HelloWorld(Resource):
    
    def get(self):
        LOG.debug("Serving  Get all request")
        hello_list = []
        parser = reqparse.RequestParser()
        #parser.add_argument('id')
        args = parser.parse_args()
        data = Hello.query.all()
        #hello_data = data.wrap()
        for hello_data_item in data:
            hello_data = hello_data_item.wrap()
            if '_id' in hello_data:
                hello_data['id'] = str(hello_data['_id'])
                del hello_data['_id']
                hello_list.append(hello_data)
    
        #normalize the name for 'id'
       
    
        return hello_list
    
        

    @swagger.doc(
        {
            'tags': ['Hello World'],
            'description': 'hello world create operation',
            'responses': response_msgs
        }
    )

    def post(self):
        """
        Adds a hello item.
        """
        hello_data = None


        try:
            data = request.get_json()
            hello_data  = Hello.unwrap(data)
            hello_data.save()
        except ExtraValueException as e:
             return e.args[0] +" is not valid input", 400
        except ValueError as e:
            return e.args[0], 400

        if hello_data:
            return '', 201, {'Location': request.path + '/' + str(hello_data.mongo_id)}
        else:
            return 'unexpected error', 500