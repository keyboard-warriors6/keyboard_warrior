const btn1 = document.getElementById('btn1');
const sec1 = document.getElementById('sec1');

btn1.addEventListener('click', () => {
  window.scrollBy({top: sec1.getBoundingClientRect().top-180, behavior: 'smooth'});
});

const btn2 = document.getElementById('btn2');
const sec2 = document.getElementById('sec2');

btn2.addEventListener('click', () => {
  window.scrollBy({top: sec2.getBoundingClientRect().top-180, behavior: 'smooth'});
});

const btn3 = document.getElementById('btn3');
const sec3 = document.getElementById('sec3');

btn3.addEventListener('click', () => {
  window.scrollBy({top: sec3.getBoundingClientRect().top-180, behavior: 'smooth'});
});

const btn4 = document.getElementById('btn4');
const sec4 = document.getElementById('sec4');

btn4.addEventListener('click', () => {
  window.scrollBy({top: sec4.getBoundingClientRect().top-180, behavior: 'smooth'});
});