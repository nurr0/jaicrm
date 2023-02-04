const ctx = document.getElementById('myChart');
const ctx2 = document.getElementById('myChart2');
const ctx3 = document.getElementById('myChart3');
const ctx4 = document.getElementById('myChart4');
const ctx5 = document.getElementById('myChart4');
// const ctx20 = document.getElementById('myChart20');
const chartbtn = document.querySelector('.chartbtn')
const chartbtnMouth = document.querySelector('.chartbtnMouth')
const chartbtnGod = document.querySelector('.chartbtnGod')
const chart3btn = document.querySelector('.chart3btn')


const massiv1 = document.querySelector('.massiv1').innerHTML
const massiv2 = document.querySelector('.massiv2').innerHTML
const massiv1Day = document.querySelector('.massiv1Day').innerHTML
const massiv2Day = document.querySelector('.massiv2Day').innerHTML
const massiv1God = document.querySelector('.massiv1God').innerHTML
const massiv2God = document.querySelector('.massiv2God').innerHTML

const lineDay = JSON.parse(document.querySelector('.lineDay').innerHTML)
const lineData = document.querySelector('.lineData').innerHTML




regexp = new RegExp("/", "gi");
regexp1 = new RegExp("'", "gi");

const corrmassiv1 = massiv1.replace(regexp,'')
const corrmassiv1Day = massiv1Day.replace(regexp,'')
const corrmassiv1God = massiv1God.replace(regexp,'')

const supercorrmassiv1 = corrmassiv1.replace(regexp1,'').slice(1).slice(0, -1);
const supercorrmassiv1Day = corrmassiv1Day.replace(regexp1,'').slice(1).slice(0, -1);
const supercorrmassiv1God = corrmassiv1.replace(regexp1,'').slice(1).slice(0, -1);
console.log(supercorrmassiv1Day);


regexpdata3 = new RegExp("'", "gi");
const array3 = lineData.replace(regexpdata3,'"')
const array003 = JSON.parse(array3)




// array1 = JSON.parse(supercorrmassiv1)
array1 = supercorrmassiv1.split(',')
array1Day = supercorrmassiv1Day.split(',')
array1God = supercorrmassiv1God.split(',')

array011 = array1[0]
array012 = array1[1]




array2 = JSON.parse(massiv2)
array2Day = JSON.parse(massiv2Day)
array2God = JSON.parse(massiv2God)


//Массив с числами pie
let x = array2.map(element => {
    return element })

let xDay = array2Day.map(element => {
    return element })

let xGod = array2God.map(element => {
      return element })


  //Массив первый с pie
let y = array1.map(element => {
    return element })
    
let yDay = array1Day.map(element => {
  return element })

let yGod = array1God.map(element => {
    return element })




let zDay = lineDay.map(element => {
    return element })

let zData = array003.map(element => {
    return element })




// new Chart(ctx, {
//   type: 'bar',
//   data: {
//     labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
//     datasets: [{
//       label: '# of Votes',
//       data: [18, 19, 3, 5, 2, 3],
//       borderWidth: 1
//     }]
//   },
//   options: {
//     scales: {
//       y: {
//         beginAtZero: true
//       }
//     }
//   }
// });

// let item1 = 200;

const pie = new Chart(ctx2, {
    type: 'pie',
    data: {
        labels: y,
        datasets: [{
          label: 'My First Dataset',
          data: x,
          backgroundColor: [
            'rgb(255, 99, 132)',
            'rgb(54, 162, 235)',
            'rgb(255, 205, 86)'
          ],
          hoverOffset: 4
        }]
    }
});


// new Chart(ctx3, {
//     type: 'line',
//     data: {
//         labels: [1,3,5],
//         datasets: [{
//           label: 'My First Dataset',
//           data: [65, 59, 80, 81, 56, 55, 40],
//           fill: false,
//           borderColor: 'rgb(75, 192, 192)',
//           tension: 0.1
//         }]},
// });

const line01 = new Chart(ctx4, {

    type: 'line',
    data: {
      labels: zDay,
      datasets: zData
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: 'Chart.js Line Chart'
        }
      }
    },
  })



chart3btn.addEventListener('click',smenaPeriod)
function smenaPeriod(){
    console.log(zDay);
    line01.data.labels = [4,5,6,7,8,9,10,11,12,13]
    line01.update()
    console.log(zDay);
}

chartbtn.addEventListener('click',smenaPeriod01)
function smenaPeriod01(){
    console.log(yDay);
    pie.data.labels = yDay;
    pie.data.datasets[0].data = xDay;
    pie.update()
    console.log(xDay);
}

chartbtnMouth.addEventListener('click',smenaPeriod02)
function smenaPeriod02(){
    console.log(yDay);
    pie.data.labels = y;
    pie.data.datasets[0].data = x;
    pie.update()
    console.log(xDay);
}

chartbtnGod.addEventListener('click',smenaPeriod03)
function smenaPeriod03(){
    console.log(yDay);
    pie.data.labels = yGod;
    pie.data.datasets[0].data = xGod;
    pie.update()
    console.log(xDay);
}

