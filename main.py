"""Write the finished news image to /output/entry.png."""
import pathlib

SOURCE = pathlib.Path(__file__).resolve().parent / "assets" / "entry.png"
TARGET = pathlib.Path("/output/entry.png")


def main():
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_bytes(SOURCE.read_bytes())


if __name__ == "__main__":
    main()
