<template>
    <div class="infinite-list-wrapper" style="overflow: auto">
      <ul class="list">
        <li class="list-item">
            <div class="shouye">
                <img src="../../assets/wjw.png" alt="" class="custom-img">
                <div class="shouye-title">
                    申医大模型
                </div>
                <div class="shouye-detail">
                    <el-tree :data="treeData" node-key="id"></el-tree>
                </div>
            </div>
        </li>
        <li class="list-item">
            <div class="nhzk">
                <div class="nhzk-text">
                    内涵质控
                </div>
                <div class="nhzk-content">
                    <div class="content-top">
                        <div class="box" style="overflow: hidden; flex: 1.5;">
                                <el-table
                                height="100%"
                                :data="visibleData"
                                ref="table"
                                :header-cell-style="tableHeaderColor"
                                @row-click="handleRowClick"
                                >
                                <el-table-column
                                    prop="name"
                                    min-width="120"
                                    :show-overflow-tooltip="true"
                                    label="规则名称"
                                    align="center"
                                    :header-style="{ background: '#409EFF', color: 'white' }"
                                    style="color: white;"
                                />
                                <el-table-column
                                    label="达标率"
                                    min-width="68"
                                    prop="result"
                                    align="center"
                                    :show-overflow-tooltip="true"
                                    :header-style="{ background: '#409EFF !important', color: 'white !important' }"
                                    style="color: white;"
                                    />
                            </el-table>
                        </div>
                        <div class="box" style="flex: 1">
                            <svg class="icon" aria-hidden="true">
                                <use xlink:href="#icon-yiyuan"></use>
                            </svg>
                            <div class="text">
                                <div class="text-title">医院总数</div>
                                <div class="text-num">2</div>
                            </div>
                        </div>
                        <div class="box" style="flex: 1">
                            <svg class="icon" aria-hidden="true">
                                <use xlink:href="#icon-zhibiaoku"></use>
                            </svg>
                            <div class="text">
                                <div class="text-title">指标总数</div>
                                <div class="text-num">249</div>
                            </div>
                        </div>
                        <div class="box" style="flex: 1">
                            <svg class="icon" aria-hidden="true">
                                <use xlink:href="#icon-danbingzhonglogo"></use>
                            </svg>
                            <div class="text">
                                <div class="text-title">单病种总数</div>
                                <div class="text-num">189</div>
                            </div>
                        </div>
                        <div class="box" style="flex: 1">
                            <svg class="icon" aria-hidden="true">
                                <use xlink:href="#icon-huaban"></use>
                            </svg>
                            <div class="text">
                                <div class="text-title">专科总数</div>
                                <div class="text-num">101</div>
                            </div>
                        </div>
                        <div class="box" style="flex: 1">
                            <svg class="icon" aria-hidden="true">
                                <use xlink:href="#icon-yiliao_dianzibingli"></use>
                            </svg>
                            <div class="text">
                                <div class="text-title">电子病历总数</div>
                                <div class="text-num">404</div>
                            </div>
                        </div>
                    </div>
                    <div class="content-mid">
                        <div class="mid-left" ref="chartPie"></div>
                        <div class="mid-right" ref="chartLine"></div>
                    </div>
                    <div class="content-bottom" ref="chartBar">
                    </div>
                </div>
            </div>
        </li>
      </ul>
    </div>
</template>
  
