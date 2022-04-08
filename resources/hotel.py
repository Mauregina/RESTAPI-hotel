from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from models.site import SiteModel
from flask_jwt_extended import jwt_required
from resources.filtros import normalize_path_params, consulta_com_cidade, consulta_sem_cidade
import sqlite3


#path /hoteis?cidade=Recife&estrelas_min=2&estrelas_max=4&diaria_min=100&diaria_max=400
path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=int) #qtd itens a serem exibidos por pagina
path_params.add_argument('offset', type=int) #qtd itens que deseja pular

class Hoteis(Resource):
    def get(self):
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()

        dados = path_params.parse_args()
        #filtra variaveis que nao foram passadas na requisicao
        dados_validos = {chave:dados[chave] for chave in dados if dados[chave] is not None}
        parametros = normalize_path_params(**dados_validos)
         
        if parametros.get('cidade'):
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta_com_cidade, tupla)
        else:                         
            tupla = tuple([parametros[chave] for chave in parametros])
            resultado = cursor.execute(consulta_sem_cidade, tupla) 

        hoteis = []
        for linha in resultado:
            hoteis.append({
            'hotel_id': linha[0],
            'nome': linha[1],
            'estrelas': linha[2],  
            'diaria': linha[3], 
            'cidade': linha[4],
            'site_id': linha[5]   
        })

        return {'hoteis': hoteis}

class Hotel(Resource):
    atributos = reqparse.RequestParser()   
    atributos.add_argument('nome', type=str, required=True, help="The field 'name' might be informed.")  
    atributos.add_argument('estrelas', type=float)  
    atributos.add_argument('diaria', type=float)
    atributos.add_argument('cidade', type=str)    
    atributos.add_argument('site_id', type=int, required=True, help="The field 'site id' might be informed.")  

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        
        if hotel:
            return hotel.json()
        return {'message': 'Hotel not found'}, 404 # not found 

    @jwt_required
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message": "Hotel id '{}' already exists.".format(hotel_id)}, 400 # bad request
        
        dados = Hotel.atributos.parse_args()
        hotel_obj = HotelModel(hotel_id, **dados)
        print('dados', dados)
        
        if not SiteModel.find_by_id(dados['site_id']):
            return {'message': 'The hotel must be associated to a valid site id'}, 400 # bad request

        try:
            hotel_obj.save_hotel()
            return hotel_obj.json(), 201 # created 
        except:
            return {'message': 'An internal error occurred trying to save hotel.'}, 500 # internal server error    

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