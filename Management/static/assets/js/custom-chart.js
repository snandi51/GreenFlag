var val_1 = JSON.parse(document.getElementById('input_1').value)
console.log(val_1)

var val_2 = JSON.parse(document.getElementById('input_2').value)
console.log(val_2)

var val_3 = JSON.parse(document.getElementById('input_3').value)
console.log(val_3)

var val_4 = JSON.parse(document.getElementById('input_4').value)
console.log(val_4)

var val_5 = JSON.parse(document.getElementById('input_5').value)
console.log(val_5)

var val_6 = JSON.parse(document.getElementById('input_6').value)
console.log(val_6)

var val_7 = JSON.parse(document.getElementById('input_7').value)
console.log(val_7)

var val_8 = JSON.parse(document.getElementById('input_8').value)
console.log(val_8)

var val_9 = JSON.parse(document.getElementById('input_9').value)
console.log(val_9)

var state_list1 = JSON.parse(document.getElementById('input_10').value)
console.log(state_list1)

const ctx = document.getElementById('myChart1');
    new Chart(ctx, {
      type: 'line',
      data: {
        labels: val_9,
        datasets: [{
          label: 'Actual',
          data: val_1,
          borderColor: ["yellow"],
          borderWidth: 1.2,
          borderWidth:2.1
        },
        {
           label: 'Predicted',
           data: val_2,
           borderWidth: 1.2,
           borderColor: ["orange"],
           borderWidth:2.1
        }
      ]
    },
  options: {
      responsive: true,
      plugins: {
        legend: {
          position: "right",
          align: "start",
          labels: {
              fontFamily: "Comic Sans MS",
              boxWidth: 20,
              boxHeight: 10,
              color: "white",
          }
        }
      },
      animation: {
        duration: 0
      },
  }
  });


const ctx2 = document.getElementById('myChart2');
new Chart(ctx2, {
  type: 'line',
  data: {
    labels: val_9,
    datasets: [{
      label: 'Actual',
      data: val_3,
      borderColor: ["yellow"],
      borderWidth: 1.2,
      borderWidth:2.1
    },
    {
       label: 'Predicted',
       data: val_4,
       borderWidth: 1.2,
       borderColor: ["orange"],
       borderWidth:2.1
    }
  ]
  },
  options: {
      responsive: true,
      plugins: {
        legend: {
          position: "right",
          align: "start",
          labels: {
              fontFamily: "Comic Sans MS",
              boxWidth: 20,
              boxHeight: 10,
              color: "white",
          },
//          title: {
//                display: true,
//                text: 'Custom Chart Title',
//                color: "white",
//                position: "left",
//          }
        }
      },
      animation: {
        duration: 0
    },
  }
});


var ctx_bar1 = document.getElementById("bar_chart1");
var bar_data1 = {
  labels: val_9,
  datasets: [{
    label: "Event",
    data: val_5,
    backgroundColor: [
        'rgba(255, 206, 86, 0.9)',
    ],
  }]
};

var options_charts = {
  scales: {
    yAxes: [{
      ticks: {
        max: 5,
        min: 1,
        stepSize: 1,
      }
    }]
  },
  plugins: {
      legend: {
          display: false
      },
    },
  tooltips: {
    enabled: true,
    mode: 'label'
  },
  scale: {
    ticks: {
      precision: 0
    }
  },
  animation: {
        duration: 0
   },
};

// Chart declaration:
var bar_chart1 = new Chart(ctx_bar1, {
  type: 'bar',
  data: bar_data1,
  options: options_charts
});

bar_data1.datasets[0].backgroundColor = bar_data1.datasets[0].data.map(function (v) {
  if (v == 1){
     return 'green';
  }
  else if (v == 2 || v == 3){
     return 'yellow';
  }
  else{
     return 'red';
  }
});


var ctx_bar2 = document.getElementById("bar_chart2");
var bar_data2 = {
  labels: val_9,
  datasets: [{
    label: "Event",
    data: val_6,
    backgroundColor: [
        'rgba(255, 206, 86, 0.9)',
    ],
  }]
};

