<template>
  <div class="container-index">
    <el-card style="height: 100%;width: 100%;">
      <el-select
        style="width: 200px;margin-left: 20px;"
        v-model="hospital"
        placeholder="选择医院"
        size="large">
        <el-option
        v-for="item in hospitalList"
        :key="item.value"
        :label="item.label"
        :value="item.value"
        />
      </el-select>
      <el-select
          style="width: 200px;margin-left: 20px;"
          v-model="type"
          placeholder="选择类型"
        >
          <el-option label="单病种" value="单病种" />
          <!-- <el-option label="专科" value="专科" /> -->
      </el-select>
      <el-button type="primary" style="margin-left: 60%;" @click="getBar" class="myButton">确定</el-button> 
      <el-button type="primary" style="margin-left: 10px;" @click="tableReset"class="myButton">重置</el-button> 
      <div class="flex-container" style="display: flex; justify-content: space-between; margin: 20px;">  
        <div class="bar-chart-container" style="flex: 1">  
          <el-card style="height: 800px; width: 850px;">  
            <div id="barChart1" style="height: 850px; width: 850px;"></div>  
          </el-card>  
        </div>  
        <div class="bar-chart-container" style="flex: 1;">  
          <el-card style="height: 800px; width: 850px;;">  
            <div id="barChart2" style="height: 850px; width: 850px;"></div>  
          </el-card>  
        </div>  
      </div>  
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import * as echarts from 'echarts'
import request from '@/api/request';

const hospitalList = ref([])
const hospital = ref('')
const type = ref('单病种')
const rateList = ref([])


const getOptionList = () => {
  request.get('/hospital_diseases/').then(res => {
    console.log(res)
    hospital.value = Object.keys(res)[0]
    console.log(hospital.value)
    Object.keys(res).forEach(key => {
      hospitalList.value.push({
        'label': key,
        'value': key
      })
    })
    getBar()
  })
}

const getRateList = () => {
  const url = '/latest_rate?hospital_name=' + hospital.value;  
  request.get(url).then(res => {  
  console.log(res); 
  rateList.value = res.rates 
  console.log(rateList)  
  }).catch(error => {  
    console.error('Error:', error);  
  });
}

