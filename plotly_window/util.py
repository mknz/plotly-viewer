import datetime
from pathlib import Path


def show(fig):
    rootdir = Path('/tmp/plotly')
    rootdir.mkdir(parents=True, exist_ok=True)
    now = datetime.datetime.now()
    timestr = now.isoformat().replace(":", "").split(".")[0]
    fig.write_html(
        str(rootdir / f"{timestr}.html"),
        full_html=False,
        include_plotlyjs=False,
        default_width='90%',
        default_height='90%',
    )