<script>
  import * as echarts from 'echarts'
  import request from '@/api/request';
  export default {
    props: {
    selectData: {
      type: Array,
      default: [],
    },
  },
  watch: {
    selectData: function (newVal, oldVal) {
      this.getBranchData();
    },
  },
  data() {
    return {
        count: 10,
        branchData: [],
        clientHeight:"",
        scrollThreshold: 5,
        orgNameData: [], // 原始数据
        currentIndex: 0, // 当前显示数据的索引
        visibleRowCount: 5, // 可见行数，根据表格高度和行高设置
        scrollInterval: null, // 定时器
        scrollDelay: 1000, // 滚动间隔，单位：毫秒
        visibleData: [],
        tableHeaderColor : {
            background: ' #79bbff !important',
            color: '#333333',
            fontSize: '14px',
            textAlign: 'center',
        },
        treeData: [
            {
                id: 1,
                label: '数据',
                children: [
                    {
                        id: 101,
                        label: '大量医学语料，卫健委提供的权威指南',
                    }
                ]
            },
            {
                id: 'placeholder', // 占位节点的 id
                label: '', // 空的 label
                // 添加一个空的 children 数组，以确保占位节点没有子节点
                children: []
            },
            {
                id: 2,
                label: '预训练数据',
                children: [
                    {
                        id: 201,
                        label: '海量医学语料，卫健委提供的权威指南',
                    }
                ]
            },
            {
                id: 'placeholder', // 占位节点的 id
                label: '', // 空的 label
                // 添加一个空的 children 数组，以确保占位节点没有子节点
                children: []
            },
            {
                id: 3,
                label: '指令微调数据',
                children: [
                    {
                        id: 301,
                        label: '上百万条医疗对话，术语库转换，归一化、推理任务，专家标注数据，多领域指令微调数据',
                    }
                ]
            },
            {
                id: 'placeholder', // 占位节点的 id
                label: '', // 空的 label
                // 添加一个空的 children 数组，以确保占位节点没有子节点
                children: []
            },
            {
                id: 4,
                label: '应用',
                children: [
                    {
                        id: 401,
                        label: '医疗问答、术语归一化、数据助手、电子病历生成',
                    }
                ]
            },
            // {
            //     id: 'placeholder', // 占位节点的 id
            //     label: '', // 空的 label
            //     // 添加一个空的 children 数组，以确保占位节点没有子节点
            //     children: []
            // },
            // {
            //     id: 5,
            //     label: '评测',
            //     children: [
            //         {
            //             id: 501,
            //             label: 'xxxx',
            //         }
            //     ]
            // }
        ],
        rateList: []
    } 
},
    mounted() {
    this.initChart();
    this.updateVisibleData();
    this.startScroll();
    this.orgNameData = []
    this.getRateList()
  },
  beforeDestroy() {
    clearInterval(this.interval); // 销毁组件前清除定时器
  },
    methods: {
        initChart() {
            const chartPie = echarts.init(this.$refs.chartPie);
            const chartBar = echarts.init(this.$refs.chartBar);
            const chartLine = echarts.init(this.$refs.chartLine)
            const optionPie = {
                title: {
                    text: "xx医院各科室指标数",
                    textStyle: {
                    color: 'black' // 修改标题字体颜色为白色
                    }
                },
                tooltip: {
                    trigger: 'item',
                    // textStyle: {
                    // color: '#ffffff' // 修改提示框字体颜色为白色
                    // }
                },
                legend: {
                    type: 'scroll',
                    orient: 'vertical',
                    left: 10,
                    right: 20,
                    top: 30,
                    bottom: 20,
                    textStyle: {
                    color: 'black' // 修改图例字体颜色为白色
                    }
                },
                series: [
                    {
                    name: 'Access From',
                    type: 'pie',
                    radius: '70%',
                    center: ['60%', '50%'],
                    data: [
                        { value: 2, name: '产科', itemStyle: { color: '#ffcc99' } },
                        { value: 1, name: '儿科', itemStyle: { color: '#ff6666' } },
                        { value: 5, name: '妇科', itemStyle: { color: '#ff99cc' } },
                        { value: 5, name: '骨科', itemStyle: { color: '#9966cc' } },
                        { value: 4, name: '呼吸内科', itemStyle: { color: '#66cc99' } },
                        { value: 6, name: '康复医学', itemStyle: { color: '#6699CC' } },
                        { value: 11, name: '麻醉', itemStyle: { color: '#996699' } },
                        { value: 2, name: '泌尿外科', itemStyle: { color: '#CC9966' } },
                        { value: 4, name: '普通外科', itemStyle: { color: '#99CC99' } },
                        { value: 9, name: '神经内科', itemStyle: { color: '#999933' } },
                        { value: 6, name: '神经外科', itemStyle: { color: '#666600' } },
                        { value: 4, name: '肾内科', itemStyle: { color: '#CCCC33' } },
                        { value: 6, name: '消化内镜', itemStyle: { color: '#339999' } },
                        { value: 6, name: '消化内科', itemStyle: { color: '#99CC33' } },
                        { value: 6, name: '心血管内科', itemStyle: { color: '#99CCFF' } }
                    ],
                    label: {
                        textStyle: {
                        color: 'black' // 修改标签字体颜色为白色
                        }
                    }
                    }
                ]
            };
            const optionBar = {
                title: {
                    text: 'xx医院各指标达标率',
                    textStyle: {
                        color: 'black' // 修改标题字体颜色为黑色
                    }
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'shadow'
                    },
                    formatter: function(params) {
                        return params[0].name + ': ' + params[0].value + '%';
                    }
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                xAxis: [
                    {
                        type: 'category',
                        data: ['髋关节置换', 'IgA肾病', '垂体腺瘤', '短暂性脑缺血发作', '房颤', '脑癌', '感染性休克早期治疗','高血压病','宫颈癌','冠心病介入治疗病','急性肺血栓栓塞症','急性心肌梗死','甲状腺癌','甲状腺结节','结肠癌','颈动脉支架植入术','脑出血','脑梗死','乳腺癌','剖宫产','脑血管造影术','HBV感染分娩母婴阻断'],
                        axisTick: {
                            alignWithLabel: true
                        },
                        axisLabel: {
                            color: 'black'
                        }
                    }
                ],
                yAxis: [
                    {
                        type: 'value',
                        axisLabel: {
                            color: 'black',
                            formatter: '{value}%'
                        }
                    }
                ],
                dataZoom: [
                    {
                        type: 'slider',
                        xAxisIndex: 0,
                        start: 0,
                        end: 100  // 初始滚动范围，可以根据需要调整
                    }
                ],
                series: [
                    {
                        name: '达标率',
                        type: 'bar',
                        itemStyle: {
                            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                                { offset: 0, color: '#6699CC' }, // 渐变起始颜色
                                { offset: 0.5, color: '#99CCFF' }, // 中间颜色
                                { offset: 1, color: '#336699' } // 渐变结束颜色
                            ])
                        },
                        barWidth: '60%',
                        data: [90, 30, 10, 100, 100, 100, 100, 100, 10, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 99 ]
                    }
                ]
            };

            const optionLine = {
                title: {
                    text: 'xx医院近一年病历数量',
                    textStyle: {
                    color: 'black' // 修改标题字体颜色为白色
                    }
                },
                tooltip: {
                    trigger: 'axis'
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                xAxis: {
                    type: 'category',
                    boundaryGap: false,
                    data: ['2023-05', '2023-06', '2023-07', '2023-08', '2023-09', '2023-10', '2023-11', '2023-12', '2024-01', '2024-02', '2024-03', '2024-04'],
                    axisLabel: {
                        color: 'black'
                    }
                },
                yAxis: {
                    type: 'value',
                    axisLabel: {
                        color: 'black'
                    }
                },
                series: [
                    {
                        // name: '一院',
                        type: 'line',
                        stack: 'Total',
                        areaStyle: {},
                        lineStyle: { // 添加lineStyle属性来指定折线样式
                            color: 'red' // 设置折线颜色为红色
                        },
                        lineStyle: { // 添加lineStyle属性来指定折线样式
                            color: 'red' // 设置折线颜色为红色
                        },
                        data: [120, 300, 600, 1000, 3000, 3004, 4000, 5000, 6000, 6500, 7000, 10000],
                    },
                    {
                        // name: '一院',
                        type: 'line',
                        stack: 'Total',
                        areaStyle: {},
                        lineStyle: { // 添加lineStyle属性来指定折线样式
                            color: 'green' // 设置折线颜色为红色
                        },
                        lineStyle: { // 添加lineStyle属性来指定折线样式
                            color: 'green' // 设置折线颜色为红色
                        },
                        data: [90, 100, 200, 900, 3080, 3704, 4500, 5500, 6500, 7000, 7900, 9000],
                    }
                ]
            };
            chartPie.setOption(optionPie)
            chartBar.setOption(optionBar)
            chartLine.setOption(optionLine)
        },
        startScroll() {
        this.scrollInterval = setInterval(() => {
        this.scrollData();
      },this.scrollDelay);
        },
        scrollData() {
        const { orgNameData, currentIndex } = this;
        const nextIndex = (currentIndex + 1) % orgNameData.length;
        this.currentIndex = nextIndex;
        if (nextIndex === 0) {
            // 如果滚动到了最后一个索引，重置为0，重新开始滚动
            this.updateVisibleData();
        } else {
            // 否则，继续滚动
            this.updateVisibleData();
        }
        },

    updateVisibleData() {
    const { orgNameData, currentIndex, visibleRowCount } = this;
    const start = currentIndex;
    const end = start + visibleRowCount;
    if (end > orgNameData.length) {
        // 计算剩余的可见行数
        const remainingRowCount = end - orgNameData.length;
        // 取剩余的可见行数和开头的数据合并来填充可见区域
        const visibleData = [...orgNameData.slice(start), ...orgNameData.slice(0, remainingRowCount)];
        this.visibleData = visibleData;
    } else {
        // 否则直接取当前索引到结束的数据填充可见区域
        this.visibleData = orgNameData.slice(start, end);
    }
    },
    handleRowClick() {
        this.$emit('childEvent', '3-2');
    },
    getRateList() {
    const url = '/latest_rate?hospital_name=';  
    request.get(url).then(res => {  
    console.log(res)
    const rateList = res.rates
    console.log(rateList)
    this.orgNameData = []
    rateList.forEach(element => {
        const item = {
            'name': element.disease + ' ' + element.indicator_number,
            'result': element.rate
        }
        this.orgNameData.push(item)
    });
    }).catch(error => {  
    console.error('Error:', error);  
    });
    }
    }
  }

  </script>
  