const getRadar = () => {
  const myChart = echarts.init(document.getElementById('barChart'));
  const option = {
    tooltip: {
      trigger: 'axis'
    },
    grid: {
      top: 40
    },
    legend: {
      left: 'center',
      data: [
        '妇科',
        '骨科',
        '呼吸内科',
        '急诊',
        '泌尿外科',
        '内分泌科',
        // '肾内科',
        // '心血管内科',
        // '神经外科',
        // '普通外科'
      ]
    },
    radar: [
      {
        indicator: [
          { text: '阴道镜高级别病变诊断符合率', max: 1 },
          { text: '恶性肿瘤系统治疗前临床病理分期评估率', max: 1 },
          { text: '（妇科）术前评估完整率率', max: 1 },
          { text: '（妇科）疑难患者MDT 治疗率', max: 1 },
          { text: '（妇科）术后出院宣教率', max: 1 },
        ],
        center: ['20%', '30%'],
        radius: 80,
        name: {
          show: true,
          textStyle: {
            color: '#000000'
          }
        }
      },
      {
        indicator: [
          { text: '骨科手术知情同意书规范填写率', max: 1 },
          { text: '术后1个月随访率', max: 1 },
          { text: '术后3个月随访率', max: 1 },
          { text: '术后6个月随访率', max: 1 },
          { text: '术后12个月随访率', max: 1 }
        ],
        radius: 80,
        center: ['50%', '30%'],
        name: {
          show: true,
          textStyle: {
            color: '#000000'
          }
        }
      },
      {
        indicator: [
          { text: '转出MICU/RICU后48h内重返率', max: 1 },
          { text: '入院 48 小时内 VTE 风险评估率', max: 1 },
          { text: '呼吸机使用前病情评估率', max: 1 },
          { text: '重点病种随访率', max: 1 }
        ],
        radius: 80,
        center: ['82%', '30%'],
        name: {
          show: true,
          textStyle: {
            color: '#000000'
          }
        }
      },
      {
        indicator: [
          { text: '急性心肌梗死（STEMI）患者平均门药时间', max: 1 },
          { text: '急性心肌梗死（STEMI）患者门药时间达标率', max: 1 },
          { text: '急性心肌梗死（STEMI）患者平均门球时间', max: 1 },
          { text: '急性心肌梗死（STEMI）患者门球时间达标率', max: 1 },
          { text: '急诊抢救室患者死亡率', max: 1 },
          { text: '急诊手术患者死亡率', max: 1 },
          { text: 'ROSC 成功率', max: 1 },
          { text: '非计划重返抢救室率', max: 1 }
        ],
        radius: 80,
        center: ['20%', '70%'],
        name: {
          show: true,
          textStyle: {
            color: '#000000'
          }
        }
      },
      {
        indicator: [
          { text: '术前病情评估率', max: 1 },
          { text: '术中手术方案更改率', max: 1 },
          { text: '前列腺癌根治切缘阳性率', max: 1 },
          { text: '膀胱癌根治术平均淋巴结清扫数', max: 1 },
        ],
        radius: 80,
        center: ['50%', '70%'],
        name: {
          show: true,
          textStyle: {
            color: '#000000'
          }
        }
      },
      {
        indicator: [
          { text: '知情同意书规范签署率', max: 1 },
          { text: '糖尿病住院患者慢性并发症评估率', max: 1 },
          { text: '难治性高血压患者肾素醛固酮比值检测率', max: 1 },
          // { text: '骨质疏松症住院患者骨折风险评估率', max: 1 }
        ],
        center: ['82%', '70%'],
        radius: 80,
        name: {
          show: true,
          textStyle: {
            color: '#000000'
          }
        }
      },
      // {
      //   indicator: [
      //     { text: '激素、免疫抑制剂治疗告知率', max: 1 },
      //     { text: '慢性肾脏病患者高血压治疗达标率', max: 1 },
      //     { text: '慢性肾脏病患者血尿酸达标率', max: 1 },
      //     { text: '慢性肾脏病患者血脂达标率', max: 1 }
      //   ],
      //   center: ['30%', '60%'],
      //   radius: 80,
      //   name: {
      //     show: true,
      //     textStyle: {
      //       color: '#000000'
      //     }
      //   }
      // },
      // {
      //   indicator: [
      //     { text: '急性非ST 段抬高型心肌梗死患者危险度分层比例', max: 1 },
      //     { text: '房颤患者血栓栓塞风险评估率', max: 1 },
      //     { text: '心内科患者出院前心脏康复率', max: 1 },
      //   ],
      //   center: ['50%', '60%'],
      //   radius: 80,
      //   name: {
      //     show: true,
      //     textStyle: {
      //       color: '#000000'
      //     }
      //   }
      // },
      // {
      //   indicator: [
      //     { text: '诊断符合率', max: 1 },
      //     { text: '计算机三维辅助手术计划系统使用率', max: 1 },
      //     { text: '术中输血率', max: 1 },
      //     { text: '术后输血率', max: 1 },
      //     { text: '术后即刻 CT 复查阳性发现率', max: 1 },
      //     { text: '术中死亡率', max: 1 }
      //   ],
      //   center: ['70%', '60%'],
      //   radius: 80,
      //   name: {
      //     show: true,
      //     textStyle: {
      //       color: '#000000'
      //     }
      //   }
      // },
      // {
      //   indicator: [
      //     { text: '知情同意书规范签署率', max: 1 },
      //     { text: '术前病情评估率', max: 1 },
      //     { text: '术前病情评估率', max: 1 },
      //   ],
      //   center: ['90%', '60%'],
      //   radius: 80,
      //   name: {
      //     show: true,
      //     textStyle: {
      //       color: '#000000'
      //     }
      //   }
      // },
    ],
    series: [
      {
        type: 'radar',
        tooltip: {
          trigger: 'item'
        },
        areaStyle: {},
        data: [
          {
            value: [0.6, 0.73, 0.85, 0.40, 0.90],
            name: '妇科'
          }
        ]
      },
      {
        type: 'radar',
        tooltip: {
          trigger: 'item'
        },
        radarIndex: 1,
        areaStyle: {},
        data: [
          {
            value: [0.85, 0.90, 0.90, 0.95, 0.95],
            name: '骨科'
          }
        ]
      },
      {
        type: 'radar',
        tooltip: {
          trigger: 'item'
        },
        radarIndex: 2,
        areaStyle: {},
        data: [
          {
            value: [0.85, 0.90, 0.90, 0.95],
            name: '呼吸内科'
          }
        ]
      },
      {
        type: 'radar',
        tooltip: {
          trigger: 'item'
        },
        radarIndex: 3,
        areaStyle: {},
        data: [
          {
            value: [0.85, 0.90, 0.90, 0.9, 0.6, 0.3, 0.7, 0.99],
            name: '急诊'
          }
        ]
      },
      {
        type: 'radar',
        tooltip: {
          trigger: 'item'
        },
        radarIndex: 4,
        areaStyle: {},
        data: [
          {
            value: [ 0.6, 0.3, 0.7, 0.99],
            name: '泌尿外科'
          }
        ]
      },
      {
        type: 'radar',
        tooltip: {
          trigger: 'item'
        },
        radarIndex: 5,
        areaStyle: {},
        data: [
          {
            value: [ 0.6, 0.3, 0.7, 0.99],
            name: '内分泌科'
          }
        ]
      },
      // {
      //   type: 'radar',
      //   tooltip: {
      //     trigger: 'item'
      //   },
      //   radarIndex: 6,
      //   areaStyle: {},
      //   data: [
      //     {
      //       value: [ 0.4, 0.9, 0.3, 0.67],
      //       name: '肾内科'
      //     }
      //   ]
      // },
      // {
      //   type: 'radar',
      //   tooltip: {
      //     trigger: 'item'
      //   },
      //   radarIndex: 7,
      //   areaStyle: {},
      //   data: [
      //     {
      //       value: [ 0.9, 0.3, 0.67],
      //       name: '心血管内科'
      //     }
      //   ]
      // },
      // {
      //   type: 'radar',
      //   tooltip: {
      //     trigger: 'item'
      //   },
      //   radarIndex: 8,
      //   areaStyle: {},
      //   data: [
      //     {
      //       value: [ 0.66, 0.78, 0.7, 0.9, 0.3, 0.67],
      //       name: '神经外科'
      //     }
      //   ]
      // },
      // {
      //   type: 'radar',
      //   tooltip: {
      //     trigger: 'item'
      //   },
      //   radarIndex: 9,
      //   areaStyle: {},
      //   data: [
      //     {
      //       value: [ 0.3, 0.67,0.9],
      //       name: '普通外科'
      //     }
      //   ]
      // },
    ]
  };
  myChart.setOption(option)
}

