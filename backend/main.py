import subprocess 
from pathlib import Path
import os  

def main():
    dir = Path(__file__).parent.absolute()
    venv = dir / ".venv" / "bin" / "python"
    subprocess.run([str(venv), "-m", "uvicorn", "app.main:app", "--reload"])   
    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n Server stopped")
        exit(0)