<style>
  .infinite-list-wrapper .list {
    padding: 0;
    margin: 0;
    list-style: none;
  }
  
  .infinite-list-wrapper .list-item {
    display: flex;
    /* align-items: center; */
    /* justify-content: center; */
    /* height: 50px; */
    /* background: var(--el-color-danger-light-9);
    color: var(--el-color-danger); */
  }
.shouye {
  /* 设置背景图片 */
   background-image: url('../../assets/dt.jpg'); 
  /* 设置背景图片大小和位置 */
   background-size: cover;
background-position: center; 
  /* 设置高度和宽度 */
  text-align: center; 
  height: 600px;
  width: 100%;
}

.shouye-title {
    color: #101734;
    font-size: 60px;
    font-family: PingFang SC;
    font-style: normal;
    font-weight: 500;
    line-height: normal;
    /* margin-left: 10%; */
    margin-top: 20px
}

.shouye-image {
  /* 设置小图片背景 */
  background-image: url('../../assets/wjw.png');
  /* 设置背景图片大小和位置 */
  /* background-size: contain; */
  /* background-position: top left; */
  /* 设置小图片大小 */
  width: 50px; /* 你可以根据需要调整宽度 */
  height: 50px; /* 你可以根据需要调整高度 */
  /* 设置绝对定位在左上角 */
  position: absolute;
}

