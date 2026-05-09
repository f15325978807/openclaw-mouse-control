# OpenClaw Mouse Control Skill

🎯 **OpenClaw 智能鼠标控制技能** - 赋予 AI Agent 完全控制用户电脑鼠标的能力

## 📋 简介

这是一个专为 OpenClaw AI Agent 设计的鼠标控制技能，基于 [desktop-agent](https://github.com/patrickporto/desktop-agent) 实现。通过这个技能，AI Agent 可以执行精准的鼠标操作，包括点击、移动、拖拽、滚动等，满足用户的各种桌面交互需求。

## ✨ 核心特性

- 🖱️ **精准鼠标控制** - 点击、移动、拖拽、滚动
- 📸 **智能屏幕分析** - 截图、图像识别、OCR 文字定位
- ⌨️ **完整键盘支持** - 文字输入、快捷键、组合键
- 📱 **应用控制** - 打开应用、切换窗口
- 🛡️ **安全确认机制** - 危险操作前自动确认
- 🔍 **元素智能识别** - 通过图像或文字定位屏幕元素

## 🚀 快速开始

### 安装依赖

在 OpenClaw 中安装此技能前，需要确保已安装 `desktop-agent` CLI：

```bash
# 使用 pipx 安装（推荐）
pipx install desktop-agent

# 或使用 pip 安装
pip install desktop-agent

# 或直接使用 uvx 运行（无需安装）
uvx desktop-agent --help
```

### 在 OpenClaw 中添加技能

```bash
# 通过 AI Agent 命令添加
npx skills add patrickporto/desktop-agent
```

## 📖 使用方法

### 基本操作流程

**重要原则**：永远先观察，再行动！

#### 1. 获取屏幕信息

```bash
# 查看屏幕尺寸
desktop-agent screen size

# 查看当前鼠标位置
desktop-agent mouse position

# 查看所有窗口
desktop-agent app list
```

#### 2. 截图分析

```bash
# 截取当前活动窗口
desktop-agent screen screenshot current.png --active

# 截取指定窗口
desktop-agent screen screenshot window.png --window "窗口标题"

# 定位屏幕上图像
desktop-agent screen locate-center button.png

# OCR 定位文字坐标
desktop-agent screen locate-text-coordinates "确定" --active
```

#### 3. 执行鼠标操作

```bash
# 单击
desktop-agent mouse click 500 300

# 双击
desktop-agent mouse double-click 500 300

# 右键单击
desktop-agent mouse right-click 500 300

# 移动鼠标
desktop-agent mouse move 960 540 --duration 0.5

# 滚动页面（正数向上，负数向下）
desktop-agent mouse scroll 5

# 拖拽
desktop-agent mouse drag 800 600 --duration 0.5
```

#### 4. 键盘操作

```bash
# 输入文本
desktop-agent keyboard write "Hello World"

# 按键
desktop-agent keyboard press enter

# 快捷键
desktop-agent keyboard hotkey "ctrl,c"
```

## 💡 实用示例

### 示例 1：自动填写表单

```bash
# 点击第一个输入框
desktop-agent mouse click 300 200
desktop-agent keyboard write "张三"

# Tab 跳到下一个字段
desktop-agent keyboard press tab
desktop-agent keyboard write "zhangsan@example.com"

# Tab 跳到下一个字段
desktop-agent keyboard press tab
desktop-agent keyboard write "13800138000"

# 提交
desktop-agent keyboard press enter
```

### 示例 2：查找并点击按钮

```bash
# 1. 截图分析
desktop-agent screen screenshot current.png --active

# 2. OCR 定位按钮文字
desktop-agent screen locate-text-coordinates "提交" --active

# 3. 点击返回的坐标
desktop-agent mouse click <返回的x> <返回的y>
```

### 示例 3：文件拖拽

```bash
# 移动到文件位置
desktop-agent mouse move 100 200

# 执行拖拽到目标位置
desktop-agent mouse drag 500 400 --duration 0.5
```

### 示例 4：复制粘贴

```bash
# 全选
desktop-agent keyboard hotkey "ctrl,a"

# 复制
desktop-agent keyboard hotkey "ctrl,c"

# 移动鼠标到目标位置
desktop-agent mouse click 500 600

# 粘贴
desktop-agent keyboard hotkey "ctrl,v"
```

## 🛡️ 安全机制

### 操作前确认

对于危险操作，系统会提示确认：

```bash
# 删除文件前会弹出确认对话框
desktop-agent message confirm "确定要删除这些文件吗？"
```

### PyAutoGUI 紧急停止

将鼠标快速移动到屏幕任意角落即可立即停止所有自动化操作。

## ⚠️ 注意事项

1. **永远不要假设坐标** - 必须通过截图分析获取准确坐标
2. **操作失败时重试** - 先截图查看状态，再决定下一步
3. **多显示器支持** - 需明确指定在哪个显示器上操作
4. **模拟人类速度** - 适当控制操作间隔，避免系统无响应
5. **分步验证** - 复杂操作每步都要验证结果

## 🔧 故障排除

### 窗口未找到

```bash
# 列出所有窗口找到正确标题
desktop-agent app list
```

### 图像识别失败

```bash
# 调整识别精度
desktop-agent screen locate-center button.png --confidence 0.6
```

### 坐标偏差

```bash
# 先移动到目标位置确认
desktop-agent mouse move 500 300
# 确认无误后再点击
desktop-agent mouse click
```

## 📚 相关资源

- [desktop-agent GitHub](https://github.com/patrickporto/desktop-agent)
- [PyAutoGUI 文档](https://pyautogui.readthedocs.io/)
- [OpenClaw 官方文档](https://openclaw.dev/)

## 📝 版本历史

- **v1.0.0** (2024) - 初始版本，支持完整的鼠标、键盘、屏幕控制功能

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

---

**享受智能化的桌面自动化体验！** 🎉
