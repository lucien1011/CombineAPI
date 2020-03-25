import glob,os,argparse,subprocess

asym_limit_name = "AsymptoticLimits"
toy_limit_name = "HybridNew"
mlfit_name = "FitDiagnostics"
signif_name = "Significance"
impact_name = "Impacts"
defaultFileName = "card.root"

class CombineOption(object):
    def __init__(self,cardDir,wsFileName=None,method=asym_limit_name,verbose=False,option=None,run_in_wsdir=False,tag=None,useHarvester=False):
        self.cardDir = cardDir
        self.wsFileName = wsFileName if wsFileName else cardDir+defaultFileName
        self.method = method
        self.verbose = verbose
        self.option = option
        self.run_in_wsdir = run_in_wsdir
        self.tag = tag
        self.useHarvester = useHarvester
        pass

class CombineAPI(object):
    def run(self,option):
        if option.method == asym_limit_name:
            self.run_asym_limit(option)
        elif option.method == toy_limit_name:
            self.run_toy_limit(option)
        elif option.method == mlfit_name:
            self.run_mlfit(option)
        elif option.method == impact_name:
            self.run_impact(option)
        elif option.method == signif_name:
            self.run_signif(option)
        else:
            raise RuntimeError,"Another option not supported atm"

    def make_cmd(self,option):
        if option.method == asym_limit_name:
            return self.make_asym_limit_cmd(option)
        elif option.method == toy_limit_name:
            return self.make_asym_limit_cmd(option)
        else:
            raise RuntimeError,"Another option not supported atm"


    def printHeader(self,option):
        print "*"*20
        print "Running on ws", option.wsFileName
        print "Method", option.method
        items = ["combine","-M",option.method,option.wsFileName]

    def run_impact(self,option):
        if option.verbose:
            self.printHeader(option)
        items = ["combineTool.py","-M",option.method,"-d",option.wsFileName,"-m","125","--doInitialFit","--robustFit","1",]
        if option.option: items += option.option
        if option.verbose:
            print " ".join(items)
        outDir = os.path.dirname(option.wsFileName)
        file_out = open(os.path.join(option.cardDir,impact_name+"_initialFit_Out.txt"),"w")
        file_err = open(os.path.join(option.cardDir,impact_name+"_initialFit_Err.txt"),"w")
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

        items = ["combineTool.py","-M",option.method,"-d",option.wsFileName,"-m","125","--doFits","--robustFit","1",]
        if option.option: items += option.option
        if option.verbose:
            print " ".join(items)
        outDir = os.path.dirname(option.wsFileName)
        file_out = open(os.path.join(option.cardDir,impact_name+"_paramFit_Out.txt"),"w")
        file_err = open(os.path.join(option.cardDir,impact_name+"_paramFit_Err.txt"),"w")
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

        items = ["combineTool.py","-M",option.method,"-d",option.wsFileName,"-m","125","-o","impacts.json",]
        if option.option: items += option.option
        if option.verbose:
            print " ".join(items)
        outDir = os.path.dirname(option.wsFileName)
        file_out = open(os.path.join(option.cardDir,impact_name+"_Out.txt"),"w")
        file_err = open(os.path.join(option.cardDir,impact_name+"_Err.txt"),"w")
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
                "combine_logger.out",
                "higgsCombine_initialFit_Test.MultiDimFit.mH125.root",
                "higgsCombine_paramFit_Test*.MultiDimFit.mH125.root",
                "impacts.json",
                ]
        for outFileName in outFileNames:
            if glob.glob(outFileName):
                os.system("mv "+outFileName+" "+option.cardDir)

    def run_signif(self,option):
        if option.verbose:
            self.printHeader(option)
        items = ["combine","-M",option.method,option.wsFileName]
        if option.option: items += option.option
        if option.verbose:
            print " ".join(items)
        outDir = os.path.dirname(option.wsFileName)
        txtFileNameTag = signif_name+"_"+option.tag if option.tag else signif_name
        file_out = open(os.path.join(option.cardDir,txtFileNameTag+"_Out.txt"),"w")
        file_err = open(os.path.join(option.cardDir,txtFileNameTag+"_Err.txt"),"w")
        out = subprocess.Popen(
                items,
                stdout=subprocess.PIPE, 
                #stdout=file_out, 
                stderr=subprocess.STDOUT,
                #stderr=file_err, 
                cwd=option.cardDir if option.run_in_wsdir else "./"
                )
        stdout,stderr = out.communicate()
        file_out.write(stdout)
        file_err.write(stdout)
        file_out.close()
        file_err.close()
        outFileNames = [
                #"fitDiagnostics.root",
                #"combine_logger.out",
                "higgsCombineTest.Significance.mH120.root",
                ]
        for outFileName in outFileNames:
            if not option.run_in_wsdir:
                if not option.tag:
                    os.system("mv "+outFileName+" "+option.cardDir)
                else:
                    outFileList = outFileName.split(".")
                    outFileList.insert(len(outFileList)-1,option.tag)
                    os.system("mv "+outFileName+" "+os.path.join(option.cardDir,".".join(outFileList)))

    def run_mlfit(self,option):
        if option.verbose:
            self.printHeader(option)
        items = ["combine","-M",option.method,option.wsFileName]
        if option.option: items += option.option
        if option.verbose:
            print " ".join(items)
        outDir = os.path.dirname(option.wsFileName)
        items.append("--out="+outDir)
        txtFileNameTag = mlfit_name+"_"+option.tag if option.tag else mlfit_name
        file_out = open(os.path.join(option.cardDir,txtFileNameTag+"_Out.txt"),"w")
        file_err = open(os.path.join(option.cardDir,txtFileNameTag+"_Err.txt"),"w")
        out = subprocess.Popen(
                items,
                stdout=subprocess.PIPE, 
                #stdout=file_out, 
                stderr=subprocess.STDOUT,
                #stderr=file_err, 
                cwd=option.cardDir if option.run_in_wsdir else "./"
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
            if not option.run_in_wsdir:
                if not option.tag:
                    os.system("mv "+outFileName+" "+option.cardDir)
                else:
                    outFileList = outputFile.split(".")
                    outFileList.insert(len(outFileList)-1,option.tag)
                    os.system("mv "+outFileName+" "+os.path.join(option.cardDir,".".join(outFileList)))

    def run_asym_limit(self,option):
        if option.verbose:
            self.printHeader(option)
        items = ["combine","-M",option.method,option.wsFileName]
        if option.option: items += option.option
        if option.verbose:
            print " ".join(items)
        file_out = open(os.path.join(option.cardDir,asym_limit_name+"_Out.txt"),"w")
        file_err = open(os.path.join(option.cardDir,asym_limit_name+"_Err.txt"),"w")
        out = subprocess.Popen(
                items,
                stdout=subprocess.PIPE, 
                #stdout=file_out, 
                stderr=subprocess.STDOUT,
                #stderr=file_err,
                cwd=option.cardDir if option.run_in_wsdir else "./"
                )
        stdout,stderr = out.communicate()
        file_out.write(stdout)
        file_err.write(stdout)
        file_out.close()
        file_err.close()
        if not option.run_in_wsdir:
            outFileName = "higgsCombineTest.AsymptoticLimits.mH120.root"
            os.system("mv "+outFileName+" "+option.cardDir)

    def make_asym_limit_cmd(self,option):
        if option.verbose:
            self.printHeader(option)
        if option.useHarvester:
            start_cmd = "combineTool.py"
        else:
            start_cmd = "combine"
        items = [start_cmd,"-M",option.method,option.wsFileName]
        if option.option: items += option.option
        if option.verbose:
            print " ".join(items)
        return " ".join(items)

    def run_toy_limit(self,option):
        if option.verbose:
            self.printHeader(option)
        items = ["combine","-M",option.method,option.wsFileName]
        if option.option: items += option.option
        if option.verbose:
            print " ".join(items)
        file_out = open(option.cardDir+toy_limit_name+"_Out.txt","w")
        file_err = open(option.cardDir+toy_limit_name+"_Err.txt","w")
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
        outFileName = "higgsCombineTest.HybridNew.mH120.root"
        os.system("mv "+outFileName+" "+option.cardDir)
