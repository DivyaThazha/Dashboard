// ﻿$(function () {
//     initRealTimeChart();
// });

function buildGraph(node,type) {
    //Real time ==========================================================================================
    var plot = $.plot('#real_time_chart'+'_'+node+'_'+type, [getValues(node,type)], {
        series: {
            shadowSize: 0,
            color: 'rgb(0, 188, 212)'
        },
        grid: {
            borderColor: '#f3f3f3',
            borderWidth: 1,
            tickColor: '#f3f3f3'
        },
        lines: {
            fill: true
        },
        yaxis: {
            min: 0,
            max: 100
        },
        xaxis: {
            min: 0,
            max: 100
        }
    });

}

usageData = {
    'slave01' : {
        'memory' : [],
        'cpu' : []
    },
    'slave02' : {
        'memory' : [],
        'cpu' : []
    },
    'slave03' : {
        'memory' : [],
        'cpu' : []
    },
    'kubernetes-sdn-master' : {
        'memory' : [],
        'cpu' : []
    }
}

function getValues(node,type)
{
    return usageData[node][type]
}
function updateCpuUsage(){
     $.ajax({
       url: 'http://130.65.159.69:7000/kube-api/metrics',
       dataType: 'json',
       type: 'get',
       success: function(resp){

    /*resp = { metrics:[
        {'node':'slave01','cpu':'20','memory':'50'}
        ,
        {'node':'slave02','cpu':'20','memory':'50'}
        ,
        {'node':'slave03','cpu':'20','memory':'50'},

        {'node':'kubernetes-sdn-master','cpu':'20','memory':'50'}]}*/

    metrics = resp.metric;
    for(i=0;i<metrics.length;i++)
    {
        var key = metrics[i]['node']
        if(key in usageData)
        {
            usageData[key]['memory'].push([usageData[key]['memory'].length,Number(metrics[i]['memory'])])
            usageData[key]['cpu'].push([usageData[key]['cpu'].length,Number(metrics[i]['cpu'])])

            if(usageData[key]['memory'].length>100)
                usageData[key]['memory'].shift()
            if(usageData[key]['cpu'].length>100)
                usageData[key]['memory'].shift()
        }
    }
    buildGraph("slave01","cpu")
    buildGraph("slave01","memory")
    buildGraph("slave02","cpu")
    buildGraph("slave02","memory")
    buildGraph("slave03","cpu")
    buildGraph("slave03","memory")
    buildGraph("kubernetes-sdn-master","cpu")
    buildGraph("kubernetes-sdn-master","memory")
     }
     })
}

