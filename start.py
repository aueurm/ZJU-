"""
学科知识整合智能体 - 一键启动脚本
同时启动后端 FastAPI 服务和前端 Vite 开发服务器
"""
import subprocess
import sys
import os
import signal
import time
from pathlib import Path

ROOT_DIR = Path(__file__).parent
BACKEND_DIR = ROOT_DIR / "src" / "backend"
FRONTEND_DIR = ROOT_DIR / "src" / "frontend"


def check_env():
    """检查环境配置"""
    env_file = ROOT_DIR / ".env"
    if not env_file.exists():
        example = ROOT_DIR / ".env.example"
        if example.exists():
            import shutil
            shutil.copy(example, env_file)
            print("[INFO] 已从 .env.example 复制生成 .env，请填写 API 密钥后重新启动")
            sys.exit(1)
        else:
            print("[WARN] 未找到 .env 文件，部分功能可能不可用")


def start_backend():
    """启动后端服务"""
    print("[启动] 后端服务 (FastAPI) -> http://localhost:8000")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(BACKEND_DIR / "app")
    return subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
        cwd=str(BACKEND_DIR),
        env=env
    )


def start_frontend():
    """启动前端服务"""
    print("[启动] 前端服务 (Vite) -> http://localhost:5173")
    npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"
    return subprocess.Popen(
        [npm_cmd, "run", "dev"],
        cwd=str(FRONTEND_DIR)
    )


def main():
    check_env()
    processes = []
    
    try:
        backend = start_backend()
        processes.append(backend)
        time.sleep(2)
        
        frontend = start_frontend()
        processes.append(frontend)
        
        print("\n" + "="*50)
        print("  学科知识整合智能体 已启动")
        print("  前端: http://localhost:5173")
        print("  后端: http://localhost:8000")
        print("  API文档: http://localhost:8000/docs")
        print("  按 Ctrl+C 停止所有服务")
        print("="*50 + "\n")
        
        for p in processes:
            p.wait()
    except KeyboardInterrupt:
        print("\n[停止] 正在关闭所有服务...")
        for p in processes:
            p.terminate()
        for p in processes:
            p.wait()
        print("[完成] 所有服务已停止")


if __name__ == "__main__":
    main()
