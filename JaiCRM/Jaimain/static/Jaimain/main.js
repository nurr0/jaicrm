const searchBtn = document.querySelector('.input-search');
const inputText = document.querySelector('.input-text')
const sidebar = document.querySelector('.left-chapters')
const sliderRight = document.querySelector('.slider__right')
const left = document.querySelector('#leftchapters')
const arrow = document.querySelector('.sidebar__arrow')
const arrowZero = document.querySelector('.sidebar__arrow-img')
const top2 = document.querySelector('.top2')
const top2Active = document.querySelector('.top2-active')
const arrow2 = document.querySelector('.sidebar__arrow-img2')
const showPartners = document.querySelector('.partners')
const showAddPartners = document.querySelector('.AddPartners')
const fileUpload = document.getElementById('id_logo')



arrow.addEventListener('click', nonActive)

function nonActive(){
    showAddPartners.classList.toggle('zero')
    showPartners.classList.toggle('zero')
    arrowZero.classList.toggle('nonActive-time');
    arrow.classList.toggle('sidebar__arrow-non');
    sidebar.classList.toggle('nonActive');
    left.classList.toggle('leftchapters-nonActive');
    const tim = setTimeout(function(){
        sidebar.classList.toggle('nonActive-time');
        top2.classList.toggle('top2-active');
        top2.classList.toggle('top2');
        top2Active.addEventListener('click', nonActive2)
    },200)
}

arrow2.addEventListener('click', nonActive2)

function nonActive2(){
    showAddPartners.classList.toggle('zero')
    showPartners.classList.toggle('zero')
    arrowZero.classList.toggle('nonActive-time');
    arrow.classList.toggle('sidebar__arrow-non');
    sidebar.classList.toggle('nonActiveTwo');
    sidebar.classList.toggle('nonActive-time');
    top2.classList.toggle('top2-active');
    top2.classList.toggle('top2');
}


const partners = document.querySelectorAll('[href="/partners/"]')[0];
partners.classList.add('partners-block')

const addPartners = document.querySelector('[href="/addpartner/"]');
addPartners.classList.add('addPartners-block')

const url = window.location.href;
if (url === 'http://127.0.0.1:8000/partners/'){
    partners.classList.add('ActiveList')
}else if (url === 'http://127.0.0.1:8000/addpartner/'){
    addPartners.classList.add('ActiveList')
}else if (url === 'http://127.0.0.1:8000/partners/1/edit//'){
    alert('mde')};


showPartners.addEventListener('click', ()=> location.href = 'http://127.0.0.1:8000/partners/')
showAddPartners.addEventListener('click', ()=> location.href = 'http://127.0.0.1:8000/addpartner/')


fileUpload.classList.add('btn-zero')

const VFail = document.querySelector('.btn-addPart');
fileUpload.addEventListener('click',failEdit)
function failEdit(){
    VFail.innerText = 'Файл выбран';
}


//Поиск (нет на всех страницах)
searchBtn.addEventListener('click', SearchEmpty)
function SearchEmpty(e){
    if (inputText.value === ''){
        e.preventDefault();
        alert('Введите текст в поиск!')
    }
}