from rich import print
from argparse import ArgumentParser, Namespace


def main(args: Namespace):
    print(args)


if __name__ == "__main__":
    parser = ArgumentParser(prog="Elsa", description="Quiz Client", epilog="Let it go, let it go")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-s", "--simulation", action="store_true", help="Enable simulation mode")
    group.add_argument("-i", "--interactive", action="store_true", help="Enable interactive mode")
    parser.add_argument("-v", "--verbose", action="store_true", help="")

    args = parser.parse_args()
    main(args)
