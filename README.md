# miaobot-qq

## 如何开始

1. 使用 `nb create` 生成项目。
2. 使用 `nb plugin create` 创建您的插件。
3. 在 `src/plugins` 文件夹下编写您的插件。
4. 使用 `nb run --reload` 运行您的机器人。

## 使用 Docker 运行

拉取镜像


```bash
docker pull ghcr.io/miaoyww/miaobot-qq:latest
```

要使用 Docker 运行您的 `miaobot-qq`，请确保您已经拥有了最新的 Docker 镜像，并且已经准备好 `.env` 文件，其中包含了所有必要的环境变量。然后，运行以下命令：

```bash
docker run -v ./.env:/app/.env -d ghcr.io/miaoyww/miaobot-qq:latest
```

这个命令将启动 `miaobot-qq` 的 Docker 容器，并从 `.env` 文件加载环境变量。

## 文档

更多信息，请参见 [NoneBot 文档](https://nonebot.dev/).
