const searchBtn = document.querySelector('.input-search');
const inputText = document.querySelector('.input-text')
const sidebar = document.querySelector('.left-chapters')
const sliderRight = document.querySelector('.slider__right')
const left = document.querySelector('#leftchapters')

searchBtn.addEventListener('click', SearchEmpty)

function SearchEmpty(e){
    if (inputText.value === ''){
        e.preventDefault();
        alert('Введите текст в поиск!')
    }
}


sidebar.addEventListener('click',nonActive)

function nonActive(){
    sidebar.classList.toggle('nonActive');
    // sliderRight.classList.toggle('slider__right-nonActive');
    left.classList.toggle('leftchapters-nonActive');
}


