let $ = require('jquery')  // jQuery now loaded and assigned to $
const dialog = require('electron').remote.dialog
const ipc = require('electron').ipcRenderer;

ipc.on("bill",function(e,json,file_g){
	//$("#bill").val(json[0])
	$("#unit").val(json[1])
	

});