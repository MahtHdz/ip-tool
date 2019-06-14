from math import pow
from operator import itemgetter
from signal import SIGINT, signal


# ///////////////////////////////Host functions///////////////////////////////////

#
def get_hosts(host_num):
    """ Array with host data """
    host_data = [0] * 3

    # Number of zeros in the subnet mask.
    host_data[0] = get_n(int(host_num), 'h')
    mask_inf = adapted_mask_host(host_data[0])      # Position
    host_data[1] = mask_inf[1]
    host_data[2] = increment_num(mask_inf)

    return host_data

#
def adapted_mask_host(n):

    i = 0
    j = 0
    temp_mask_segment = ''
    subnet_mask = [0] * 4
    mask_inf = [0] * 2
    flag = 32 - n
    count = 1
    pos = 0
    while i < 4:
        if j < 8:
            if count <= flag:
                temp_mask_segment += '1'
                pos = i
                count += 1
            else:
                temp_mask_segment += '0'
            j += 1
        else:
            subnet_mask[i] = temp_mask_segment
            i += 1
            j = 0
            temp_mask_segment = ''

    i = 0
    while i < 4:
        decimal = bin(int(subnet_mask[i], 2))
        subnet_mask[i] = bin_to_dec(str(decimal))
        i += 1

    print("Mascara de subred adaptada: {}".format(subnet_mask))
    mask_inf[0] = subnet_mask
    mask_inf[1] = pos
    return mask_inf


# //////////////////////////////Subnet functions//////////////////////////////////

# Return the segment of binary numbers (eight) which changes in the subnet mask
def modify_8_bits_segment(n, binary_segment):

    # Arr with the new changes (the segment and the n var)
    modification_info = [0] * 2
    i = 0

    # Zero segment case
    if binary_segment == '0':
        # reset var
        binary_segment = ''
        while n > 0:
            # append a 1
            binary_segment += '1'
            i += 1
            # Substract one bit
            n -= 1
        if len(binary_segment) < 8:
            while len(binary_segment) < 8:
                # append a 0
                binary_segment += '0'

    else:
        # Convert the string segment into a list
        binary_segment = list(binary_segment)
        while (i < 8) and (n > 0):
            if binary_segment[i] == '0':
                # append a 1
                binary_segment[i] = '1'
                i += 1
                # Substract one bit
                n -= 1
            else:
                i += 1

        # Convert the list into a string
        binary_segment = ''.join(binary_segment)

    # Segment that gonna replace the older segment (in binary)
    binary = bin(int(binary_segment, 2))
    # Convert the binary into decimal system
    decimal = bin_to_dec(binary)

    # Save the data
    modification_info[0] = decimal
    modification_info[1] = n

    return modification_info

# Return the new subnet mask
def adapted_subnet_mask(subnet_mask, n):

    i = 0
    # Array with the subnet mask inf.
    mask_inf = []
    # Array with the new changes (new segment and the n var)
    modification_info = [0] * 2

    while i < 4:

        if subnet_mask[i] < 255:
            # Convert the integer segment to binary segment
            binary_segment = dec_to_bin(subnet_mask[i])
            # Modify the segment
            modification_info = modify_8_bits_segment(n, binary_segment)

            subnet_mask[i] = modification_info[0]
            n = modification_info[1]

            # Break in case the n number becomes 0
            if n == 0:
                break
            else:
                i += 1
        else:
            i += 1

    mask_inf.append(subnet_mask)           # Subnet mask
    mask_inf.append(i)                     # Position of the last modified segment

    print("Adapted subnet mask: {}".format(subnet_mask))
    return mask_inf

# //////////////////////////////General functions/////////////////////////////////

# Return a converted decimal number into decimal number
def bin_to_dec(x):
    return int(x, 2)

# Return a converted binary number into decimal number
def dec_to_bin(x):
    return f'{x:b}'

# Function to split any string according to the parameter
def split_input_data(ip):
    ip = ip.split('.')

    # Input size verify
    # Return -1 in case of wrong size
    if len(ip) != 4:
        ip = -1
        #ip = string_to_int_Arr(ip)

    return ip

