const {app,BrowserWindow,ipcMain} = require ("electron")
const url = require('url')
const path = require('path')
const {PythonShell}  =require('python-shell');
const request = require('request')
const fs = require('fs');

let win,bill_form,file_g

function create(){
	win = new BrowserWindow({width: 800, height: 600})
	win.loadURL(url.format({
		pathname: path.join(__dirname, 'index.html'), 
     	protocol: 'file:', 
     	slashes: true 
	})) 

	
}
function create_bill(){
	bill_form = new BrowserWindow({width: 800, height: 600,show:false})
	bill_form.loadURL(url.format({
		pathname: path.join(__dirname, 'bill.html'), 
     	protocol: 'file:', 
     	slashes: true 
	})) 
}




ipcMain.on('led',function(e,file){
	file_g=file
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

ipcMain.on("detect",function(e){
	var formData={
		'image':fs.createReadStream("E:\\Projects\\desktop_app\\app\\result\\1.jpg")
	}
	request.post({url:'http://127.0.0.1:80', formData: formData}, function optionalCallback(err, httpResponse, body) {
 		if (err) {
    		return console.error('upload failed:', err);
  		}
  		create_bill()
  		bill_form.once('ready-to-show', () => {
  		let json = JSON.parse(body);
  		//console.log(body["0"])
  		console.log(file_g)
  		bill_form.webContents.send("bill",json,file_g)
  		bill_form.show()
  		win.close()
  		win=null


});
	});
	win.webContents.send("load")
});	





app.on('ready', create) 