var options_charts = {
  scales: {
    yAxes: [{
      ticks: {
        max: 5,
        min: 1,
        stepSize: 1,
      }
    }]
  },
  plugins: {
      legend: {
          display: false
      },
    },
  tooltips: {
    enabled: true,
    mode: 'label'
  },
  scale: {
    ticks: {
      precision: 0
    }
  },
  animation: {
        duration: 0
   },
};

// Chart declaration:
var bar_chart2 = new Chart(ctx_bar2, {
  type: 'bar',
  data: bar_data2,
  options: options_charts
});

bar_data2.datasets[0].backgroundColor = bar_data2.datasets[0].data.map(function (v) {
  if (v == 1){
     return 'green';
  }
  else if (v == 2 || v == 3){
     return 'yellow';
  }
  else{
     return 'red';
  }
});

var ctx_bar3 = document.getElementById("bar_chart3");
var bar_data3 = {
  labels: val_9,
  datasets: [{
    label: "Event",
    data: val_7,
    backgroundColor: [
        'rgba(255, 206, 86, 0.9)',
    ],
  }]
};

var options_charts = {
  scales: {
    yAxes: [{
      ticks: {
        max: 5,
        min: 1,
        stepSize: 1,
      }
    }]
  },
  plugins: {
      legend: {
          display: false
      },
    },
  tooltips: {
    enabled: true,
    mode: 'label'
  },
  scale: {
    ticks: {
      precision: 0
    }
  },
  animation: {
        duration: 0
   },
};

// Chart declaration:
var bar_chart3 = new Chart(ctx_bar3, {
  type: 'bar',
  data: bar_data3,
  options: options_charts
});

bar_data3.datasets[0].backgroundColor = bar_data3.datasets[0].data.map(function (v) {
  if (v == 1){
     return 'green';
  }
  else if (v == 2 || v == 3){
     return 'yellow';
  }
  else{
     return 'red';
  }
});


var ctx_bar4 = document.getElementById("bar_chart4");
var bar_data4 = {
  labels: val_9,
  datasets: [{
    label: "Event",
    data: val_8,
    backgroundColor: [
        'rgba(255, 206, 86, 0.9)',
    ],
  }]
};

bar_data4.datasets[0].backgroundColor = bar_data4.datasets[0].data.map(function (v) {
  if (v == 1){
     return 'green';
  }
  else if (v == 2 || v == 3){
     return 'yellow';
  }
  else{
     return 'red';
  }
});

//bar_data4.datasets.backgroundColor = bar_data4[1].y.map(function (v) {
//  return v < 2 ? 'rgba(219, 64, 82, 0.7)' : 'rgb(158,202,225)'
//});

var options_charts = {
  scales: {
    yAxes: [{
      ticks: {
        max: 5,
        min: 1,
        stepSize: 1,
      }
    }]
  },
  plugins: {
      legend: {
          display: false
      },
    },
  tooltips: {
    enabled: true,
    mode: 'label'
  },
  scale: {
    ticks: {
      precision: 0
    }
  },
  animation: {
        duration: 0
   },
};

// Chart declaration:
var bar_chart4 = new Chart(ctx_bar4, {
  type: 'bar',
  data: bar_data4,
  options: options_charts
});



var pieCanvas = document.getElementById("pieChart");
var pieData = {
    labels: [
        "Normal State",
        "Noisy State",
        "Failure State",
    ],
    datasets: [
        {
            data: state_list1,
            backgroundColor: [
                "green",
                "yellow",
                "red",
            ]
        }]
};


var pie_options = {
            layout: {
                padding: {
                  top: 5
                }
            },
            plugins: {
                legend: {
                position: "left",
                    labels: {
                        boxWidth: 0,
                        boxHeight:0,
                        font: {
                            size: 0
                        }
                    }
                }
            },
            animation: {
                duration: 0
            },

        };

var pieChart = new Chart(pieCanvas, {
  type: 'pie',
  data: pieData,
  options: pie_options
});


