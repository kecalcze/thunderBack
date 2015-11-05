__author__ = 'Bivoj'

import zipfile, os

class Compressor:
    def compress(self, inputDir, outputDir):
        print("Compressing: " + inputDir)
        # concatenate the folders for file name
        zipfilename = "%s.zip" % (outputDir + "test")
        zfile = zipfile.ZipFile(os.path.join(inputDir, zipfilename), 'w', zipfile.ZIP_DEFLATED)
        # rootlen => zipped files don't have a deep file tree
        rootlen = len(inputDir) + 1
        for base, dirs, files in os.walk(inputDir):
            for file in files:
                fn = os.path.join(base, file)
                zfile.write(fn, fn[rootlen:])
        zfile.close()