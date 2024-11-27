__author__ = 'Bivoj'
import zipfile
import os

class Compressor:
    def compress(self, inputDir, outputDir, filename="test"):
        os.remove(inputDir + '/lock')
        print("Compressing: " + inputDir)
        # concatenate the folders for file name
        zipfilename = "%s.zip" % (outputDir + filename)
        zfile = zipfile.ZipFile(os.path.join(inputDir, zipfilename), 'w', zipfile.ZIP_DEFLATED)
        # rootlen => zipped files don't have a deep file tree
        rootlen = len(inputDir) + 1
        for base, dirs, files in os.walk(inputDir):
            for file in files:
                fn = os.path.join(base, file)
                zfile.write(fn, fn[rootlen:])
        zfile.close()
        return os.path.join(inputDir, zipfilename)

    def decompress(self, inputFile, outputDir):
        fh = open(inputFile, 'rb')
        z = zipfile.ZipFile(fh)
        for name in z.namelist():
            z.extract(name, outputDir)
        fh.close()
