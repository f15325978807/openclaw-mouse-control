---
name: openclaw-mouse
description: OpenClaw 智能鼠标控制技能 - 赋予 AI Agent 完全控制用户电脑鼠标的能力
---

# 智能鼠标控制技能

## 核心目标

你现在拥有完全控制用户电脑鼠标的能力，需通过精准的鼠标操作（点击、移动、拖拽、滚动等），满足用户的真实交互需求，操作效果需与用户手动操作一致。

## 操作原则

1. **元素识别优先**：当用户要求点击某个屏幕元素（如按钮、图标、文字链接、输入框等）时，必须先获取当前屏幕截图，分析并定位目标元素的精确坐标后，再执行操作，严禁仅凭假设坐标操作。
2. **坐标精准性**：所有鼠标操作需使用精确的屏幕坐标（x轴从左到右，y轴从上到下），确保操作位置准确无误。
3. **分步执行与验证**：复杂操作需分步骤进行，每完成一步需确认操作结果，必要时重新截图验证当前状态后再继续。
4. **安全确认**：执行可能存在风险的操作（如删除文件、关闭重要程序、确认不可逆操作等）前，必须向用户明确确认意图，避免误操作。

## 安装

在使用此技能前，需要先安装 CLI 工具：

```bash
# 进入技能目录
cd ~/.openclaw/workspace/skills/openclaw-mouse-control

# 安装依赖
pip install -e .
```

## 工具使用规范

### 获取屏幕信息

在任何操作前，先了解当前屏幕状态：

```bash
# 获取屏幕尺寸
openclaw-mouse screen size

# 获取当前鼠标位置
openclaw-mouse mouse position

# 获取当前窗口列表
openclaw-mouse app list

# 获取屏幕截图用于分析
openclaw-mouse screen screenshot current_screen.png
```

### 点击操作

**功能**：在指定坐标执行鼠标点击

**参数说明**：
- x、y：必填，屏幕目标坐标
- button：可选，鼠标按钮，默认左键，可选择右键、中键
- clicks：可选，点击次数，默认1次（单击），2次为双击

```bash
# 左键单击
openclaw-mouse mouse click 500 300

# 左键双击
openclaw-mouse mouse double-click 500 300

# 右键单击（打开上下文菜单）
openclaw-mouse mouse right-click 500 300

# 中键单击
openclaw-mouse mouse middle-click 500 300

# 在当前鼠标位置单击
openclaw-mouse mouse click
```

### 移动鼠标

**功能**：将鼠标指针移动到指定坐标

**参数说明**：
- x、y：必填，目标坐标
- duration：可选，移动持续时间（秒），默认0.2秒，值越大移动越平滑

```bash
# 快速移动到目标位置
openclaw-mouse mouse move 960 540

# 平滑移动（动画效果）
openclaw-mouse mouse move 960 540 --duration 0.5
```

### 滚动页面

**功能**：在当前鼠标位置或指定坐标滚动页面

**参数说明**：
- clicks：必填，滚动格数，正数向上滚动，负数向下滚动
- x、y：可选，滚动位置坐标，默认为当前鼠标位置

```bash
# 向上滚动5格
openclaw-mouse mouse scroll 5

# 向下滚动5格
openclaw-mouse mouse scroll -5

# 在指定位置向上滚动
openclaw-mouse mouse scroll 3 800 600
```

### 拖拽操作

**功能**：从起点坐标拖拽到终点坐标

**参数说明**：
- x、y：必填，拖拽终点坐标
- duration：可选，拖拽持续时间（秒），默认0.5秒
- button：可选，拖拽使用的鼠标按钮，默认左键

```bash
# 拖拽到目标位置
openclaw-mouse mouse drag 800 600

# 慢速拖拽（更精确）
openclaw-mouse mouse drag 800 600 --duration 1.0
```

### 截图分析

**功能**：获取当前屏幕完整截图，用于分析屏幕内容和定位元素

```bash
# 截图当前活动窗口
openclaw-mouse screen screenshot current_screen.png

# 截图指定区域 (x, y, width, height)
openclaw-mouse screen screenshot region.png --region "100,100,500,400"

# 获取屏幕尺寸
openclaw-mouse screen size

# 检查坐标是否在屏幕内
openclaw-mouse screen on-screen 500 300
```

### 键盘操作

```bash
# 输入文本
openclaw-mouse keyboard write "Hello World"

# 按键
openclaw-mouse keyboard press enter

# 快捷键
openclaw-mouse keyboard hotkey "ctrl,c"

# 按住键
openclaw-mouse keyboard keydown shift

# 释放键
openclaw-mouse keyboard keyup shift
```

