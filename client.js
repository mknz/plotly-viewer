const ws = new WebSocket('ws://127.0.0.1:8765/');
const figContainer = document.getElementById('fig-container');
const fileIds = new Set();
let initDone = false;

const sleep = (milliseconds) => {
  return new Promise(resolve => setTimeout(resolve, milliseconds));
};

const SendFileIds = async () => {
  while (true) {
    await ws.send(JSON.stringify(Array.from(fileIds)));
    await sleep(1000);
  }
};
// Keep sending list of files forever
ws.onopen = SendFileIds;

function showFig (fileId) {
  for (let i = 0; i < figContainer.children.length; i++) {
    const figSubContainer = figContainer.children[i];
    if ((figSubContainer.id === fileId + '_sc')) {
      figSubContainer.style.display = 'block';
    } else {
      figSubContainer.style.display = 'none';
    }
  }
}

const init = async function () {
  // Wait 2 seconds for loading, then show last added figure
  // Show loading message
  const loading = document.createElement('p');
  loading.id = 'loading';
  loading.textContent = 'Loading...';
  document.body.appendChild(loading);

  // Asynchronously wait
  await sleep(2000);

  // Show last figure
  const fileIdsArr = Array.from(fileIds);
  fileIdsArr.sort();
  showFig(fileIdsArr[fileIdsArr.length - 1]);

  // Delete loading message
  loading.remove();

  // Show link list
  const figList = document.getElementById('fig-list');
  figList.style.display = 'block';
  initDone = true;
};
init();

function updateLinkList () {
  const figList = document.getElementById('fig-list');
  if (!initDone) { figList.style.display = 'none'; }
  // Init figure link list
  while (figList.firstChild) {
    figList.removeChild(figList.firstChild);
  }
  // Update figure link list
  const fileIdsArr = Array.from(fileIds);
  fileIdsArr.sort();
  for (let i = 0; i < fileIdsArr.length; i++) {
    const fileId = fileIdsArr[i];
    const link = document.createElement('button');
    link.textContent = fileId;
    link.onclick = function () { showFig(fileId); };
    figList.appendChild(link);
  }
}

ws.onmessage = function (event) {
  const data = JSON.parse(event.data);
  if (!fileIds.has(data.id)) { // New file
    const fileId = data.id;
    fileIds.add(fileId);
    console.log('Added ', fileId);
    const fig = data.fig;

    // Create figure element
    const newFig = document.createElement('div');
    newFig.id = fileId;
    Plotly.newPlot(newFig, fig.data, fig.layout);

    // Create figure sub container
    const figSubContainer = document.createElement('div');
    figSubContainer.id = newFig.id + '_sc';

    // Set title
    const title = document.createElement('h4');
    // Remove ext
    const titleText = fileId.split('.').slice(0, -1).join('.');
    title.textContent = titleText;

    figSubContainer.appendChild(title);
    figSubContainer.appendChild(newFig);
    figSubContainer.className = 'fig';
    figSubContainer.style.display = 'none'; // Hide at init
    figContainer.appendChild(figSubContainer);
    if (initDone) { showFig(fileId); } // Show added figure
  }
  updateLinkList();
};
