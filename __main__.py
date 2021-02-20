#//////////////////////////////////Libraries//////////////////////////////////////
import src.sys.Core as Core
import src.tools.IPOp as IPOp

from signal import SIGINT, signal


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Main Function<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# Main function
if __name__ == "__main__":
    bannerPath = "src/sys/banner"
    ip = IPOp.IP()
    sys = Core.System()

    signal(SIGINT, sys.signal_handler)
    ################# Banner block ################
    # Open the banner file (READ_ONLY)            #
    fp = open(bannerPath, "r", encoding='UTF-8')
    # Display the banner                          #
    print(fp.read())                              #
    ###############################################

    op = sys.setTheMainOperation()
    
    rootIP = ip.getInputIP()
    
    # Convert the string array to an int one
    ip.string_to_int_Arr(rootIP)
    # Getting the class of the root IP
    ipClass = ip.getClass(rootIP[0])
    
    default = True
    while True:
        # Asking the type of subnet mask (nssm = non-default subnet mask)
        ndsm = input(
            " The IP have a non-default subnet mask prefix? \n [Y/n]:")
        if ndsm.lower() == 'y':
            while True:
                subnetMaskPrefix = input(
                    "\n Enter the subnet mask prefix below: ")
                # Check the input data
                if (subnetMaskPrefix.isdigit()) and (int(subnetMaskPrefix) > 0) and (int(subnetMaskPrefix) <= 32):
                    subnetMaskPrefix = int(subnetMaskPrefix)
                    default = False
                    ip.setTriada(rootIP, -1, subnetMaskPrefix, default)
                    break
                else:
                    print(
                        "\n Error: Illegal prefix value!\n Please enter a valid number.")
            break
        elif ndsm.lower() == 'n':
            print("Using default subnet mask...")
            ip.setTriada(rootIP, ipClass, -1, default)
            break
        else:
            print("\n Error: Invalid option.")
    
    sys.executeOp(op, ip.getTriada())
