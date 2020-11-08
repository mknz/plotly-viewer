# Plotly Viewer

## Install
```
git clone https://github.com/mknz/plotly-viewer
cd ./plotly-viewer
sudo make install
```
This installs `ipv` command and `savefig` IPython startup function.

```
ipv
```

This command launches IPython with Plotly viewer and server. You can save Plotly figure by passing it to `savefig` function.
```
>>> savefig(px.imshow(np.random.random((10, 10))))
>>> savefig px.imshow(np.random.random((10, 10)))  # With %autocall
```
The figure is saved to `plotly_figs` directory with timestamp filename.

## Uninstall
```
sudo make uninstall
```
