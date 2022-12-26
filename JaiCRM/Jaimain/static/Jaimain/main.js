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

if (JSON.parse(localStorage.getItem('tasks')) == 1){
    console.log('privet')
    nonActive()
} else if (JSON.parse(localStorage.getItem('tasks')) == 0){
    console.log('privet2')
    
    
}

function proverka(){
    if (JSON.parse(localStorage.getItem('tasks')) == 1){
        console.log('privet')
        nonActive()
    } else if (JSON.parse(localStorage.getItem('tasks')) == 0){
        console.log('privet2')
        nonActive2()
    }
}

// if (JSON.parse(localStorage.getItem('tasks')) == 1){
//     console.log('privet')
//     nonActive()
// }


arrow.addEventListener('click', nonActive)

function nonActive(){
    localStorage.setItem('tasks', JSON.stringify(1))
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
    localStorage.setItem('tasks', JSON.stringify(0))
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
partners.addEventListener('click',()=>
    localStorage.setItem('tasks', JSON.stringify(0))
)

const users = document.querySelector('[href="/users/"]');
users.classList.add('addPartners-block')
users.addEventListener('click',()=>
    localStorage.setItem('tasks', JSON.stringify(0))
)

const url = window.location.href;
if (url === 'http://127.0.0.1:8000/partners/'){
    partners.classList.add('ActiveList')
}else if (url === 'http://127.0.0.1:8000/partners/1/'){
    partners.classList.add('ActiveList')    
}else if (url === 'http://127.0.0.1:8000/addpartner/'){
    partners.classList.add('ActiveList')  
}else if (url === 'http://127.0.0.1:8000/partners/1/edit/'){
    partners.classList.add('ActiveList') 
}else if (url === 'http://127.0.0.1:8000/users/' || url === 'http://127.0.0.1:8000/registeruser/' ){
    users.classList.add('ActiveList')
}else if (url === 'http://127.0.0.1:8000/login/'){
    sidebar.classList.add('nonActive-time')
}



showPartners.addEventListener('click', ()=> 
    location.href = 'http://127.0.0.1:8000/partners/',
    // localStorage.setItem('tasks', JSON.stringify(1)),
    proverka()
    )
showAddPartners.addEventListener('click', ()=> 
    location.href = 'http://127.0.0.1:8000/users/',
    // localStorage.setItem('tasks', JSON.stringify(1)),
        proverka()
)

if (url === 'http://127.0.0.1:8000/addpartner/'){
    fileUpload.classList.add('btn-zero')
    const VFail = document.querySelector('.btn-addPart');
    fileUpload.addEventListener('click',failEdit)
}



function failEdit(){
    setTimeout(function(){
        VFail.innerText = 'Файл выбран';
    },1000)

}

const NamePartners = document.querySelector('.form-label')
const InputNamePartners = document.querySelector('.form-input')
const logoPartners = document.querySelectorAll('.form-label')[1]
const descriptionPartners = document.querySelectorAll('.form-label')[2]
const AreadescriptionPartners = document.querySelector('#id_description')
const TextdescriptionPartners = document.querySelectorAll('#id_description')[0]
const contactPartners = document.querySelectorAll('.form-label')[3]
const contactPhonePartners = document.querySelectorAll('.form-label')[4]
const contactEmailPartners = document.querySelectorAll('.form-label')[5]
const contactDataStartPartners = document.querySelectorAll('.form-label')[6]
const contactDataEndPartners = document.querySelectorAll('.form-label')[7]
const ActivityPart = document.querySelectorAll('.form-label')[8]
const dataDayPart = document.querySelectorAll('#id_time_start_working_day')[0]
const dataMonthPart = document.querySelectorAll('#id_time_start_working_month')[0]
const dataDayPartTwo = document.querySelector('#id_time_expires_day')
const dataMonthPartTwo = document.querySelector('#id_time_expires_month')

const TextContactLico = document.querySelector('#id_partner_person')
const TextContactPhone = document.querySelector('#id_partner_tel')
const TextContactEmail = document.querySelector('#id_partner_email')
const TextContactInn = document.querySelector('#id_iin')

if (url === 'http://127.0.0.1:8000/login/'){
    const LoginPage = document.querySelector('.content-text')
    LoginPage.classList.add('content-textLogin')

    const LoginPageLogin = document.querySelectorAll('.form-label')[0];
    LoginPageLogin.classList.add('nonActive-time')
    const LoginPageInput = document.querySelectorAll('.form-input')[0];
    LoginPageInput.setAttribute('placeholder','Введите логин')
    LoginPageInput.classList.add('input__login')

    const LoginPagePass = document.querySelectorAll('.form-label')[1];
    LoginPagePass.classList.add('nonActive-time')
    const LoginPageInputPass = document.querySelectorAll('.form-input')[1];
    LoginPageInputPass.setAttribute('placeholder','Введите пароль')
    LoginPageInputPass.classList.add('input__login')

}



if (url === 'http://127.0.0.1:8000/addpartner/'){


descriptionPartners.classList.add('p__addPart-desc')
AreadescriptionPartners.classList.add('p__addPart-width')

dataDayPart.classList.add('p__addPart-dataDay')
dataMonthPart.classList.add('p__addPart-dataDay')
dataDayPartTwo.classList.add('p__addPart-dataDay')
dataMonthPartTwo.classList.add('p__addPart-dataDay')

InputNamePartners.classList.add('p__addPart-widthRight')
TextdescriptionPartners.classList.add('p__addPart-widthRight')
TextContactLico.classList.add('p__addPart-widthRight')
TextContactPhone.classList.add('p__addPart-widthRight')
TextContactEmail.classList.add('p__addPart-widthRight')
TextContactInn.classList.add('p__addPart-widthRight')
}



//Поиск (нет на всех страницах)
// searchBtn.addEventListener('click', SearchEmpty)
// function SearchEmpty(e){
//     if (inputText.value === ''){
//         e.preventDefault();
//         alert('Введите текст в поиск!')
//     }
// }


//Поиск у пользователей
let filter = function () {
    let input = document.querySelector('.filter-input');

    input.addEventListener('keyup', FilterUser)

    function FilterUser(){
        //Ловеркейс для поиска
        let filter = input.value.toLowerCase(),
        //Ищем все li у ul
        filterElements = document.querySelectorAll('#filter-list li');

        filterElements.forEach((item) => {
            if (item.innerHTML.toLowerCase().indexOf(filter) > -1) {
                item.style.display = '';
            } else {
                item.style.display = 'none';
            }
        })}
    
};

filter();

// const imgSort = document.querySelector('.header_users-list-last')
// imgSort.addEventListener('click', sortTable);

// function sortTable(){
//     let list, i, switching, b, shouldSwitch;

//     list = document.querySelector('.list-articles');
//     switching = true;

//     while (switching) {

//         switching = false;
//         b = list.querySelectorAll('.fistUsers');

//         for (i = 0; i < (b.length - 1); i++) {

//             shouldSwitch = false;

//             if (b[i].innerHTML.toLowerCase() > b[i + 1].innerHTML.toLowerCase()) {

//                 shouldSwitch = true;
//                 break;
//         }
//     }
//     if (shouldSwitch) {

//       b[i].parentNode.insertBefore(b[i + 1], b[i]);
//       switching = true;
//     }
//   }
// }

