### Registry V2.0
1. 运行 docker-compose up -d

1. 配置insecure-registries 可以通过IP访问，否则只能通过localhost:5000访问
    ```shell script
    echo '{ "insecure-registries":["172.16.1.146:5000"] }' > /etc/docker/daemon.json
    sudo systemctl daemon-reload
    sudo systemctl restart docker
    ```
3. 查询
    ```shell script
    curl http://10.0.3.10:5000/v2/_catalog
    ```




