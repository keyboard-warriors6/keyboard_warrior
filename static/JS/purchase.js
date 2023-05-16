const infos = document.querySelectorAll('.item-price')
const totalPrice = document.getElementById('total-price')
let sum = 0

infos.forEach((info) => {
  const price = Number(info.children[0].children[0].textContent)
  const cnt = Number(info.children[1].children[0].textContent)

  sum += price * cnt
})

totalPrice.textContent = sum