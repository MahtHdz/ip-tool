from math import pow
from operator import itemgetter
from signal import SIGINT, signal


# ///////////////////////////////Host functions///////////////////////////////////


def get_hosts(host_num):
    """ Array with host data """
    host_data = [0] * 3

    host_data[0] = get_n(int(host_num), 'h')        # Number of zeros in the subnet mask.
    mask_inf = adapted_mask_host(host_data[0])      # Position
    host_data[1] = mask_inf[1]
    host_data[2] = increment_num(mask_inf)

    return host_data


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

#Return the segment of binary numbers (eight) which changes in the subnet mask
def modify_8_bits_segment(n, binary_segment):
    
    #Arr with the new changes (the segment and the n var)
    modification_info = [0] * 2
    i = 0
    
    #Case the segment is == 0
    if binary_segment == '0':
        #reset var
        binary_segment = ''
        while n > 0:
            #append a 1
            binary_segment += '1'
            i += 1
            #Substract one bit
            n -= 1
        if len(binary_segment) < 8:
            while len(binary_segment) < 8:
                #append a 0
                binary_segment += '0'

    else:
        #Convert the string segment into a list
        binary_segment = list(binary_segment)
        while (i < 8) and (n > 0):
            if binary_segment[i] == '0':
                #append a 1
                binary_segment[i] = '1'
                i += 1
                #Substract one bit
                n -= 1
            else:
                i += 1

        #Convert the list into a string
        binary_segment = ''.join(binary_segment)
    
    #Segment that gonna replace the older segment (in binary)
    binary = bin(int(binary_segment, 2))
    #Convert the binary into decimal system
    decimal = bin_to_dec(binary)

    #Save the data
    modification_info[0] = decimal
    modification_info[1] = n
    
    return modification_info

#Return the new subnet mask
def adapted_subnet_mask(subnet_mask, n):

    i = 0
    #Array with the subnet mask inf.
    mask_inf = []
    #Array with the new changes (new segment and the n var)
    modification_info = [0] * 2

    while i < 4:
        
        if subnet_mask[i] < 255:
            #Convert the integer segment to binary segment
            binary_segment = dec_to_bin(subnet_mask[i])
            #Modify the segment
            modification_info = modify_8_bits_segment(n, binary_segment)
            
            subnet_mask[i] = modification_info[0]
            n = modification_info[1]
            
            #Break in case the n number becomes 0
            if n == 0:
                break
            else:
                i += 1
        else:
            i += 1
    
    mask_inf.append(subnet_mask)        #Subnet mask
    mask_inf.append(i)                  #Position of the last modified segment

    print("Adapted subnet mask: {}".format(subnet_mask))
    return mask_inf


# //////////////////////////////General functions/////////////////////////////////

#Return a converted decimal number into decimal number
def bin_to_dec(x):
    return int(x, 2)

#Return a converted binary number into decimal number
def dec_to_bin(x):
    return f'{x:b}'

#Function to split any string according to the parameter
def split_input_data(ip):
    ip = ip.split('.')
    
    #Input size verify
    #Return -1 in case of wrong size
    if len(ip) != 4:
        ip = -1
        #ip = string_to_int_Arr(ip)

    return ip

#Convert a string array (of integer numbers) into an int array 
def string_to_int_Arr(ipA):
    i = 0
    
    while i < 4:
        temp = int(ipA[i])
        ipA[i] = temp
        i += 1

#Return the default subnet mask for class A
def A():
    subnet_mask = [0] * 4
    subnet_mask[0] = 255
    return subnet_mask

#Return the default subnet mask for class B
def B():
    i = 0
    subnet_mask = [0] * 4
    while i < 2:
        subnet_mask[i] = 255
        i += 1
    return subnet_mask

#Return the default subnet mask for class C
def C():
    i = 0
    subnet_mask = [0] * 4
    while i < 3:
        subnet_mask[i] = 255
        i += 1
    return subnet_mask

#Return the incremental number for the subnet list
def increment_num(mask_inf):
    
    i = 1
    while True:
        if int(mask_inf[1]) == i:                #Search the position of the last modified segment
            inc = 256-int(mask_inf[0][i])
            break
        else:
            i += 1
    
    print("Increment number: {}\n".format(inc))
    return inc


def eight_bits(ipA):
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

#Return the number of zeros which gonna change in the subnet mask.
def get_n(num_host_request, operation_type):
    
    #Number of zeros
    n = 0
    #Conditional
    operation_result = 0
    
    while True:

        #Subnets formula
        if operation_type == 's':
            operation_result = pow(2, n)
        #Host's formula
        elif operation_type == 'h':
            operation_result = (pow(2, n)-2)
        
        if  operation_result >= num_host_request:
            break
        else:
            n = n + 1
    print("n = {}".format(n))
    return n

