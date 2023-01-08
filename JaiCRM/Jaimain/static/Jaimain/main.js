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
const showShop = document.querySelector('.shops')
const fileUpload = document.getElementById('id_logo')
const category1 = document.querySelector('.category ')

if (JSON.parse(localStorage.getItem('tasks')) == 1){
    console.log('privet')
    nonActive()
} else if (JSON.parse(localStorage.getItem('tasks')) == 0){
    console.log('privet2')
    
}

function proverka(){
    if (JSON.parse(localStorage.getItem('tasks')) == 1){
        console.log('privet')
        
    } else if (JSON.parse(localStorage.getItem('tasks')) == 0){
        console.log('privet2')
        
    }
}


category1.classList.add('category10')

arrow.addEventListener('click', nonActive)

function nonActive(){
    localStorage.setItem('tasks', JSON.stringify(1))
    category1.classList.toggle('zero')
    showAddPartners.classList.toggle('zero')
    showShop.classList.toggle('zero')
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
    category1.classList.toggle('zero')
    showAddPartners.classList.toggle('zero')
    showShop.classList.toggle('zero')
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

const shop = document.querySelector('[href="/shops/"]');
shop.classList.add('shop')
shop.addEventListener('click',()=>
    localStorage.setItem('tasks', JSON.stringify(0))
)

const category = document.querySelector('[href="/product_categories/"]');
category.classList.add('category')
category.addEventListener('click',()=>
    localStorage.setItem('tasks', JSON.stringify(0))
)

const propertyBlock = document.querySelector('[href="/product_properties/"]');
propertyBlock.classList.add('property-block')
propertyBlock.addEventListener('click',()=>
    localStorage.setItem('tasks', JSON.stringify(0))
)

const settingsBlock = document.querySelector('[href="/sku/"]');
settingsBlock.classList.add('settings-block')
settingsBlock.addEventListener('click',()=>
    localStorage.setItem('tasks', JSON.stringify(0))
)

const url = window.location.href;
if (url === 'http://127.0.0.1:8000/partners/'){
    partners.classList.add('ActiveList')
}else if (url === 'http://127.0.0.1:8000/shops/'){
    shop.classList.add('ActiveList')    
}else if (url === 'http://127.0.0.1:8000/product_categories/'){
    category.classList.add('ActiveList')    
}else if (url === 'http://127.0.0.1:8000/partners/1/'){
    partners.classList.add('ActiveList')  
}else if (url === 'http://127.0.0.1:8000/addpartner/'){
    partners.classList.add('ActiveList')  
}else if (url === 'http://127.0.0.1:8000/partners/1/edit/'){
    partners.classList.add('ActiveList') 
}else if (url === 'http://127.0.0.1:8000/product_properties/'){
    propertyBlock.classList.add('ActiveList') 
}else if (url === 'http://127.0.0.1:8000/sku/'){
    settingsBlock.classList.add('ActiveList') 
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

showShop.addEventListener('click', ()=> 
location.href = 'http://127.0.0.1:8000/shops/',
// localStorage.setItem('tasks', JSON.stringify(1)),
    proverka()
)

category1.addEventListener('click', ()=> 
location.href = 'http://127.0.0.1:8000/product_categories/',
// localStorage.setItem('tasks', JSON.stringify(1)),
    proverka()
)

if (url === 'http://127.0.0.1:8000/addpartner/'){
    fileUpload.classList.add('btn-zero')
    const VFail = document.querySelector('.btn-addPart');
    fileUpload.addEventListener('click',failEdit)
    function failEdit(){
        setTimeout(function(){
            VFail.innerText = 'Файл выбран';
        },1000)
    
    }
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

if (url === 'http://127.0.0.1:8000/registeruser/'){
    const RegistName = document.querySelectorAll('.form-input')[0];
    RegistName.classList.add('form-inputRegister');
    const RegistFamily = document.querySelectorAll('.form-input')[1];
    RegistFamily.classList.add('form-inputRegister');
    const RegistLogin = document.querySelectorAll('.form-input')[2];
    RegistLogin.classList.add('form-inputRegister');
    const RegistPass = document.querySelectorAll('.form-input')[3];
    RegistPass.classList.add('form-inputRegister');
    const RegistPass2 = document.querySelectorAll('.form-input')[4];
    RegistPass2.classList.add('form-inputRegister');
    const RegistMail = document.querySelectorAll('.form-input')[5];
    RegistMail.classList.add('form-inputRegister');
    const RegistPart = document.querySelectorAll('.form-input')[6];
    RegistPart.classList.add('form-inputRegister');
    const RegistPhone = document.querySelectorAll('.form-input')[7];
    RegistPhone.classList.add('form-inputRegister');
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
if (url === 'http://127.0.0.1:8000/shops/' || url === 'http://127.0.0.1:8000/partners/' || url === 'http://127.0.0.1:8000/users/' || url === 'http://127.0.0.1:8000/product_categories/'){
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
}





if (url === 'http://127.0.0.1:8000/users/'  || url === 'http://127.0.0.1:8000/product_properties/'  || url === 'http://127.0.0.1:8000/sku/'){
    const fuck = document.querySelector('.btn-fuck') 
    
    fuck.addEventListener('click',sortTable)  

    function sortTable() {
        console.log('fuck') 
        var table, rows, switching, i, x, y, shouldSwitch;
        table = document.getElementById("myTable");
        switching = true;

        while (switching) {

          switching = false;
          rows = table.getElementsByTagName("TR");

          for (i = 1; i < (rows.length - 1); i++) {

            shouldSwitch = false;

            x = rows[i].getElementsByTagName("TD")[0];
            y = rows[i + 1].getElementsByTagName("TD")[0];
            //check if the two rows should switch place:
            if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {

              shouldSwitch = true;
              break;
            }
          }
          if (shouldSwitch) {

            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
          }
        }
      }

    //   const btnON = document.querySelector('.btnOn01')
    //   const trTable = document.querySelector('.trStyle')
    //   const stroka = document.querySelector('.list-articles')
    //   const searchUser = document.querySelector('.d7')
    //   const headerUsers = document.querySelector('.headers__users')
    //   btnON.addEventListener('click', smenaVida);
    //   function smenaVida(){
    //     trTable.classList.toggle('zero1')
    //     stroka.classList.toggle('zero1')
    //     fuck.classList.toggle('zero1')
    //     headerUsers.classList.toggle('zero1')
    //     // searchUser.classList.toggle('zero1')
    //   }
}

if (url === 'http://127.0.0.1:8000/users/' || url === 'http://127.0.0.1:8000/product_properties/' || url === 'http://127.0.0.1:8000/sku/'){
    let filter02 = function () {
        let input = document.querySelector('.filter-input');

        input.addEventListener('keyup', FilterUser)

        function FilterUser(){
            //Ловеркейс для поиска
            let filter = input.value.toLowerCase(),
            //Ищем все li у ul
            filterElements = document.querySelectorAll("tr:not(:first-child)");

            filterElements.forEach((item) => {
                if (item.innerHTML.toLowerCase().indexOf(filter) > -1) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            })}
        
    };

    filter02();
}


if (url === 'http://127.0.0.1:8000/product_categories/') {
        document.querySelectorAll('.title').forEach((el) => {
            el.addEventListener('click',()=>{
                let content = el.nextElementSibling ;
                console.log(content)

                if(content.style.maxHeight){
                    document.querySelectorAll('.children').forEach((el)=>el.style.maxHeight = null)
                } else{
                    document.querySelectorAll('.children').forEach((el)=>el.style.maxHeight = null)
                    // content.style.maxHeight = content.scrollHeight +'px';
                    // content.style.opacity="1";
                    content.classList.toggle('opa')
                }
                
            })
        })
         
        


        




    let filter03 = function () {
        let input = document.querySelector('.filter-input');

        input.addEventListener('keyup', FilterUser)

        function FilterUser(){
            //Ловеркейс для поиска
            let filter = input.value.toLowerCase(),
            //Ищем все li у ul
            filterElements = document.querySelectorAll(".menu");

            filterElements.forEach((item) => {
                if (item.innerHTML.toLowerCase().indexOf(filter) > -1) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            })}
        
    };

    filter03();
}

if (url === 'http://127.0.0.1:8000/add_sku/' ){
    const nameSku = document.querySelector('label[for="id_name"]')
    const AreaNameSku = document.querySelector('#id_name')
    nameSku.classList.add('p__addPart-width')
    
    const imgSku = document.querySelector('label[for="id_image"]')
    imgSku.classList.add('p__addPart-width')

    const descSku = document.querySelector('label[for="id_description"]')
    descSku.classList.add('p__addPart-width')

    const articulSku = document.querySelector('label[for="id_identifier"]')
    articulSku.classList.add('p__addPart-width')

    const proizvoditelSku = document.querySelector('label[for="id_producer"]')
    proizvoditelSku.classList.add('p__addPart-width')

    const categoryySku = document.querySelector('label[for="id_category"]')
    categoryySku.classList.add('p__addPart-width')

    const provertyAll = document.querySelectorAll('.form-group')
    const provertyAll01 = document.querySelectorAll('.form-group > div')[0]
    provertyAll01.classList.toggle('properyAll')
    const provertyAll02 = document.querySelectorAll('.form-group > div')[1]
    provertyAll02.classList.toggle('properyAll')
    const provertyAll03 = document.querySelectorAll('.form-group > div')[2]
    provertyAll03.classList.toggle('properyAll')
    const provertyAll04 = document.querySelectorAll('.form-group > div')[3]
    provertyAll04.classList.toggle('properyAll')
    const provertyAll05 = document.querySelectorAll('.form-group > div')[4]
    provertyAll05.classList.toggle('properyAll')

    const proverty01 = document.querySelector('#id_productpropertyrelation_set-0-DELETE')
    proverty01.setAttribute('checked','checked')
    const proverty02 = document.querySelector('#id_productpropertyrelation_set-1-DELETE')
    proverty02.setAttribute('checked','checked')
    const proverty03 = document.querySelector('#id_productpropertyrelation_set-2-DELETE')
    proverty03.setAttribute('checked','checked')
    const proverty04 = document.querySelector('#id_productpropertyrelation_set-3-DELETE')
    proverty04.setAttribute('checked','checked')
    const proverty05 = document.querySelector('#id_productpropertyrelation_set-4-DELETE')
    proverty05.setAttribute('checked','checked')

    document.querySelectorAll('.title').forEach((el) => {
        el.addEventListener('click',()=>{
            let content = el.nextElementSibling ;
            console.log(content)
            let contentPAll = content.querySelectorAll('p')[2]
            let contentP = content.querySelectorAll('p')[2].querySelector('input[type=checkbox]')
            contentP.removeAttribute('checked')
            console.log(contentP)

            document.querySelector('.plus').remove()

            if(content.style.maxHeight){
                provertyAll.forEach((el)=>el.style.maxHeight = null)
            } else{
                provertyAll.forEach((el)=>el.style.maxHeight = null)
                content.classList.toggle('opa1')
                contentPAll.classList.toggle('zero1')
                // contentP.removeAttribute('checked')
            }
            
        })
    })
}

if (/edit/.test(location.href )  && /sku/.test(location.href )){
    settingsBlock.classList.add('ActiveList') 

    const nameSku = document.querySelector('label[for="id_name"]')
    const AreaNameSku = document.querySelector('#id_name')
    nameSku.classList.add('p__addPart-width')
    
    const imgSku = document.querySelector('label[for="id_image"]')
    imgSku.classList.add('p__addPart-width')

    const imgSkuEdit = document.querySelector('#id_image')
    imgSkuEdit.classList.add('imgSkuEdit')

    const descSku = document.querySelector('label[for="id_description"]')
    descSku.classList.add('p__addPart-width')

    const articulSku = document.querySelector('label[for="id_identifier"]')
    articulSku.classList.add('p__addPart-width')

    const proizvoditelSku = document.querySelector('label[for="id_producer"]')
    proizvoditelSku.classList.add('p__addPart-width')

    const categoryySku = document.querySelector('label[for="id_category"]')
    categoryySku.classList.add('p__addPart-width')
}