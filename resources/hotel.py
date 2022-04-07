from ast import arguments
from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required

class Hoteis(Resource):
    def get(self):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):
    atributos = reqparse.RequestParser()   
    atributos.add_argument('nome', type=str, required=True, help="The field 'name' might be informed.")  
    atributos.add_argument('estrelas', type=float)  
    atributos.add_argument('diaria', type=float)
    atributos.add_argument('cidade', type=str)    

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found'}, 404 # not found 

    @jwt_required
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id '{}' already exists.".format(hotel_id)}, 400
        
        dados = Hotel.atributos.parse_args()
        hotel_obj = HotelModel(hotel_id, **dados )
        
        try:
            hotel_obj.save_hotel()
            return {'message': 'Hotel created successfully!'}, 201 # created
        except:
            return {'message': 'An internal error occurred trying to save hotel.'}, 500 # internal server error  
        return hotel_obj.json(), 201 # created   

    @jwt_required
    def put(self, hotel_id):
        dados = Hotel.atributos.parse_args()   
        hotel_found = HotelModel.find_hotel(hotel_id)

        if hotel_found:
            hotel_found.update_hotel(**dados)
            hotel_found.save_hotel()
            return hotel_found.json(), 200 # updated
        
        hotel_obj = HotelModel(hotel_id, **dados )
        try:
            hotel_obj.save_hotel()
            return {'message': 'Hotel created successfully!'}, 201 # created
        except:
            return {'message': 'An internal error occurred trying to save hotel.'}, 500 # internal server error  
        return hotel_obj.json(), 201 # created 

    @jwt_required
    def delete(self, hotel_id):

        hotel = HotelModel.find_hotel(hotel_id)

        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message': 'An internal error occurred trying to delete hotel.'}, 500 # internal server error   
            return {'message': 'Hotel deleted'} 
        return {'message': 'Hotel not found'}, 404 # not found