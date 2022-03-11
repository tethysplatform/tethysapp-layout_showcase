from tethys_sdk.base import TethysAppBase, url_map_maker


class LayoutShowcase(TethysAppBase):
    """
    Tethys app class for Layout Showcase.
    """

    name = 'Layout Showcase'
    index = 'layout_showcase:quick_start'
    icon = 'layout_showcase/images/icon.gif'
    package = 'layout_showcase'
    root_url = 'layout-showcase'
    color = '#045c34'
    description = 'A Tethys app that demonstrates how to use various layout views.'
    tags = ''
    enable_feedback = False
    feedback_emails = []

    def url_maps(self):
        """
        Add controllers
        """
        from .controllers.map_layout import MapLayoutShowcase
        UrlMap = url_map_maker(self.root_url)

        url_maps = (
            UrlMap(
                name='quick_start',
                url='layout-showcase',
                controller='layout_showcase.controllers.quick_start.quick_start'
            ),
            UrlMap(
                name='map_layout',
                url='layout-showcase/map-layout',
                controller=MapLayoutShowcase.as_controller()
                # controller=login_required(MapLayoutShowcase.as_controller())
            ),
        )

        return url_maps