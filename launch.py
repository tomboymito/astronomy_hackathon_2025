import threading
import sys
import signal
import uvicorn
from PyQt5.QtWidgets import QApplication
from frontend.front import MainWindow
import run  # Import the FastAPI app from run.py

def run_backend():
    """Run the FastAPI backend server using uvicorn."""
    uvicorn.run(run.app, host="0.0.0.0", port=8000, log_level="info")

def main():
    # Start backend server in a separate thread
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()

    # Start the PyQt5 frontend GUI in the main thread
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # Handle graceful shutdown on SIGINT (Ctrl+C)
    def signal_handler(sig, frame):
        print("Shutting down...")
        app.quit()

    signal.signal(signal.SIGINT, signal_handler)

    exit_code = app.exec_()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
