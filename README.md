# gpdvega [![Coverage Status](https://coveralls.io/repos/github/iliatimofeev/gpdvega/badge.svg?branch=master)](https://coveralls.io/github/iliatimofeev/gpdvega?branch=master) [![Build Status](https://travis-ci.com/iliatimofeev/gpdvega.svg?branch=master)](https://travis-ci.com/iliatimofeev/gpdvega) [![HitCount](http://hits.dwyl.io/iliatimofeev/gpdvega.svg)](http://hits.dwyl.io/iliatimofeev/gpdvega) [![GitHub license](https://img.shields.io/github/license/iliatimofeev/gpdvega.svg)](https://github.com/iliatimofeev/gpdvega/blob/master/LICENSE) [![GitHub issues](https://img.shields.io/github/issues/iliatimofeev/gpdvega.svg)](https://github.com/iliatimofeev/gpdvega/issues)

`gpdvega` is a bridge between [`GeoPandas`](http://geopandas.org/) a geospatial extension of [`Pandas`](https://pandas.pydata.org/) and the declarative statistical visualization library [`Altair`](https://altair-viz.github.io/), which allows to seamlessly chart geospatial data using `altair`.

## Example

~~~python
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
~~~

![output](docs\_static\word_pop_est.png)

## Install

### Dependencies

gpdvega requires:

- Altair (>= 2.1.0 )
- GeoPandas (>= 0.4.0)

### User installation

not yet ready

> using `pip`
>
>     pip install gpdvega
>
> or `conda`
>
>     conda install gpdvega

### Changelog

See the [changelog](<https://iliatimofeev.github.io/gpdvega/whats_new.html>)
for a history of notable changes to gpdvega