### 消息对话框

```bash
# 显示警告
openclaw-mouse message alert "操作完成！"

# 确认对话框
openclaw-mouse message confirm "确定要删除吗？"

# 输入对话框
openclaw-mouse message prompt "请输入你的名字："
```

### 应用控制

```bash
# 打开应用
openclaw-mouse app open notepad

# 聚焦窗口
openclaw-mouse app focus "记事本"

# 列出所有窗口
openclaw-mouse app list
```

## 完整工作流程示例

### 示例 1：打开并操作应用程序

```bash
# 步骤1: 打开应用程序
openclaw-mouse app open notepad

# 步骤2: 等待应用启动，列出窗口确认
openclaw-mouse app list

# 步骤3: 聚焦到应用程序窗口
openclaw-mouse app focus "Notepad"

# 步骤4: 输入文本
openclaw-mouse keyboard write "Hello World"
```

### 示例 2：查找并点击按钮

```bash
# 步骤1: 获取屏幕截图
openclaw-mouse screen screenshot analysis.png

# 步骤2: 查看屏幕尺寸
openclaw-mouse screen size

# 步骤3: 移动鼠标到目标位置并点击
openclaw-mouse mouse move 500 300
openclaw-mouse mouse click
```

### 示例 3：填写表单

```bash
# 点击第一个输入框
openclaw-mouse mouse click 300 200

# 输入内容
openclaw-mouse keyboard write "张三"

# 按 Tab 跳到下一个字段
openclaw-mouse keyboard press tab

# 输入邮箱
openclaw-mouse keyboard write "zhangsan@example.com"

# 再次按 Tab 跳到下一个字段
openclaw-mouse keyboard press tab

# 输入电话号码
openclaw-mouse keyboard write "13800138000"

# 按 Enter 提交表单
openclaw-mouse keyboard press enter
```

### 示例 4：拖拽操作（文件移动）

```bash
# 步骤1: 获取屏幕信息
openclaw-mouse screen size

# 步骤2: 移动鼠标到拖拽起点
openclaw-mouse mouse move 100 200

# 步骤3: 执行拖拽到终点
openclaw-mouse mouse drag 500 400 --duration 0.5
```

### 示例 5：复制粘贴操作

```bash
# 全选
openclaw-mouse keyboard hotkey "ctrl,a"

# 复制
openclaw-mouse keyboard hotkey "ctrl,c"

# 移动鼠标到目标位置
openclaw-mouse mouse click 500 600

# 粘贴
openclaw-mouse keyboard hotkey "ctrl,v"
```

## 注意事项

1. **永远不要假设屏幕坐标**，必须通过截图分析或用户明确告知获取准确坐标。
2. **若一次操作未成功**，先截图查看当前状态，再决定下一步操作，避免重复无效操作。
3. **支持多显示器环境**，但操作前需用户明确说明在哪个显示器上执行。
4. **操作时需模拟人类操作速度**，适当控制操作间隔，避免操作过快导致系统无响应。
5. PyAutoGUI 有紧急停止功能：将鼠标快速移动到屏幕角落（四个角之一）会立即停止所有操作。

## 安全考虑

1. **危险操作需确认**：在执行删除文件、关闭程序、格式化等不可逆操作前，必须使用确认对话框向用户确认。
2. **敏感信息保护**：不要在日志中记录或暴露用户的密码、银行卡号等敏感信息。
3. **分步验证**：对于复杂的多步骤操作，每一步都要验证结果后再继续。

## 常见错误处理

### 窗口未找到

```bash
# 列出所有可见窗口，找到正确的窗口标题
openclaw-mouse app list

# 使用模糊匹配重新聚焦
openclaw-mouse app focus "部分窗口标题"
```

### 坐标超出屏幕

```bash
# 获取屏幕尺寸
openclaw-mouse screen size

# 检查坐标是否在屏幕内
openclaw-mouse screen on-screen 1500 900
```

### 点击位置偏移

```bash
# 先移动到目标位置查看
openclaw-mouse mouse move 500 300

# 确认位置正确后再点击
openclaw-mouse mouse click
```

## 性能优化建议

1. **减少不必要的截图**：只在对操作结果存疑时才截图验证。
2. **使用键盘快捷键**：优先使用 `openclaw-mouse keyboard hotkey` 而不是多次鼠标点击。
3. **批量文本输入**：使用一次 `keyboard write` 输入完整文本，而不是多次调用。
4. **选择合适的拖拽速度**：精确操作使用 `--duration 1.0`，快速操作使用默认速度。
