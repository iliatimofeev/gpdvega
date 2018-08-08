import altair as alt
import geopandas as gpd
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
    """Replace a DataFrame by a data model with values."""
    if isinstance(data, gpd.GeoDataFrame):
        data = alt.utils.sanitize_dataframe(data)
        values = geopandas_to_dict(data)
        return {'values': json.dumps(values)}
    else:
        return alt.to_values(data)


alt.data_transformers.register(
    'gpd_to_values',
    lambda data: alt.pipe(data, alt.limit_rows, gpd_to_values)
)
alt.data_transformers.enable('gpd_to_values')
