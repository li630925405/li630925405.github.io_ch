# 栗子星中文博客

访问地址：<https://li630925405.github.io/li630925405.github.io_ch/>

本仓库保存 Hexo / NexT 生成的静态页面，GitHub Pages 从 `master` 分支根目录发布。

如果以后从原来的 Hexo 源项目重新生成，请先在源项目的 `_config.yml` 中设置：

```yaml
url: https://li630925405.github.io/li630925405.github.io_ch
root: /li630925405.github.io_ch/
```

博客部署在子目录中，资源、文章和主题配置中的路径都需要包含此前缀。
发布前可在本仓库运行：

```sh
python3 scripts/check-pages.py
```

配置说明：<https://hexo.io/docs/configuration#URL>

已知历史资源缺失：`2020/10/22/music/` 文章引用的 7 张本地插图未包含在原仓库中。
