.. gpdvega documentation master file, created by
   sphinx-quickstart on Mon Jul 23 21:32:49 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

gpdvega
===================================
``gpdvega`` is a bridge between GeoPandas_ a geospatial extension of Pandas_ and the declarative statistical visualization library Altair_, which allows to seamlessly chart geospatial data.
The source is available on `GitHub <https://github.com/iliatimofeev/gpdvega>`_. 

.. altair-plot::

    import altair as alt
    import geopandas as gpd
    import gpdvega 

    alt.renderers.enable('notebook') # render for Jupyter Notebook

    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    # GeoDataFrame could be passed as usual pd.DataFrame 
    alt.Chart(world[world.continent!='Antarctica']).mark_geoshape(
    ).project(
    ).encode( 
        color='pop_est', # shorthand infer types as for regular pd.DataFrame
        tooltip='id:Q' # GeoDataFrame.index is accessible as id
    ).properties( 
        width=500,
        height=300
    )

Installation
------------

using `pip`::
 
    pip install gpdvega
 
or `conda`::
 
    conda install gpdvega

.. toctree::
    :maxdepth: 2
    :caption: Documentation

    gallery/index
    user_guide/API
    whats_new



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _Pandas: http://pandas.pydata.org/
.. _GeoPandas: http://geopandas.org/
.. _Altair: http://altair-viz.github.io/
.. _Git Issues: http://github.com/iliatimofeev/gpdvega/issues
