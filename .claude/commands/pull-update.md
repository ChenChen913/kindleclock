---
description: 从 GitHub 拉取最新代码，并检查是否需要安装新依赖
---

# 1. 获取当前状态
在执行拉取之前，请先运行以下 Bash 命令查看状态，不要问我，直接运行：

<bash>
# 获取远程最新信息，但不合并
git fetch origin

# 查看当前分支状态（是落后 behind 还是领先 ahead）
git status

# (可选) 如果是 Node 项目，检查 package.json 是否有变动
# cat package.json 
</bash>

# 2. 执行逻辑
根据上面的输出信息，请执行以下步骤：

1. **检查是否有冲突风险**：
   - 如果 `git status` 显示本地有“未提交的更改 (Uncommitted changes)”，请**停止操作**，并警告我：“本地有未提交的更改，请先提交或暂存后再拉取。”

2. **执行拉取**：
   - 如果本地很干净，且 `git status` 显示“Your branch is behind...”，请运行 `git pull`。
   - 如果显示“Your branch is up to date”，请告诉我“当前已经是最新版本，无需拉取”。

3. **后续检查 (智能建议)**：
   - 如果刚刚成功执行了拉取，请检查是否有新的依赖包需要安装（例如 `package.json` 或 `requirements.txt` 有变动）。
   - 如果有变动，请询问我是否要运行 `npm install` 或 `pip install`。