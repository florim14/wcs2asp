import subprocess
from os import path



def filename_separator(filePath):
    if filePath.endswith(".lp"):
        filePath = filePath.split("/")
        return (filePath[len(filePath) - 1]).split(".lp")[0]
    else:
        raise IOError('Please provide an appropriate file. The file should be a .lp file!')

def clingo_operation(filePath, mode):
    modePath = get_mode_path(mode)
    process = subprocess.Popen(['clingo', filePath, modePath, "--enum-mode=domRec", "--heuristic=Domain", "0"],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    savedFilePath = "Solution/" + filename_separator(filePath) + "Solution.txt"
    f = open(savedFilePath, "w+")
    f.write(stdout.decode("utf-8"))
    f.close()
    return savedFilePath


def get_mode_path(mode):
    if mode == 2:
        return "clingoEncodingSupportedModels.lp"
    elif mode == 3:
        return "clingoForAbductionEncodingMinimalModels.lp"
    else:
        return "clingoEncodingMinimalModels.lp"
