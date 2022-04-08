from flask_restful import Resource
from models.site import SiteModel


class Sites(Resource):
    def get(self):
        return {'sites': [site.json() for site in SiteModel.query.all()]}

class Site(Resource):
    def get(self, url):
        site = SiteModel.find_site(url)

        if site:
            return site.json()
        return {'message': 'Site not found'}, 404 # not found         

    def post(self, url):
        site = SiteModel.find_site(url)

        if site:
            return {'message': 'The site {} already exists.'.format(site)}, 400 # bad request

        site = SiteModel(url)

        try:
            site.save_site()
            return {'message': 'Site created successfully!'}, 201 # created
        except:
            return {'message': 'An internal error occurred trying to save site.'}, 500 # internal server error  

    def delete(self, url):
        site = SiteModel.find_site(url)

        if site:
            try:
                site.delete_site()
            except:
                return {'message': 'An internal error occurred trying to delete site.'}, 500 # internal server error   
            return {'message': 'Site deleted'} 
        return {'message': 'Site not found'}, 404 # not found