.nhzk {
    width: 100%;
    height: 100%;
}

.nhzk-text {
    color: #101734;
    font-size: 50px;
    font-family: PingFang SC;
    font-style: normal;
    font-weight: 500;
    line-height: normal;
    /* margin-left: 10%; */
    margin-top: 50px
}

.nhzk-detail {
    display: flex;
    flex-direction: column;
    flex-shrink: 0;
    color: #101734;
    font-size: 20px;
    font-family: PingFang SC;
    font-style: normal;
    font-weight: 400;
    line-height: 28px;
    /* margin-left: 10%; */
    margin-bottom: 50px;
}

.nhzk-content {
    /* background-image: url("../../assets/nhzk.svg"); */
    height: 1000px;
    width: 100%; /* 使用整个容器宽度 */
    background-size: cover;
    background-position: center;
    margin-left: 0; /* 移除左边距 */
    float: right;
    
}


.content-top {
    display: flex;
    justify-content: space-between; /* 使小框之间等距排列 */
    margin-top: 10px; /* 添加整体上边距 */
    height: 20%;
}

.box {
    flex: 1; /* 平均分割每个小框 */
    display: flex;
    height: 100%; /* 调整小框的高度 */
    border: 2px solid black; /* 设置边框为白色 */
    border-radius: 5%;
    margin: 10px;
    align-items: center; /* 垂直居中 */
    justify-content: space-between; /* 水平居中 */
}

.text-title {
    color: black;
    font-size: 30px;
    font-family: PingFang SC;
    font-style: normal;
    font-weight: 400;
    line-height: 28px;
    margin: 10px
}

.text-num {
    color: black;
    font-size: 50px;
    font-family: PingFang SC;
    font-style: normal;
    font-weight: 400;
    line-height: 28px;
    float: right;
    margin: 10px;
    margin-top: 30px;
}

.icon {
    width: 80px; /* 设置图标宽度 */
    height: 80px; /* 设置图标高度 */
    margin: 10px;
}

/* 添加小框之间的间隔 */
.box + .box {
    margin-left: 10px;
    overflow: hidden; /* 隐藏溢出内容 */
}

.content-mid {
    display: flex; /* 使用 flex 布局 */
    height: 35%;
    width: 100%;
    margin-top: 20PX;
}

.mid-left {
    flex: 3; /* 左边占据 4 格 */
}

.mid-right {
    flex: 6; /* 右边占据 6 格 */
}

.content-bottom {
    margin-top: 10px;
    width: 100%;
    height: 35%;
}

.shouye-detail {
    width: 80%;
    margin-left: 10%;
    margin-top: 20px;
}

.el-tree {
    font-size: 24px;
}

.custom-img {
    width: 80px; /* 图片宽度 */
    height: auto; /* 让高度自适应 */
    margin-top: 30px
}

/* 设置.el-tree元素的背景为透明，以及一些其他样式 */
.el-tree{
    margin-left: 50%;
    font-size: 24px;
    color: black;
    background: rgba(0,0,0,0);
    .el-checkbox__inner{
        background:rgba(0,0,0,0);
    }
    .el-tree-node__content:hover {
        background: transparent;
    }
    .el-tree-node:focus>.el-tree-node__content {
        background-color: rgba(0,0,0,0);
    }

    
}

/* 调整 el-tree 节点标志的大小 */
.el-tree-node__expand-icon {
  font-size: 20px; /* 设置节点标志的字体大小为 20 像素 */
}


</style>
  