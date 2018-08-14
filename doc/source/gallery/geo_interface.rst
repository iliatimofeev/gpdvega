.. _gallery_geo_iterface:


Working with ``__geo_interface__``
==================================

Use :func:`gpdvega.geojson_feature` to store an object that provides ``__geo_interface__`` support.
Module ``geopandas.GeoDataFrame`` implements that interface,
for list of other supported object see `manifest <https://gist.github.com/sgillies/2217756>`__

.. altair-plot::

    import altair as alt
    import geopandas as gpd
    import gpdvega 

    alt.renderers.enable('notebook') # render for Jupyter Notebook
    alt.data_transformers.enable(consolidate_datasets=False) # altair issue #1091

    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    alt.Chart(
        data = gpdvega.geojson_feature( # converting to GeoJSON object 
                    world[world.continent=='Africa'],
                    "features" # split collection of features into objects
            )
    ).mark_geoshape( 
    ).project(
    ).encode(
        fill = alt.Color('id:N',legend=None), 
        # data values are stored under nested `properties` object
        tooltip=['properties.name:O'], 
    ).properties( 
        width=500,
        height=300
    )

