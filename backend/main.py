import subprocess 
import sys 
def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py [start[stop]]")
        sys.exit(1)
    command = sys.argv[1]
    if command == "start":
        subprocess.run(["./scripts/activate.sh"])
    elif command == "stop":
        subprocess.run(["./scripts/deactivate.sh"])
    else:
        print(f"Unknown command: {command}") 


if __name__ == "__main__":
    main()