# Convert a string array (the member integer numbers) into an int array
def string_to_int_Arr(ipA):
    i = 0

    while i < 4:
        temp = int(ipA[i])
        ipA[i] = temp
        i += 1

# Return the incremental number for the subnet list
def increment_num(mask_inf):

    i = 1
    while True:
        # Search the position of the last modified segment
        if int(mask_inf[1]) == i:  
            inc = 256-int(mask_inf[0][i])
            break
        else:
            i += 1

    print("Increment number: {}\n".format(inc))
    return inc

#Return a matrix of the IP to easier handle of it
def eight_bits(ipA):

    #Initialize the matrix
    temp_ipA = [''] * 8, [''] * 8, [''] * 8, [''] * 8
    i = 0
    j = 1
    
    temp = ''
    while i < 4:
        ipA[i] = dec_to_bin(ipA[i])
        if len(ipA[i]) < 8:
            while j <= (8-len(ipA[i])):
                temp += '0'
                j += 1
        temp += str(ipA[i])
        ipA[i] = temp
        j = 1
        i += 1
        temp = ''

    i = 0
    j = 0
    while i < 4:
        j = 0
        while j < 8:
            temp_ipA[i][j] = ipA[i][j]
            j += 1
        i += 1

    return temp_ipA

# Return the number of zeros which gonna change in the subnet mask.
def get_n(num_host_request, operation_type):

    # Number of zeros
    n = 0
    # Conditional
    operation_result = 0

    while True:

        # Subnets formula
        if operation_type == 's':
            operation_result = pow(2, n)
        # Host's formula
        elif operation_type == 'h':
            operation_result = (pow(2, n)-2)

        if operation_result >= num_host_request:
            break
        else:
            n = n + 1
    print("n = {}".format(n))
    return n

# Return the ip_class_var of the IP
def ip_class(first_8_Bits):

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

    print("\n\nThe IP belongs to the {} class.\n\n".format(class_arr[ip_class - 1]))
    return ip_class

# Return the net IP (special_subnet_mask_num)
def special_net_ip(ipA, special_mask_num):
    i = 0
    j = 0
    temp = ''

    # Convert the array int into string-hex array
    binary = eight_bits(ipA)

    net_ip = [0] * 4

    # Counter that saves the number of bits to been through the loop
    count = 1
    while i < 4:
        if j < 8:
            if count <= special_mask_num:
                temp += "{0:b}".format(int(binary[i][j]) & 1)
            else:
                temp += "{0:b}".format(int(binary[i][j]) & 0)
            count += 1
            j += 1
        else:
            net_ip[i] = temp
            i += 1
            j = 0
            temp = ''

    i = 0
    while i < 4:
        net_ip[i] = bin_to_dec(bin(int(net_ip[i], 2)))
        i += 1

    print("\n\nLa ip de red de la ip ingresada es: {}".format(net_ip))
    return net_ip

# Return the subnet mask of an IP (special_subnet_mask_num)
def special_subnet_mask(special_mask_num):
    i = 0
    j = 0
    temp_mask_segment = ''
    subnet_mask = [0] * 4

    # Counter that saves the number of bits to been through the loop
    count = 1
    while i < 4:
        if j < 8:
            if count <= special_mask_num:
                temp_mask_segment += '1'
            else:
                temp_mask_segment += '0'
            count += 1
            j += 1
        else:
            subnet_mask[i] = temp_mask_segment
            i += 1
            j = 0
            temp_mask_segment = ''

    i = 0
    while i < 4:
        subnet_mask[i] = bin_to_dec(bin(int(subnet_mask[i], 2)))
        i += 1

    print("La mascara de subred de la ip ingresada es: {}".format(subnet_mask))
    return subnet_mask

