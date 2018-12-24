# monitor_demo
基于tornado和websocket的硬件监视系统

## 本地运行项目
1. 克隆项目到本地
```shell
git clone https://github.com/Sbwillbealier/monitor_demo.git
```
2. 创建并激活虚拟环境(可省略)
```
# 新建Python3版本的虚拟环境
conda create --name python3 python=3.5  
# 激活Python3环境
activate python3 
```
3. 安装依赖

进入项目目录
```
pip install -r requirements.txt
```
4. 迁移数据库
```
python app\models\models.py
```
5. 运行程序
``` 
python manage.py --port=8000  # 指定端口
```
6. 运行日志采集脚本
```
python log.py  # 单独运行采集内存/交换分区/cpu使用率
```
7. 查看
```
127.0.0.1:8000
```

### 截图
![截图](screenshots/1.png)  
![截图](screenshots/2.png)  
![截图](screenshots/3.png)  
![截图](screenshots/4.png)  