#Return the category of the IP
def ip_category(first_8_Bits):

    if (first_8_Bits >= 1) and (first_8_Bits <= 127):
        print("\n\nThe IP belongs to the A class.\n\n")
        ip_class = 1
    elif (first_8_Bits >= 128) and (first_8_Bits <= 191):
        print("\n\nThe IP belongs to the B class.\n\n")
        ip_class = 2
    elif (first_8_Bits >= 192) and (first_8_Bits <= 223):
        print("\n\nThe IP belongs to the C class.\n\n")
        ip_class = 3
    elif (first_8_Bits >= 224) and (first_8_Bits <= 239):
        print("\n\nThe IP belongs to the D class.\n\n")
        ip_class = 4
    elif (first_8_Bits >= 240) and (first_8_Bits <= 255):
        print("\n\nThe IP belongs to the E class.\n\n")
        ip_class = 5
    return ip_class

#Return the net IP (special_subnet_mask_num)
def special_net_ip(ipA, special_mask_num):
    i = 0
    j = 0
    temp = ''

    #Convert the array int into string-hex array
    binary = eight_bits(ipA)

    net_ip = [0] * 4

    #Counter who saves the number of bits to been through the loop
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

#Return the subnet mask of an IP (special_subnet_mask_num)
def special_subnet_mask(special_mask_num):
    i = 0
    j = 0
    temp_mask_segment = ''
    subnet_mask = [0] * 4

    #Counter who saves the number of bits to been through the loop
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

#Return the broadcast IP (special_subnet_mask_num)
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

#Return the net IP (default_subnet_mask_num)
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

#Return the subnet mask (default_subnet_mask_num)
def default_mask(ip_class):
    switcher = {
        1: A,
        2: B,
        3: C,
    }
    func = switcher.get(ip_class, lambda: "Invalid option.")
    print("\n\nSubnet mask: {}".format(func()))
    return func()

#Return the broadcast IP (default_subnet_mask_num)
def ip_broadcast_func(subnet_ip, category):

    i = 0
    copy_subnet_ip = [0] * 4
    while i < 4:
        copy_subnet_ip[i] = subnet_ip[i]
        i += 1

    binary_subnet = eight_bits(copy_subnet_ip)
    broadcast_ip = [0] * 4

    i = category
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

#Function to make sure if the input data (The IP) are correct
def limits_check(ipA):

    #Verifying first the var content (case: wrong data)
    if ipA == -1:
        anws = False

    else:
        anws = True
        i = 0
        while i < 4:
            #Verifying the array content (it's an IP?)
            if (ipA[i].isdigit() == True) and (int(ipA[0]) != 0) and (int(ipA[i]) >= 0) and (int(ipA[i]) < 256) :
                i += 1
            else:
                anws = False
                break

    return anws


def auto_increment_decrement(ip, type_op, pos, increment_num, subnet_num_pos):

    i = 0
    if type_op == 'i':
        while i < 4:
            if ip[i] > 255:
                if i == 1:
                    print("¡El rango de la dirección ip se a excedido!")
                else:
                    ip[i] = 0
                    i -= 1
                    ip[i] = ip[i] + 1
                    i += 1
            else:
                i += 1

    elif type_op == 'd':

        if pos == 3:
            ip[pos] += increment_num - 1

        else:

            if subnet_num_pos == True:
                ip[pos] += increment_num - 1

            elif ip[pos] == 0:
                ip[pos] = increment_num - 1

            i = pos + 1
            while i < 4:
                ip[i] = 255
                i += 1

    return ip


def signal_handler(sig, frame):
    print("\nLa ejecución de programa a sido interrumpida.")
    print("El programa a finalizado.")
    exit(0)

#Print the subnet list
def generate_list(subnet_list, net_ip):

    i = 0
    total_prints = 0
    broadcast_ip_subnet = [0] * 4
    tmp_subnet_ip = [0] * 4
    tmp_broadcast_ip_subnet = [0] * 4
    size = len(subnet_list)
    while i < size:
        total_prints += subnet_list[i][0]
        i += 1

    i = 0
    j = 0
    k = 0
    l = 0

    print(" Red\t\tIP-red\t\t\t\tRango\t\t\t\t    Broadcast")
    while i < total_prints:

        while j < subnet_list[k][0]:

            if j == 0:

                if i == 0:
                    auto_check_and_copy(broadcast_ip_subnet,
                                        net_ip, tmp_subnet_ip)
                    auto_increment_decrement(
                        broadcast_ip_subnet, 'd', subnet_list[k][1], subnet_list[k][2], False)

                else:
                    net_ip[subnet_list[k-1][1]] += subnet_list[k-1][2]
                    auto_check_and_copy(broadcast_ip_subnet,
                                        net_ip, tmp_subnet_ip)
                    auto_increment_decrement(
                        broadcast_ip_subnet, 'd', subnet_list[k][1], subnet_list[k][2], True)

            else:
                net_ip[subnet_list[k][1]] += subnet_list[k][2]
                auto_increment_decrement(net_ip, 'i', 0, 0, False)
                auto_check_and_copy(broadcast_ip_subnet, net_ip, tmp_subnet_ip)
                auto_increment_decrement(
                    broadcast_ip_subnet, 'd', subnet_list[k][1], subnet_list[k][2], True)

            while l < 4:
                tmp_broadcast_ip_subnet[l] = broadcast_ip_subnet[l]
                l += 1

            l = 0
            range_h = range_hosts(
                tmp_subnet_ip, tmp_broadcast_ip_subnet, subnet_list[k][1])
            print("  {}\t    {}\t{}      \t{}".format(
                i, net_ip, range_h, broadcast_ip_subnet))
            i += 1
            j += 1

        k += 1
        j = 0


