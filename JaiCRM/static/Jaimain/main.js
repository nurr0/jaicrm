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
       
        
    }
}


category1.classList.add('category10')
category1.classList.add('zero1')

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

const suppliesBlock = document.querySelector('[href="/supplies/"]');
suppliesBlock.classList.add('suppliesBlock')
suppliesBlock.addEventListener('click',()=>
    localStorage.setItem('tasks', JSON.stringify(0))
)

const tovariNaSklade = document.querySelector('[href="/products_in_stock/"]');
tovariNaSklade.classList.add('tovariNaSklade')
tovariNaSklade.addEventListener('click',()=>
    localStorage.setItem('tasks', JSON.stringify(0))
)

const regisProdaz = document.querySelector('[href="/receipt_registration/"]');
regisProdaz.classList.add('regisProdaz')
regisProdaz.addEventListener('click',()=>
    localStorage.setItem('tasks', JSON.stringify(0))
)

const prodazh = document.querySelector('[href="/sell_receipt_list/"]');
prodazh.classList.add('prodazh')
prodazh.addEventListener('click',()=>
    localStorage.setItem('tasks', JSON.stringify(0))
)

const dashboard = document.querySelector('[href="/dashboard/"]');
dashboard.classList.add('dashboard')
dashboard.addEventListener('click',()=>
    localStorage.setItem('tasks', JSON.stringify(0))
)

const customers = document.querySelector('[href="/customers/"]');
customers.classList.add('customers')
customers.addEventListener('click',()=>
    localStorage.setItem('tasks', JSON.stringify(0))
)

