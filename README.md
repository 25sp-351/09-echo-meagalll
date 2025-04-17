# Threaded Echo & Web Server in Python

Basic threaded TCP echo server and a simple HTTP server in Python. 

It includes:
- echo.py: A multi-threaded **echo server** with line buffering and a verbose mode
- web_test.py: A simple **HTTP server** that can be tested in browser with the link: http://localhost:2345/
- mul_thread_test.py: A **client test script** to simulate partial and multi-line messages during echo.py

---

### `More Info. on echo.py`
A multi-threaded TCP echo server that:
- Handles multiple clients at the same time
- Supports partial and multi-line reads
- Includes a `-v` flag to enable verbose logging



```bash
python3 echo.py [-v]
