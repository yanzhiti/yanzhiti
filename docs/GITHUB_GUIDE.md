# GitHub 新手贡献指南

> 本指南专为中文新手开发者编写，帮助你在 GitHub 上参与开源项目贡献。

---

## 📚 目录

1. [GitHub 账号基础](#1-github-账号基础)
2. [贡献代码的标准流程（Fork + PR）](#2-贡献代码的标准流程fork--pr)
3. [日常开发中的常用 Git 操作](#3-日常开发中的常用-git-操作)
4. [参与 Issues 讨论](#4-参与-issues-讨论)
5. [项目维护者操作](#5-项目维护者操作)
6. [常见问题解答](#6-常见问题解答)

---

## 1. GitHub 账号基础

### 1.1 注册 GitHub 账号

1. 访问 https://github.com
2. 点击 **Sign up** 注册
3. 填写用户名（建议用英文，用于展示）、邮箱、密码
4. 完成人机验证
5. 选择免费计划（Free）

> ⚠️ **重要**：用户名建议使用真实姓名拼音或常用英文昵称，因为这个会公开显示。

### 1.2 配置 SSH Key（推荐）

使用 SSH Key 可以免去每次输入用户名密码的麻烦。

**Windows PowerShell:**
```powershell
# 1. 检查是否已有 SSH Key
cat ~/.ssh/id_rsa.pub

# 2. 如果没有，生成新的 SSH Key
ssh-keygen -t rsa -C "你的邮箱@example.com"

# 3. 一路回车，使用默认位置和空密码
```

**3. 在 GitHub 网页添加 SSH Key：**
1. 点击右上角头像 → **Settings**
2. 左侧菜单找到 **SSH and GPG keys**
3. 点击 **New SSH key**
4. Title 随便填（如 "我的电脑"）
5. Key 框里粘贴 `~/.ssh/id_rsa.pub` 的全部内容
6. 点击 **Add SSH key**

**验证是否成功：**
```bash
ssh -T git@github.com
# 应该看到: Hi 用户名! You've successfully authenticated...
```

### 1.3 GitHub Token vs SSH Key

| 方式 | 用途 | 安全性 |
|------|------|--------|
| **SSH Key** | 推送代码到自己的仓库 | ✅ 安全，本地保存 |
| **Personal Access Token (PAT)** | API 调用、CI/CD、第三方工具 | ✅ 安全，按需生成 |
| **用户名 + 密码** | 已废弃 ❌ | ❌ 不安全，已不支持 |

**生成 GitHub Token：**
1. GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. 点击 **Generate new token**
3. 设置名称、过期时间
4. 勾选 `repo`（完全控制私有仓库）和 `workflow`
5. 点击 Generate
6. **立即复制保存**，刷新页面后无法再查看

---

## 2. 贡献代码的标准流程（Fork + PR）

> 这是 GitHub 开源项目贡献的标准方式，称为 "Fork & Pull Request"

### 2.1 Fork 项目

1. 在 GitHub 上打开目标项目页面（如 https://github.com/yanzhiti/yanzhiti）
2. 点击右上角 **Fork** 按钮
3. 选择你的账号，等待创建完成
4. 你会看到页面标题变成 `你的用户名/yanzhiti`

### 2.2 克隆你 Fork 的仓库到本地

```bash
# 使用 SSH（推荐）
git clone git@github.com:你的用户名/yanzhiti.git
cd yanzhiti

# 或使用 HTTPS
git clone https://github.com/你的用户名/yanzhiti.git
cd yanzhiti
```

### 2.3 添加上游仓库（保持同步）

```bash
# 添加上游仓库的远程地址
git remote add upstream https://github.com/yanzhiti/yanzhiti.git

# 验证远程仓库配置
git remote -v
# 应该看到:
# origin    git@github.com:你的用户名/yanzhiti.git (fetch)
# origin    git@github.com:你的用户名/yanzhiti.git (push)
# upstream  https://github.com/yanzhiti/yanzhiti.git (fetch)
# upstream  https://github.com/yanzhiti/yanzhiti.git (push)
```

### 2.4 创建功能分支

> ⚠️ **重要**：永远不要在 main 分支上直接修改！

```bash
# 创建新分支
git checkout -b feature/你的功能名称

# 或创建修复 bug 的分支
git checkout -b fix/修复什么问题

# 查看所有分支
git branch -a
```

### 2.5 修改代码并提交

```bash
# 查看修改了哪些文件
git status

# 查看具体改动
git diff

# 添加要提交的文件
git add src/你的修改文件.py

# 或者添加所有改动
git add .

# 提交（写清楚提交信息）
git commit -m "fix: 修复了 XXX 问题"

# 提交信息规范示例：
# feat: 添加了新的用户登录功能
# fix: 修复了登录页面闪退的问题
# docs: 更新了 README 说明
# refactor: 重构了 XXX 代码
# test: 添加了 XXX 的单元测试
```

### 2.6 推送到你的 Fork 仓库

```bash
# 推送当前分支到你的 origin
git push origin feature/你的功能名称
```

### 2.7 创建 Pull Request (PR)

1. 在 GitHub 上打开你的 Fork 仓库页面
2. 你会看到一条黄色的 **"Compare & pull request"** 提示，点击它
3. 填写 PR 描述：
   - **Title**：简短描述你的改动
   - **Description**：详细说明改了什么、为什么改、怎么测试的
4. 检查 diff 确保改动正确
5. 点击 **Create pull request**

### 2.8 同步上游仓库的最新代码

```bash
# 切换到 main 分支
git checkout main

# 拉取上游最新代码
git fetch upstream
git merge upstream/main

# 推送到你的 origin
git push origin main
```

---

## 3. 日常开发中的常用 Git 操作

### 3.1 查看状态和历史

```bash
git status                    # 查看当前状态
git log --oneline             # 查看提交历史（一行一条）
git log --graph --oneline     # 查看分支图
git show 提交ID               # 查看某次提交的具体改动
```

### 3.2 分支操作

```bash
git branch                      # 查看本地分支
git branch -a                  # 查看所有分支（包括远程）
git checkout 分支名             # 切换分支
git checkout -b 新分支名        # 创建并切换新分支
git branch -d 分支名           # 删除分支
git push origin --delete 分支名 # 删除远程分支
```

### 3.3 撤销操作

```bash
# 撤销工作区的改动（未 git add）
git checkout -- 文件名
# 或
git restore 文件名

# 撤销 git add（取消暂存）
git reset HEAD 文件名

# 撤销最近的提交（保留代码改动）
git reset --soft HEAD~1

# 撤销最近的提交（不保留代码改动）
git reset --hard HEAD~1
```

### 3.4 暂存工作

```bash
git stash           # 暂存当前工作（临时保存）
git stash pop       # 恢复暂存的工作
git stash list      # 查看所有暂存
git stash drop      # 删除暂存
```

### 3.5 标签操作（版本发布）

```bash
git tag v1.0.0              # 创建轻量标签
git tag -a v1.0.0 -m "版本1发布"  # 创建附注标签
git push origin v1.0.0      # 推送标签到远程
git push origin --tags      # 推送所有标签
```

---

## 4. 参与 Issues 讨论

### 4.1 搜索现有 Issues

在项目页面点击 **Issues** 标签：
- 使用 **Search** 搜索关键词
- 使用 **Labels** 筛选（如 "bug", "enhancement", "help wanted"）
- 使用 **Milestones** 查看版本计划

### 4.2 创建新 Issue

1. 点击 **New issue** 按钮
2. 选择 Issue 类型：
   - **Bug report** - 报告 Bug
   - **Feature request** - 请求新功能
   - **Question** - 提问
3. 填写格式：
   ```
   ## 问题描述
   [清晰描述遇到的问题]

   ## 复现步骤
   1. 打开...
   2. 点击...
   3. 出现...

   ## 预期行为
   [你期望发生什么]

   ## 实际行为
   [实际发生了什么]

   ## 环境信息
   - OS: Windows 10
   - Python: 3.11
   - 版本: 2.2.0
   ```

### 4.3 参与讨论

- 在 Issue 下留言，提出问题或解决方案
- 点击 **Subscribe** 关注 Issue 动态
- 对有帮助的评论点 👍 表示支持

---

## 5. 项目维护者操作

### 5.1 管理 Pull Request

1. 在仓库页面点击 **Pull requests** 标签
2. 点击某个 PR 查看详情
3. 可以在 PR 中：
   - 查看代码改动 (Files changed)
   - 添加评论 (Add a comment)
   - 批准 PR (Approve)
   - 请求修改 (Request changes)
   - 合并 PR (Merge)

### 5.2 合并策略

| 合并方式 | 命令 | 适用场景 |
|---------|------|---------|
| **Merge** | 保留所有提交历史 | 多人协作，完整历史 |
| **Squash** | 压缩为一条提交 | 清理历史，保持整洁 |
| **Rebase** | 变基到最新分支 | 线性历史 |

### 5.3 添加贡献者

1. Settings → Manage access → Invite a collaborator
2. 输入贡献者的 GitHub 用户名
3. 贡献者接受邀请后，可以直接 push 到仓库

### 5.4 设置分支保护

1. Settings → Branches → Add branch protection rule
2. 设置 `main` 分支保护：
   - ✅ Require pull request reviews before merging
   - ✅ Require status checks to pass before merging
   - ✅ Include administrators
   - ❌ Allow force pushes（建议禁用）

---

## 6. 常见问题解答

### Q1: 忘记了 GitHub 密码怎么办？

访问 https://github.com/password_reset 按流程重置。

### Q2: SSH Key 不生效，提示权限拒绝？

```bash
# 测试 SSH 连接
ssh -T git@github.com

# 如果失败，检查 SSH Agent 是否运行
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_rsa
```

### Q3: GitHub 页面打不开或很慢？

- 使用镜像站：https://hub.fastgit.xyz/ （GitHub 的镜像）
- 或使用 VPN/代理

### Q4: 如何删除我的 Fork？

在 GitHub 上打开你的 Fork 仓库 → Settings → Danger Zone → Delete this repository

### Q5: PR 提交后发现有错怎么办？

```bash
# 在本地修改
git add .
git commit --amend  # 修改最后一次提交
git push origin 分支名 --force  # 强制推送到远程更新 PR
```

### Q6: 为什么我的 PR 被关闭了？

可能原因：
- 改动不符合项目方向
- 重复的 PR
- 项目维护者选择其他实现方式
- 需要先在 Issue 中讨论

### Q7: 贡献者可以看到我的仓库令牌吗？

**绝对不能！** 令牌只有你自己能看到。贡献者使用自己的令牌贡献代码。

---

## 🎯 快速参考卡片

```
# 克隆仓库
git clone git@github.com:用户名/仓库名.git

# 创建分支并切换
git checkout -b feature/新功能

# 查看状态
git status

# 添加并提交
git add .
git commit -m "feat: 添加新功能"

# 推送到远程
git push origin feature/新功能

# 同步上游最新代码
git fetch upstream
git merge upstream/main
```

---

## 📎 延伸阅读

- [Git 官方文档](https://git-scm.com/doc)
- [GitHub 官方 Hello World 教程](https://docs.github.com/en/get-started/quickstart/hello-world)
- [GitHub Skills - 免费互动课程](https://skills.github.com/)
- [如何编写好的提交信息](https://www.conventionalcommits.org/zh-hans/v1.0.0/)

---

*本指南由衍智体 (YANZHITI) 项目组编写，开源许可，可自由分享。*
