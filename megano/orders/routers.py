from rest_framework.routers import SimpleRouter, Route


class MyRouter(SimpleRouter):
    routes = [
        Route(
            url=r'^{prefix}/active/$',
            mapping={'get': 'active'},
            name='{basename}_active',
            detail=True,
            initkwargs={'suffix': 'Detail'}
        ),
        Route(
            url=r'^{prefix}/$',
            mapping={'get': 'list', 'post': 'submit_basket'},
            name='{basename}_list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),

        Route(
            url=r'^{prefix}/{lookup}/$',
            mapping={'post': 'update', 'get': 'details'},
            name='{basename}_detail',
            detail=True,
            initkwargs={'suffix': 'Detail'}
        ),
    ]
