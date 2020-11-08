import datetime
import os
from pathlib import Path


def savefig(fig, file_format='json'):
    """Save plotly figure locally (default is JSON).

    This saves {TIMESTAMP}.json in {CURRENT DIRECTORY}/plotly_figs
    >>> %autocall
    >>> savefig px.scatter(np.random.random((10, 2)))
    """
    rootdir = Path(os.getcwd()) / 'plotly_figs'
    rootdir.mkdir(parents=True, exist_ok=True)
    now = datetime.datetime.now()
    timestr = now.isoformat().replace(":", "").split(".")[0]
    if file_format == 'json':
        fig.write_json(
            str(rootdir / f"{timestr}.json"),
        )
    elif file_format == 'html':
        fig.write_html(
            str(rootdir / f"{timestr}.html"),
            full_html=False,
            include_plotlyjs=False,
        )
    else:
        raise ValueError(f'Unsupported format: {file_format}')
