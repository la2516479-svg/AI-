"""
api_server.py —— AI学习任务管理器 V2 的 HTTP 接口层
=================================================
把现有的 TaskManager（本地 Python + MySQL）包成一个 Web API。

本文件是「HTTP 第 1 天」的练习载体，每一处都对应一个知识点：
  · 客户端 / 服务器模型  → 你的浏览器 / 终端 = 客户端，这个进程 = 服务器
  · Request             → 请求行 + 请求头 + 请求体（见 _read_json_body）
  · Response            → 状态行 + 响应头 + 响应体（见 _send_json）
  · GET / POST          → 取数据用 GET，提交数据用 POST
  · 状态码              → 200 / 201 / 400 / 404 / 405 / 503

启动：在 PyCharm Terminal 运行  python api_server.py
练习：用浏览器、curl 或 Postman 访问 http://127.0.0.1:8000
"""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

from task_manager import TaskManager
from mysql.connector import Error as MySQLError


class TaskAPIHandler(BaseHTTPRequestHandler):
    server_version = "StudyManagerAPI/1.0"

    # ---- 工具：统一发送 JSON 响应（这就是 Response 的「状态行 + 头 + 体」）----
    def _send_json(self, status, payload=None):
        # status 对应「状态码」：200 成功 / 201 已创建 / 400 参数错 ...
        self.send_response(status)
        # 响应头 Header：告诉客户端返回的是 JSON、用 UTF-8 编码
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        # 响应体 Body：真正的数据
        if payload is not None:
            # default=str：遇到 datetime 等不能序列化的类型时转成字符串
            # （JSON 只能装 字符串/数字/布尔/列表/字典/null，日期不行）
            body = json.dumps(payload, ensure_ascii=False, default=str).encode("utf-8")
            self.wfile.write(body)

    def _read_json_body(self):
        """读取请求体 Body 并解析成 dict（对应 POST 提交的 JSON 数据）"""
        # 请求头里的 Content-Length 告诉我们 Body 有多少字节
        length = int(self.headers.get("Content-Length", 0) or 0)
        raw = self.rfile.read(length) if length else b"{}"
        try:
            return json.loads(raw.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return None  # 解析失败 → 交给调用方返回 400

    def _with_manager(self, fn):
        """安全打开 TaskManager；数据库连不上时返回 503（服务器不可用）"""
        try:
            mgr = TaskManager()
        except MySQLError as e:
            self._send_json(503, {"error": "数据库未连接，请先启动 MySQL", "detail": str(e)})
            return
        try:
            fn(mgr)
        finally:
            mgr.close()

    # ---- GET：取数据（查）----
    def do_GET(self):
        parsed = urlparse(self.path)
        path, qs = parsed.path, parse_qs(parsed.query)

        # 健康检查：不需要数据库，永远返回 200
        if path == "/":
            self._send_json(200, {
                "service": "AI学习任务管理器 API",
                "endpoints": {
                    "GET  /tasks": "查看全部任务（加 ?q=关键词 可搜索）",
                    "POST /tasks": "新增任务，Body 传 JSON",
                },
            })
            return

        if path == "/tasks":
            def handle(mgr):
                # ?q=xxx 存在就走搜索，否则查全部
                if "q" in qs:
                    tasks = mgr.search_tasks(qs["q"][0])
                else:
                    tasks = mgr.get_all_tasks()
                # 200 OK：请求成功，返回数据
                self._send_json(200, {"count": len(tasks), "tasks": tasks})
            self._with_manager(handle)
            return

        # 其它路径都不存在 → 404 Not Found
        self._send_json(404, {"error": "Not Found", "path": path})

    # ---- POST：提交数据（增）----
    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path != "/tasks":
            self._send_json(404, {"error": "Not Found", "path": path})
            return

        # 1) 读请求体（Body）
        data = self._read_json_body()
        if data is None:
            # 400 Bad Request：请求体不是合法 JSON
            self._send_json(400, {"error": "请求体不是合法 JSON"})
            return

        # 2) 校验必填字段
        required = ["title", "subject", "minutes", "priority"]
        if not all(k in data for k in required):
            # 400 Bad Request：缺少必填字段
            self._send_json(400, {"error": "缺少必填字段", "required": required})
            return

        # 3) 写入数据库
        def handle(mgr):
            mgr.add_task(data["title"], data["subject"], data["minutes"], data["priority"])
            # 201 Created：资源创建成功（POST 新增用 201，不是 200）
            self._send_json(201, {"msg": "任务创建成功"})
        self._with_manager(handle)

    # ---- 其它方法统一 405（留给第 2 天练习）----
    def do_DELETE(self):
        self._send_json(405, {"error": "DELETE 暂未实现，留给第 2 天"})

    def do_PUT(self):
        self._send_json(405, {"error": "PUT 暂未实现，留给第 2 天"})

    # 关掉默认访问日志的噪音
    def log_message(self, fmt, *args):
        pass


def main():
    host, port = "127.0.0.1", 8000
    server = HTTPServer((host, port), TaskAPIHandler)
    print(f"服务器已启动： http://{host}:{port}")
    print("   按 Ctrl+C 停止")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止服务器")
        server.server_close()


if __name__ == "__main__":
    main()
