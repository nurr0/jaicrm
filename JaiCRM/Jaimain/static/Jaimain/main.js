const searchBtn = document.querySelector('.input-search');
const inputText = document.querySelector('.input-text')
const sidebar = document.querySelector('.left-chapters')
const sliderRight = document.querySelector('.slider__right')
const left = document.querySelector('#leftchapters')
const arrow = document.querySelector('.sidebar__arrow')
const top2 = document.querySelector('.top2')
const top2Active = document.querySelector('.top2-active')
const arrow2 = document.querySelector('.sidebar__arrow-img2')






arrow.addEventListener('click',nonActive)

function nonActive(){

    //Открыть плашку мини
    arrow.classList.toggle('sidebar__arrow-non');
    sidebar.classList.toggle('nonActive');
    // sliderRight.classList.toggle('slider__right-nonActive');
    left.classList.toggle('leftchapters-nonActive');
    const tim = setTimeout(function(){
        sidebar.classList.toggle('nonActive-time');
        top2.classList.toggle('top2-active');
        top2.classList.toggle('top2');
        top2Active.addEventListener('click', nonActive2)
    },300)
}

arrow2.addEventListener('click', nonActive2)

function nonActive2(){

    arrow.classList.toggle('sidebar__arrow-non');
    sidebar.classList.toggle('nonActive');
    sidebar.classList.toggle('nonActiveTwo');
    left.classList.toggle('leftchapters-nonActive');
    sidebar.classList.toggle('nonActive-time');
    top2.classList.toggle('top2-active');
    top2.classList.toggle('top2');
    
}


const partners = document.querySelectorAll('[href="/partners/"]')[1];
const addPartners = document.querySelector('[href="/addpartner/"]');
const url = window.location.href;
if (url === 'http://127.0.0.1:8000/partners/'){
    addPartners.classList.add('nonActiveList')
}else if (url === 'http://127.0.0.1:8000/addpartner/'){
    partners.classList.add('nonActiveList')
}

const partners_link = document.querySelector('.partners');
partners_link.addEventListener('click',()=> location.href = 'http://127.0.0.1:8000/partners/')


//Поиск (нет на всех страницах)
searchBtn.addEventListener('click', SearchEmpty)
function SearchEmpty(e){
    if (inputText.value === ''){
        e.preventDefault();
        alert('Введите текст в поиск!')
    }
}