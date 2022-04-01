from tethys_sdk.base import TethysAppBase, url_map_maker
from tethys_sdk.app_settings import SpatialDatasetServiceSetting


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

    def spatial_dataset_service_settings(self):
        sds_settings = (
            SpatialDatasetServiceSetting(
                name='primary_geoserver',
                description='A GeoServer with sample data loaded (topp:usa_population) for the Map Layout demo.',
                engine=SpatialDatasetServiceSetting.GEOSERVER,
                required=False
            ),
        )
        
        return sds_settings
