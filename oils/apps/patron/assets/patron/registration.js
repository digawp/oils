import $ from 'jquery'

$('#id_identification_1').on('input', function(e){
  $('#id_username').val(e.currentTarget.value)
})