const getBar = () => {
  const hospitalName = hospital.value;
  const diseaseType = type.value;
  const makeChart = (containerId, labels, rates, titleText) => {
    const myChart = echarts.init(document.getElementById(containerId));
    const option = {
      title: {
        text: titleText,
        textStyle: {
          color: '#333',
          fontWeight: 'bold',
          fontSize: 16
        },
        left: '10%',
        top: '5%',
      },
      tooltip: {
        trigger: 'axis', 
        formatter: function (params) {  
                var value = params[0].value;  
                    return params[0].seriesName + ': ' + (value * 100).toFixed(0) + '%';  
        }
      },
      grid: {
        left: '10%',
        rigth: '10%',
        top: '15%',
        bottom: '35%',
        width: '80%',
        height: '55%'
      },
      xAxis: {
        gridIndex: 0,
        type: 'category',
        data: labels,
        axisLabel: {
          formatter: function(params) {
            var newParamsName = "";
            var paramsNameNumber = params.length;
            var provideNumber = 4;
            var rowNumber = Math.ceil(paramsNameNumber / provideNumber);

            if (paramsNameNumber > provideNumber) {
              for (var p = 0; p < rowNumber; p++) {
                var tempStr = "";
                var start = p * provideNumber;
                var end = start + provideNumber;

                if (p === rowNumber - 1) {
                  tempStr = params.substring(start, paramsNameNumber);
                } else {
                  tempStr = params.substring(start, end) + "\n";
                }

                newParamsName += tempStr;
              }
            } else {
              newParamsName = params;
            }

            return newParamsName;
          }
        }
      },
      yAxis: {
        gridIndex: 0,
        type: 'value',
        axisLabel: {  
          formatter: function (value, index) {  
              return (value * 100).toFixed(0) + '%';
          } 
        },
      },
      series: [{
        data: rates,
        type: 'bar',
        data: rates.map((rate, index) => ({
          value: rate,
          itemStyle: {
            color: index === Math.floor(rates.length / 2) ? 'rgb(35, 125, 255)' : 'lightgray'
          }
          })),
        xAxisIndex: 0,
        yAxisIndex: 0,
        name: '达标率',
        barWidth: 20,
        // label: {
        //   normal: {
        //     show: true,
        //     position: 'top',
        //     color: '#000000'
        //   }
        // },
        itemStyle: {
          normal: {
            borderRadius: [10, 10, 0, 0],
            color: 'rgb(35, 125, 255)'
          }
        }
      }],
    };
    myChart.setOption(option);
  };
  const lastLabel = [];
  const lastRate = [];
  const topLabel = [];
  const topRate = [];
  const req = {
    "hospital_name": hospitalName,
    "disease_type": diseaseType
  };
  console.log(req);
  const queryString = Object.keys(req).map(key => `${encodeURIComponent(key)}=${encodeURIComponent(req[key])}`).join('&');
  const url = '/top_last_num?' + queryString;
  request.get(url).then(res => {
    console.log(res);
    res.last_num.forEach(function(obj) {
      const label = obj.disease + '-' + obj.indicator_name;
      const rate = obj.rate;
      lastLabel.push(label);
      lastRate.push(rate);
    });
    res.top_num.forEach(function(obj) {
      const label = obj.disease + '-' + obj.indicator_name;
      const rate = obj.rate;
      topLabel.push(label);
      topRate.push(rate);
    });
    makeChart('barChart1', topLabel, topRate, '指标达标率TOP10');
    makeChart('barChart2', lastLabel, lastRate, '指标达标率Bottom10');
  });
};


const changeChart = () => {
  const myChart = echarts.init(document.getElementById('barChart'));
  myChart.dispose()
  if (type.value === '专科') {
    getRadar()
  } else {
    getBar()
  }
}

const tableReset = () => {
  hospital.value = ''
  type.value = ''
} 

onMounted(() => {
  getOptionList()
  // changeChart()
});

</script>

<style scoped>
.bar-chart {
  width: 100%;
  height: 700px;
  margin: 10px auto;
  border-radius: 5px
}
.container-index {
  flex-direction: column;
  width: 100%;
  height: 100%;
  font-family: 'PingFang';
  display: flex;  
  justify-content: center; 
  background-color: white;
}

.myButton{
  border-radius: 20px;
  width: 120px;
  
}
</style>
