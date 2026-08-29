import sys
import time


def main():
    if len(sys.argv) < 2:
        print("Usage: case5_input_dependent.py <integer>")
        raise SystemExit(1)

    try:
        value = int(sys.argv[1])
    except ValueError:
        print("Input must be an integer.")
        raise SystemExit(1)

    if value > 0:
        print(f"Input {value} caused a normal termination.")
        return

    print(f"Input {value} triggered an infinite loop.")
    while True:
        time.sleep(0.1)


if __name__ == "__main__":
    main()
