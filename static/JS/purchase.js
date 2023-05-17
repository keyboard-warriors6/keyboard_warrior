const infos = document.querySelectorAll('.item-price')
const totalPrice = document.getElementById('total-price')
let sum = 0

function AddComma(num){
  const regexp = /\B(?=(\d{3})+(?!\d))/g;
  return num.toString().replace(regexp, ',');
}

infos.forEach((info) => {
  let price = Number(info.children[0].children[0].textContent)
  const cnt = Number(info.children[1].children[0].textContent)

  sum += price * cnt

  price = AddComma(price)
  info.children[0].children[0].textContent = price
})

const total = AddComma(sum);
totalPrice.textContent = total

const address = document.getElementById('address').textContent
const addressTag = document.querySelector('[name=address]')

addressTag.value = address