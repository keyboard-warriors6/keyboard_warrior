const postalcode = document.getElementById('postalcode')
const addr = document.getElementById('id_address')
addr.classList.add('w-5/6')
addr.readOnly = true

addr.value = user_address

document.getElementById('address').addEventListener('click', search)


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
      document.getElementById("id_address").value = roadAddr + extraRoadAddr
    },
    theme: {
      bgColor: "#F5F5F5",
      pageBgColor: "#FFFFCC",
      emphTextColor: "#99CCFF",
      outlineColor: "#99CCFF"
    }
  }).open();
}