console.log('kategorikaca.js is connected')

$("#kaca_nonpartisi.kaca").ready(function() {
    if($("#kategoriKaca").val() == "P"){
         $("#kaca_nonpartisi.kaca").css('display','None')
    }
});
$("#kaca_partisi.kaca").ready(function() {
    if($("#kategoriKaca").val() == "N"){
         $("#kaca_partisi.kaca").css('display','None')
    }
});



function getDataKategoriKaca(){
    var selectBox = document.getElementById('kategoriKaca').value;
    console.log(selectBox);
    if (selectBox == 'P'){
    $("#kaca_partisi").show();
    $("#kaca_nonpartisi").hide();
  }else if(selectBox == 'N') {
    $("#kaca_nonpartisi").show();
    $("#kaca_partisi").hide();
  }
}




