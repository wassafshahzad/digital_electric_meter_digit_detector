let $ = require('jquery')  // jQuery now loaded and assigned to $
const dialog = require('electron').remote.dialog
const ipc = require('electron').ipcRenderer;

$('#countbtn').on('click', () => {
	dialog.showOpenDialog(function (fileNames) {
		 if (fileNames === undefined) {return};
  		 var fileName = fileNames[0];
  		 console.log(fileName)
  		 ipc.send('led',fileName)
  }); 
}) 


ipc.on("load",function(e){
	$("#content").html("<img class='img-responsive' src='loader3.gif' alt='Chania'><br><p>Loading</p>")
});

ipc.on("image",function(e){
	$("#content").html("<h3>Extracted</h3><br><img class='img-responsive' src='result/1.jpg' alt='Chania'>")
});