# tethysapp-layout_showcase
A Tethys app that demonstrates how to use Tethys Layouts.

1. Install

    ```
    tethys install
    ```

2. OpenCage Geocoding API Key (Optional)

    The Map Layout includes a reverse geocoding capability (address search) that is powered by the [OpenCage Geocoding API](https://opencagedata.com/). To enable this feature in the demo you will need to acquire an OpenCage API key. Use their [Quick Start](<https://opencagedata.com/api#quickstart>) guide to learn how to obtain an API key. Then enter the API key in the `geocode_api_key` setting of the app.

3. GeoServer (Optional)

    The Layout Showcase App has a Spatial Dataset Service Setting that can be used to link a GeoServer service to the app. When included, the Map Layout demo will display the US States layer hosted by GeoServer. Any GeoServer can be used, so long as it contains the demo layers. See [Assign Spatial Dataset Services](http://docs.tethysplatform.org/en/stable/tethys_sdk/tethys_services/spatial_dataset_services.html#assign-spatial-dataset-service) for how to add a GeoServer as a Spatial Dataset Service and link it to an app.
