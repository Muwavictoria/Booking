var options = {
    series: [{
    name: 'Direct',
    data: [35, 41, 36, 26, 45, 48, 52]
    
  }, {
    name: 'Capital',
    data: [44, 55, 57, 56, 61, 58, 63]
  }],
    chart: {
    type: 'bar',
    height: 230,
    toolbar:{
      show: false
    }
  },
  dropShadow:{
    enabled: true,
    top: 1,
    left: 1,
    blur: 1,
    color: '#511365',
    opacity:0.3
  },
  colors: ['#fc8edf', '#c28d5a'],
  plotOptions: {
    bar: {
      horizontal: false,
      columnWidth: '55%',
      endingShape: 'rounded'
    },
  },
  dataLabels: {
    enabled: false
  },
  legend:{
    position: 'bottom',
    horizontalAlign: 'center',
    fontsize: '14px',
    markers:{
      width: 10,
      height: 10,
    },
    itemMargin: {
      horizontal: 0,
      vertical: 8
    }
  },
  grid:{
    borderColor: '#f7f7f7'
  },
  stroke: {
    show: true,
    width: 2,
    colors: ['transparent']
  },
  xaxis: {
    categories: ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun'],
  },
  yaxis: {
    title: {
      text: ''
    }
  },
  fill: {
    opacity: 2
  },
  tooltip: {
    y: {
      formatter: function (val) {
        return "$ " + val + " thousands"
      }
    }
  }
  };

  var chart = new ApexCharts(document.querySelector("#weekly"), options);
  chart.render();

 


  // monthly
  var options = {
    series: [{
    name: 'Direct',
    data: [35, 41, 36, 26, 45, 48, 52,78,28,29,20,50,51,21,124,36,35,35,67,74,33,55,66,23,76,90,20,20,29,105,110]
    
  }, {
    name: 'Capital',
    data: [44, 55, 57, 56, 61, 58, 63,70,80,90,95,100,102,104,105,110,112,140,150,180,160,77,66,78,94,95,105,112]
  }],
    chart: {
    type: 'bar',
    height: 230,
    toolbar:{
      show: false
    }
  },
  dropShadow:{
    enabled: true,
    top: 1,
    left: 1,
    blur: 1,
    color: '#511365',
    opacity:0.3
  },
  colors: ['#fc8edf', '#c28d5a'],
  plotOptions: {
    bar: {
      horizontal: false,
      columnWidth: '55%',
      endingShape: 'rounded'
    },
  },
  dataLabels: {
    enabled: false
  },
  legend:{
    position: 'bottom',
    horizontalAlign: 'center',
    fontsize: '14px',
    markers:{
      width: 10,
      height: 10,
    },
    itemMargin: {
      horizontal: 0,
      vertical: 8
    }
  },
  grid:{
    borderColor: '#f7f7f7'
  },
  stroke: {
    show: true,
    width: 2,
    colors: ['transparent']
  },
  xaxis: {
    categories: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
  },
  yaxis: {
    title: {
      text: ''
    }
  },
  fill: {
    opacity: 2
  },
  tooltip: {
    y: {
      formatter: function (val) {
        return "$ " + val + " thousands"
      }
    }
  }
  };

  var chart = new ApexCharts(document.querySelector("#monthly"), options);
  chart.render();

//  yearly
var options = {
  series: [{
  name: 'Direct',
  data: [35, 41, 36, 26, 45, 48, 52]
  
}, {
  name: 'Capital',
  data: [44, 55, 57, 56, 61, 58, 63]
}],
  chart: {
  type: 'bar',
  height: 230,
  toolbar:{
    show: false
  }
},
dropShadow:{
  enabled: true,
  top: 1,
  left: 1,
  blur: 1,
  color: '#511365',
  opacity:0.3
},
colors: ['#fc8edf', '#c28d5a'],
plotOptions: {
  bar: {
    horizontal: false,
    columnWidth: '55%',
    endingShape: 'rounded'
  },
},
dataLabels: {
  enabled: false
},
legend:{
  position: 'bottom',
  horizontalAlign: 'center',
  fontsize: '14px',
  markers:{
    width: 10,
    height: 10,
  },
  itemMargin: {
    horizontal: 0,
    vertical: 8
  }
},
grid:{
  borderColor: '#f7f7f7'
},
stroke: {
  show: true,
  width: 2,
  colors: ['transparent']
},
xaxis: {
  categories: ['Jan', 'Feb', 'Mar', 'April', 'May', 'June', 'July', 'Aug', 'sept','Oct','Nov', 'dec'],
},
yaxis: {
  title: {
    text: ''
  }
},
fill: {
  opacity: 2
},
tooltip: {
  y: {
    formatter: function (val) {
      return "$ " + val + " thousands"
    }
  }
}
};

var chart = new ApexCharts(document.querySelector("#yearly"), options);
chart.render();

