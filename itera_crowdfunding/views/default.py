from pyramid.view import view_config


@view_config(route_name='home', renderer='itera_crowdfunding:templates/mytemplate.jinja2')
def my_view(request):
    return {'project': 'itera-crowdfunding'}
