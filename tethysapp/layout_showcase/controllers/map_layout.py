import json
import logging
from pathlib import Path
from urllib.parse import urlparse, urljoin

from django.http import JsonResponse
from django.urls import reverse_lazy
from rest_framework.authtoken.models import Token

from tethys_sdk.layouts import MapLayout
from tethys_sdk.routing import controller

from tethysapp.layout_showcase.app import LayoutShowcase as app

log = logging.getLogger(f'tethys.{__name__}')

@controller(
    name="map_layout",
    url="layout-showcase/map-layout",
    app_workspace=True,
)
class MapLayoutShowcase(MapLayout):
    app = app
    template_name = 'layout_showcase/custom_map_layout.html'
    back_url = reverse_lazy('layout_showcase:quick_start')
    map_title = 'Map Layout'
    map_subtitle = 'Showcase'
    basemaps = [
        'OpenStreetMap',
        'ESRI',
        'Stamen',
        {'Stamen': {'layer': 'toner', 'control_label': 'Black and White'}},
    ]
    default_center = [-98.583, 39.833]  # USA Center
    initial_map_extent = [-65.69, 23.81, -129.17, 49.38]  # USA EPSG:2374
    default_zoom = 5
    max_zoom = 16
    min_zoom = 2
    # plot_slide_sheet = True
    # show_legends = True
    # show_map_clicks = True
    # show_map_click_popup = True
    # show_properties_popup = True
    show_custom_layer = True

    def compose_layers(self, request, map_view, app_workspace, *args, **kwargs):
        """
        Add layers to the given MapView and create associated layer group objects.
        """
        # Get URL to GeoServer WMS Service from App Setting
        geoserver_wms_url = self.app.get_spatial_dataset_service(
            'primary_geoserver', 
            as_public_endpoint=True,
            as_wms=True
        )

        # WMS Layer
        self.geoserver_workspace = 'topp'
        wms_layer = self.build_wms_layer(
            endpoint=geoserver_wms_url,
            server_type='geoserver',
            layer_name='topp:states',
            layer_title="WMS Layer",
            layer_variable='population',
            visible=False,
            selectable=True,
            geometry_attribute='the_geom',
        )

        # Load GeoJSON into Python objects from file
        us_states_path = Path(app_workspace.path) / 'map_layout' / 'us-states.json'
        with open(us_states_path) as gj:
            us_states_geojson = json.loads(gj.read())

        # GeoJSON Layer
        geojson_layer = self.build_geojson_layer(
            geojson=us_states_geojson,
            layer_name='us-states',
            layer_title='GeoJSON Layer',
            layer_variable='reference',
            selectable=True,
            visible=True,
            extent=[-63.69, 12.81, -129.17, 49.38],
        )
        
        # ArcGIS Layer
        arc_gis_layer = self.build_arc_gis_layer(
            endpoint='https://sampleserver1.arcgisonline.com/ArcGIS/rest/services/Specialty/ESRI_StateCityHighway_USA/MapServer',
            layer_name='ESRI_StateCityHighway',
            layer_title='ArcGIS Layer',
            layer_variable='highways',
            visible=False,
            extent=[-173, 17, -65, 72],
        )

        # Add layers to map
        map_view.layers.extend([
            geojson_layer,
            wms_layer,
            arc_gis_layer,
        ])

        # Define the layer groups
        layer_groups = [
            self.build_layer_group(
                id='usa-layer-group',
                display_name='Layers',
                layer_control='radio',
                layers=[geojson_layer, wms_layer, arc_gis_layer],
            ),
        ]

        return layer_groups

    @classmethod
    def get_vector_style_map(cls):
        return {
            'MultiPolygon': {'ol.style.Style': {
                'stroke': {'ol.style.Stroke': {
                    'color': 'orange',
                    'width': 3
                }}
            }},
            'Polygon': {'ol.style.Style': {
                'stroke': {'ol.style.Stroke': {
                    'color': 'blue',
                    'width': 3
                }}
            }},
        }
