import altair as alt
import geopandas as gpd
import six
import json
import warnings
from toolz.curried import curry


def geopandas_to_dict(data):
    try:
        if ('geometry' != data.geometry.name) and ('geometry' in data.columns):
            warnings.warn(
                "Column name 'geometry' is reserved name for " +
                "GeoDataFrame. Column named 'geometry' should contain " +
                "actual displaying geometry or not be used. Data of column " +
                "will not be accessible from the chart description. "
            )
        if 'type' in data.columns:
            warnings.warn(
                "Column name 'type' is reserved name for GeoDataFrame. " +
                "Data of column 'type' will not be accessible from the " +
                "chart description."
            )
        if 'id' in data.columns:
            warnings.warn(
                "Column name 'id' is reserved name for GeoDataFrame for " +
                "index values. Data of column 'id' will not be accessible " +
                "from the chart description."
            )
        if data.crs:
            data = data.to_crs(epsg=4326)
        return [dict(
                    row,
                    type=feature['type'],
                    geometry=feature['geometry'],
                    id=feature['id']
                    ) for row, feature in zip(
                            data.drop(
                                data.geometry.name,
                                axis=1
                            ).to_dict('row'),
                            data.geometry.__geo_interface__['features']
                        )
                ]
    except AttributeError as err:
        if str(err).startswith('No geometry data set yet'):
            warnings.warn("GeoDataFrame has no geometry to display.")
            return data.to_dict('row')
        else:
            raise


@curry
def gpd_to_values(data):
    """Replace a GeoDataFrame by a data model with values.
    Columns values stored as Foreign Members of GeoJSON feature objects"""
    if isinstance(data, gpd.GeoDataFrame):
        data = alt.utils.sanitize_dataframe(data)
        values = geopandas_to_dict(data)
        return {'values': json.dumps(values)}
    else:
        return alt.to_values(data)


@curry
def gpd_to_json(data):
    """Write the data model to a .json file and return a url based data model.
    Columns values stored as Foreign Members of GeoJSON feature objects"""
    if isinstance(data, gpd.GeoDataFrame):
        data = alt.utils.sanitize_dataframe(data)
        values = geopandas_to_dict(data)
        return alt.to_json({'values': values})
    else:
        return alt.to_json(data)


alt.data_transformers.register(
    'gpd_to_values',
    lambda data: alt.pipe(data, alt.limit_rows, gpd_to_values)
)
alt.data_transformers.register(
    'gpd_to_json',
    lambda data: alt.pipe(data, alt.limit_rows, gpd_to_json)
)

alt.data_transformers.enable('gpd_to_values')


def geojson_feature(data, feature='features', **kwargs):
    """A convenience function for extracting features from a geojson object or url

    Parameters
    ----------
    data : anyOf(string, geojson.GeoJSON)
        string is interpreted as URL from which to load the data set.
        geojson.GeoJSON is interpreted as data set itself.

    feature : string
        The JSON property containing the GeoJSON object set to convert to
          a GeoJSON feature collection. For example ``features[0].geometry``.

    **kwargs :
        additional keywords passed to JsonDataFormat

    """
    if isinstance(data, six.string_types):
        return alt.UrlData(
                    url=data,
                    format=alt.JsonDataFormat(
                        type='json',
                        property=feature,
                        **kwargs
                    )
                )
    elif hasattr(data, '__geo_interface__'):
        if isinstance(data, gpd.GeoDataFrame):
            data = alt.utils.sanitize_dataframe(data)
        return alt.InlineData(
                    values=data.__geo_interface__,
                    format=alt.JsonDataFormat(
                        type='json',
                        property=feature,
                        **kwargs
                    )
                )
    else:
        warnings.warn("data of type {0} not recognized".format(type(data)))
        return data
