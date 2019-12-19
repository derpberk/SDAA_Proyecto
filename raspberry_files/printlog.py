

def printlog(str,type = ""):


    class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'

    if(type == "WARNING"):
        print(bcolors.BOLD + bcolors.WARNING + "LOG: " + str + bcolors.ENDC)
    elif(type == "INFO"):
        print(bcolors.BOLD + bcolors.OKBLUE + "LOG: " + str + bcolors.ENDC)
    elif(type == "OK"):
        print(bcolors.BOLD + bcolors.OKGREEN + "LOG: " + str + bcolors.ENDC)
    elif(type == "ERROR"):
        print(bcolors.BOLD + bcolors.FAIL + "LOG: " + str + bcolors.ENDC)
    else:
        print( "LOG: " + str)
