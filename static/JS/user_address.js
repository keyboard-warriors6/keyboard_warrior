const address = document.getElementById('id_user_address')
address.readOnly = true

document.getElementById('user_address').addEventListener('click', search)

function search() {
  new daum.Postcode({
    oncomplete: function(data) {
      let roadAddr = data.roadAddress
      let extraRoadAddr = ''
      if(data.bname !== '' && /[동|로|가]$/g.test(data.bname)){
        extraRoadAddr += data.bname
      }
      if(data.buildingName !== '' && data.apartment === 'Y'){
        extraRoadAddr += (extraRoadAddr !== '' ? ', ' + data.buildingName : data.buildingName)
      }
      if(extraRoadAddr !== ''){
        extraRoadAddr = ' (' + extraRoadAddr + ')'
      }

      document.getElementById('postalcode').value = data.zonecode
      document.getElementById("id_user_address").value = roadAddr + extraRoadAddr
    },
    theme: {
      bgColor: "#F5F5F5",
      pageBgColor: "#FFFFCC",
      emphTextColor: "#99CCFF",
      outlineColor: "#99CCFF"
    }
  }).open();
}