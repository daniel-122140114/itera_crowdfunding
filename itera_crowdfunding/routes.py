def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('campaigns', '/campaigns')
    config.add_route('campaign', '/campaigns/{id}')
    config.add_route('get_token','/token')