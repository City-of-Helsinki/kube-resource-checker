import os
from dotenv import load_dotenv

from prometheus.manager import Manager
from arguments.args import Args
import auth.dex


args = Args()

load_dotenv(args.getEnvFileName())

range=os.environ.get('RANGE', '1w')

hostapi=os.environ.get('HOSTAPI')

print (f"Collect data from '{hostapi}' on range '{range}'")

session = auth.dex.getSession()

manager = Manager(session, hostapi, range)
manager.collectData()
manager.printResults()
#manager.analyse()
manager.printBalance()
manager.outputHtlm()
