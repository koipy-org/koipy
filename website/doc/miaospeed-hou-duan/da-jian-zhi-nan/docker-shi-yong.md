# docker使用

miaospeed支持在docker里运行（简易版基本参数启动）：

```bash
docker run -idt \
   --name miaospeed \
   --network=host \
   --restart always \
   airportr/miaospeed:latest \
   server -bind 0.0.0.0:8765 -path miaospeed -token SbbieN2e{Q?W -mtls
```

完整参数启动，不需要的参数自行删除，请不要直接复制这个启动，否则无法连接：

```bash
docker run -idt \
   --name miaospeed \
   --network=host \
   --restart always \
   airportr/miaospeed:latest \
   server -bind 0.0.0.0:8765 -token SbbieN2e{Q?W \
   -mtls \
   -connthread 32 \
   -nospeed \
   -pausesecond 1 \
   -speedlimit 1073741824 \
   -verbose \
   -whitelist 111111|22222|333333 \
   -serverpublickey "PATH_TO_miaospeed.crt" \
   -serverprivatekey "PATH_TO_miaospeed.key"
```

参数解释查看搭建指南那一页
