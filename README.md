# Plotly Viewer

## Quickstart

```bash
git clone https://github.com/mknz/plotly-viewer
cd ./plotly-viewer
sudo make install
```

This installs `ipython-plotly-viewer` command and `savefig` in IPython startup function.

```bash

ipython-plotly-viewer
```

The command launches IPython with Plotly viewer and server.
You can save Plotly figure by passing it to `savefig` function.

```Python
>>> savefig(px.imshow(np.random.random((10, 10))))
>>> savefig px.imshow(np.random.random((10, 10)))  # With %autocall
```

Above command saves figure data to `plotly_figs` directory with timestamp filename.

## Uninstall

```bash
sudo make uninstall
```
