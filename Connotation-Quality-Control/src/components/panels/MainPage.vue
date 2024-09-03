<template>
    <div class="container1">
      <!-- 顶部部分 -->
      <div class="top">
        <div class="top-left">
          <div class="top-left-title" style="display: flex; align-items: center;">
            <span class="title">病历内涵质控</span>
            <el-icon class="icon">  
                <ArrowRight/>  
            </el-icon>
            <span @click="go" class="clickable-span">查看更多</span>
          </div>
          <el-divider style="margin: 5px;"/>
          <div class="box" style="overflow: hidden; flex: 1.5;">
            <el-table
                height="100%"
                :data="tableData"
                ref="table">
                <el-table-column
                    prop="name"
                    min-width="120"
                    :show-overflow-tooltip="true"
                    label="规则名称"
                    style="color: white;"/>
                <el-table-column prop="result" label="达标率" min-width="68">
                    <template #default="scope">
                        <span style="color: red">{{ scope.row.result }}</span>
                    </template>
                </el-table-column>
            </el-table>
            </div>
        </div>
        <div class="top-gap"></div>
        <div class="top-middle">
            <div class="top-left-title" style="display: flex; align-items: center;">
            <span class="title">观测数据</span>
            </div>
            <el-divider style="margin: 5px;"/>
            <div class="statistic">
                <div class="row">  
                    <div class="block">  
                        <svg class="icon" aria-hidden="true" width="20" height="20">  
                            <use xlink:href="#icon-hospital"></use>  
                        </svg>  
                        <div class="text-container">  
                            <span class="text-title">医院总数</span>  
                            <span class="text-num">2</span>  
                        </div>  
                    </div>
                    <div class="block">  
                        <svg class="icon" aria-hidden="true" width="20" height="20">  
                            <use xlink:href="#icon-zhuankehuli"></use>  
                        </svg>  
                        <div class="text-container">  
                            <span class="text-title">专科指标总数</span>  
                            <span class="text-num">101</span>  
                        </div>  
                    </div>
                </div>  
                <div class="row">  
                    <div class="block">  
                        <svg class="icon" aria-hidden="true" width="20" height="20">   
                            <use xlink:href="#icon-zhibiao"></use>  
                        </svg>  
                        <div class="text-container">  
                            <span class="text-title">单病种指标总数</span>  
                            <span class="text-num">189</span>  
                        </div>  
                    </div> 
                    <div class="block">  
                        <svg class="icon" aria-hidden="true" width="20" height="20">  
                            <use xlink:href="#icon-bingli"></use>  
                        </svg>  
                        <div class="text-container">  
                            <span class="text-title">电子病历总数</span>  
                            <span class="text-num">{{ recordNum }}</span>  
                        </div>  
                    </div>  
                </div> 
                <div class="row">
                    <!-- <div class="block">  
                        <svg class="icon" aria-hidden="true" width="20" height="20">  
                            <use xlink:href="#icon-tubiao_-"></use>  
                        </svg>
                        <div class="text-container">  
                            <span class="text-title">单病种总数</span>  
                            <span class="text-num">189</span>  
                        </div>  
                    </div> 
                    <div class="final"></div>    -->
                </div> 
            </div>
        </div>
        <div class="top-gap"></div>
        <div class="top-right">
            <div class="top-left-title" style="display: flex; align-items: center;">
            <span class="title">1院单病种指标数</span>
            </div>
            <el-divider style="margin: 5px;"/>
            <div class="mid-left" ref="chartPie"></div>
        </div>
      </div>
      <!-- <div class="middle">
        <div class="top-left-title" style="display: flex; align-items: center;">
            <span class="title">1院近一年病历数量</span>
        </div>
        <el-divider style="margin: 5px;"/>
        <div style="height: 300px;width: 100%;" ref="chartBar">
        </div>
      </div> -->
      <div class="gap"></div>
      <div class="bottom">
        <div class="top-left-title" style="display: flex; align-items: center;">
            <span class="title">1院各指标达标率</span>
        </div>
        <el-divider style="margin: 5px;"/>
        <div style="height: 600px;width: 100%;" ref="chartLine"></div>
      </div>
    </div>
</template>
  
