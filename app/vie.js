let $ = require('jquery')  // jQuery now loaded and assigned to $
const dialog = require('electron').remote.dialog
const ipc = require('electron').ipcRenderer;

$('#countbtn').on('click', () => {
	if($('#countbtn').text()=="Click here"){
		dialog.showOpenDialog(function (fileNames) {
		if (fileNames === undefined) {return};
  		var fileName = fileNames[0];
  		console.log(fileName)
  		ipc.send('led',fileName)
  		});
	}
	else {
		ipc.send("detect")		
  		}
}) 


ipc.on("load",function(e){
	$("#content").html("<img class='img-responsive' src='loader3.gif' alt='Chania'><br><p>Loading</p>")
	$("#butt").hide()
	$("#countbtn").text("continue")

});

ipc.on("image",function(e){
	$("#content").html("<h3>Extracted</h3><br><br><img class='img-responsive' src='result/1.jpg' alt='Chania'><p>The Led is extracted using Hog as a feature extractor and svm classifier.The image is first converted to binary form and contours having length greater than heigh are passed to hog+svm for classification.</p>")
	$('#butt').show()
});