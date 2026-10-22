# Instagram App operator

通过 macOS iPhone 镜像运营移动 App 的 Instagram 账号，支持设备切换、断线重连、账号核验、Insights 复盘、相关互动与发布验证。

- 主 Skill：[instagram-app-operator](skills/instagram-app-operator/SKILL.md)
- 镜像依赖：[iphone-mirroring-operator](skills/iphone-mirroring-operator/SKILL.md)
- 每轮经验保存：[persistence](skills/instagram-app-operator/references/persistence.md)

把这两个 Skill 目录安装到 Codex 的个人技能目录。账号与设备映射、截图、运营数据和原始聊天留在本地。

自动同步使用本地配置指定的仓库地址；Stop 钩子需用户在 Codex 中审核信任。它只保存主 Skill 的可复用经验，不会无人值守操作 Instagram。
