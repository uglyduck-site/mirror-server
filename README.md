# 容器镜像加速服务器
本项目可快速部署容器镜像加速服务器。由于配置格式及docker客户端配置限制， 本项目仅适用于使用`containerd runtime`的容器镜像加速。

# 前置要求
- `Python`版本 3.8+
- 安装`docker`
- 安装`docker compose`
- 一个公网可解析的域名

# 填写配置文件
在`config.json`中填写必要的配置：
- `registries`: 需要加速的镜像站列表, 填写域名即可， 默认为`https`协议；
- `domain`: 加速器域名，需提前申请并注册到互联网名称服务器，公网可解析；
- `email`: 填写一个合法的邮箱地址即可;

# 运行
执行以下命令，将自动申请`SSL`证书(如在`nginx/ssl`目录下没有证书存在)，生成配置文件，并启动加速器：
```bash
python3 main.py
```
输出内容例如：
```bash
Checking environment...
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

# containerd客户端配置
1. 为每个目标站点创建配置目录(目录名称可以随便写，能看懂即可)
```bash
mkdir -p /etc/containerd/certs.d/dockerhub # 源站点registry-1.docker.io
mkdir -p /etc/containerd/certs.d/quary     # 源站点quary.io
...
```

2. 为各个站点配置加速(配置文件名为`hosts.toml`)
其中:
- `server`为源镜像站点
- `host.`后面是加速器站点及uri, 格式为`<加速器域名>/<源站点域名>`

示例1: dockerhub加速配置
```bash
cat <<EOF > /etc/containerd/certs.d/dockerhub/hosts.tomal
server = "https://registry-1.docker.io"
[host."https://docker.uglyduck.site/registry-1.docker.io"]
  capabilities = ["pull", "resolve"]
EOF
```

示例2: quary.io加速配置
```bash
cat <<EOF > /etc/containerd/certs.d/quary/hosts.tomal
server = "https://quary.io"
[host."https://docker.uglyduck.site/quary.io"]
  capabilities = ["pull", "resolve"]
EOF
```

如上， 为每个需要加速的站点都进行上述配置。

# 重启containerd
```bash
systemctl restart containerd
```

# 测试配置
## docker测试
docker需在/etc/docker/daemon.json中进行配置， 且只能加速dockerhub的镜像， 本项目不针对docker客户端加速。

## 使用ctr客户端测试
使用ctr命令拉取镜像时需要指定`--hosts-dir`参数：
```bash
ctr image pull docker.io/library/amazoncorretto:11 --hosts-dir /etc/containerd/certs.d

docker.io/library/amazoncorretto:11:                                              resolved       |++++++++++++++++++++++++++++++++++++++|
index-sha256:6c4b652bb05c91148d08c0c0856875725744d3368f195a7a1b4013910ba8efc0:    exists         |++++++++++++++++++++++++++++++++++++++|
manifest-sha256:c9ebd5d4c48014cc08040eec2adb3c1da77b3e1d1e47b05450dd088873f77c26: exists         |++++++++++++++++++++++++++++++++++++++|
config-sha256:cb1efffd6bb7aeeaa2c36cb00d7201547c222f712ee80ed1aa856368f90272a4:   exists         |++++++++++++++++++++++++++++++++++++++|
layer-sha256:f956a2176a592b2f85941102c85f1a745c5e74f263c66fc5212bf9eb619f28e1:    downloading    |+++++++++++++++++++-------------------| 31.0 MiB/59.8 MiB
layer-sha256:88fcfc4c5843cedbd18a8793ed07b4046649d10f26bb1b69d14be76b565cb914:    downloading    |++++++++++++++++++++------------------| 75.0 MiB/141.3 MiB
elapsed: 5.7 s                                                                    total:  106.0  (18.6 MiB/s)
```

## 使用nerdctl客户端测试
配置并重启containerd后， nerdctl可以自动识别到加速器配置：
```bash
nerdctl pull docker.io/library/amazoncorretto:11

docker.io/library/amazoncorretto:11:                                              resolved       |++++++++++++++++++++++++++++++++++++++|
index-sha256:6c4b652bb05c91148d08c0c0856875725744d3368f195a7a1b4013910ba8efc0:    exists         |++++++++++++++++++++++++++++++++++++++|
manifest-sha256:c9ebd5d4c48014cc08040eec2adb3c1da77b3e1d1e47b05450dd088873f77c26: exists         |++++++++++++++++++++++++++++++++++++++|
config-sha256:cb1efffd6bb7aeeaa2c36cb00d7201547c222f712ee80ed1aa856368f90272a4:   exists         |++++++++++++++++++++++++++++++++++++++|
layer-sha256:88fcfc4c5843cedbd18a8793ed07b4046649d10f26bb1b69d14be76b565cb914:    downloading    |++++++++++++++------------------------| 54.0 MiB/141.3 MiB
layer-sha256:f956a2176a592b2f85941102c85f1a745c5e74f263c66fc5212bf9eb619f28e1:    downloading    |++++++--------------------------------| 11.0 MiB/59.8 MiB
elapsed: 2.1 s                                                                    total:  65.0 M (30.9 MiB/s)
```
