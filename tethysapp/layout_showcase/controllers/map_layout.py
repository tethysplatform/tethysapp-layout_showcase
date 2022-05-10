import json
import logging
from pathlib import Path
from urllib.parse import urlparse, urljoin

from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib import messages
from rest_framework.authtoken.models import Token

from tethys_sdk.layouts import MapLayout
from tethys_sdk.routing import controller
from tethys_sdk.app_settings import TethysAppSettingNotAssigned

from tethysapp.layout_showcase.app import LayoutShowcase as app

log = logging.getLogger(f'tethys.{__name__}')

@controller(
    name="map_layout",
    url="layout-showcase/map-layout",
    app_workspace=True,
)
class MapLayoutShowcase(MapLayout):
    template_name = 'layout_showcase/custom_map_layout.html'
    app = app
    back_url = reverse_lazy('layout_showcase:quick_start')
    basemaps = [
        'OpenStreetMap',
        'ESRI',
        'Stamen',
        {'Stamen': {'layer': 'toner', 'control_label': 'Black and White'}},
    ]
    default_center = [-98.583, 39.833]  # USA Center
    default_zoom = 5
    feature_selection_multiselect = True
    geocode_extent = [-127.26563, 23.56399, -66.09375, 50.51343]
    geoserver_workspace = 'topp'  # TODO: Generalize this out (more than one workspace?)
    initial_map_extent = [-127.26563, 23.56399, -66.09375, 50.51343]  # USA EPSG:4326
    map_subtitle = 'Showcase'
    map_title = 'Map Layout'
    max_zoom = 16
    min_zoom = 2
    plot_slide_sheet = True
    # show_map_clicks = True  # Can be enabled with feature selection
    # show_map_click_popup = True  # Do not enable this and show_properties_popup at the same time
    show_properties_popup = True  # Do not enable this and show_map_click_popup at the same time
    
    @property
    def geocode_api_key(self):
        if not getattr(self, '_geocode_api_key', None):
            self._geocode_api_key = self.app.get_custom_setting('geocode_api_key')
        return self._geocode_api_key

    def compose_layers(self, request, map_view, app_workspace, *args, **kwargs):
        """
        Add layers to the given MapView and create associated layer group objects.
        """
        # Get URL to GeoServer WMS Service from App Setting
        try:
            geoserver_wms_url = self.app.get_spatial_dataset_service(
                'primary_geoserver', 
                as_public_endpoint=True,
                as_wms=True
            )
            wms_configured = True
        except TethysAppSettingNotAssigned:
            wms_configured = False
            messages.warning(request, 'Assign a GeoServer in app settings to see a WMS layer example.')

        # WMS Layer
        wms_layer = None
        if wms_configured:
            wms_layer = self.build_wms_layer(
                endpoint=geoserver_wms_url,
                server_type='geoserver',
                layer_name='topp:states',
                layer_title="WMS Layer",
                layer_variable='population',
                visible=True,
                selectable=True,
                geometry_attribute='the_geom',
                excluded_properties=['STATE_FIPS', 'SUB_REGION'],
                plottable=True,
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
            visible=wms_layer is None,
            extent=[-63.69, 12.81, -129.17, 49.38],
            plottable=True,
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
        if wms_configured and wms_layer:
            layers = [wms_layer, geojson_layer, arc_gis_layer]
        else:
            layers = [geojson_layer, arc_gis_layer]

        map_view.layers.extend(layers)

        # Define the layer groups
        layer_groups = [
            self.build_layer_group(
                id='usa-layer-group',
                display_name='Layers',
                layer_control='radio',
                layers=layers,
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
                }},
                'fill': {'ol.style.Fill': {
                    'color': 'rgba(255, 140, 0, 0.1)'
                }}
            }},
            'Polygon': {'ol.style.Style': {
                'stroke': {'ol.style.Stroke': {
                    'color': 'green',
                    'width': 3
                }},
                'fill': {'ol.style.Fill': {
                    'color': 'rgba(0, 255, 0, 0.1)'
                }}
            }},
        }

    def get_plot_for_layer_feature(self, request, layer_name, feature_id, *args, **kwargs):
        """
        Retrieves plot data for given feature on given layer.

        Args:
            layer_name (str): Name/id of layer.
            feature_id (str): ID of feature.

        Returns:
            str, list<dict>, dict: plot title, data series, and layout options, respectively.
        """
        # Define data
        month = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                'August', 'September', 'October', 'November', 'December']
        high_2000 = [32.5, 37.6, 49.9, 53.0, 69.1, 75.4, 76.5, 76.6, 70.7, 60.6, 45.1, 29.3]
        low_2000 = [13.8, 22.3, 32.5, 37.2, 49.9, 56.1, 57.7, 58.3, 51.2, 42.8, 31.6, 15.9]
        high_2007 = [36.5, 26.6, 43.6, 52.3, 71.5, 81.4, 80.5, 82.2, 76.0, 67.3, 46.1, 35.0]
        low_2007 = [23.6, 14.0, 27.0, 36.8, 47.6, 57.7, 58.9, 61.2, 53.3, 48.5, 31.0, 23.6]
        high_2014 = [28.8, 28.5, 37.0, 56.8, 69.7, 79.7, 78.5, 77.8, 74.1, 62.6, 45.3, 39.9]
        low_2014 = [12.7, 14.3, 18.6, 35.5, 49.9, 58.0, 60.0, 58.6, 51.7, 45.2, 32.2, 29.1]
        
        layout = {
            'xaxis': {
                'title': 'Month'
            },
            'yaxis': {
                'title': 'Temperature (degrees F)'
            }
        }

        data = [{
                'name': 'High 2014',
                'mode': 'lines',
                'x': month,
                'y': high_2014,
                'line': {
                    'dash': 'solid',
                    'width': 4,
                    'color': 'red'
                }
            }, {
                'name': 'Low 2014',
                'mode': 'lines',
                'x': month,
                'y': low_2014,
                'line': {
                    'dash': 'solid',
                    'width': 4,
                    'color': 'blue'
                }
            }, {
                'name': 'High 2007',
                'mode': 'lines',
                'x': month,
                'y': high_2007,
                'line': {
                    'dash': 'dash',
                    'width': 4,
                    'color': 'red'
                }
            }, {
                'name': 'Low 2007',
                'mode': 'lines',
                'x': month,
                'y': low_2007,
                'line': {
                    'dash': 'dash',
                    'width': 4,
                    'color': 'blue'
                }
            }, {
                'name': 'High 2000',
                'mode': 'lines',
                'x': month,
                'y': high_2000,
                'line': {
                    'dash': 'dot',
                    'width': 4,
                    'color': 'red'
                }
            }, {
                'name': 'Low 2000',
                'mode': 'lines',
                'x': month,
                'y': low_2000,
                'line': {
                    'dash': 'dot',
                    'width': 4,
                    'color': 'blue'
                }
            }
        ]
        return 'Average High and Low Temperatures', data, layout
