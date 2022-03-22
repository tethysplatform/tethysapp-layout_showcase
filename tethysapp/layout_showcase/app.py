from tethys_sdk.base import TethysAppBase, url_map_maker


class LayoutShowcase(TethysAppBase):
    """
    Tethys app class for Layout Showcase.
    """

    name = 'Layout Showcase'
    index = 'quick_start'
    icon = 'layout_showcase/images/icon.gif'
    package = 'layout_showcase'
    root_url = 'layout-showcase'
    color = '#045c34'
    description = 'A Tethys app that demonstrates how to use various layout views.'
    tags = ''
    enable_feedback = False
    feedback_emails = []
