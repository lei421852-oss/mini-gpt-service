# mini-gpt-service

## 项目目标

将已经训练完成的 character-level GPT 模型封装为 FastAPI 推理服务，为后续模型加载与文本生成接口提供清晰、轻量的工程基础。

## 当前状态

项目处于初始化阶段。目前仅包含标准 Python 项目结构、基础依赖配置、FastAPI 应用入口和健康检查接口；尚未实现模型加载、推理流程或业务逻辑。

## 后续模块规划

- `app/api/`：HTTP API 路由。
- `app/core/`：应用级基础配置。
- `app/services/`：推理服务编排。
- `app/model/`：模型加载与推理封装。
- `configs/`：项目配置文件。
- `tests/`：自动化测试。

## 本地运行

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

启动后可访问 `http://127.0.0.1:8000/health` 检查服务状态。

