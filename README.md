# MCP 服务器项目

## 📖 项目简介

这是一个基于 **Model Context Protocol (MCP)** 的 Python 服务器项目。MCP 是一个用于连接大型语言模型与外部数据源和工具的开放协议。本项目实现了一个简单的 MCP 服务器，提供了基础的工具和资源功能。

## ✨ 主要功能

- 🔧 **工具集成**: 提供多个实用工具函数
  - `hello`: 个性化问候工具
  - `add_numbers`: 数学加法计算器
- 📚 **资源管理**: 动态资源访问
  - `greeting`: 个性化问候语资源
- 🚀 **FastMCP**: 基于现代 Python 异步框架构建
- 📡 **标准通信**: 支持 stdio 传输协议

## 🛠️ 技术栈

- **Python 3.8+**: 主要编程语言
- **MCP 1.9.1**: Model Context Protocol 核心库
- **FastMCP**: 快速 MCP 服务器框架
- **Pydantic**: 数据验证和序列化
- **Uvicorn**: ASGI 服务器

## 📦 安装说明

### 1. 克隆项目

```bash
git clone <your-repository-url>
cd <project-directory>
```

### 2. 创建虚拟环境

```bash
# 创建虚拟环境
python -m venv mcp-env

# 激活虚拟环境
# Windows
mcp-env\Scripts\activate
# macOS/Linux
source mcp-env/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

## 🚀 使用方法

### 启动服务器

```bash
# 方法1: 直接运行主服务器
python src/server.py

# 方法2: 运行测试脚本（验证环境）
python test.py
```

### 测试环境

运行测试脚本来验证 MCP 环境是否正确配置：

```bash
python test.py
```

预期输出：
```
测试Python环境
MCP导入成功
FastMCP实例创建成功
```

## 📋 API 文档

### 工具 (Tools)

#### 1. hello
**描述**: 一个简单的问候工具

**参数**:
- `name` (string): 要问候的名字

**返回值**: 
- `string`: 问候消息

**示例**:
```python
# 输入: name="张三"
# 输出: "你好，张三！"
```

#### 2. add_numbers
**描述**: 加法计算器

**参数**:
- `a` (int): 第一个数字
- `b` (int): 第二个数字

**返回值**:
- `int`: 两个数字的和

**示例**:
```python
# 输入: a=5, b=3
# 输出: 8
```

### 资源 (Resources)

#### greeting://{name}
**描述**: 获取个性化问候语

**参数**:
- `name` (string): 用户名字

**返回值**:
- `string`: 个性化的问候消息

**示例**:
```python
# 输入: name="李四"
# 输出: "欢迎，李四！这是一个动态资源示例。"
```

## 📁 项目结构

```
.
├── README.md              # 项目说明文档
├── requirements.txt       # Python 依赖包列表
├── test.py               # 环境测试脚本
├── src/                  # 源代码目录
│   └── server.py         # MCP 服务器主文件
├── mcp-env/              # Python 虚拟环境
└── .git/                 # Git 版本控制
```

## 🔧 开发指南

### 添加新工具

1. 在 `src/server.py` 中添加新的工具函数：

```python
@mcp.tool()
def your_new_tool(param1: str, param2: int) -> str:
    """工具描述
    
    Args:
        param1: 参数1描述
        param2: 参数2描述
    
    Returns:
        返回值描述
    """
    try:
        # 工具逻辑实现
        result = f"处理结果: {param1} - {param2}"
        print(f"工具执行成功: {result}")  # 日志输出
        return result
    except Exception as e:
        print(f"工具执行错误: {e}")  # 错误日志
        raise
```

### 添加新资源

```python
@mcp.resource("your-resource://{param}")
def get_your_resource(param: str) -> str:
    """资源描述
    
    Args:
        param: 资源参数
    
    Returns:
        资源内容
    """
    try:
        # 资源获取逻辑
        content = f"资源内容: {param}"
        print(f"资源获取成功: {content}")  # 日志输出
        return content
    except Exception as e:
        print(f"资源获取错误: {e}")  # 错误日志
        raise
```

## 🐛 故障排除

### 常见问题

1. **导入错误**: 确保已激活虚拟环境并安装所有依赖
2. **端口占用**: 检查是否有其他服务占用相同端口
3. **权限问题**: 确保有足够的文件读写权限

### 调试模式

启用详细日志输出：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 贡献指南

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 📧 Email: your-email@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/your-username/your-repo/issues)

## 🙏 致谢

感谢以下开源项目的支持：

- [Model Context Protocol](https://github.com/modelcontextprotocol/python-sdk)
- [FastMCP](https://github.com/jlowin/fastmcp)
- [Pydantic](https://github.com/pydantic/pydantic)

---

⭐ 如果这个项目对您有帮助，请给它一个星标！
