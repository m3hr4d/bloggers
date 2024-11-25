import os
import sys

def test_python_path():
    print("Current working directory:", os.getcwd())
    print("\nPython path:")
    for path in sys.path:
        print(f"- {path}")
    
    print("\nEnvironment variables:")
    print(f"PYTHONPATH: {os.getenv('PYTHONPATH')}")
    print(f"FLASK_APP: {os.getenv('FLASK_APP')}")
    print(f"FLASK_ENV: {os.getenv('FLASK_ENV')}")

if __name__ == "__main__":
    test_python_path()
