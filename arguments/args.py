import argparse

 
class Args:
    def __init__(self):
        # Initialize parser
        self.parser = argparse.ArgumentParser()

            
        # Adding optional argument
        self.parser.add_argument("-e", "--environmentType", default='qa', help = "Environment type (qa|prod ,default is qa) ")
        
        # Read arguments from command line
        self.args = self.parser.parse_args()
        
    def getEnvFileName(self):
        basename = "./.env"
        return f"{basename}.{self.args.environmentType}"