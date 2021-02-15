#//////////////////////////////////Libraries//////////////////////////////////////
from math import pow
from operator import itemgetter
from signal import SIGINT, signal
from typing import Literal, NoReturn, Tuple

#
class IP():
    #######################################
    # Note: *string* means variable name. #
    #######################################

    # Class constructor
    def __init__(self) -> None:
        super().__init__()

    #////////////////////////////////Host functions///////////////////////////////////
    # Return the data generated for a new subnet mask
    def adapted_subnet_mask_case_host(self, n: int) -> list[int]:
        # Position variables to any bit in the IP array
        i = 0
        j = 0

        # Binary octet for the new subnet mask
        temp_mask_octet = ''
        # Final subnet mask array
        subnet_mask = [0] * 4
        # Array with the subnet mask data
        mask_data = list()
        # Flag to change the status on all remained bits to zero
        flag = 32 - n
        # Counter to change the status bit by bit of the binary octets to one until *count* equal to *flag*
        count = 1
        # Position of the last modified binary octet
        pos = 0

        # Building the subnet mask in binary system
        while i < 4:
            if j < 8:
                # Checking the limits
                if count <= flag:
                    # Adding a bit with status one in the binary octet
                    temp_mask_octet += '1'
                    # Increment the counter on one
                    count += 1
                    # Position of the last bit with status one
                    if count - 1 == flag:
                        # Current position of the last binary octet modified
                        pos = i

                else:
                    # Adding a bit with status zero
                    temp_mask_octet += '0'
                # Increment one bit position
                j += 1

            else:
                # Saving the binary octet previously generated in the final subnet mask array
                subnet_mask[i] = temp_mask_octet
                # Increment one binary octet
                i += 1
                # Reset the bit position to zero
                j = 0
                # Reset the temporal binary octet for a new one
                temp_mask_octet = ''

        #Reset the current binary octet position to zero
        i = 0
        while i < 4:
            # Convert every binary octet to an integer number
            subnet_mask[i] = int(subnet_mask[i], 2)
            i += 1

        print(" Subnet mask for the requested network: {}".format(subnet_mask))
        # Saving the subnet mask data in mask_data array
        mask_data.append(subnet_mask)
        # Saving the position of the last modified binary octet
        mask_data.append(pos)
        return mask_data

    #///////////////////////////////Subnet functions//////////////////////////////////
    # Return the info generated for a new subnet mask
    def adapted_subnet_mask(self, subnet_mask: list, n: int) -> Tuple[list, int]:

        # Binary octet position in the IP array
        i = 0
        # Array with the essential subnet mask data
        mask_data = []
        # Array with the new changes (modified binary octet and the *n* var)
        modification_data = [0] * 2

        # Generating the new subnet mask IP address
        while i < 4:
            if subnet_mask[i] < 255:
                # Convert the integer IP octet to a binary octet
                binary_octet = self.dec_to_bin(subnet_mask[i])
                # Modify the binary octet
                modification_data = self.modified_eight_bit_octet(n, binary_octet)

                subnet_mask[i] = modification_data[0]
                n = modification_data[1]

                # Break in case the *n* var becomes zero
                if n == 0:
                    break
                else:
                    i += 1
            else:
                i += 1

        # Saving the subnet mask data in mask_data array
        mask_data.append(subnet_mask)
        # Saving the position of the last modified binary octet
        mask_data.append(i)

        print(" Subnet mask for the requested network: {}".format(subnet_mask))
        return mask_data

    # Return the binary octet modified in the subnet mask
    def modified_eight_bit_octet(self, n: int, binary_octet: list) -> list[int]:

        # Arr with the new changes (the binary octet and the *n* var)
        modification_data = list()
        # Bit position
        i = 0

        # Zero binary octet case
        if binary_octet == '0':
            # Reset the binary octet
            binary_octet = ''
            while n > 0:
                # Append a bit with status one
                binary_octet += '1'
                # Substract one bit
                n -= 1
            if len(binary_octet) < 8:
                while len(binary_octet) < 8:
                    # Append a bit with status zero
                    binary_octet += '0'

        else:
            # Convert the string of binary_octet var to a char list
            binary_octet = list(binary_octet)
            while (i < 8) and (n > 0):
                if binary_octet[i] == '0':
                    # Append a bit with status one
                    binary_octet[i] = '1'
                    # Increment one bit position
                    i += 1
                    # Substract one bit
                    n -= 1
                else:
                    # Increment one bit position
                    i += 1

            # Convert the char list to string
            binary_octet = ''.join(binary_octet)

        # Convert the binary octet to a decimal number
        decimal_no = int(binary_octet, 2)

        # Saving the modified binary octet in the IP address
        modification_data.append(decimal_no)
        # Saving the modified *n* variable
        modification_data.append(n)

        return modification_data

    # //////////////////////////////General functions/////////////////////////////////
    # Convert an integer number to a binary one
    def dec_to_bin(self, x: int) -> str:
        binary_octet = f'{x:b}'
        # Verifying the binary octet length
        if len(binary_octet) < 8:
            # Temporal var to complete the 8-bit octet
            temp = ''
            # Size of the binary_octet array
            octet_size = len(binary_octet)
            # Filling the temporal binary octet
            while octet_size < 8:
                # Adding a bit with status zero
                temp += "0"
                octet_size += 1
            # Merge *temp* var with *binary_octet* var
            temp += binary_octet
            # Saving the final binary octet
            binary_octet = temp
        return binary_octet

    # Function to split any string according to the character given in the parameter setup
    def split_input_data(self, ip: str) -> list:
        ip = ip.split('.')

        ############-> First Data Speculation <-#############
        # Verifying input data size after split
        # Return -1 in case of different size to the expected
        if len(ip) != 4:
            ip = -1

        return ip

    # Convert a string array (members are integer numbers) to an integer array
    def string_to_int_Arr(self, ipA: list[str]) -> None:
        # Segment position
        i = 0
        while i < 4:
            # Convert the string to an integer number
            ipA[i] = int(ipA[i])
            i += 1

    # Return the incremental number for the subnet list
    def increment_num(self, mask_data: list) -> int:
        # Position of the last modified octet
        pos = mask_data[1]

        # Obtaining the increment number
        inc = 256-int(mask_data[0][pos])
        print("Increment number: {}\n".format(inc))
        return inc

    #Return a matrix of the IP to easier handle of it
    def eight_bits(self, ipA:list[int]) -> list[str]:

        i = 0
        j = 0
        while i < 4:
            # Create temporal binary octet of 8 bits
            temp = ["0"] * 8
            # Saving the binary string
            bin_num = self.dec_to_bin(ipA[i])
            while j < 8:
                # Making the string an editable array
                temp[j] = bin_num[j]
                j += 1
            # Saving the final binary octet in the original array
            ipA[i] = temp
            j = 0
            i += 1

        return ipA

    # Return the number of zeros which gonna change in the subnet mask.
    def get_n(self, num_host_request: int, operation_type: str) -> int:

        # Number of zeros
        n = 0
        # Conditional
        operation_result = 0

        while True:
            # Subnet formula
            if operation_type == 's':
                operation_result = pow(2, n)
            # Host formula
            elif operation_type == 'h':
                operation_result = (pow(2, n)-2)

            if (operation_result > num_host_request) or (operation_result == num_host_request): 
                break
            else:
                n = n + 1
        print("n = {}".format(n))
        return n

    # Return the ip_class_var of the IP
    def ip_class(self, first_8_Bits: int) -> int:
        ip_class = None
        class_arr = ['A', 'B', 'C', 'D', 'E']
        if (first_8_Bits >= 1) and (first_8_Bits <= 127):
            ip_class = 1
        elif (first_8_Bits >= 128) and (first_8_Bits <= 191):
            ip_class = 2
        elif (first_8_Bits >= 192) and (first_8_Bits <= 223):
            ip_class = 3
        elif (first_8_Bits >= 224) and (first_8_Bits <= 239):
            ip_class = 4
        elif (first_8_Bits >= 240) and (first_8_Bits <= 255):
            ip_class = 5

        print("\n\nThe IP belongs to the {} class.\n\n".format(
            class_arr[ip_class - 1]))
        return ip_class

    # Return the net IP (noDefault subnet mask prefix)
    def special_net_ip(self, ipA: list[int], noDefault_mask_prefix: int) -> list[int]:
        i = 0
        j = 0
        # Temporal binary octet
        temp = ''

        # Convert the segment in the array (integers) to a string 8-bits octets
        binary = self.eight_bits(ipA)
        net_ip = [0] * 4

        # Flag to stop the assignment of one in the bit status
        flag = 1
        while i < 4:
            if j < 8:
                # Making AND operations
                if flag <= noDefault_mask_prefix:
                    temp += "{0:b}".format(int(binary[i][j]) & 1)
                    flag += 1
                else:
                    temp += "{0:b}".format(int(binary[i][j]) & 0)
                j += 1
            else:
                # Saving the binary octet created in the IP array
                net_ip[i] = temp
                # Reset the temporal binary octet for a new one
                temp = ''
                i += 1
                j = 0

        i = 0
        # Convert the binary octets of the new IP on integer numbers.
        while i < 4:
            net_ip[i] = int(net_ip[i], 2)
            i += 1

        print("\n\nThe newtwork IP of the input IP is: {}".format(net_ip))
        return net_ip

    # Return the subnet mask of an IP (noDefault subnet mask prefix)
    def noDefault_network_mask(self, noDefault_mask_prefix: int) -> list[int]:
        i = 0
        j = 0
        temp_mask_octet = ''
        # Final subnet mask
        subnet_mask = [0] * 4

        # Counter that saves the number of bits to been through the loop
        count = 1
        while i < 4:
            if j < 8:
                # Setting the values to one on all the bits before noDefault mask prefix value
                if count <= noDefault_mask_prefix:
                    temp_mask_octet += '1'
                else:
                    temp_mask_octet += '0'
                count += 1
                j += 1
            else:
                # Saving the binary octet in the IP array
                subnet_mask[i] = temp_mask_octet
                i += 1
                j = 0
                temp_mask_octet = ''

        i = 0
        # Convert the binary octets into integers on the IP array
        while i < 4:
            subnet_mask[i] = int(subnet_mask[i], 2)
            i += 1

        print("The subnet mask of the input IP is: {}".format(subnet_mask))
        return subnet_mask

    # Return the broadcast IP (noDefault subnet mask prefix)
    def network_broadcast_ip(self, subnet_ip: list[int], noDefault_mask_prefix: int) -> list[int]:

        i = 0
        # Temporal array
        copy_subnet_ip = [0] * 4

        while i < 4:
            copy_subnet_ip[i] = subnet_ip[i]
            i += 1

        # Convert the IP segments(integers) into binary octets
        binary_subnet = self.eight_bits(copy_subnet_ip)
        # Final broadcast IP
        broadcast_ip = [0] * 4

        # FLAGS
        # Number of the octet in the IP array to start the AND type operations
        pos_i = noDefault_mask_prefix // 8
        # Number of the bit in the octet to start the AND operations
        pos_j = noDefault_mask_prefix % 8
        # Flag to reset *pos_i* to 0
        reset = False

        while pos_i < 4:
            if reset == False:
                # Modify the IP starting on pos_j flag to changing bits value to 1 (for each octet)
                while pos_j < 8:
                    binary_subnet[pos_i][pos_j] = "1"
                    pos_j += 1
                pos_j = 0
                pos_i += 1
                # Change the state of reset flag to True
                if pos_i > 3:
                    reset = True
                    pos_i = 0
            else:
                # Start with pos_i = 0
                # Temporal binary octet to make it integer
                temp = ""
                while pos_j < 8:
                    # Copying all the octet
                    temp += binary_subnet[pos_i][pos_j]
                    pos_j += 1
                pos_j = 0
                #Saving the binary octet in the final IP array
                broadcast_ip[pos_i] = int(temp, base=2)
                pos_i += 1

        print("Broadcast IP: {}\n\n".format(broadcast_ip))

    # Return the net IP (default subnet mask prefix)
    def net_ip_func(self, ipA: list[int], subnet_mask: list[int]) -> list[int]:

        i = 0
        # Convert the initial IP in sections of 8 bits
        binary = self.eight_bits(ipA)
        # Convert the original subnet mask IP in sections of 8 bits
        binary_subnet_mask = self.eight_bits(subnet_mask)
        # Final array with the network IP
        net_ip = [''] * 4

        while i < 4:
            # Temporal var for AND operations
            aux = ''
            aux_subnet_mask = ''
            # Temporal var for saving each section of 8 bits
            temp = [''] * 8
            j = 0
            # AND operations between initial IP and the subnet IP
            while j < 8:
                temp[j] = "{0:b}".format(
                    int(binary[i][j]) & int(binary_subnet_mask[i][j]))
                # Saving the new section of 8 bits
                aux += temp[j]
                aux_subnet_mask += binary_subnet_mask[i][j]
                j += 1

            # Saving the data in the final array
            net_ip[i] = aux
            subnet_mask[i] = aux_subnet_mask
            i += 1

        i = 0
        # Convert the sections of 8 bits of the IPs on integers and saving them
        while i < 4:
            net_ip[i] = int(net_ip[i], base=2)
            subnet_mask[i] = int(binary_subnet_mask[i], base=2)
            i += 1

        print("The network IP of the input IP is: {}".format(net_ip))
        return net_ip

    # Return the subnet mask (default subnet mask prefix)
    def default_mask(self, ip_class: int) -> list[int]:
        # Note: ip_class represent the letter of the class (A = 1, B = 2, C = 3)

        i = 0
        subnet_mask = [0] * 4

        # Making the subnet mask
        while i < ip_class:
            subnet_mask[i] = 255
            i += 1

        print("\n\nSubnet mask: {}".format(subnet_mask))
        return subnet_mask

    # Return the broadcast IP (default subnet mask prefix)
    def ip_broadcast_func(self, subnet_ip: list[int], ip_class: int) -> None:

        i = 0
        # Final broadcast IP array
        broadcast_ip = [0] * 4

        while i < 4:
            j = 0
            temp = ''
            # Copy the numbers in the array before the octet value that belongs to IP class number
            if i < ip_class:
                broadcast_ip[i] = subnet_ip[i]
            else:
                # Filling the remaining octets with values of one ​on the bit status
                while j < 8:
                    temp += "1"
                    j += 1
                # Making the octet integer and saving it in the final array
                broadcast_ip[i] = int(temp, base=2)
            i += 1

        print("Broadcast ip: {}\n\n".format(broadcast_ip))

    # Function to make sure if the input data (The IP) are correct
    def limits_check(self, ipA: list[str]) -> bool:

        # Verifying first the var content (case: wrong data)
        if ipA == -1:
            anws = False

        else:
            anws = True
            i = 0

            # Cheking the first element of the array
            if (ipA[i].isdigit() == True) and (int(ipA[i]) > 0) and (int(ipA[i]) < 256):
                i += 1
                # Verifying the remainder elements in the array (it's an IP?)
                while i < 4:
                    if (ipA[i].isdigit() == True) and (int(ipA[i]) >= 0) and (int(ipA[i]) < 256):
                        i += 1
                    else:
                        anws = False
                        break
            else:
                anws = False

        return anws

        # Verify if the IP isn't overflowed
    
    # Verify if the network IP it was not overflowed
    def fix_ip(self, net_ip: list[int]) -> None:
        i = 3

        # Loop to increase correctly every increment number
        while i > 0:
            # Check if the current position its overflowed
            if net_ip[i] == 256:
                # Set 0 to current position and add a 1 to the previous one
                net_ip[i] = 0
                net_ip[i - 1] += 1
            i -= 1

    # Generate broadcast IP for every subnet
    def make_broadcast_ip(self, broadcast_subnet_ip: list[int], pos: int, increment_num: int) -> list[int]:

        i = 0

        # First we need to increase the actual position with the increment number
        broadcast_subnet_ip[pos] += increment_num - 1

        # Then fill the remaining positions with 255 in case of current position are less than 3
        if pos < 3:
            i = pos + 1
            while i <= 3:
                broadcast_subnet_ip[i] = 255
                i += 1

        return broadcast_subnet_ip

    # Prepare the IPs for print
    def set_ready(self, net_ip: list[int], tmp_subnet_ip: list[int], broadcast_subnet_ip: list[int], subnet_list, arr_pos: int) -> None:

        i = 0

        # Fuction to verify if the IP isn't overflowed
        self.fix_ip(net_ip)

        # Prepare the broadcast IP and the temporal subnet IP for the next step
        while i < 4:
            tmp_subnet_ip[i] = net_ip[i]
            broadcast_subnet_ip[i] = net_ip[i]
            i += 1

        # Generate the broadcast IP (previously prepared)
        # with the information in the subnet_list array
        # for range operations
        self.make_broadcast_ip(broadcast_subnet_ip,
                          subnet_list[arr_pos][1], subnet_list[arr_pos][2])

    # Print the subnet list
    def generate_list(self, subnet_list: list, net_ip: list[int]) -> None:

        i = 0
        # Number of total prints (inizialiced)
        total_prints = 0
        # Individual broadcast of each subnet
        broadcast_subnet_ip = [0] * 4

        # This are the temporal subnet IP & broadcast subnet IP initialized
        tmp_subnet_ip = [0] * 4
        tmp_broadcast_subnet_ip = [0] * 4

        # Size represent the number of subnets without repetition in the array
        size = len(subnet_list)
        while i < size:
            total_prints += subnet_list[i][0]
            i += 1

        # Number of the current subnet to print
        i = 0
        # Number of subnets to print for each network
        j = 0
        # Current position in the subnet data array
        k = 0
        print("\n#################################################################################################")
        print("Net No.\t       Network IP\t\t\tRange\t\t\t\t    Broadcast")

        # Printing the list
        while i < total_prints:
            while j < subnet_list[k][0]:
                if j == 0:
                    # Initial case (the original IP doesn't been modified)
                    if i == 0:
                        # Prepare the inserted IPs in the function
                        self.set_ready(net_ip, tmp_subnet_ip,
                                  broadcast_subnet_ip, subnet_list, k)

                    else:
                        # Second case (The first subnet to print for the current network)
                        net_ip[subnet_list[k-1][1]] += subnet_list[k-1][2]
                        # Prepare the inserted IPs in the function
                        self.set_ready(net_ip, tmp_subnet_ip,
                                  broadcast_subnet_ip, subnet_list, k)

                else:
                    # Third case (The remaining subnets to print in the current network)
                    net_ip[subnet_list[k][1]] += subnet_list[k][2]
                    # Prepare the inserted IPs in the function
                    self.set_ready(net_ip, tmp_subnet_ip,
                              broadcast_subnet_ip, subnet_list, k)

                # Position int the array for the broadcast IPs
                l = 0
                # Copy the broadcast IP to a temporary one for range operations
                while l < 4:
                    tmp_broadcast_subnet_ip[l] = broadcast_subnet_ip[l]
                    l += 1
                l = 0

                # Range of hosts for the current subnet
                range_h = self.range_hosts(tmp_subnet_ip, tmp_broadcast_subnet_ip)

                print("  {}\t    {}\t{}      \t{}".format(
                    i, net_ip, range_h, broadcast_subnet_ip))
                i += 1
                j += 1

            k += 1
            j = 0

    # Obtain the range of hosts for the current subnet
    def range_hosts(self, tmp_net_ip: list[int], tmp_broadcast_subnet_ip: list[int]) -> list[int]:

        # Array for save the range
        range_arr = [0] * 2
        # Last position of both IPs
        i = 3

        # Add one host on the net IP
        tmp_net_ip[i] += 1
        # Subtract one host on the broadcast IP
        tmp_broadcast_subnet_ip[i] -= 1

        # Saving the data
        range_arr[0] = tmp_net_ip
        range_arr[1] = tmp_broadcast_subnet_ip

        return range_arr

    # Function to verify the input in a number request
    def number_request_verification(self, var: int) -> list[int, bool]:

        # Var to break the loop
        is_a_number = True

        if var.isdigit() == True:
            # Convert the string var into an int one.
            var = int(var)
        else:
            print("Error: Invalid number.")
            is_a_number = False

        return var, is_a_number

    # Set the IP and return it splitted, in case of invalid input data, return -1
    def set_the_ip(self) -> list[str]:
        ip = input(" Set the IP: ")
        # Trying to split the input in 4 parts
        return self.split_input_data(ip)