# Return the broadcast IP (special_subnet_mask_num)
def special_broadcast_ip(subnet_ip, special_mask_num):

    i = 0
    copy_subnet_ip = [0] * 4
    while i < 4:
        copy_subnet_ip[i] = subnet_ip[i]
        i += 1

    binary_subnet = eight_bits(copy_subnet_ip)
    broadcast_ip = [0] * 4
    pos_i = special_mask_num // 8
    pos_j = special_mask_num % 8
    i = pos_i
    j = pos_j
    k = 0
    temp = [''] * 8

    while k < j:
        temp[k] += binary_subnet[i][k]
        k += 1

    k = 0
    while i < 4:
        if j < 8:
            temp[j] = "1"
            j += 1

        else:
            while k < 8:
                binary_subnet[i][k] = temp[k]
                k += 1
            k = 0
            j = 0
            i += 1
            temp = [''] * 8

    i = 0
    temp = ''
    while i < 4:
        j = 0
        temp = ''
        while j < 8:
            temp += str(binary_subnet[i][j])
            j += 1
        broadcast_ip[i] = bin_to_dec(bin(int(temp, base=2)))
        i += 1

    print("Broadcast ip: {}\n\n".format(broadcast_ip))

# Return the net IP (default_subnet_mask_num)
def net_ip_func(ipA, subnet_mask):
    i = 0
    binary = eight_bits(ipA)
    binary_subnet_mask = eight_bits(subnet_mask)
    net_ip = [''] * 4
    aux = ''

    while i < 4:
        temp = [''] * 8
        j = 0
        while j < 8:
            temp[j] = "{0:b}".format(
                int(binary[i][j]) & int(binary_subnet_mask[i][j]))
            aux += temp[j]
            j += 1

        net_ip[i] = aux
        aux = ''
        i += 1

    i = 0
    while i < 4:
        j = 0
        temp = ''
        while j < 8:
            temp += str(binary_subnet_mask[i][j])
            j += 1
        net_ip[i] = bin_to_dec(bin(int(net_ip[i], base=2)))
        subnet_mask[i] = bin_to_dec(bin(int(temp, base=2)))
        i += 1

    print("La ip de red de la ip ingresada es: {}".format(net_ip))

    return net_ip

# Return the subnet mask (default_subnet_mask_num)
def default_mask(ip_class):
    #Note:ip_class represent the letter of the class (A = 1, B = 2, C = 3) 
    
    i = 0
    subnet_mask = [0] * 4

    #Making the subnet mask
    while i < ip_class:
        subnet_mask[i] = 255
        i += 1
    
    print("\n\nSubnet mask: {}".format(subnet_mask))
    return subnet_mask

# Return the broadcast IP (default_subnet_mask_num)
def ip_broadcast_func(subnet_ip, ip_class_var):

    i = 0
    copy_subnet_ip = [0] * 4
    while i < 4:
        copy_subnet_ip[i] = subnet_ip[i]
        i += 1

    binary_subnet = eight_bits(copy_subnet_ip)
    broadcast_ip = [0] * 4

    i = ip_class_var
    while i < 4:
        j = 0
        while j < 8:
            binary_subnet[i][j] = "1"
            j += 1
        i += 1

    i = 0
    temp = ''
    while i < 4:
        j = 0
        temp = ''
        while j < 8:
            temp += str(binary_subnet[i][j])
            j += 1
        broadcast_ip[i] = bin_to_dec(bin(int(temp, base=2)))
        i += 1
    print("Broadcast ip: {}\n\n".format(broadcast_ip))

# Function to make sure if the input data (The IP) are correct
def limits_check(ipA):

    # Verifying first the var content (case: wrong data)
    if ipA == -1:
        anws = False

    else:
        anws = True
        i = 0
        while i < 4:
            # Verifying the array content (it's an IP?)
            if (ipA[i].isdigit() == True) and (int(ipA[0]) != 0) and (int(ipA[i]) >= 0) and (int(ipA[i]) < 256):
                i += 1
            else:
                anws = False
                break

    return anws

# Function in case of the user press ctrl + c to exit
def signal_handler(sig, frame):
    print("\nThe execution of the program has been interrupted.")
    print("The program has finalized.")
    exit()

# Verify if the IP isn't overflowed
def fix_ip(net_ip):
    i = 3

    # Loop to increase correctly every increment number
    while i > 0:
        # Check if the current position its overflowed
        if net_ip[i] == 256:
            # Set 0 to current position and add a 1 to the previous one
            net_ip[i] = 0
            net_ip[i - 1] += 1
        i-= 1

