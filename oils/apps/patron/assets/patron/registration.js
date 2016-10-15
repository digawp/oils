import $ from 'jquery'

$('#id_identification_1').on('input', function(e){
  $('#id_username').val(e.currentTarget.value)
})

$('#id_membership_type').on('input', function(e){
  let curMemTypId = e.currentTarget.value
  if (curMemTypId !== ""){
    let url = `/api/memberships/membershiptype/${curMemTypId}/`
    fetch(url).then(resp=>resp.json()).then(data=>{
      $('#id_loan_duration').val(data['loan_duration'])
      $('#id_loan_limit').val(data['loan_limit'])
      $('#id_renewal_limit').val(data['renewal_limit'])
    })
  }
})
