// const clientId = Number(document.querySelector('select[name=customer]').value)
const client = document.querySelector('select[name=customer]')
const RazdelTovari = document.querySelector('.glavTovariMid')
// const inputcenaSychetomSkidki = RazdelTovari.querySelectorAll('input[type=number]')
// const inputcenaSychetomSkidki = RazdelTovari.querySelectorAll('input[name*=price_with_discount]')
const inputcenaSychetomSkidki = document.querySelectorAll('input[name*=price_with_discount]')

// const cenaSychetomSkidki = [...RazdelTovari.querySelectorAll('input[type=number]')]
const cenaSychetomSkidki = [...document.querySelectorAll('input[name*=price_with_discount]')]



let totalzArea = document.querySelector('.totalzArea')

for (let item of inputcenaSychetomSkidki){
    item.addEventListener('change',smenaCeniSkidki)
    function smenaCeniSkidki(){
        const totalZ = cenaSychetomSkidki.reduce(function (sum, currentAccount) {
            return Number(sum) + Number(currentAccount.value);
            },0)
        console.log(totalZ);
        let kolVo = item.previousElementSibling.previousElementSibling;
        console.log(kolVo);
        console.log(kolVo.value);
        
        totalzArea.innerHTML = totalZ * Number(kolVo.value);
    }
}
const kolVoArray = document.querySelectorAll('input[name*=amount]')
for (let kolVoItem of kolVoArray){
    kolVoItem.addEventListener('change',smenaKolVo)
    function smenaKolVo(){
        cenasYchetom = kolVoItem.nextElementSibling.nextElementSibling;
        const totalZ = cenaSychetomSkidki.reduce(function (sum, currentAccount) {
            return Number(sum) + Number(currentAccount.value);
            },0)
        totalzArea.innerHTML = totalZ *  Number(kolVoItem.value)
    }
}

// const spisivaemBonysi = document.querySelector('input[name=points_used')
var spisivaemBonysi

async function GetCustomers(){
    let response = await fetch('/api/v1/customers/'); 
    let result = await response.json();
    console.log(result);
    let bonys = result.find(res => {
        const clientId = Number(document.querySelector('select[name=customer]').value)
        return res.id == clientId})
    console.log(bonys);
    console.log(bonys.points_amount);
    spisivaemBonysi = document.querySelector('input[name=points_used]')
    // spisivaemBonysi.value = bonys.points_amount;
    spisivaemBonysi.value = 0;
    const bonysiClient = document.querySelector('.bonysiClient')
    bonysiClient.innerHTML = bonys.points_amount;

    spisivaemBonysi.addEventListener('change', proverkaBonysov)
    function proverkaBonysov(){
        if (spisivaemBonysi.value > bonys.points_amount){
            let res = confirm('У клиента нет столько бонусов! Обнулить бонусы?')
            if (res){
                // spisivaemBonysi.value = bonys.points_amount;
                spisivaemBonysi.value = 0;
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
            let res = confirm('Списываемые бонусы больше чем БСЛ! Обнулить бонусы?')
            if (res){
                // spisivaemBonysi.value = bonys.points_amount;
                spisivaemBonysi.value = 0;
            } else {
                // alert('Просьба отредактировать "Списываемые бонусы!')
            }
            // alert('БСЛ')
            // spisivaemBonysi.value = bonys.points_amount;
        }
    }
}

// GetCustomers()

client.addEventListener('change',GetCustomers)



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
            
            let cenasEchetomSkidki = item.nextElementSibling.nextElementSibling.nextElementSibling.nextElementSibling
            console.log(cenasEchetomSkidki);
            
            cenasEchetomSkidki.value = Number(ystanCena.get_sell_price);
            smenaCeniSkidki()
            
    }
    
   
}



const skidkas = document.querySelectorAll('input[name*=-discount]')
for (let skidka of skidkas){
    skidka.addEventListener('change',skidkaPlus)
    function skidkaPlus(){
        console.log('Привет бро');
        console.log(skidka);
        let ystanCenaSkidka = skidka.previousElementSibling.previousElementSibling
        console.log(ystanCenaSkidka);

        let cenaSkidka = skidka.nextElementSibling
        cenaSkidka.value = Number(ystanCenaSkidka.value) -  ((Number(ystanCenaSkidka.value) / 100) * Number(skidka.value))
        smenaCeniSkidki()
        
    }
}


const UstanovlenCena = document.querySelectorAll('input[name*=price_in_stock]')
for (let item of UstanovlenCena){
    item.setAttribute('readonly','1')
}




const vidBonysov = document.querySelector('select[name=points_achieve_or_spend]')

vidBonysov.addEventListener('change',smenaVidBonysov)
function smenaVidBonysov(){
    if (vidBonysov.value == 'recieve' ){
        spisivaemBonysi = document.querySelector('input[name=points_used]');
        spisivaemBonysi.value = 0;
        spisivaemBonysi.setAttribute('disabled', 1)
    }
    if (vidBonysov.value == 'spend' ){
        spisivaemBonysi = document.querySelector('input[name=points_used]');
        spisivaemBonysi.removeAttribute('disabled')
    }
}
smenaVidBonysov()