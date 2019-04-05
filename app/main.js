const {app,BrowserWindow,ipcMain} = require ("electron")
const url = require('url')
const path = require('path')
const {PythonShell}  =require('python-shell');

let win

function create(){
	win = new BrowserWindow({width: 800, height: 600})
	win.loadURL(url.format({
		pathname: path.join(__dirname, 'index.html'), 
     	protocol: 'file:', 
     	slashes: true 
	})) 
	
}




ipcMain.on('led',function(e,file){
	win.webContents.send("load")
	const { spawn } = require('child_process');
    const pyProg = spawn('python', ['async_svm.py',file]);
    pyProg.stdout.on('data', (data) => {
    	win.webContents.send("image")
	});
	pyProg.stderr.on('data', (data) => {
    	console.log(data.toString())
	});
});
	

app.on('ready', create) 