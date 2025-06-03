from pyramid.config import Configurator
from itera_crowdfunding.cors import add_cors_preflight_handler
from dotenv import load_dotenv


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    load_dotenv()
    with Configurator(settings=settings) as config:
        config.include('itera_crowdfunding.cors')
        config.add_cors_preflight_handler()


        config.include('pyramid_jinja2')
        config.include('.routes')
        config.scan()
    
    return config.make_wsgi_app()
