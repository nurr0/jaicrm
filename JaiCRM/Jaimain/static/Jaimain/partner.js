const btnApi2 = document.querySelector('.btn__api3')
const modal  = document.querySelector('.modal3')
const imgCross = document.querySelector('.imgCross')

btnApi2.addEventListener('click', btnApiAction2)
function btnApiAction2(){
    modal.classList.toggle('zero3')
    window.scrollBy(0, -800)
    
}

imgCross.addEventListener('click', imgCrossAction)
function imgCrossAction(){
    modal.classList.toggle('zero3')
}
console.log('Вау');

const formElemBtn = document.querySelector('.btn__submit-form')
formElemBtn.addEventListener('click', postForm)
async function postForm(e){
    
    // e.preventDefault();
    
    

    let response = await fetch('/api/v1/sales_channel/', {
        method: 'POST',

        body: new FormData(formElem)
    });

    let result = await response.json();
 
}
/////////////////////////////////


const btnApi4 = document.querySelector('.btn__api4')
const modal4  = document.querySelector('.modal4')
const imgCross4 = document.querySelector('.imgCross4')

btnApi4.addEventListener('click', btnApiAction4)
function btnApiAction4(){
    modal4.classList.toggle('zero4')
    console.log('Привет');
    window.scrollBy(0, -800)
    
}

imgCross4.addEventListener('click', imgCrossAction4)
function imgCrossAction4(){
    modal4.classList.toggle('zero4')
}


const formElemBtn4 = document.querySelector('.btn__submit-form4')
formElemBtn4.addEventListener('click', postForm4)
async function postForm4(e){
    
    // e.preventDefault();
    
    

    let response = await fetch('/api/v1/payment_form/', {
        method: 'POST',

        body: new FormData(formElem2)
    });

    let result = await response.json();
 
}