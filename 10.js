const INPUT_REGEX = /.*<\s*(-?\d*),\s*(-?\d*)>.*<\s*(-?\d*),\s*(-?\d*)>/;
let HAS_LOADED_FILE = false;
const points = [];
let current_tick = 10515;
let current_scale = 0.7;

fetch('./inputs/day10_1.txt')
  .then(response => response.text())
  .then(text => {
    const lines = text.split('\r\n');
    for (const line of lines) {
      if (line.length > 0) {
        const matches = line.match(INPUT_REGEX);
        const point = {
          x: Number(matches[1]),
          y: Number(matches[2]),
          vx: Number(matches[3]),
          vy: Number(matches[4]),
        };
        points.push(point);
      }
    }
    console.log('FILE LOAD OK', points.length);
    HAS_LOADED_FILE = true;

    go();
  });

function go() {
  const vizCanvas = document.getElementById('vizContainer');

  const ctx = vizCanvas.getContext('2d');

  ctx.save();

  const WIDTH = vizCanvas.width;
  const HEIGHT = vizCanvas.height;
  ctx.translate(WIDTH / 2, HEIGHT / 2);

  ctx.beginPath();
  ctx.fillStyle = 'black';
  ctx.rect(-WIDTH / 2, -HEIGHT / 2, WIDTH, HEIGHT);
  ctx.fill();

  const scale = current_scale;

  ctx.beginPath();
  ctx.fillStyle = 'white';
  for (const p of points) {
    const x = (p.x + current_tick * p.vx) * scale;
    const y = (p.y + current_tick * p.vy) * scale;
    ctx.rect(x - 1, y - 1, 2, 2);
  }
  ctx.fill();

  ctx.restore();
}

function tick_increment() {
  current_tick += 100;
  const tickDOM = document.getElementById('tickTxt');
  tickDOM.innerHTML = current_tick;
  go();
}

function getInput() {
  const tickInput = document.getElementById('tickInput');
  current_tick = Number(tickInput.value);

  const tickDOM = document.getElementById('tickTxt');
  tickDOM.innerHTML = current_tick;

  go();
}

function getScale() {
  const scaleInput = document.getElementById('scaleInput');
  current_scale = Number(scaleInput.value);

  const scaleDOM = document.getElementById('scaleTxt');
  scaleDOM.innerHTML = current_scale;

  go();
}

function tick_decrement() {
  current_tick -= 100;
  const tickDOM = document.getElementById('tickTxt');
  tickDOM.innerHTML = current_tick;
  go();
}
