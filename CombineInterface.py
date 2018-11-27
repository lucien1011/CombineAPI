import glob,os,argparse,subprocess

asym_limit_name = "AsymptoticLimits"
mlfit_name = "FitDiagnostics"
defaultFileName = "card.root"

class CombineOption(object):
    def __init__(self,cardDir,wsFileName=None,method=asym_limit_name,verbose=False,option=None,):
        self.cardDir = cardDir
        self.wsFileName = wsFileName if wsFileName else cardDir+defaultFileName
        self.method = method
        self.verbose = verbose
        self.option = option
        pass

class CombineAPI(object):
    def run(self,option):
        if option.method == asym_limit_name:
            self.run_asym_limit(option)
        elif option.method == mlfit_name:
            self.run_mlfit(option)
        else:
            raise RuntimeError,"Another option not supported atm"

    def run_mlfit(self,option):
        if option.verbose:
            print "*"*20
            print "Running on ws", option.wsFileName
            print "Method", option.method
        items = ["combine","-M",option.method,option.wsFileName]
        if option.option: items += option.option
        outDir = os.path.dirname(option.wsFileName)
        items.append("--out="+outDir)
        file_out = open(option.cardDir+mlfit_name+"_Out.txt","w")
        file_err = open(option.cardDir+mlfit_name+"_Err.txt","w")
        out = subprocess.Popen(
                items,
                stdout=subprocess.PIPE, 
                #stdout=file_out, 
                stderr=subprocess.STDOUT,
                #stderr=file_err, 
                )
        stdout,stderr = out.communicate()
        file_out.write(stdout)
        file_err.write(stdout)
        file_out.close()
        file_err.close()
        outFileNames = [
                #"fitDiagnostics.root",
                "combine_logger.out",
                "higgsCombineTest.FitDiagnostics.mH120.root",
                "*.png",
                ]
        for outFileName in outFileNames:
            if glob.glob(outFileName):
                os.system("mv "+outFileName+" "+option.cardDir)

    def run_asym_limit(self,option):
        if option.verbose:
            print "*"*20
            print "Running on ws", option.wsFileName
            print "Method", option.method
        items = ["combine","-M",option.method,option.wsFileName]
        if option.option: items += option.option
        file_out = open(option.cardDir+asym_limit_name+"_Out.txt","w")
        file_err = open(option.cardDir+asym_limit_name+"_Err.txt","w")
        out = subprocess.Popen(
                items,
                stdout=subprocess.PIPE, 
                #stdout=file_out, 
                stderr=subprocess.STDOUT,
                #stderr=file_err, 
                )
        stdout,stderr = out.communicate()
        file_out.write(stdout)
        file_err.write(stdout)
        file_out.close()
        file_err.close()
        outFileName = "higgsCombineTest.AsymptoticLimits.mH120.root"
        os.system("mv "+outFileName+" "+option.cardDir)
