# 容器镜像加速服务器
本项目可快速部署容器镜像加速服务器。

# 前置要求
- `Python`版本 3.8+
- 安装`certbot`
- 安装`docker`
- 安装`docker compose`
- 一个公网可解析的域名

# 填写配置文件
在`config.json`中填写必要的配置：
- `registries`: 需要加速的镜像站列表, 填写域名即可， 默认为`https`协议；
- `domain`: 加速器域名，需提前申请并注册到互联网名称服务器，公网可解析；
- `email`: 填写一个合法的邮箱地址即可

# 运行
执行以下命令，将自动申请`SSL`证书(如在`nginx/ssl`目录下没有证书存在)，生成配置文件，并启动加速器：
```bash
python3 main.py
```
输出内容例如：
```bash
Applying SSL certificate...
SSL certificate for docker.uglyduck.site is already present.
Generating registry server configurations...
registry-1.docker.io
docker.elastic.co
gcr.io
k8s.gcr.io
quay.io
nvcr.io
rocks.canonical.com
mcr.microsoft.com
Generating Nginx configuration...
Generating Docker Compose configuration...
Starting Docker Compose...
[+] Running 10/10
 ✔ Network mirror-server_default   Created                                                                                                                                   0.1s 
 ✔ Container registry-1_docker_io  Started                                                                                                                                   0.2s 
 ✔ Container mcr_microsoft_com     Started                                                                                                                                   0.2s 
 ✔ Container docker_elastic_co     Started                                                                                                                                   0.2s 
 ✔ Container nginx                 Started                                                                                                                                   0.2s 
 ✔ Container gcr_io                Started                                                                                                                                   0.2s 
 ✔ Container rocks_canonical_com   Started                                                                                                                                   0.2s 
 ✔ Container quay_io               Started                                                                                                                                   0.2s 
 ✔ Container k8s_gcr_io            Started                                                                                                                                   0.2s 
 ✔ Container nvcr_io               Started                                                                                                                                   0.2s 
Docker Compose has started successfully.
```

# 关闭加速器
```bash
docker compose down
```