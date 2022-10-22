"""调试项目"""

from os import environ
from uvicorn import run

if __name__ == "__main__":
    # 环境变量
    with open(__file__.replace("dev.py", ".env")) as env:
        env_t = env.read()
        for i in env_t.split("\n"):
            key, val = i.split("=")
            environ[key] = val

    # trace/info/warning/error
    run("app:app", log_level="info", reload=True)
