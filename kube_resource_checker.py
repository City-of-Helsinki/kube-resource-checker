import os
from dotenv import load_dotenv

from prometheus.manager import Manager
from arguments.args import Args
import auth.dex


args = Args()

load_dotenv(args.getEnvFileName())

hostapi = os.environ.get("HOSTAPI")
range = os.environ.get("RANGE", "1w")

session = auth.dex.getSession()

infoMessage = (
    f"{args.getInfo()}\nMetrics is collected from '{hostapi}' on range '{range}'"
)
print(infoMessage)

manager = Manager(session, hostapi, range)
manager.collectData()

if args.args.debug:
    manager.printResults()

print("Summary:")
manager.printBalance()
manager.outputHtlm(infoMessage)
