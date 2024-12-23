import random
import time
from argparse import ArgumentParser, Namespace

from redis import ConnectionPool, StrictRedis
from rich import print

r = StrictRedis(connection_pool=ConnectionPool().from_url("redis://localhost:6379"))


def simulate():
    while True:
        for i in range(1, 20):
            r.zincrby("quiz_1", value=f"player{i}", amount=random.randint(-10, 30))
        time.sleep(3)


def main(args: Namespace):
    if args.simulation:
        simulate()


if __name__ == "__main__":
    parser = ArgumentParser(prog="Elsa", description="Quiz Client", epilog="Let it go, let it go")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-s", "--simulation", action="store_true", help="Enable simulation mode")
    group.add_argument("-i", "--interactive", action="store_true", help="Enable interactive mode")
    parser.add_argument("-v", "--verbose", action="store_true", help="")
    args = parser.parse_args()

    main(args)
