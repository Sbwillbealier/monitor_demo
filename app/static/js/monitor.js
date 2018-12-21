// 1.定义长连接
var conn = null;

// 2. 定义长连接函数
function connect() {
    // 断开上次连接
    disconnect();

    // 定义协议,提供SockJS可能使用的列表传输
    var transports = ['websocket'];

    // 创建连接对象,并转化协议
    conn = new SockJS('http://127.0.0.1:8000/real/time', transports);

    // 提示未连接
    log("warning", "正在建立连接...");

    // 建立连接
    conn.onopen = function () {
        console.log('open');
        conn.send('test');
        log("success", "连接成功");
    };
    // 建立接收消息
    conn.onmessage = function (e) {
        // console.log('message', e.data);
        update_ui(e);
    };
    // 关闭连接
    conn.onclose = function () {
        console.log('close');
        log("danger", "连接断开");
    };

    // 每隔一秒发送消息给服务器
    setInterval(function () {
        conn.send('system');
    }, 1000)
}

// 3.定义断开连接的函数
function disconnect() {
    if (conn != null) {
        conn.close();
        // 赋值为空，下次继续使用
        conn = null;
    }
}

// 4.刷新时重新连接
if (conn == null) {
    connect();
} else {
    disconnect();
}

//进度条变化
function progress_status(val) {
    var data = "";
    if (val >= 0 && val < 25) {
        data = " bg-success";
    } else if (val >= 25 && val < 50) {
        data = "";
    } else if (val >= 50 && val < 75) {
        data = " bg-warning";
    } else if (val >= 75 && val <= 100) {
        data = " bg-success";
    }
    return data
}


// 实时更新信息
function update_ui(e) {
    // 传入的更新数据
    let data = JSON.parse(e.data);  // 把json字符串解析出json对象

    // 平均CPU使用率更新
    option_cpu_avg.series[0].data[0] = (data['cpu']['percent_avg'] / 100).toFixed(4);
    option_cpu_avg.title[0].text = data['dt'] + "-CPU平均使用率";
    myChart_cpu_avg.setOption(option_cpu_avg);

    // 每个CPU使用率更新
    let cpu_per = "";
    for (let k in data['cpu']['percent_per']) {
        let num = parseInt(k);
        cpu_per += "<tr><td class='text-primary' style='width: 30%'>CPU" + num + "</td>";
        cpu_per += "<td><div class='progress'><div class='progress-bar progress-bar-striped progress-bar-animated" + progress_status(data['cpu']['percent_per'][k]) + "' role='progressbar' aria-valuenow='" + data['cpu']['percent_per'][k] + "' aria-valuemin='0' aria-valuemax='100' style='width: " + data['cpu']['percent_per'][k] + "%'>" + data['cpu']['percent_per'][k] + "%</div></div></td></tr>";
    }
    let tb_cpu_per = document.getElementById('tb_cpu_per');
    tb_cpu_per.innerHTML = cpu_per;

    // 更新内存信息仪表盘
    option_mem.series[0].data[0].value = data['mem']['percent'];
    option_mem.title[0].text = data['dt'] + "-内存使用率";
    myChart_mem.setOption(option_mem);

    // 更新内存信息表格
    document.getElementById('mem_percent').innerHTML = data['mem']['percent'];
    document.getElementById('mem_total').innerHTML = data['mem']['total'];
    document.getElementById('mem_used').innerHTML = data['mem']['used'];
    document.getElementById('mem_free').innerHTML = data['mem']['free'];

    // 更新交换分区信息仪表盘
    option_swap.series[0].data[0].value = data['swap']['percent'];
    option_swap.title[0].text = data['dt'] + "-交换分区使用率";
    myChart_swap.setOption(option_swap);

    // 更新交换分区信息表格
    document.getElementById('swap_percent').innerHTML = data['swap']['percent'];
    document.getElementById('swap_total').innerHTML = data['swap']['total'];
    document.getElementById('swap_used').innerHTML = data['swap']['used'];
    document.getElementById('swap_free').innerHTML = data['swap']['free'];

    // 更新网络信息饼状图
    var net = "";
    for (var k in data['net']) {
        var cd = data['net'][k];
        if (parseInt(cd['bytes_sent']) != 0 && parseInt(cd["bytes_recv"]) != 0) {
            var index = parseInt(k) + 1;
            var op = eval("option_net" + index);
            var ch = eval("myChart_net" + index);
            op.title[0].text = data["dt"] + "-" + cd["name"] + "网卡信息";
            op.series[0].data = [
                {
                    "value": cd['packets_recv'],
                    "name": "接收包数"
                },
                {
                    "value": cd['packets_sent'],
                    "name": "发送包数"
                }
            ];
            op.series[1].data = [
                {
                    "value": cd['bytes_recv'],
                    "name": "接收字节"
                },
                {
                    "value": cd['bytes_sent'],
                    "name": "发送字节"
                }
            ];
            ch.setOption(op);
        }
        // 更新网络信息表
        net += "<tr><td>" + cd['name'] + "</td>";
        net += "<td class='text-danger'>" + cd['bytes_sent'] + "</td>";
        net += "<td class='text-danger'>" + cd['bytes_recv'] + "</td>";
        net += "<td class='text-danger'>" + cd['packets_sent'] + "</td>";
        net += "<td class='text-danger'>" + cd['packets_recv'] + "</td>";
        net += "<td>" + cd['family'] + "</td>";
        net += "<td>" + cd['address'] + "</td>";
        net += "<td>" + cd['netmask'] + "</td>";
        if (cd['broadcast'] != null) {
            net += "<td>" + cd['broadcast'] + "</td></tr>";
        } else {
            net += "<td>无</td></tr>";

        }
    }
    document.getElementById('net_info_tb').innerHTML = net;

    // 更新磁盘信息
    var disk = "";
    for (var k in data['disk']) {
        var d = data['disk'][k];
        disk += "<tr><td>" + d['device'] + "</td>";
        disk += "<td>" + d['mountpoint'] + "</td>";
        disk += "<td>" + d['fstype'] + "</td>";
        disk += "<td>" + d['opts'] + "</td>";
        disk += "<td>" + d['used']['total'] + "</td>";
        disk += "<td>" + d['used']['used'] + "</td>";
        disk += "<td>" + d['used']['free'] + "</td>";
        disk += "<td><div class='progress'><div class='progress-bar "
            + progress_status(d['used']['percent'])
            + "' role='progressbar' style='width: " + d['used']['percent'] +
            "   aria-valuenow='" + d['used']['percent'] + "' aria-valuemin='0'" +
            "' aria-valuemax='100'>" + d['used']['percent'] +
            "</div></div></td></tr>"
    }
    document.getElementById('disk_info_tb').innerHTML = disk;
}

// 连接状态提醒
function log(cls, msg) {
    document.getElementById('monitor_status').innerHTML = "<div class='alert alert-" + cls + "'>" + msg + "</div>";
}