# Function in case of the user press ctrl + c to exit
def signal_handler(signum, frame) -> NoReturn:
    print("\n\n Warning: Execution was interrupted.")
    print(" Killing process . . .\n (X_X) -> EXIT_CODE: 0xDEAD")
    exit()


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Main_Function<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def main():

    signal(SIGINT, signal_handler)
    ################# Banner block ################
    # Open the banner file (READ_ONLY)            #
    fp = open("banner.ban", "r", encoding='UTF-8')#
    # Display the banner                          #
    print(fp.read())                              #
    ###############################################

    ip = IP()

    while True: 
        print("\n\n                    Generate: ")
        print("     i -> subnets only with the input IP.")
        print("     h -> subnets with a host number requirement.\n")
        answer = input(" #: ")
        if answer == 'h' or answer == 'i':
            break
        else:
            print("\n Error: invalid option.")

    # Trying to set the root IP array
    ipA = ip.set_the_ip()
    # Loop in case of invalid input data
    while ip.limits_check(ipA) == False:
        print(
            "\n The input data doesn't look like an IP address.\n Please set a correct one.\n")
        ipA = ip.set_the_ip()

    # Convert the string array to an int one
    ip.string_to_int_Arr(ipA)

    # Getting the class of the root IP
    ip_class_var = ip.ip_class(ipA[0])

    if ip_class_var == 4 or ip_class_var == 5:
            print(
                " Exception: Classes D & E are only used for Multicasting and Military Purposes.")
            exit()
    else:
        while True:
            # Asking the type of subnet mask (ssnm = special subnet mask)
            ssnm = input(
                " The IP have a special subnet mask? \n y = yes\tn = no (set the standard subnet mask)\n #:")

            if ssnm.lower() == 'y':
                while True:
                    special_mask_num = input(
                        "\n Enter the subnet mask prefix below: ")
                    # Verifying the input data
                    if (special_mask_num.isdigit()) and (int(special_mask_num) > 0) and (int(special_mask_num) <= 32):
                        special_mask_num = int(special_mask_num)
                        break
                    else:
                        print(
                            "\n Illegal value for subnet mask! Please enter a valid number.")

                # Network IP
                net_ip = ip.special_net_ip(ipA, special_mask_num)
                # Network Mask
                subnet_mask = ip.noDefault_network_mask(special_mask_num)
                # Broadcast IP
                ip.network_broadcast_ip(net_ip, special_mask_num)
                break

            elif ssnm.lower() == 'n':
                # Net IP
                subnet_mask = ip.default_mask(ip_class_var)
                # Subnet Mask
                net_ip = ip.net_ip_func(ipA, subnet_mask)
                # Broadcast IP
                ip.ip_broadcast_func(net_ip, ip_class_var)
                break

            else:
                print("\n Error: Invalid option. Select one of the following options: ")

    # According to the first question (subnet or host) make the respective operations
    # Subnet case
    if answer == 'i':

        # Temporal data array with the information of the subnet
        temp_subnet = [0] * 3

        # Number of subnets to generate
        while True:
            subnets_num = input(
                " Enter the number of subnets you want to generate: ")
            if subnets_num.isdigit() and int(subnets_num) > 0:
                break
            else:
                print(" Error: Invalid number.")

        # Array with the data for print the list
        subnet_list = []
        # Number of subnets to generate
        temp_subnet[0] = int(subnets_num) + 1
        # Number of zeros which gonna change in the subnet mask.
        n = ip.get_n(int(subnets_num), 's')
        # Obtaining the subnet mask information
        mask_inf = ip.adapted_subnet_mask(subnet_mask, n)
        # Position of the last modified octet of 8 bits
        temp_subnet[1] = mask_inf[1]
        # Incremental number for the subnet
        inc_num = ip.increment_num(mask_inf)
        temp_subnet[2] = inc_num
        # Save the temporal data array with the information of the subnet
        subnet_list.append(temp_subnet)
        # Generate and print the subnet list
        ip.generate_list(subnet_list, net_ip)

    # Host case
    elif answer == 'h':
        # Verifying the input data
        is_a_number = None
        while True:
            subnets_num = input(
                " How many subnets of n-hosts do you want generate?\t(omitting repetitions)\n #: ")
            subnets_num, is_a_number = ip.number_request_verification(
                subnets_num)
            if is_a_number == True:
                print("")
                break

        # Initialized the temporal list
        temp_subnet_list = [0] * subnets_num

        i = 0
        while i < subnets_num:
            print("|//////////////////////////////////////////////////////////////|")
            while True:
                hosts_no = input(
                    " Enter the number of hosts you want to obtain for the network num. {}: ".format(i+1))
                hosts_no, is_a_number = ip.number_request_verification(
                    hosts_no)
                if is_a_number == True:
                    break

            while True:
                no_subnets_of_n_hosts = input(
                    " How many subnets of {} hosts do you want to obtain?\n #: ".format(hosts_no))
                no_subnets_of_n_hosts, is_a_number = ip.number_request_verification(
                    no_subnets_of_n_hosts)
                if is_a_number == True:
                    break

            # Temporal array for the every subnet information
            temp_subnet = [0] * 4
            # Array with host data
            host_data = [0] * 3

            # Number of zeros which gonna change in the subnet mask.
            host_data[0] = ip.get_n(int(hosts_no), 'h')
            # Obtaining the subnet mask information
            mask_inf = ip.adapted_subnet_mask_case_host(host_data[0])
            # Position of the last modified octet of 8 bits
            host_data[1] = mask_inf[1]
            # Incremental number for the subnet
            host_data[2] = ip.increment_num(mask_inf)

            # Subnet No. request
            temp_subnet[0] = no_subnets_of_n_hosts + 1
            # Position of the last modified octet of 8 bits
            temp_subnet[1] = host_data[1]
            # Incremental number for the subnet
            temp_subnet[2] = host_data[2]
            # Number of hosts for the subnet
            temp_subnet[3] = hosts_no
            # Save the temporal data array with the information of the subnet
            temp_subnet_list[i] = temp_subnet
            i += 1
            print("|//////////////////////////////////////////////////////////////|")

        # Sorting the subnet list to descending form based on the no. of hosts
        sorted_subnet_list = sorted(
            temp_subnet_list, key=itemgetter(3), reverse=True)

        i = 0
        final_subnet_list = [0] * subnets_num
        # Saving the final data in the array for print (sorted)
        while i < subnets_num:
            temp_subnet = [0] * 3
            temp_subnet[0] = sorted_subnet_list[i][0]
            temp_subnet[1] = sorted_subnet_list[i][1]
            temp_subnet[2] = sorted_subnet_list[i][2]
            final_subnet_list[i] = temp_subnet
            i += 1

        ip.generate_list(final_subnet_list, net_ip)


# Start point
main()