<script setup>  
  import { ref, onMounted } from 'vue'  
  import * as echarts from 'echarts' 
  import { ArrowRight } from '@element-plus/icons-vue'
  import { defineEmits } from 'vue'; 
  import request from '@/api/request';
    
  const chartPie = ref(null)  
  const chartBar = ref(null)  
  const chartLine = ref(null)  
  const emit = defineEmits(['activeName']);
  const tableData = ref([])
  const recordNum = ref(0)

    const go = () => {
        emit('activeName','3-3')
    }

    const getTopRate = () => {
        const req = {
            "num": 4,
            // "hospital_name": hospital.value,
            // "disease_type": type.value
        }
        const queryString = Object.keys(req).map(key => `${encodeURIComponent(key)}=${encodeURIComponent(req[key])}`).join('&');
        const url = '/top_last_num?' + queryString;
        request.get(url).then(res => {
            console.log(res)
            res.top_num.forEach(function(obj) {
                const item = {
                'name': obj.disease + ' ' + obj.indicator_name,
                'result':  Number(obj.rate*100).toFixed(0) + '%'
                }
            tableData.value.push(item)
            });
        })
        request.get('/distinct_emr_id_count').then(res => {
            console.log(res)
            recordNum.value = res.distinct_emr_id_count
        })
        request.get('/disease_counts_for_hospital').then(res => {
            console.log(res)
            const diseaseList = []
            res.forEach(item => {
                diseaseList.push({
                    name: item.disease,
                    value: item.count,
                    itemStyle: { color: generateLowSaturationColor() }
                })
            })
            const mychartPie = echarts.init(chartPie.value)   
            const optionPie = {
                        tooltip: {
                            trigger: 'item',
                            // textStyle: {
                            // color: '#ffffff'
                            // }
                        },
                        legend: {
                            type: 'plain',
                            orient: 'vertical',
                            right: 0,
                            top: 20,
                            bottom: 20,
                            itemGap: 15,
                            textStyle: {
                                color: 'black'
                            },
                            formatter: function (name) {
                                // 截取前三个字符并在后面添加省略号
                                return name.length > 3 ? name.substring(0, 3) + '...' : name;
                            },
                            tooltip: {
                                show: true,
                                formatter: function (params) {
                                    // 显示完整的文本
                                    return params.name;
                                }
                            }
                        },

                        grid: {  
                            left: '30%', 
                            right: '20%',
                            bottom: '3%',  
                            containLabel: true  
                        },
                        series: [
                            {
                            name: '指标数',
                            type: 'pie',
                            radius: ['60%', '80%'],
                            center: ['20%', '50%'],
                            labelLine: {  
                                show: false
                            },
                            label: {  
                                show: true,  
                                formatter: function (params) {  
                                    return '总指标数：108';  
                                },  
                                position: 'center',  
                                fontSize: 20,
                                fontWeight: 400,
                                color: 'black'
                            },  
                            data: diseaseList
                            }
                        ]
            };  
            mychartPie.setOption(optionPie) 
        })
    }

    const getRateList = () => {
        const url = '/latest_rate?hospital_name=';  
        request.get(url).then(res => {  
        console.log(res)
        const rateList = res.rates
        console.log(rateList)
    const name = []
    const result = []
    rateList.forEach(element => {
        name.push(element.disease + '-' + element.indicator_name)
        // const rate = Number(element.rate*100).toFixed(0) + '%';
        // console.log(rate)
        result.push(element.rate)
    });
    console.log(name)
    console.log(result)
    if (chartLine.value) {  
    const mychartLine = echarts.init(chartLine.value);  
    const option = {
            color: ['#5793f3', '#5195ff'],  
            tooltip: {  
                trigger: 'axis',  
                formatter: function (params) {  
                var value = params[0].value;  
                    return params[0].seriesName + ': ' + (value * 100).toFixed(0) + '%';  
                }
            },  
            grid: {  
                left: '2%',  
                right: '2%',  
                bottom: '5%', 
                containLabel: true  
            },  
            xAxis: {  
                type: 'category',  
                data: name,  
                axisLine: {  
                    lineStyle: {  
                        color: '#aaa'  
                    }  
                },  
                axisTick: {  
                    lineStyle: {  
                        color: '#aaa'  
                    }  
                },  
                axisLabel: {
                    formatter: function(params) {
                        var newParamsName = "";
                        var paramsNameNumber = params.length;
                        var provideNumber = 5;
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
                type: 'value',  
                axisLabel: {  
                    formatter: function (value, index) {  
                        return (value * 100).toFixed(0) + '%';
                    },
                    color: '#999'   
                },
                axisLine: {  
                    lineStyle: {  
                        color: '#aaa'  
                    }  
                },  
                axisTick: {  
                    lineStyle: {  
                        color: '#aaa'  
                    }  
                } 
            },  
            series: [{  
                name: '达标率',  
                type: 'line',  
                smooth: true,  
                symbolSize: 30, // 设置标记图形的大小  
                data: result,  
                areaStyle: {  
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{  
                        offset: 0,  
                        color: 'rgba(87, 147, 243, 0.8)' // 渐变起始颜色  
                    }, {  
                        offset: 1,  
                        color: 'rgba(87, 147, 243, 0)' // 渐变结束颜色  
                    }])  
                }  
            }]  
        };  
    
        mychartLine.setOption(option);  
    }
    }).catch(error => {  
    console.error('Error:', error);  
    });
    }

    const generateLowSaturationColor = () => {
      const h = Math.floor(Math.random() * 360); // 0-359
      const s = Math.floor(Math.random() * 21) + 30; // 30-50% (低饱和度)
      const l = Math.floor(Math.random() * 21) + 70; // 70-90% (高亮度)
      return `hsl(${h},${s}%,${l}%)`;
    };

  onMounted(() => {  
    getRateList()
    getTopRate()
})  
</script>