def auto_check_and_copy(broadcast_ip_subnet, net_ip, tmp_subnet_ip):

    i = 0
    auto_increment_decrement(net_ip, 'i', 0, 0, False)
    while i < 4:
        tmp_subnet_ip[i] = net_ip[i]
        broadcast_ip_subnet[i] = net_ip[i]
        i += 1


def range_hosts(net_ip, broadcast_ip_subnet, subnet_pos):

    r = [0] * 2
    if subnet_pos != 3:
        i = 3
    else:
        i = subnet_pos

    net_ip[i] += 1
    broadcast_ip_subnet[i] -= 1
    r[0] = net_ip
    r[1] = broadcast_ip_subnet

    return r


def set_the_ip():
    ip = input("Set the IP: ")
    #Trying to split the IP in 4 parts
    return split_input_data(ip)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Main_Function>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def main(answer):

    i = 0
    ipA = set_the_ip()
    #Loop to set a correct IP 
    while limits_check(ipA) == False:
        print("\nThe input data doesn't look like an IP address.\nPlease set a correct one.\n")
        ipA = set_the_ip()
    
    #Convert the string array into an int array
    string_to_int_Arr(ipA)
    
    #Getting the IP's category
    category = ip_category(ipA[0])

    while True:
        #Classes D & E exception (Classes without default subnet mask)
        if category == 4 or category == 5:
            #Asssign directly the answer to the question below
            ssnm = 'y'
        else:
            #Asking the type of subnet mask (ssnm = special subnet mask)
            ssnm = input(
                "The IP have a special subnet mask? \n\t y = yes\tn = no (set the standard subnet mask)\n#R:")
    
        if ssnm.lower() == 'y':

            while True:
                special_mask_num = input("\nEnter the subnet mask number below: ")
                
                #Verifying the input data
                if (special_mask_num.isdigit()) and (int(special_mask_num) > 0) and (int(special_mask_num) <= 32):
                    special_mask_num = int(special_mask_num)
                    break 
                else:
                    print(
                        "\nIllegal value for subnet mask! Please enter a valid number.")

            net_ip = special_net_ip(ipA, special_mask_num)         #Net IP
            subnet_mask = special_subnet_mask(special_mask_num)    #Subnet Mask
            special_broadcast_ip(net_ip, special_mask_num)         #Broadcast IP
            break

        elif ssnm.lower() == 'n':

            subnet_mask = default_mask(category)                   #Net IP
            net_ip = net_ip_func(ipA, subnet_mask)                 #Subnet Mask
            ip_broadcast_func(net_ip, category)                    #Broadcast IP
            break

        else:
            print("\nError! Invalid option. Select one of the following options: ")

    #According to the first question (subnet or host) make the respective operations
    #Case subnet 
    if answer == 's':

        #Temporal data array with the information of the subnet
        temp_subnet = [0] * 3 
        
        #Number of subnets to generate
        while True:
            subnet_num = input("Enter the number of subnets you want to generate: ")
            if subnet_num.isdigit() and int(subnet_num) > 0:
                break
            else:
                print("Invalid input!")

        #Array with the data for print the list
        subnet_list = []
        
        temp_subnet[0] = int(subnet_num)                      #Number of subnets to generate
        #Number of zeros which gonna change in the subnet mask.
        n = get_n(int(subnet_num), 's')                       
        mask_inf = adapted_subnet_mask(subnet_mask, n)        #Obtaining the subnet mask information
        temp_subnet[1] = mask_inf[1]                          #Position of the last modified segment of 8 bits
        inc_num = increment_num(mask_inf)                     #Incremental number for the subnet
        temp_subnet[2] = inc_num                              
        subnet_list.append(temp_subnet)
        generate_list(subnet_list, net_ip)                    #Generate and print the subnet list
    
    #Case host
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
        print("\n#################################################################################################")

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Init_code>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
signal(SIGINT, signal_handler)

################# Banner block #################
#Open the banner file (READ_ONLY)              #
fp = open("banner.ban", "r", encoding='UTF-8') #
# Display the banner                           #
print(fp.read())                               #
################################################

while True:
    answer = input(
        "\n---------------> Generate subnets only with the IP or subnets based on hosts? \n---------------> Subnets = s\tHosts = h\n#R: ")
    if answer == 'h' or answer == 's':
        break
    else:
        print("\nInput data error!")

main(answer)
