console.log('kategoripintu.js is connected')
$("#pintu_nonpartisi.pintu").ready(function() {
    if($("#kategoriPintu").val() == "P"){
         $("#pintu_nonpartisi.pintu").css('display','None')
    }
});
$("#pintu_partisi.pintu").ready(function() {
    if($("#kategoriPintu").val() == "N"){
         $("#pintu_partisi.pintu").css('display','None')
    }
});


function getDataKategoriPintu(){
    var selectBox = document.getElementById('kategoriPintu').value;
    console.log(selectBox);
    if (selectBox == 'P'){
    $("#pintu_partisi").show();
    $("#pintu_nonpartisi").hide();
  }else if(selectBox == 'N') {
    $("#pintu_nonpartisi").show();
    $("#pintu_partisi").hide();
  }
}
