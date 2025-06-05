import logging

from .bot import TsundereBot

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")


def main():
    TsundereBot().run()


if __name__ == "__main__":
    main()