# tiktok-mcp
MCP for download video from tiktok

## Server Composition

### `import_server`
- Chỉ có thể import `tools`, `resources` và `prompt` không thể import `custom_route`
- Sao chép tĩnh: Sao chép các thành phần tại thời điểm import => những chỉnh sửa sau import sẽ không được update
- Hiệu suất cao hơn do đã được sao chép tại thời điểm chạy
- Có thể thêm prefix để phân biệt giữa các component

=> Sử dụng khi các thành phần đã được xây dựng xong (không có thay đổi trong quá trình chạy). Yêu cầu hiệu suất cao.

```python
# weather_server.py
from fastmcp import FastMCP

weather_server = FastMCP(name="Weather")

@weather_server.tool()
def get_forecast(city: str) -> str:
    return f"Thời tiết ở {city} được dự báo là nắng."

# calculator_server.py
from fastmcp import FastMCP

calculator_server = FastMCP(name="Calculator")

@calculator_server.tool()
def add(a: int, b: int) -> int:
    return a + b

# main_server.py
from fastmcp import FastMCP
from weather_server import weather_server
from calculator_server import calculator_server

main_server = FastMCP(name="Main")

# Import tĩnh các server con với tiền tố
main_server.import_server(weather_server, prefix="weather")
main_server.import_server(calculator_server, prefix="calc")

if __name__ == "__main__":
    main_server.run()
```

### dynamic mount

- Thay vì copy như `import_server`, phương pháp này sẽ tạo uỷ quyền cho subserver tại thời điểm chạy
- Dynamic mount => tạo liên kết động cho subserver (nếu 1 subserver bị lỗi thì các chức năng trên mainserver cũng không hoạt động)
- Latency lớn hơn `import_server`

```python
# main_server_mounted.py
from fastmcp import FastMCP
from weather_server import weather_server
from calculator_server import calculator_server

main_server = FastMCP(name="MainMounted")

# Mount động các server con với tiền tố
main_server.mount(weather_server, prefix="weather")
main_server.mount(calculator_server, prefix="calc")

if __name__ == "__main__":
    main_server.run()
```
