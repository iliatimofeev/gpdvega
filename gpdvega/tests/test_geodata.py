import altair as alt
import gpdvega # noqa:F401
import pytest
import json
from shapely.geometry import shape
import geopandas as gpd
import pandas as pd


def _create_geojson():
    return {
                "type": "FeatureCollection",
                "bbox": [
                    -161.30174569731454,
                    -60.39157788643298,
                    172.67580002536624,
                    42.438347020953984
                ],
                "features": [
                    {
                        "type": "Feature",
                        "properties": {"prop": 1},
                        "geometry": {
                            "type": "LineString",
                            "coordinates": [
                                [-69.2980008004234, 23.18780298146116],
                                [-161.30174569731454, -60.39157788643298],
                                [172.67580002536624, 24.151450472748962]
                            ]
                        },
                        "id": "0",
                        "bbox": [
                            -161.30174569731454,
                            -60.39157788643298,
                            172.67580002536624,
                            24.151450472748962
                        ]
                    },
                    {
                        "type": "Feature",
                        "properties": {"prop": 2},
                        "geometry": {
                            "type": "LineString",
                            "coordinates": [
                                [156.03047546751765, 42.43834702095399],
                                [35.46296546950265, -18.185542212943375],
                                [152.53211600051463, 23.471406463455793]
                                ]
                        },
                        "id": "1",
                        "bbox": [
                            35.46296546950265,
                            -18.185542212943375,
                            156.03047546751765,
                            42.438347020953984
                        ]
                    },
                    {
                        "type": "Feature",
                        "properties": {"prop": 3},
                        "geometry": {
                            "type": "LineString",
                            "coordinates": [
                                [-133.98414913936503, 25.39468871174894],
                                [145.04376601680605, 13.058626381790845],
                                [170.30576801294046, 38.67128737163435]
                                ]
                        },
                        "id": "2",
                        "bbox": [
                            -133.98414913936503,
                            13.058626381790845,
                            170.30576801294046,
                            38.67128737163435
                        ]
                        }
                ]
            }


def _create_fake_geo_interface():
    class FakeGeoJSON:
        __geo_interface__ = _create_geojson()
    return FakeGeoJSON()


def geojson2gdp(obj):
    return gpd.GeoDataFrame(
        [g["properties"] for g in obj["features"]],
        geometry=[shape(g["geometry"]) for g in obj["features"]],
        index=[g["id"] for g in obj["features"]],
        crs='+init=epsg:4326'
    )


def test_default_pipe():
    assert(alt.data_transformers.active == 'gpd_to_values')


def test_max_rows_pipe():
    alt.data_transformers.enable('gpd_to_values', max_rows=1)
    data = geojson2gdp(_create_geojson())
    with pytest.raises(alt.MaxRowsError):
        data = alt.pipe(data, alt.data_transformers.get())
    alt.data_transformers.enable('gpd_to_json', max_rows=1)
    with pytest.raises(alt.MaxRowsError):
        data = alt.pipe(data, alt.data_transformers.get())
    alt.data_transformers.enable('gpd_to_values')


# to_values
def test_gpd_to_values():

    data = _create_geojson()
    for a, b in zip(
                json.loads(gpdvega.gpd_to_values(geojson2gdp(data))['values']),
                data['features']):
        assert a['id'] == b['id']
        assert a['prop'] == b['properties']['prop']
        assert a['geometry'] == b['geometry']


def test_gpd_to_values_no_geom():

    data = gpd.GeoDataFrame(pd.np.arange(3), columns=['param'])
    with pytest.warns(UserWarning,
                      match="GeoDataFrame has no geometry to display."):
        for a, b in zip(
                        json.loads(gpdvega.gpd_to_values(data)['values']),
                        data.param.tolist()):
                assert a['param'] == b


def test_gpd_to_values_warnings():
    data = geojson2gdp(_create_geojson())
    with pytest.warns(UserWarning, match="Column name 'type'"):
        gpdvega.gpd_to_values(data.assign(type='type'))
    with pytest.warns(UserWarning, match="Column name 'id'"):
        gpdvega.gpd_to_values(data.assign(id='id'))
    with pytest.warns(UserWarning, match="Column name 'geometry'"):
        gpdvega.gpd_to_values(
                data.rename(
                            columns={'geometry': 'g'}
                            ).set_geometry('g').assign(geometry='xxx')
            )


def test_gpd_to_values_pd():
    data = pd.DataFrame(pd.np.arange(3), columns=['param'])
    assert gpdvega.gpd_to_values(data) == alt.to_values(data)


# to_json
def test_gpd_to_json_pd():
    data = pd.DataFrame(pd.np.arange(3), columns=['param'])
    assert gpdvega.gpd_to_json(data) == alt.to_json(data)


def test_gpd_to_json():

    data = _create_geojson()
    r = gpdvega.gpd_to_json(geojson2gdp(data))
    with open(r['url']) as fp:
        rvalues = json.load(fp)
        for a, b in zip(
                    rvalues,
                    data['features']):
            assert a['id'] == b['id']
            assert a['prop'] == b['properties']['prop']
            assert a['geometry'] == b['geometry']


# geojson_feature
def test_geojson_feature():

    def Chart(data, **arg):
        return alt.Chart(
                        gpdvega.geojson_feature(data, 'test_prop')
                ).mark_geoshape().project().encode(**arg)
    # Fake GeoInterface
    data = _create_fake_geo_interface()
    with alt.data_transformers.enable(consolidate_datasets=False):
        dct = Chart(data).to_dict()

    assert dct['data']['format'] == {'type': 'json', 'property': 'test_prop'}
    assert dct['data']['values'] == data.__geo_interface__

    # url
    data = "url.json"
    with alt.data_transformers.enable(consolidate_datasets=False):
        dct = Chart(data).to_dict()

    assert dct['data']['format'] == {'type': 'json', 'property': 'test_prop'}
    assert dct['data']['url'] == data

    # GeoPandas

    data = geojson2gdp(_create_geojson())
    with alt.data_transformers.enable(consolidate_datasets=False):
        dct = Chart(data).to_dict()

    assert dct['data']['format'] == {'type': 'json', 'property': 'test_prop'}

    assert json.dumps(dct['data']['values'], sort_keys=True) == \
        json.dumps(data.__geo_interface__, sort_keys=True)

    # GeoPandas sanitize_dataframe
    data['time'] = pd.date_range('2018-01-01', periods=data.index.size)
    with alt.data_transformers.enable(consolidate_datasets=False):
        dct = Chart(data).to_dict()


def test_geojson_feature_warn():
    with pytest.warns(UserWarning, match="data of type"):
        gpdvega.geojson_feature(555)
