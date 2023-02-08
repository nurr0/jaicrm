// const clientId = Number(document.querySelector('select[name=customer]').value)
const client = document.querySelector('select[name=customer]')
const RazdelTovari = document.querySelector('.glavTovariMid')
// const inputcenaSychetomSkidki = RazdelTovari.querySelectorAll('input[type=number]')
const inputcenaSychetomSkidki = RazdelTovari.querySelectorAll('input[name*=discount]')

// const cenaSychetomSkidki = [...RazdelTovari.querySelectorAll('input[type=number]')]
const cenaSychetomSkidki = [...RazdelTovari.querySelectorAll('input[name*=discount]')]



let totalzArea = document.querySelector('.totalzArea')

for (let item of inputcenaSychetomSkidki){
    item.addEventListener('change',smenaCeniSkidki)
    function smenaCeniSkidki(){
        const totalZ = cenaSychetomSkidki.reduce(function (sum, currentAccount) {
            return Number(sum) + Number(currentAccount.value);
            },0)
        console.log(totalZ);
        totalzArea.innerHTML = totalZ;
    }
}


// const spisivaemBonysi = document.querySelector('input[name=points_used')
var spisivaemBonysi

async function GetCustomers(){
    let response = await fetch('/api/v1/customers/'); 
    let result = await response.json();
    console.log(result);
    let bonys = result.find(item => {
        const clientId = Number(document.querySelector('select[name=customer]').value)
        return item.id == clientId})
    console.log(bonys);
    console.log(bonys.points_amount);
    spisivaemBonysi = document.querySelector('input[name=points_used')
    spisivaemBonysi.value = bonys.points_amount;

    spisivaemBonysi.addEventListener('change', proverkaBonysov)
    function proverkaBonysov(){
        if (spisivaemBonysi.value > bonys.points_amount){
            let res = confirm('У клиента нет столько бонусов! Вернуть прошлое значение?')
            if (res){
                spisivaemBonysi.value = bonys.points_amount;
            } else {
                // alert('Просьба отредактировать "Списываемые бонусы!')
            }
            // alert('У клиента нет столько бонусов!')
            // spisivaemBonysi.value = bonys.points_amount;
        }
        let totalzArea = document.querySelector('.totalzArea')
        console.log(totalzArea.innerHTML);
        
        const bsl = Number(document.querySelector('.bsl').innerHTML)
        console.log(bsl);
        

        formyla = (Number(totalzArea.innerHTML) / 100) * bsl;
        console.log(formyla);
        
        if (spisivaemBonysi.value > formyla){
            let res = confirm('Списываемые бонусы больше чем БСЛ! Вернуть прошлое значение?')
            if (res){
                spisivaemBonysi.value = bonys.points_amount;
            } else {
                // alert('Просьба отредактировать "Списываемые бонусы!')
            }
            // alert('БСЛ')
            // spisivaemBonysi.value = bonys.points_amount;
        }
    }
}



client.addEventListener('change',GetTovari)

async function GetTovari(){
    let response = await fetch('/api/v1/product_in_stock/'); 
    let result = await response.json();
}

const tovariArray = document.querySelectorAll('select[name*=product]')
for (let item of tovariArray){
        item.addEventListener('click', vuborTovari)
        async function vuborTovari(){
            console.log(item.value);
            let response = await fetch('/api/v1/product_in_stock/'); 
            let result = await response.json();
            console.log(result);

            let ystanCena = result.find(obj=>{
               return obj.id == item.value
            })
            console.log(ystanCena);
            console.log(item)
            const cena = item.nextElementSibling 
            console.log(cena);
            cena.value = Number(ystanCena.get_sell_price);

            let checkboxxx = item.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling;
            console.log(checkboxxx);
            checkboxxx.classList.remove('checked')
            
            
            
            
    }
    
    GetTovari()
}