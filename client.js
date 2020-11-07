var ws = new WebSocket('ws://127.0.0.1:8765/');
var figContainer = document.getElementById('fig-container');
var figList = document.getElementById('fig-list');

var file_ids = new Set();

const sleep = (milliseconds) => {
  return new Promise(resolve => setTimeout(resolve, milliseconds));
};

const SendFileIds = async () => {
  while (true) {
    await ws.send(JSON.stringify(Array.from(file_ids)));
    console.log('sent', file_ids);
    await sleep(2000);
  }
};
// Keep sending list of files forever
ws.onopen = SendFileIds;

ws.onmessage = function (event) {
  var data = JSON.parse(event.data);
  if (!file_ids.has(data['id'])) {
    file_ids.add(data['id']);
    console.log('Added ', data['id']);
    var fig = data['fig'];
    var newFig = document.createElement('div');
    newFig.id = data['id'];
    Plotly.newPlot(newFig, fig.data, fig.layout);
    var figSubContainer = document.createElement('div');

    // Set title
    var title = document.createElement('h4');
    var titleText = data['id'].split('.').slice(0, -1).join('.');
    title.textContent = titleText;
    figSubContainer.appendChild(title);
    figSubContainer.appendChild(newFig);
    figSubContainer.className = 'fig';
    if (file_ids.size > 1) {
      figSubContainer.style.display = 'none';
    }
    figContainer.appendChild(figSubContainer);
  }
};
