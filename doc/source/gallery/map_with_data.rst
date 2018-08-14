.. _gallery_map_with_data:


Interactive bar and map from a single data source
=======================================================

This is a layered geographic visualization that shows population by country in Africa

.. altair-plot::
    
    import altair as alt
    import geopandas as gpd
    import gpdvega 

    alt.renderers.enable('notebook') # render for Jupyter Notebook

    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

    brush = alt.selection_single(encodings=["y"],on="mouseover", empty='none')
    color = alt.Color('pop_est', scale= alt.Scale(type='pow', exponent=0.4))

    alt.hconcat(
        alt.Chart().mark_bar().encode(
            x=alt.X('pop_est', scale=alt.Scale(nice=False)),
            y=alt.Y('name', sort=alt.SortField(field='pop_est', 
                                                op='sum', order='descending')),
            tooltip=['name','pop_est','gdp_md_est'],
            color=alt.condition(brush, alt.value('lightgray'), color)
            ).add_selection(
                brush
            ).properties( 
                width=200,
                height=450
            ),
        alt.Chart().mark_geoshape().project().encode( 
            color=alt.condition(
                brush,
                alt.value('lightgray'),
                color,
            ),
            tooltip=['name','pop_est','gdp_md_est'],
            ).properties( 
                width=300,
                height=450,
                title='Africa population'
            ),
        data=world[world.continent == 'Africa']
    )   
    
.. toctree::
   :hidden: