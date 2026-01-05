---
description: 自动检测Git状态，提交代码，推送到远程，并尝试创建PR
---

# 1. 获取上下文信息
请在我的电脑上运行以下 Bash 命令，获取当前的 Git 状态，不需要问我：

<bash>
# 检查当前 git 状态
echo "=== GIT STATUS ==="
git status

# 检查当前有哪些具体修改（只看文件名和统计）
echo "=== GIT DIFF STAT ==="
git diff --stat
</bash>

# 2. 执行逻辑指令
根据上面运行获取到的信息，请按顺序执行以下操作：

1. **检查更改**：
   - 如果没有更改，直接告诉我“没有需要提交的内容”并结束。
   - 如果有未跟踪（untracked）或修改的文件，继续下一步。

2. **执行提交**：
   - 运行 `git add .`
   - 根据 `git diff` 的内容，帮我写一个简洁、符合规范的 Commit Message。
   - 运行 `git commit -m "你的Commit Message"`。

3. **推送到远程**：
   - 运行 `git push`。

4. **创建 PR (可选)**：
   - 检查是否安装了 `gh` (GitHub CLI)。
   - 如果安装了，尝试运行 `gh pr create --fill`。
   - 如果没安装，只提示“代码已推送”。