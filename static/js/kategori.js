console.log('kategori.js is connected')
var kat = $("#kategoriDinding").val()
console.log(kat)

$("#dinding_nonpartisi.dinding").ready(function() {
    if($("#kategoriDinding").val() == "P"){
         $("#dinding_nonpartisi.dinding").css('display','None')
    }
});
$("#dinding_partisi.dinding").ready(function() {
    if($("#kategoriDinding").val() == "N"){
         $("#dinding_partisi.dinding").css('display','None')
    }
});

function getData(){
    var selectBox = document.getElementById('kategoriDinding').value;
    console.log(selectBox);
    if (selectBox == 'P'){
    $("#dinding_partisi").show();
    $("#dinding_nonpartisi").hide();
  }else if(selectBox == 'N') {
    $("#dinding_nonpartisi").show();
    $("#dinding_partisi").hide();
  }
}