# Generate broadcast IP for every subnet
def make_broadcast(broadcast_subnet_ip, pos, increment_num):
    
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
def set_ready(net_ip, tmp_subnet_ip, broadcast_subnet_ip, subnet_list, arr_pos):

    i = 0

    # Fuction to verify if the IP isn't overflowed
    fix_ip(net_ip)

    # Prepare the broadcast IP and the temporal subnet IP for the next step
    while i < 4:
        tmp_subnet_ip[i] = net_ip[i]
        broadcast_subnet_ip[i] = net_ip[i]
        i += 1

    # Generate the broadcast IP (previously prepared) 
    # with the information in the subnet_list array
    # for the range operations
    make_broadcast(broadcast_subnet_ip, subnet_list[arr_pos][1], subnet_list[arr_pos][2])

# Print the subnet list
def generate_list(subnet_list, net_ip):

    i = 0
    # Number of total prints (inizialiced) 
    total_prints = 0
    # Individual broadcast of each subnet
    broadcast_subnet_ip = [0] * 4
    
    # This are the temporal subnet IP & broadcast subnet IP initialized
    tmp_subnet_ip = [0] * 4
    tmp_broadcast_subnet_ip = [0] * 4
    
    #Size represent the number of subnets without repetition in the array
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
    
    #Printing the list 
    while i < total_prints:
        while j < subnet_list[k][0]:
            if j == 0:
                # Initial case (the original IP doesn't been modified)
                if i == 0:
                    # Prepare the inserted IPs in the function
                    set_ready(net_ip, tmp_subnet_ip, broadcast_subnet_ip, subnet_list, k)
                    
                else:
                    # Second case (The first subnet to print for the current network)       
                    net_ip[subnet_list[k-1][1]] += subnet_list[k-1][2]
                    # Prepare the inserted IPs in the function
                    set_ready(net_ip, tmp_subnet_ip, broadcast_subnet_ip, subnet_list, k)
                    
            else:
                # Third case (The remaining subnets to print in the current network)
                net_ip[subnet_list[k][1]] += subnet_list[k][2]
                # Prepare the inserted IPs in the function
                set_ready(net_ip, tmp_subnet_ip, broadcast_subnet_ip, subnet_list, k)                
            
            # Position int the array for the broadcast IPs
            l = 0
            # Copy the broadcast IP to a temporary one for range operations 
            while l < 4:
                tmp_broadcast_subnet_ip[l] = broadcast_subnet_ip[l]
                l += 1
            l = 0

            #Range of hosts for the current subnet
            range_h = range_hosts(tmp_subnet_ip, tmp_broadcast_subnet_ip, subnet_list[k][1])

            print("  {}\t    {}\t{}      \t{}".format(i, net_ip, range_h, broadcast_subnet_ip))
            i += 1
            j += 1

        k += 1
        j = 0

# Obtain the range of hosts for the current subnet
def range_hosts(net_ip, broadcast_subnet_ip, subnet_pos):

    
    r = [0] * 2
    if subnet_pos != 3:
        i = 3
    else:
        i = subnet_pos

    net_ip[i] += 1
    broadcast_subnet_ip[i] -= 1
    r[0] = net_ip
    r[1] = broadcast_subnet_ip

    return r

