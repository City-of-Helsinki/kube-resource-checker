import argparse
import arguments.version

from datetime import datetime


class Args:
    def __init__(self):
        # Initialize parser
        self.parser = argparse.ArgumentParser()

        # Adding optional argument
        self.parser.add_argument(
            "-e",
            "--environmentType",
            default="qa",
            help="Environment type refer to .env file extension. Default value is qa",
        )
        self.parser.add_argument(
            "-d", "--debug", help="Enable debug prints", action="store_true"
        )

        # Read arguments from command line
        self.args = self.parser.parse_args()

    def getEnvFileName(self):
        basename = "./.env"
        return f"{basename}.{self.args.environmentType}"

    def getInfo(self):
        return f"{self.parser.prog} version {arguments.version.version}  on {datetime.now()}"