const url = window.location.href;
if (/partners/.test(location.href )){
    partners.classList.add('ActiveList')
}else if (/shops/.test(location.href )){
    shop.classList.add('ActiveList')    
}else if (/product_categories/.test(location.href )){
    category.classList.add('ActiveList')    

}else if (/addpartner/.test(location.href )){
    partners.classList.add('ActiveList')  

}else if (/product_properties/.test(location.href ) ){
    propertyBlock.classList.add('ActiveList') 
}else if (/customers/.test(location.href ) ){
    customers.classList.add('ActiveList') 
}else if (/sku/.test(location.href )){
    settingsBlock.classList.add('ActiveList') 
}else if (/dashboard/.test(location.href )){
    dashboard.classList.add('ActiveList') 
}else if (/supplies/.test(location.href )  ||  /add_supply/.test(location.href )  ){
    suppliesBlock.classList.add('ActiveList')
}else if (/products_in_stock/.test(location.href ) || /add_price/.test(location.href )){
    tovariNaSklade.classList.add('ActiveList')
}else if (/sell_receipt_list/.test(location.href )){
    prodazh.classList.add('ActiveList')
}else if (/receipt_registration/.test(location.href )){
    regisProdaz.classList.add('ActiveList')
}else if (/users/.test(location.href ) || /registeruser/.test(location.href ) ){
    users.classList.add('ActiveList')
}else if (/login/.test(location.href )){
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

if (/addpartner/.test(location.href )){
    // fileUpload.classList.add('btn-zero')
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

if (/login/.test(location.href )){
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

if (/registeruser/.test(location.href )){
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

if (/addpartner/.test(location.href )){


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




//Поиск у пользователей и партнеров
if (/shops/.test(location.href ) ||  /users/.test(location.href )||  /partners/.test(location.href ) || /product_categories/.test(location.href ) ){
    let filter = function () {
        let input = document.querySelector('.filter-input');

        

        input.addEventListener('keyup', FilterUser)
        

        function FilterUser(){
            //Ловеркейс для поиска
            let filter = input.value.toLowerCase(),
            //Ищем все li у ul
            filterElements = document.querySelectorAll('#filter-list li');
            //Странное решение
            if (input.value == ''){
                location.reload()}

            filterElements.forEach((item) => {
                if (item.innerHTML.toLowerCase().indexOf(filter) > -1) {
                    // item.style.display = '';
                    item.classList.remove('zero1')
                    item.classList.remove('num')
                
                } else {
                    // item.style.display = 'none';
                    item.classList.add('zero1')
                    item.classList.add('num')
                }
            })}
            
        
    };
    filter();
}





if (/users/.test(location.href )  || /product_properties/.test(location.href )  || location.pathname === '/sku/' || /products_in_stock/.test(location.href ) || /sell_receipt_list/.test(location.href )  ||   /supplies/.test(location.href ) || /customers/.test(location.href ) ){
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


}

if (/supplies/.test(location.href )){
    let filter04 = function () {
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

    filter04();
}

if (/users/.test(location.href ) ||/product_properties/.test(location.href ) || location.pathname === '/sku/' || /products_in_stock/.test(location.href ) ){
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

if ( /sell_receipt_list/.test(location.href )){
    let filter06 = function () {
        let input = document.querySelector('.filter-input');

        input.addEventListener('keyup', FilterUser)

        function FilterUser(){
            //Ловеркейс для поиска
            let filter = input.value.toLowerCase(),
            //Ищем все li у ul
            filterElements = document.querySelector('.trStyle').querySelectorAll("tr:not(:first-child)");

            filterElements.forEach((item) => {
                if (item.innerHTML.toLowerCase().indexOf(filter) > -1) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            })}
        
    };

    filter06();
}


if (/product_categories/.test(location.href ) ) {
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

if (/add_sku/.test(location.href )  ){
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

    const provertyAll06 = document.querySelectorAll('.form-group > div')[5]
    provertyAll06.classList.toggle('properyAll')
    const provertyAll07 = document.querySelectorAll('.form-group > div')[6]
    provertyAll07.classList.toggle('properyAll')
    const provertyAll08 = document.querySelectorAll('.form-group > div')[7]
    provertyAll08.classList.toggle('properyAll')
    const provertyAll09 = document.querySelectorAll('.form-group > div')[9]
    provertyAll09.classList.toggle('properyAll')
    const provertyAll10 = document.querySelectorAll('.form-group > div')[10]
    provertyAll10.classList.toggle('properyAll')

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

    const proverty06 = document.querySelector('#id_productpropertyrelation_set-6-DELETE')
    proverty06.setAttribute('checked','checked')
    const proverty07 = document.querySelector('#id_productpropertyrelation_set-7-DELETE')
    proverty07.setAttribute('checked','checked')
    const proverty08 = document.querySelector('#id_productpropertyrelation_set-8-DELETE')
    proverty08.setAttribute('checked','checked')
    const proverty09 = document.querySelector('#id_productpropertyrelation_set-9-DELETE')
    proverty09.setAttribute('checked','checked')
    const proverty10 = document.querySelector('#id_productpropertyrelation_set-10-DELETE')
    proverty10.setAttribute('checked','checked')

    document.querySelectorAll('.plus').forEach((el) => {
        el.addEventListener('click',()=>{
            let content = el.nextElementSibling ;
            console.log(content)
            let contentPAll = content.querySelectorAll('p')[2]
            let contentP = content.querySelectorAll('p')[2].querySelector('input[type=checkbox]')
            contentP.removeAttribute('checked')
            console.log(contentP)

            document.querySelector('.plus').classList.toggle('zero5')

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
    document.querySelectorAll('.plusminus').forEach((el) => {
        el.addEventListener('click',()=>{
            let papa = el.closest('.properyAll')
            let znach = el.parentElement.querySelector('input')
            znach.value = ''
            let svoystvo = el.parentElement.querySelector('select')
            svoystvo.options = '0'
            svoystvo.value = '';
            let check = el.parentElement.querySelector('input[type=checkbox]')
            check.setAttribute('checked','checked')
            document.querySelector('.plus').classList.toggle('zero5')
            papa.classList.toggle('opa1')
            
            
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

    //Убираем пустые блоки
    const xz0 = document.querySelector('#id_productpropertyrelation_set-0-value')
    if (xz0 != null){
        const zxc0 = xz0.value;
        parentxz0 = xz0.closest("p");
        glavParentxz0 = parentxz0.closest("div");
        console.log(zxc0)

        if (zxc0 == ''){
            glavParentxz0.classList.toggle('zero1')
            glavParentxz0.insertAdjacentHTML('beforeBegin','<img class="title plus" src="/static/Jaimain/images/plus.png" alt=""></img>')

            document.querySelectorAll('.title').forEach((el) => {
                el.addEventListener('click',()=>{
                    let content1 = el.nextElementSibling ;
                    console.log(content1)

                    content1.classList.toggle('zero1')
                    el.remove()
 
                })
            })
    
        }

    }

    const xz1 = document.querySelector('#id_productpropertyrelation_set-1-value')
    if (xz1 != null){
        const zxc1 = xz1.value; //значение
        parentxz1 = xz1.closest("p"); // тег p
        glavParentxz1 = parentxz1.closest("div"); //высший тег div
        console.log(zxc1)
        if (zxc1 == ''){
            glavParentxz1.classList.toggle('zero1')
            glavParentxz1.insertAdjacentHTML('beforeBegin','<img class="title plus" src="/static/Jaimain/images/plus.png" alt=""></img>')

            document.querySelectorAll('.title').forEach((el) => {
                el.addEventListener('click',()=>{
                    let content1 = el.nextElementSibling ;
                    console.log(content1)

                    content1.classList.toggle('zero1')
                    el.remove()

                })
            })
    
        }
    }


    const xz2 = document.querySelector('#id_productpropertyrelation_set-2-value')
    if (xz2 != null){
        const zxc2 = xz2.value;
        parentxz2 = xz2.closest("p");
        glavParentxz2 = parentxz2.closest("div");
        console.log(zxc2)

        if (zxc2 == ''){
            glavParentxz2.classList.toggle('zero1')
            glavParentxz2.insertAdjacentHTML('beforeBegin','<img class="title plus" src="/static/Jaimain/images/plus.png" alt=""></img>')

            document.querySelectorAll('.title').forEach((el) => {
                el.addEventListener('click',()=>{
                    let content1 = el.nextElementSibling ;
                    console.log(content1)
                    content1.classList.toggle('zero1')
                    el.remove()

                    
                })
            })
    
        }
    }

    const xz3 = document.querySelector('#id_productpropertyrelation_set-3-value')
    if (xz3 != null){
        const zxc3 = xz3.value; //значение
        parentxz3 = xz3.closest("p"); // тег p
        glavParentxz3 = parentxz3.closest("div"); //высший тег div
        papaGlavParentxz3 = glavParentxz3.closest(".form-group")
        console.log(zxc3)

        if (zxc3 == ''){
            glavParentxz3.classList.toggle('zero1')
            glavParentxz3.insertAdjacentHTML('beforeBegin','<img class="title plus" src="/static/Jaimain/images/plus.png" alt=""></img>')

            
            document.querySelectorAll('.title').forEach((el) => {
                el.addEventListener('click',()=>{
                    let content1 = el.nextElementSibling ;
                    console.log(content1)

                    content1.classList.toggle('zero1')
                    el.remove()

                    
                })
            })
            

        }
    }

    const xz4 = document.querySelector('#id_productpropertyrelation_set-4-value')
    if (xz4 !== null){
        const zxc4 = xz4.value; //значение
        parentxz4 = xz4.closest("p"); // тег p
        glavParentxz4 = parentxz4.closest("div"); //высший тег div
        papaGlavParentxz4 = glavParentxz4.closest(".form-group")
        console.log(zxc4)

        if (zxc4 == ''){
            glavParentxz4.classList.toggle('zero1')
            glavParentxz4.insertAdjacentHTML('beforeBegin','<img class="title plus" src="/static/Jaimain/images/plus.png" alt=""></img>')

            document.querySelectorAll('.title').forEach((el) => {
                el.addEventListener('click',()=>{
                    let content1 = el.nextElementSibling ;
                    console.log(content1)

                    content1.classList.toggle('zero1')
                    el.remove()

                    
                })
            })
        }
    
    }

    const xz5 = document.querySelector('#id_productpropertyrelation_set-5-value')
    if (xz5 !== null){
        const zxc5 = xz5.value; //значение
        parentxz5 = xz5.closest("p"); // тег p
        glavParentxz5 = parentxz5.closest("div"); //высший тег div
        console.log(zxc5)
        if (zxc5 == ''){
            glavParentxz5.classList.toggle('zero1')
            glavParentxz5.insertAdjacentHTML('beforeBegin','<img class="title plus" src="/static/Jaimain/images/plus.png" alt=""></img>')

            document.querySelectorAll('.title').forEach((el) => {
                el.addEventListener('click',()=>{
                    let content1 = el.nextElementSibling ;
                    console.log(content1)

                    content1.classList.toggle('zero1')
                    el.remove()

                    
                })
            })
            
        }
    }

    const xz6 = document.querySelector('#id_productpropertyrelation_set-6-value')
    if (xz6 !== null){
        const zxc6 = xz6.value; //значение
        parentxz6 = xz6.closest("p"); // тег p
        glavParentxz6 = parentxz6.closest("div"); //высший тег div
        console.log(zxc6)
        if (zxc6 == ''){
            glavParentxz6.classList.toggle('zero1')
            glavParentxz6.insertAdjacentHTML('beforeBegin','<img class="title plus" src="/static/Jaimain/images/plus.png" alt=""></img>')

            document.querySelectorAll('.title').forEach((el) => {
                el.addEventListener('click',()=>{
                    let content1 = el.nextElementSibling ;
                    console.log(content1)

                    content1.classList.toggle('zero1')
                    el.remove()

                    
                })
            })
    
        }
    }

    const xz7 = document.querySelector('#id_productpropertyrelation_set-7-value')
    if (xz7 !== null){
        const zxc7 = xz7.value; //значение
        parentxz7 = xz7.closest("p"); // тег p
        glavParentxz7 = parentxz7.closest("div"); //высший тег div
        console.log(zxc7)
        if (zxc7 == ''){
            glavParentxz7.classList.toggle('zero1')
            glavParentxz7.insertAdjacentHTML('beforeBegin','<img class="title plus" src="/static/Jaimain/images/plus.png" alt=""></img>')

            document.querySelectorAll('.title').forEach((el) => {
                el.addEventListener('click',()=>{
                    let content1 = el.nextElementSibling ;
                    console.log(content1)

                    content1.classList.toggle('zero1')
                    el.remove()

                    
                })
            })
    
        }
    }
}
// const widthPolya = document.querySelectorAll('span[class*=select2-container]')
// for (let item of widthPolya){
//     item.classList.add('widthPilya')
// }



// if (/partners/.test(location.href ) ){
//     // let count = 8; //всего записей
//     let count = document.querySelectorAll(".num").length;
//     let cnt = 4; //сколько отображаем сначала
//     let cnt_page = Math.ceil(count / cnt); //кол-во страниц

//     //выводим список страниц
//     let paginator = document.querySelector(".paginator");
//     let page = "";
//     for (var i = 0; i < cnt_page; i++) {
//     page += "<span data-page=" + i * cnt + "  id=\"page" + (i + 1) + "\">" + (i + 1) + "</span>";
//     }
//     paginator.innerHTML = page;

//     //выводим первые записи {cnt}
//     let div_num = document.querySelectorAll(".num");
//     for (var i = 0; i < div_num.length; i++) {
//         if (i < cnt) {
//             div_num[i].style.display = "block";
//         }
//     }

//     let main_page = document.getElementById("page1");
//     main_page.classList.add("paginator_active");

//     //листаем
//     function pagination(event) {
//         let e = event || window.event;
//         let target = e.target;
//         let id = target.id;
        
//         if (target.tagName.toLowerCase() != "span") return;
        
        
//         let data_page = +target.dataset.page;
//         main_page.classList.remove("paginator_active");
//         main_page = document.getElementById(id);
//         main_page.classList.add("paginator_active");

//         let j = 0;
//         for (let i = 0; i < div_num.length; i++) {
//             // var data_num = div_num[i].dataset.num;
//             var data_num = div_num[i].querySelector('.btn__text').href[31]
//             // document.querySelectorAll(".num")[0].querySelector('.btn__text').href[31]
//             if (data_num <= data_page || data_num >= data_page)
//             div_num[i].style.display = "none";

//         }
//         for (let i = data_page; i < div_num.length; i++) {
//             if (j >= cnt) break;
//             div_num[i].style.display = "block";
//             j++;
//             }
//     }

//         const spanNumber = document.querySelectorAll('span')
//         for (let item of spanNumber){
//             item.classList.add('spanNumber')
//         }
// }

// if (/add_supply/.test(location.href ) ){
//     const tovarz = document.querySelectorAll('.form-group1')
//     const plus1 = document.querySelector('.plus1')
//     for (let item of tovarz){
//         item.classList.toggle('zero1')
//     }

//     plus1.addEventListener('click', plus1Action)
//     function plus1Action(){
//         for (let item of tovarz){
//             if (item.classList.contains('zero1')){
//                 item.classList.toggle('zero1')
//                 const checkbox = item.querySelector('input[type=checkbox]')
//                 checkbox.removeAttribute('checked')
//                 return
//             }

//         }
//     }
//     const checkDelete = document.querySelectorAll('input[type=checkbox]')

//     const proverty01 = document.querySelector('#id_productsinsupply_set-0-DELETE')
//     proverty01.setAttribute('checked','checked')
//     const proverty02 = document.querySelector('#id_productsinsupply_set-1-DELETE')
//     proverty02.setAttribute('checked','checked')
//     // const proverty03 = document.querySelector('#id_productsinsupply_set-2-DELETE')
//     // proverty03.setAttribute('checked','checked')
//     // const proverty04 = document.querySelector('#id_productsinsupply_set-3-DELETE')
//     // proverty04.setAttribute('checked','checked')
//     // const proverty05 = document.querySelector('#id_productsinsupply_set-4-DELETE')
//     // proverty05.setAttribute('checked','checked')
//     // const proverty06 = document.querySelector('#id_productsinsupply_set-5-DELETE')
//     // proverty06.setAttribute('checked','checked')
//     // const proverty07 = document.querySelector('#id_productsinsupply_set-6-DELETE')
//     // proverty07.setAttribute('checked','checked')
//     // const proverty08 = document.querySelector('#id_productsinsupply_set-7-DELETE')
//     // proverty08.setAttribute('checked','checked')
//     // const proverty09 = document.querySelector('#id_productsinsupply_set-8-DELETE')
//     // proverty09.setAttribute('checked','checked')
//     // const proverty10 = document.querySelector('#id_productsinsupply_set-9-DELETE')
//     // proverty10.setAttribute('checked','checked')


//     const udalit1 = document.querySelectorAll('p')[9]
//     udalit1.classList.toggle('zero')

//     const udalit2 = document.querySelectorAll('p')[13]
//     udalit2.classList.toggle('zero')

//     // const udalit3 = document.querySelectorAll('p')[17]
//     // udalit3.classList.toggle('zero')

//     // const udalit4 = document.querySelectorAll('p')[21]
//     // udalit4.classList.toggle('zero')

//     // const udalit5 = document.querySelectorAll('p')[25]
//     // udalit5.classList.toggle('zero')

//     // const udalit6 = document.querySelectorAll('p')[29]
//     // udalit6.classList.toggle('zero')

//     // const udalit7 = document.querySelectorAll('p')[33]
//     // udalit7.classList.toggle('zero')

//     // const udalit8 = document.querySelectorAll('p')[37]
//     // udalit8.classList.toggle('zero')

//     // const udalit9 = document.querySelectorAll('p')[41]
//     // udalit9.classList.toggle('zero')

//     // const udalit10 = document.querySelectorAll('p')[45]
//     // udalit10.classList.toggle('zero')

//     document.querySelectorAll('.title0').forEach((el) => {
//         el.addEventListener('click',()=>{
//             let content = el.nextElementSibling ;
           
//             let contentP = content.querySelector('input[type=checkbox]')
//             contentP.setAttribute('checked','checked')
            
//             content.classList.toggle('zero1')
//             el.classList.toggle('zero1')

//         })
//     })
//     const postav = document.querySelector('label[for="id_supplier"]')
//     postav.classList.add('p__addPart-width')

//     const doc = document.querySelector('label[for="id_document"]')
//     doc.classList.add('p__addPart-width')

//     const date = document.querySelector('label[for="id_date_day"]')
//     date.classList.add('p__addPart-width')

//     const sklad = document.querySelector('label[for="id_warehouse"]')
//     sklad.classList.add('p__addPart-width')
    

// }

// if (/receipt_registration/.test(location.href ) ){
//     const tovarz = document.querySelectorAll('.form-group')
//     const plus1 = document.querySelector('.plus')
//     for (let item of tovarz){
//         item.classList.toggle('zero1')
//     }

//     plus1.addEventListener('click', plus1Action)
//     function plus1Action(){
//         for (let item of tovarz){
//             if (item.classList.contains('zero1')){
//                 item.classList.toggle('zero1')
//                 const checkbox = item.querySelector('input[type=checkbox]')
//                 checkbox.removeAttribute('checked')
//                 return
//             }

//         }
//     }

//     const proverty01 = document.querySelector('#id_prods-0-DELETE')
//     proverty01.setAttribute('checked','checked')
//     // const proverty02 = document.querySelector('#id_prods-1-DELETE')
//     // proverty02.setAttribute('checked','checked')

//     document.querySelectorAll('.title0').forEach((el) => {
//         el.addEventListener('click',()=>{
//             let content = el.nextElementSibling ;
           
//             let contentP = content.querySelector('input[type=checkbox]')
//             contentP.setAttribute('checked','checked')
            
//             content.classList.toggle('zero1')
//             el.classList.toggle('zero1')

//         })
//     })

//     // const udalit1 = document.querySelectorAll('div')[33]
//     // udalit1.classList.toggle('zero')

//     // const udalit2 = document.querySelectorAll('div')[41]
//     // udalit2.classList.toggle('zero')
// }

if (/product_properties/.test(location.href )){
    const arTd = document.querySelectorAll('.tdStyle')
    
    const formElemBtn = document.querySelector('.btn__submit-form')
    formElemBtn.addEventListener('click', postForm)
    async function postForm(e){
        let areaName = document.querySelector('.formElem-name').value
        // e.preventDefault();
        for (let item of arTd){
            if (areaName == item.innerHTML){
                alert('Данное свойство уже имеется! Добавьте другое')
                e.preventDefault();
                
            }else if(areaName !== item.innerHTML){
                console.log('Все ок!')
                
            }   
        }
    
        let response = await fetch('http://127.0.0.1:8000/api/v1/propertylist/', {
          method: 'POST',

          body: new FormData(formElem)
        });
    
        let result = await response.json();
    
        // alert(result.message);
       
    }
    const btnApi = document.querySelector('.btn__api')
    const modal  = document.querySelector('.modal')
    const imgCross = document.querySelector('.imgCross')

    btnApi.addEventListener('click', btnApiAction)
    function btnApiAction(){
        modal.classList.toggle('zero1')
    }

    imgCross.addEventListener('click', imgCrossAction)
    function imgCrossAction(){
        modal.classList.toggle('zero1')
    }

 
}

if (/product_categories/.test(location.href )){
    const arTd = document.querySelectorAll('a')
    
    const formElemBtn = document.querySelector('.btn__submit-form')
    formElemBtn.addEventListener('click', postForm)
    async function postForm(e){
        
        let areaName = document.querySelector('.formElem-name').value
        // e.preventDefault();
        for (let item of arTd){
            if (areaName == item.innerHTML){
                alert('Данная категория уже имеется! Добавьте другую')
                e.preventDefault();
                
            }else if(areaName !== item.innerHTML){
                console.log('Все ок!')
                
            }   
        }
    
        let response = await fetch('http://127.0.0.1:8000/api/v1/product_cats/', {
          method: 'POST',

          body: new FormData(formElem)
        });
    
        let result = await response.json();
    

       
    }
    const btnApi = document.querySelector('.btn__api')
    const modal  = document.querySelector('.modal')
    const imgCross = document.querySelector('.imgCross')

    btnApi.addEventListener('click', btnApiAction)
    function btnApiAction(){
        modal.classList.toggle('zero1')
    }

    imgCross.addEventListener('click', imgCrossAction)
    function imgCrossAction(){
        modal.classList.toggle('zero1')
    }
    async function getCategory(){
        const podskazka = document.querySelector('.podskazka')
        let response = await fetch('http://127.0.0.1:8000/api/v1/product_cats/');
        
        let result = await response.json();

        let div = document.createElement('option');
        podskazka.appendChild(div)

        for (let item of result){
            let div = document.createElement('option');
            let option = document.createElement('option');
            console.log("id: " + item.id + "   " + "Имя категории " + item.name)
            // const nameItem = "id: " + item.id + "   " + "Имя категории " + item.name
            const nameItem =  item.name
            // podskazka.appendChild(option)
            podskazka.appendChild(div)
            div.innerHTML = nameItem
            const idOpt = item.id
            div.setAttribute('value',idOpt)
            if (item.level == 1){
                div.innerHTML = "--- " + div.innerHTML
            }
            if (item.level == 2){
                div.innerHTML = "------ " + div.innerHTML
            }
            if (item.level == 3){
                div.innerHTML = "--------- " + div.innerHTML
            }
            if (item.level == 4){
                div.innerHTML = "------------ " + div.innerHTML
            }
            if (item.level == 5){
                div.innerHTML = "--------------- " + div.innerHTML
            }
            

        }


     
    }
    getCategory()
 
}

if (/shops/.test(location.href )){
    const arTd = document.querySelectorAll('.name__shop')
    
    const formElemBtn = document.querySelector('.btn__submit-form')
    formElemBtn.addEventListener('click', postForm)
    async function postForm(e){
        let areaName = document.querySelector('.formElem-name').value
        // e.preventDefault();
        for (let item of arTd){
            if (areaName == item.innerHTML){
                alert('Данная точка уже имеется! Добавьте другую')
                e.preventDefault();
                
            }else if(areaName !== item.innerHTML){
                console.log('Все ок!')
                
            }   
        }
    
        let response = await fetch('/api/v1/shoplist/', {
          method: 'POST',

          body: new FormData(formElem)
        });
    
        let result = await response.json();
    
        // alert(result.message);
       
    }
    const btnApi = document.querySelector('.btn__api')
    const modal  = document.querySelector('.modal')
    const imgCross = document.querySelector('.imgCross')

    btnApi.addEventListener('click', btnApiAction)
    function btnApiAction(){
        modal.classList.toggle('zero1')
    }

    imgCross.addEventListener('click', imgCrossAction)
    function imgCrossAction(){
        modal.classList.toggle('zero1')
    }

    
 
}

if (/sell_receipt_list/.test(location.href )){
    const arTd = document.querySelectorAll('.tdStyle')
    
    const formElemBtn = document.querySelector('.btn__submit-form')
    formElemBtn.addEventListener('click', postForm)
    async function postForm(e){
        
        e.preventDefault();
        
        let host = location.host
        let response = await fetch('/api/v1/sales_report_export/', {
          method: 'POST',

          body: new FormData(formElem)
        });
    
        let result = await response.json();
    
        // alert(result.message);
       
    }
    const btnApi = document.querySelector('.btn__api')
    const modal  = document.querySelector('.modal')
    const imgCross = document.querySelector('.imgCross')

    btnApi.addEventListener('click', btnApiAction)
    function btnApiAction(){
        modal.classList.toggle('zero1')
    }

    imgCross.addEventListener('click', imgCrossAction)
    function imgCrossAction(){
        modal.classList.toggle('zero1')
    }

 
}

const btnApiOt = document.querySelector('.btn__apiOt')
const modalOt  = document.querySelector('.modalOt')
const imgCrossOt = document.querySelector('.imgCrossOt')
const divArea = document.querySelector('.reportsApi')

btnApiOt.addEventListener('click', btnApiActionOt)
    function btnApiActionOt(){
        modalOt.classList.toggle('zero1')

        let filterOt = function () {
            let input = document.querySelector('.filter-inputOt');
            input.addEventListener('keyup', FilterUser)

            function FilterUser(){
                //Ловеркейс для поиска
                let filter = input.value.toLowerCase(),
                //Ищем все li у ul
                filterElements = document.querySelectorAll('.otcheti');
                //Странное решение
                // if (input.value == ''){
                //     location.reload()}
    
                filterElements.forEach((item) => {
                    if (item.innerHTML.toLowerCase().indexOf(filter) > -1) {
                        // item.style.display = '';
                        item.classList.remove('zero1')
                        item.classList.remove('num')
                    
                    } else {
                        // item.style.display = 'none';
                        item.classList.add('zero1')
                        item.classList.add('num')
                    }
                })}
                
            
        };
        filterOt();
       
    }

imgCrossOt.addEventListener('click', imgCrossActionOt)
function imgCrossActionOt(){
    modalOt.classList.toggle('zero1')
    // divArea.innerHTML = '';
}

async function postForm(e){
        
    // e.preventDefault();
    // let user = {
    //     page_size: 1,
    //   };
    
    let response = await fetch('/api/v1/reports/');
    // let response = await fetch('/api/v1/reports/', {
    //     method: 'POST',
    //     headers: {
    //       'Content-Type': 'application/json;charset=utf-8'
    //     },
    //     body: JSON.stringify(user)
    //   });

    let result = await response.json();
    
    console.log(result)
    // const divArea = document.querySelector('.reportsApi')
   
    for (let item of result){
        let divId = item.id
        let divFile = item.file
        let divName = item.file_name
        let divGod = item.datetime
        let divData = divGod.slice(0,10)
        let divDataDay = divGod.slice(11,16)

        const divNew = document.createElement('div')
        // divNew.innerHTML = divId + " " + divFile + " " + divName + " " + divData
        divNew.innerHTML = `<div class='otcheti otcheti1'>  <div class='z x'>${divName}</div>  <div class='z'>${divData}</div> <div class='z'>${divDataDay}</div>   <a class='btn' href="${divFile}">Скачать</a>  </div>`
        divArea.appendChild(divNew)
        
    }
    
     
   
}
postForm()

if (/add_price/.test(location.href )  ){
    
    const poschitat = document.querySelectorAll('.procent__btn') 
    
    for (let item of poschitat){
    // poschitat.addEventListener('click',podchet)
        item.addEventListener('click',podchet)

        function podchet(e){
            e.preventDefault();
        
            // const div = poschitat.closest('div')
            const div = item.closest('div')
            const glavDiv = div.closest('.form-group-addPrice')

            const procentVnytr = div.querySelector('.procent__text').value
            const cenaVnytr = glavDiv.querySelector("input[type='number']")
            const poslenyaStoimVnytr = glavDiv.querySelectorAll("input[type='text']")[1].value
            console.log(div)
            console.log(procentVnytr)
            console.log(glavDiv);
            console.log(typeof(cenaVnytr));
            console.log(poslenyaStoimVnytr);
            const result = Number(poslenyaStoimVnytr) + ( Number(poslenyaStoimVnytr) * (Number(procentVnytr) / 100))
            console.log(result);
            cenaVnytr.value = result

        }
    }

}

if (/receipt_registration/.test(location.href )  ){
    const inputsss = document.querySelectorAll("input[type='number']")
    for (let item of inputsss){
        item.classList.add('inputsss')
    }
    const inputsssCelect = document.querySelectorAll("select")
    for (let item of inputsssCelect){
        item.classList.add('inputsss')
    }

    
    
    const poschitat = document.querySelectorAll('.procent__btn') 
    
    for (let item of poschitat){

        item.addEventListener('click',podchet)

        function podchet(e){
            e.preventDefault();
        
            // const div = poschitat.closest('div')
            const div = item.closest('div')
            const glavDiv = div.closest('.form-group-addPrice')

            const procentVnytr = div.querySelector('.procent__text').value
            const cenaVnytr = glavDiv.querySelector("input[type='number']")
            const poslenyaStoimVnytr = glavDiv.querySelectorAll("input[type='text']")[1].value
            console.log(div)
            console.log(procentVnytr)
            console.log(glavDiv);
            console.log(typeof(cenaVnytr));
            console.log(poslenyaStoimVnytr);
            const result = Number(poslenyaStoimVnytr) + ( Number(poslenyaStoimVnytr) * (Number(procentVnytr) / 100))
            console.log(result);
            cenaVnytr.value = result

        }
    }

}