# Set the IP and return it splitted
def set_the_ip():
    ip = input("Set the IP: ")
    # Trying to split the IP in 4 parts
    return split_input_data(ip)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Main_Function>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def main():

    signal(SIGINT, signal_handler)    
    ################# Banner block ################
    # Open the banner file (READ_ONLY)            #
    fp = open("banner.ban", "r", encoding='UTF-8')#
    # Display the banner                          #
    print(fp.read())                              #
    ###############################################

    while True:
        answer = input(
            "\n---------------> Generate subnets only with the IP or subnets based on hosts? \n---------------> IP Only = i\tHosts = h\n#R: ")
        if answer == 'h' or answer == 'i':
            break
        else:
            print("\nInput data error!")

    i = 0
    ipA = set_the_ip()
    # Loop to set a correct IP
    while limits_check(ipA) == False:
        print(
            "\nThe input data doesn't look like an IP address.\nPlease set a correct one.\n")
        ipA = set_the_ip()

    # Convert the string array into an int array
    string_to_int_Arr(ipA)

    # Getting the class of the IP
    ip_class_var = ip_class(ipA[0])

    while True:
        if ip_class_var == 4 or ip_class_var == 5:
            print("Exception: Classes D & E are only used for Multicasting and Military Purposes.")
            exit()
        else:
            # Asking the type of subnet mask (ssnm = special subnet mask)
            ssnm = input(
                "The IP have a special subnet mask? \n\t y = yes\tn = no (set the standard subnet mask)\n#R:")

        if ssnm.lower() == 'y':

            while True:
                special_mask_num = input(
                    "\nEnter the subnet mask number below: ")

                # Verifying the input data
                if (special_mask_num.isdigit()) and (int(special_mask_num) > 0) and (int(special_mask_num) <= 32):
                    special_mask_num = int(special_mask_num)
                    break
                else:
                    print(
                        "\nIllegal value for subnet mask! Please enter a valid number.")

            net_ip = special_net_ip(ipA, special_mask_num)  # Net IP
            subnet_mask = special_subnet_mask(special_mask_num)  # Subnet Mask
            special_broadcast_ip(net_ip, special_mask_num)  # Broadcast IP
            break

        elif ssnm.lower() == 'n':

            subnet_mask = default_mask(ip_class_var)  # Net IP
            net_ip = net_ip_func(ipA, subnet_mask)  # Subnet Mask
            ip_broadcast_func(net_ip, ip_class_var)  # Broadcast IP
            break

        else:
            print("\nError: Invalid option. Select one of the following options: ")

    # According to the first question (subnet or host) make the respective operations
    # Subnet case
    if answer == 'i':

        # Temporal data array with the information of the subnet
        temp_subnet = [0] * 3

        # Number of subnets to generate
        while True:
            subnet_num = input(
                "Enter the number of subnets you want to generate: ")
            if subnet_num.isdigit() and int(subnet_num) > 0:
                break
            else:
                print("Invalid input!")

        # Array with the data for print the list
        subnet_list = []

        temp_subnet[0] = int(subnet_num)  # Number of subnets to generate
        # Number of zeros which gonna change in the subnet mask.
        n = get_n(int(subnet_num), 's')
        # Obtaining the subnet mask information
        mask_inf = adapted_subnet_mask(subnet_mask, n)
        # Position of the last modified segment of 8 bits
        temp_subnet[1] = mask_inf[1]
        inc_num = increment_num(mask_inf)  # Incremental number for the subnet
        temp_subnet[2] = inc_num
        subnet_list.append(temp_subnet)
        # Generate and print the subnet list
        generate_list(subnet_list, net_ip)

    # Host case
    elif answer == 'h':
        subnet_for_host_num = int(input(
            "¿Cuántas subredes de n-host desea obtener?\t(omitiendo repeticiones)\n#R: "))
        temp_subnet_list = [0] * subnet_for_host_num
        print("")
        while i < subnet_for_host_num:
            print("|//////////////////////////////////////////////////////////////|")
            host_num = int(input(
                "Ingrese el numero de hosts que desea obtener para la red núm. {}: ".format(i+1)))
            subnet_num = int(
                input("¿Cuántas subredes de {} hosts desea obtener?\n#R: ".format(host_num)))

            temp_subnet = [0] * 4
            host_data = get_hosts(host_num)
            temp_subnet[0] = subnet_num  # Subnet No. request
            temp_subnet[1] = host_data[1]
            temp_subnet[2] = host_data[2]
            temp_subnet[3] = host_num
            temp_subnet_list[i] = temp_subnet
            i += 1
            print("|//////////////////////////////////////////////////////////////|")

        # Sorting the subnet list to descending form
        sorted_subnet_list = sorted(
            temp_subnet_list, key=itemgetter(3), reverse=True)
        final_subnet_list = [0] * subnet_for_host_num

        i = 0

        # Saving the final data in the array for print (sorted)
        while i < subnet_for_host_num:
            temp_subnet = [0] * 3
            temp_subnet[0] = sorted_subnet_list[i][0]
            temp_subnet[1] = sorted_subnet_list[i][1]
            temp_subnet[2] = sorted_subnet_list[i][2]
            final_subnet_list[i] = temp_subnet
            i += 1
       
        generate_list(final_subnet_list, net_ip)

#Start point
main()
