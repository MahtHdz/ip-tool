#//////////////////////////////////Libraries//////////////////////////////////////
from math import pow
from typing import Literal, NoReturn, Tuple

#
class IP():

    _base = list()
    _triada = list()
    ########################################################
    # Note: Strings between * * reference a variable name. #
    ########################################################

    # Class constructor
    def __init__(self) -> None:
        super().__init__()

    #////////////////////////////////Host functions///////////////////////////////////
    # Return the data generated for a new subnet mask
    def adapted_subnet_mask_case_host(self, n: int) -> list:
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
    def adapted_subnet_mask(self, subnet_mask: list, n: int) -> tuple:

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
                modification_data = self.modified_eight_bit_octet(
                    n, binary_octet)

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
    def modified_eight_bit_octet(self, n: int, binary_octet: list) -> list:

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
    
    #
    def genSubnetMask(self):
        pass

    #
    def getInputIP(self) -> list:
        # Trying to set the root IP array
        ipA = self.set_the_ip()
        # Loop in case of invalid input data
        while self.limits_check(ipA) == False:
            print(
                "\n The input data doesn't look like an IP address.\n Please set a correct one.\n")
            ipA = self.set_the_ip()
        return ipA

    #
    def getTriada(self) -> list:
        return self._triada
    
    #
    def setTriada(self, rootIP: list, ipClass: int, subnetMaskPrefix: int, default: bool) -> None:
        if default:
            # Subnet Mask
            subnetMask = self.defaultSubnetMask(ipClass)
            # Net IP
            networkIP = self.networkIPDefaultSM(rootIP, subnetMask)
            # Broadcast IP
            broadcast = None
            self.broadcastForDefaultSM(networkIP, ipClass)
        else:
             # Network IP
            networkIP = self.networkIPNonDefaultSM(rootIP, subnetMaskPrefix)
            # Subnet Mask
            subnetMask = self.nonDefaultSubnetMask(subnetMaskPrefix)
            # Broadcast IP
            broadcast = None
            self.broadcastForNonDefaultSM(networkIP, subnetMaskPrefix)
        
        self._triada.append(networkIP)
        self._triada.append(subnetMask)
        #self._triada.append(broadcast)

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
    def string_to_int_Arr(self, ipA: list) -> None:
        # Segment position
        i = 0
        while i < 4:
            # Convert the string to an integer number
            ipA[i] = int(ipA[i])
            i += 1

    # Return the incremental number of the subnet list
    def incrementNo(self, mask_data: list) -> int:
        # Position of the last modified octet
        pos = mask_data[1]

        # Obtaining the increment number
        inc = 256-int(mask_data[0][pos])
        print(" Increment number: {}\n".format(inc))
        return inc

    #Return a matrix of the IP to easier handle of it
    def eight_bits(self, ipA: list) -> list:

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

    # Return the number of zeros that gonna change in the subnet mask.
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
        print("\n n = {}".format(n))
        return n

    # Return the IP class
    def getClass(self, firstOctet: int) -> int:
        ipClass = None
        class_arr = ['A', 'B', 'C', 'D', 'E']
        if (firstOctet >= 1) and (firstOctet <= 127):
            ipClass = 1
        elif (firstOctet >= 128) and (firstOctet <= 191):
            ipClass = 2
        elif (firstOctet >= 192) and (firstOctet <= 223):
            ipClass = 3
        elif (firstOctet >= 224) and (firstOctet <= 239):
            ipClass = 4
        elif (firstOctet >= 240) and (firstOctet <= 255):
            ipClass = 5

        print("\n\n The IP belongs to {} class.\n\n".format(class_arr[ipClass - 1]))
        
        # The IP can be used for public propuse?
        if ipClass == 4 or ipClass == 5:
            print(
                " Exception: Classes D & E are only used for Multicasting and Military Purposes.")
            exit(0)
        else:
            return ipClass

    # Function to make sure if the input data (The IP) are correct
    def limits_check(self, ipA: list) -> bool:

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
    def fix_ip(self, net_ip: list) -> None:
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
    def make_broadcast_ip(self, broadcast_subnet_ip: list, pos: int, increment_num: int) -> list:

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
    def set_ready(self, net_ip: list, tmp_subnet_ip: list, broadcast_subnet_ip: list, subnet_list, arr_pos: int) -> None:

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
    def generate_list(self, subnet_list: list, net_ip: list) -> None:

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
                range_h = self.range_hosts(
                    tmp_subnet_ip, tmp_broadcast_subnet_ip)

                print("  {}\t    {}\t{}      \t{}".format(
                    i, net_ip, range_h, broadcast_subnet_ip))
                i += 1
                j += 1

            k += 1
            j = 0

    # Obtain the range of hosts for the current subnet
    def range_hosts(self, tmp_net_ip: list, tmp_broadcast_subnet_ip: list) -> list:

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
    def number_request_verification(self, var: int) -> list:

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
    def set_the_ip(self) -> list:
        ip = input(" Set the IP: ")
        # Trying to split the input in 4 parts
        return self.split_input_data(ip)

    # ///////////////////////// Default Subnet Mask Prefix ////////////////////////////
    # Return the net IP (default subnet mask prefix)
    def networkIPDefaultSM(self, ipA: list, subnet_mask: list) -> list:

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
    def defaultSubnetMask(self, ipClass: int) -> list:
        # Note: ipClass represent the letter of the class (A = 1, B = 2, C = 3)

        i = 0
        subnet_mask = [0] * 4

        # Making the subnet mask
        while i < ipClass:
            subnet_mask[i] = 255
            i += 1

        print("\n\nSubnet mask: {}".format(subnet_mask))
        return subnet_mask

    # Return the broadcast IP (default subnet mask prefix)
    def broadcastForDefaultSM(self, subnet_ip: list, ipClass: int) -> None:

        i = 0
        # Final broadcast IP array
        broadcast_ip = [0] * 4

        while i < 4:
            j = 0
            temp = ''
            # Copy the numbers in the array before the octet value that belongs to IP class number
            if i < ipClass:
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

    # /////////////////////// Non-default Subnet Mask Prefix //////////////////////////
    # Return the net IP (noDefault subnet mask prefix)
    def networkIPNonDefaultSM(self, ipA: list, noDefault_mask_prefix: int) -> list:
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
    def nonDefaultSubnetMask(self, noDefault_mask_prefix: int) -> list:
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

    # Return the broadcast IP (non-default subnet mask prefix)
    def broadcastForNonDefaultSM(self, subnet_ip: list, noDefault_mask_prefix: int) -> list:

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
