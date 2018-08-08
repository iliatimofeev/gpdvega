import altair as alt
import gpdvega # noqa:F401


def test_default_pipe():
    assert(alt.data_transformers.active == 'gpd_to_values')

