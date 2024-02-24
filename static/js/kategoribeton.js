console.log('kategoribeton.js is connected')

$("#beton_nonpartisi.beton").ready(function() {
    if($("#kategoriBeton").val() == "P"){
         $("#beton_nonpartisi.beton").css('display','None')
    }
});
$("#beton_partisi.beton").ready(function() {
    if($("#kategoriBeton").val() == "N"){
         $("#dinding_partisi.beton").css('display','None')
    }
});


function getDataKategoriBeton(){
    var selectBox = document.getElementById('kategoriBeton').value;
    console.log(selectBox);
    if (selectBox == 'P'){
    $("#beton_partisi").show();
    $("#beton_nonpartisi").hide();
  }else if(selectBox == 'N') {
    $("#beton_nonpartisi").show();
    $("#beton_partisi").hide();
  }
}
