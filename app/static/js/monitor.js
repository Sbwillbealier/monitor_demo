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
    // 建立连接
    conn.onopen = function () {
        console.log('open');
        conn.send('test');
    };
    // 建立接收消息
    conn.onmessage = function (e) {
        console.log('message', e.data);
    };
    // 关闭连接
    conn.onclose = function () {
        console.log('close');
    };

    // 每隔一秒发送消息给服务器
    setInterval(function () {
        conn.send('server');
    }, 10000)
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