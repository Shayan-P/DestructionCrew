let canvas = document.getElementById("canvas");
let context = canvas.getContext("2d");
let w = 0, h = 0
let bw = 0, bh = 0
let cw = 40
const p = 0

windowW = window.innerWidth
windowH = window.innerHeight
canvas.width = windowW-10
canvas.height = windowH-10

let board

function drawBoard(_w, _h) {
    context.beginPath()
    context.clearRect(0, 0, canvas.width, canvas.height)
    w = _w
    h = _h
    cw = Math.min(canvas.width/w, canvas.height/h)-3
    bh = h * cw
    bw = w * cw
    for (let x = 0; x <= bw; x += cw) {
        context.moveTo(0.5 + x + p, p)
        context.lineTo(0.5 + x + p, bh + p)
    }

    for (let x = 0; x <= bh; x += cw) {
        context.moveTo(p, 0.5 + x + p);
        context.lineTo(bw + p, 0.5 + x + p);
    }

    context.strokeStyle = "black";
    context.stroke();

    board = []
    for (let x = 0; x < w; x++){
        board.push([])
        for (let y = 0; y < h; y++){
            board[x].push(undefined)
            putCell(x, y)
        }
    }
}

function getCursorPosition(canvas, event, cw) {
    const rect = canvas.getBoundingClientRect()
    const x = event.clientX - rect.left
    const y = event.clientY - rect.top
    const cy = (y + (cw - y % cw)) / cw
    const cx = (x + (cw - x % cw)) / cw
    return [cx, cy]
}

let defaultCellType = -1
let defaultCellValue = -1
let defaultResource = -1

function setBread(value){
    defaultCellType = 2
    defaultCellValue = value
    defaultResource = 1
}
function setGrass(value){
    defaultCellType = 2
    defaultCellValue = value
    defaultResource = 2
}
function setEmpty(value){
    defaultCellType = 2
    defaultCellValue = 0
    defaultResource = -1
}
function setWall(value){
    defaultCellType = 3
    defaultCellValue = 0
    defaultResource = -1
}
function setBase1(){
    defaultCellType = 0
    defaultCellValue = 0
    defaultResource = -1
}
function setBase2(){
    defaultCellType = 1
    defaultCellValue = 0
    defaultResource = -1
}

function get_default_cell(x, y){
    let ret = {
        "row": y,
        "col": x,
        "cell_type": defaultCellType,
        "rec1": 0,
        "rec2": 0
    }
    if(defaultResource === 1){
        ret.rec1 = defaultCellValue
    }
    if(defaultResource === 2){
        ret.rec2 = defaultCellValue
    }
    return ret
}
function putCell(x, y){
    if(x >= bw || y >= bh)
        return

    if(defaultCellType === 0){
        putColor(x, y, "red")
    }
    if(defaultCellType === 1){
        putColor(x, y, "blue")
    }
    if(defaultCellType === 2){
        if(defaultResource === 1){
            putColor(x, y, "yellow", defaultCellValue)
        }
        else if(defaultResource === 2){
            putColor(x, y, "green", defaultCellValue)
        }
        else{
            putColor(x, y, "grey")
        }
    }
    if(defaultCellType === 3){
        putColor(x, y, "black")
    }
    board[x][y] = get_default_cell(x, y)
}


function exportBoard(){
    let ret = {
        "MAP_HEIGHT": h,
        "MAP_WIDTH": w,
        "SHIFT_X": 0,
        "SHIFT_Y": 0,
        "cells_type": []
    }
    for(let x = 0; x < w; x++){
        for(let y = 0; y < h; y++){
            ret.cells_type.push(board[x][y])
        }
    }
    let xhr = new XMLHttpRequest();
    xhr.open("POST", "/write_map", true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify(ret));
}


function putColor(x, y, color, text){
    if(x >= bw || y >= bh)
        return
    let context2 = canvas.getContext("2d");
    context2.clearRect((x-1) * cw + 1, (y-1) * cw + 1, cw-2, cw-2)
    context2.beginPath();
    context2.fillStyle = color;
    context2.fillRect((x-1) * cw + 1, (y-1) * cw + 1, cw-2, cw-2)
    if(text) {
        context2.fillStyle = "black"
        context2.textAlign = "center"
        context2.font = "20px Arial";
        context2.fillText(text, (x-1) * cw + cw * 0.5, (y-1) * cw + cw * 0.6);
    }
}

canvas.addEventListener('mousedown', function (e) {
    let [x, y] = getCursorPosition(canvas, e, cw)
    putCell(x, y)
})

setEmpty()