<style scoped>
/* 设置整体布局容器 */
.container1 {
  flex-direction: column;
  width: 100%;
  height: 100%;
  font-family: 'PingFang';
  display: flex;  
  justify-content: center; 
}

/* 设置顶部部分 */
.top {
  /* margin-top: 20px; */
  flex: 0 0 40%;
  display: flex;
  margin-bottom: 20px; /* 添加底部缝隙 */
}

/* 设置顶部部分的左中右部分 */
.top-left, .top-middle, .top-right {
  flex: 1;
  border-radius: 10px
}

.top-left, .top-middle {
  background-color: white; /* 金黄色 */
}

.top-middle {
    flex: 1.5;
}

.top-right {
  flex: 2;
  background-color: white; 
}

.middle {
  background-color: white; 
  margin-bottom: 20px;
  border-radius: 10px
}

.bottom {
    flex: 0 0 60%;
  background-color: white;
  border-radius: 10px;
}

/* 设置顶部和中间部分之间的缝隙 */
.top-gap, .gap {
  width: 20px; /* 设置宽度为20px来创建缝隙 */
}

.icon svg {
  margin-left: 10px; /* 调整图标与文字之间的间距 */
}

.top-left-title {
    margin: 8px;
    padding: 10px
}

.title {
  /* 你可以添加一些文本样式，如字体大小、颜色等 */
  color: black;
  font-weight: 600;
  font-size: 20px;
}

.icon {
    display: flex;
    align-items: center;
    font-size: 20px;
}

.statistic {  
    display: flex;  
    flex-direction: column;  
    height: 230px; /* 设置.statistic的高度 */  
}  
  
.row {  
    display: flex;  
    justify-content: space-between; /* 在每排的块之间添加空间 */  
    flex: 1; /* 使得每行都平分垂直空间 */  
    margin: 10px;  
}  
  
.row:last-child {  
    margin-bottom: 0; /* 移除最后一行的下边距 */  
}  
  
.block {  
    flex: 1 1; /* 平均分配空间 */  
    margin-right: 10px; /* 块之间的缝隙（只在同一行内的块之间有效） */  
    height: 100%; /* 使得块占据整行的高度（可选） */  
    background-color: rgb(223, 235, 255); /* 示例背景色 */  
    border-radius: 10px;
    border: 2px solid rgb(81, 153, 242);
} 

.final {
    flex: 1 1; /* 平均分配空间 */  
    margin-right: 10px; /* 块之间的缝隙（只在同一行内的块之间有效） */  
    height: 100%; /* 使得块占据整行的高度（可选） */  
}
  
.row .block:last-child {  
    margin-right: 0; /* 移除每行最后一个块的右侧缝隙 */  
}  

.block {  
    display: flex;  
    align-items: center; /* 垂直居中对齐子元素 */  
}  
  
.icon {  
    margin: 10px 7px; /* 图标和文本之间的间距 */  
}  
  
.text-container {  
    /* 这里不需要设置 flex-direction，因为默认就是行方向 */  
    display: flex;  
    align-items: center; /* 如果需要确保文本垂直居中对齐 */  
}  
  
.text-title{  
    margin: 0; /* 移除默认的margin */  
    font-size: 14px;
    width: 150px;
    /* 你可以在这里添加更多的样式，比如字体大小、颜色等 */  
}  
  
  
.text-num {  
    font-weight: 600; /* 标题加粗 */
    font-size: 2em; /* 数字稍大一些 */  
    margin-left: 40px;
    float: right;
}

.mid-left {
    height: 250px;
    width: 800px
}

.clickable-span {
    cursor: pointer;
    /* 添加其他样式，例如修改颜色、下划线等 */
}
</style>