.. _API:

API reference
======================


Data transformers
-----------------

``gpdvega`` register two data transformers:
    *   ``'gpd_to_values'`` stores GeoDataFrame as inline values in the chart definition using :py:func:`gpdvega.gpd_to_values`.
    *   ``'gpd_to_json'`` stores GeoDataFrame as separate json file with array of GeoJSON object and includes a link to it into chart definition using :py:func:`gpdvega.gpd_to_json`

.. note::

    ``gpdvega`` enables ``'gpd_to_values'`` as active data tranformer.
    Please see Altair data transformers_  documentation for description of data pipeline mechanism




API
-------------

.. automodule:: gpdvega
   :members:


.. _transformers: https://altair-viz.github.io/user_guide/data_transformers.html
