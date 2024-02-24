$("#dinding_nonpartisi.dinding").css('display','None')
$("#dinding_partisi.dinding").css('display','None')


$("select#kategoriDinding").change(function(){
  var selectedVal = $(this).val();
  console.log(selectedVal);
  if (selectedVal == 'dinding_partisi'){
    $("div#"+selectedVal).show();
    $("div#dinding_nonpartisi").hide();
  }else {
    $("div#"+selectedVal).show();
    $("div#dinding_partisi").hide();
  }


});

$("#kaca_nonpartisi.kaca").css('display','None')
$("#kaca_partisi.kaca").css('display','None')


$("select#kategoriKaca").change(function(){
  var selectedVal = $(this).val();
  console.log(selectedVal);
  if (selectedVal == 'kaca_partisi'){
    $("div#"+selectedVal).show();
    $("div#kaca_nonpartisi").hide();
  }else {
    $("div#"+selectedVal).show();
    $("div#kaca_partisi").hide();
  }


});

$("#beton_nonpartisi.beton").css('display','None')
$("#beton_partisi.beton").css('display','None')

$("select#kategoriBeton").change(function(){
  var selectedVal = $(this).val();
  console.log(selectedVal);
  if (selectedVal == 'beton_partisi'){
    $("div#"+selectedVal).show();
    $("div#beton_nonpartisi").hide();
  }else {
    $("div#"+selectedVal).show();
    $("div#beton_partisi").hide();
  }


});

$("#nonpartisi.classnonpartisi").css('display','None')
$("#partisi.classpartisi").css('display','None')


$("select#kategoriPintu").change(function(){
  var selectedVal = $(this).val();
  console.log(selectedVal);
  if (selectedVal == 'partisi'){
    $("div#"+selectedVal).show();
    $("div#nonpartisi").hide();
  }else {
    $("div#"+selectedVal).show();
    $("div#partisi").hide();
  }


});
console.log('kategori.js is connected')
