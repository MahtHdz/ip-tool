from math import pow
from operator import itemgetter
from signal import SIGINT, signal

#///////////////////////////////////////////////////////////////////////////////
def get_n_host(num):
    i = 0
    while True:
        if (pow(2,i)-2) >= num:
            break
        i=i+1
    print("n = {}".format(i))
    return i

def get_hosts(host_num):

    host_data = [0] * 3
    mask_inf = [0] * 2

    host_data[0] = get_n_host(int(host_num))
    mask_inf = adapted_mask_host(host_data[0])
    host_data[1] = mask_inf
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
        i+=1

    print("Mascara de subred adaptada: {}".format(subnet_mask))
    mask_inf[0] = subnet_mask
    mask_inf[1] = pos
    return mask_inf

#///////////////////////////////////////////////////////////////////////////////

def get_n_subnet(num):
    i = 0
    while True:
        if num == 0:
            break
        if pow(2,i) >= num:
            break
        i=i+1
    print("n = {}".format(i))
    return i

def pos_subnet_mask(i, subnet_mask, decimal):
    mask_inf = []
    subnet_mask[i] = decimal
    mask_inf.append(subnet_mask)
    mask_inf.append(i)
    return mask_inf

def change_binary_subnet(n):
    i = 1
    final= ''
    while i <= n:
        final+='1'
        i+=1
    while len(final) < 8:
        final+='0'
    return final

def adapted_mask_subnet(subnet_mask, n):
    mask_inf = []
    if n == 0:
        mask_inf.append(subnet_mask)
        mask_inf.append(str(n))
    else:
        binary = bin(int(change_binary_subnet(n), 2))
        decimal = bin_to_dec(binary)
        if int(subnet_mask[1]) == 0:
            mask_inf = pos_subnet_mask(1, subnet_mask, decimal)

        elif int(subnet_mask[2]) == 0:
            mask_inf = pos_subnet_mask(2, subnet_mask, decimal)

        elif int(subnet_mask[3]) == 0:
            mask_inf = pos_subnet_mask(3, subnet_mask, decimal)

    print("Mascara de subred adaptada: {}".format(subnet_mask))
    return mask_inf

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
def bin_to_dec(x):
    return int(x, 2)

def dec_to_bin(x):
    return f'{x:b}'

def split_string(ip):
    ip = ip.split('.')
    if len(ip) == 4:
        ip = string_int_A(ip)
    else:
        ip = -1

    return ip

def int_string_A(ip):
    i = 0
    ip_str = [0] * 4
    while i < 4:
        ip_str[i] = str(ip[i])
        i += 1
    return ip_str

def string_int_A(ip):
    i = 0
    ip_int = [0] * 4
    while i < 4:
        ip_int[i] = int(ip[i])
        i += 1
    return ip_int

def A():
    subnet_mask = [0] * 4
    subnet_mask[0] = 255
    return subnet_mask

def B():
    i = 0
    subnet_mask = [0] * 4
    while i < 2:
        subnet_mask[i] = 255
        i += 1
    return subnet_mask

def C():
    i = 0
    subnet_mask = [0] * 4
    while i < 3:
        subnet_mask[i] = 255
        i += 1
    return subnet_mask

def default_mask(ip_class):
    switcher = {
        1:A,
        2:B,
        3:C,
    }
    func = switcher.get(ip_class, lambda: "Invalid option.")
    print ("Mascara de subred: {}".format(func()))
    return func()

def increment_num(mask_inf):
    inc = 0
    if int(mask_inf[1]) == 0:
        inc = 0
    elif int(mask_inf[1]) == 1:
        inc = 256-int(mask_inf[0][1])
    elif int(mask_inf[1]) == 2:
        inc = 256-int(mask_inf[0][2])
    elif int(mask_inf[1]) == 3:
        inc = 256-int(mask_inf[0][3])
    print("Numero de incremento: {}".format(inc))
    return inc

def eight_bits(ipA):
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
    return ipA

def ip_category(first_8_Bits):
    if (first_8_Bits >= 1) and (first_8_Bits <= 127):
        print("\n\nLa ip pertenece a la clase A.\n\n")
        ip_class = 1
    elif (first_8_Bits >= 128) and (first_8_Bits <= 191):
        print("\n\nLa ip pertenece a la clase B.\n\n")
        ip_class = 2
    elif (first_8_Bits >= 192) and (first_8_Bits <= 223):
        print("\n\nLa ip pertenece a la clase C.\n\n")
        ip_class = 3
    elif (first_8_Bits >= 224) and (first_8_Bits <= 239):
        print("\n\nLa ip pertenece a la clase D.\n\n")
        ip_class = 4
    elif (first_8_Bits >= 240) and (first_8_Bits <= 255):
        print("\n\nLa ip pertenece a la clase E.\n\n")
        ip_class = 5
    return ip_class

def special_net_ip(ipA, special_mask_num):
    i = 0
    j = 0
    temp = ''
    temp_mask_segment = ''
    binary = eight_bits(ipA)
    subnet_ip_and_subnet_mask = [0] * 2
    subnet_mask = [0] * 4
    net_ip = [0] * 4
    count = 1
    while i < 4:
        if j < 8:
            if count <= special_mask_num:
                temp += "{0:b}".format(int(binary[i][j]) & 1)
                temp_mask_segment += '1'
            else:
                temp += "{0:b}".format(int(binary[i][j]) & 0)
                temp_mask_segment += '0'
            count += 1
            j += 1
        else:
            net_ip[i] = temp
            subnet_mask[i] = temp_mask_segment
            i += 1
            j = 0
            temp_mask_segment = ''
            temp = ''

    i = 0
    while i < 4:
        net_ip[i] = bin_to_dec(bin(int(net_ip[i], 2)))
        subnet_mask[i] = bin_to_dec(bin(int(subnet_mask[i], 2)))
        i += 1
    print("La ip de red de la ip ingresada es: {}".format(net_ip))
    print("La mascara de subred de la ip ingresada es: {}".format(subnet_mask))
    subnet_ip_and_subnet_mask[0] = net_ip
    subnet_ip_and_subnet_mask[1] = subnet_mask
    return subnet_ip_and_subnet_mask

def net_ip_func(ipA, subnet_mask):
    i = 0
    j = 0
    temp = ''
    binary = eight_bits(ipA)
    subnet_mask = eight_bits(subnet_mask)
    net_ip = [0] * 4
    while i < 4:
        if j < 8:
            temp += "{0:b}".format(int(binary[i][j]) & int(subnet_mask[i][j]))
            j += 1
        else:
            net_ip[i] = temp
            i += 1
            j = 0
            temp = ''
    i = 0
    while i < 4:
        net_ip[i] = bin_to_dec(bin(int(net_ip[i], 2)))
        subnet_mask[i] = bin_to_dec(bin(int(subnet_mask[i], 2)))
        i += 1
    print("La ip de red de la ip ingresada es: {}".format(net_ip))
    return net_ip

def special_ip_broadcast(subnet_ip, special_mask_num):

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
    temp = ''

    while k < j:
        temp += binary_subnet[i][k]
        k+=1

    while i < 4:
        if j < 8:
            temp += "1"
            j += 1
        else:
            binary_subnet[i] = temp
            i += 1
            j = 0
            temp = ''
    i = 0
    while i < 4:
        broadcast_ip[i] = bin_to_dec(bin(int(binary_subnet[i], 2)))
        i += 1
    print("Broadcast ip: {}".format(broadcast_ip))
    return broadcast_ip

def ip_broadcast_func(subnet_ip, category):

    i = 0
    copy_subnet_ip = [0] * 4
    while i < 4:
        copy_subnet_ip[i] = subnet_ip[i]
        i += 1

    binary_subnet = eight_bits(copy_subnet_ip)
    broadcast_ip = [0] * 4
    i = category
    temp = ''
    j = 0
    while i < 4:
        if j < 8:
            temp += "1"
            j += 1
        else:
            binary_subnet[i] = temp
            i += 1
            j = 0
            temp = ''
    i = 0
    while i < 4:
        broadcast_ip[i] = bin_to_dec(bin(int(binary_subnet[i], 2)))
        i += 1
    print("Broadcast ip: {}".format(broadcast_ip))
    return broadcast_ip

def limits_check(ipA):

    if ipA == -1:
        anws = False
    else:
        anws = True
        i = 0
        while i < 4 :
            if ipA[i] < 256:
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


    return '\x1b[1;37;40m' + text + '\x1b[0m'

def signal_handler(sig, frame):
    print("\nLa ejecución de programa a sido interrumpida.")
    print("El programa a finalizado.")
    exit(0)

def generate_list(subnet_for_host, net_ip):

    i = 0
    total_prints = 0
    broadcast_ip_subnet = [0] * 4
    tmp_subnet_ip = [0] * 4
    tmp_broadcast_ip_subnet = [0] * 4
    size = len(subnet_for_host)
    while i < size:
        total_prints += subnet_for_host[i][0]
        i += 1

    i = 0
    j = 0
    k = 0
    l = 0

    print(" Red\t\tIP-red\t\t\t\tRango\t\t\t\t    Broadcast")
    while i < total_prints:

        while j < subnet_for_host[k][0]:

            if j == 0:

                if  i == 0:
                    auto_check_and_copy(broadcast_ip_subnet, net_ip, tmp_subnet_ip)
                    auto_increment_decrement(broadcast_ip_subnet, 'd', subnet_for_host[k][1], subnet_for_host[k][2], False)

                else:
                    net_ip[subnet_for_host[k-1][1]] += subnet_for_host[k-1][2]
                    auto_check_and_copy(broadcast_ip_subnet, net_ip, tmp_subnet_ip)
                    auto_increment_decrement(broadcast_ip_subnet, 'd', subnet_for_host[k][1], subnet_for_host[k][2], True)

            else:
                net_ip[subnet_for_host[k][1]] += subnet_for_host[k][2]
                auto_increment_decrement(net_ip, 'i', 0, 0, False)
                auto_check_and_copy(broadcast_ip_subnet, net_ip, tmp_subnet_ip)
                auto_increment_decrement(broadcast_ip_subnet, 'd', subnet_for_host[k][1], subnet_for_host[k][2], True)

            while l < 4:
                tmp_broadcast_ip_subnet[l] = broadcast_ip_subnet[l]
                l+= 1

            l = 0
            range_h = range_hosts(tmp_subnet_ip, tmp_broadcast_ip_subnet, subnet_for_host[k][1])
            print("  {}\t    {}\t{}      \t{}".format(i, net_ip, range_h, broadcast_ip_subnet))
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

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
def questions(answer):

    i = 0
    ip = input("Ingrese una dirección ip: ")
    ipA = split_string(ip)

    while limits_check(ipA) == False:
        print("\nLa dirección ip proporcionada no es válida.\n")
        ip = input("Ingrese una dirección ip: ")
        ipA = split_string(ip)

    category = ip_category(ipA[0])
    ssnm = input("¿Su ip tiene una mascara de subred especial? \n\t y = yes\tn = no\n#R:")
    if ssnm.lower() == 'y':

        special_mask_num = int(input("Ingrese el numero de la mascara de subred a continuación: "))
        subnet_ip_and_subnet_mask = special_net_ip(ipA, special_mask_num)
        net_ip = subnet_ip_and_subnet_mask[0]
        subnet_mask = subnet_ip_and_subnet_mask[1]
        ip_broadcast = special_ip_broadcast(net_ip, special_mask_num)

    elif ssnm.lower() == 'n':

        subnet_mask = default_mask(category)
        net_ip = net_ip_func(ipA, subnet_mask)
        ip_broadcast = ip_broadcast_func(net_ip, category)

    else:
        print("Ingrese una opción válida.")
    if answer == 's':
        temp_subnet = [0] * 3
        subnet_num = input("Ingrese el numero de subredes que desea obtener: ")
        subnet_for_subnet = []
        temp_subnet[0] = int(subnet_num)
        n = get_n_subnet(int(subnet_num))
        mask_inf = adapted_mask_subnet(subnet_mask, n)
        temp_subnet[1] = mask_inf[1]
        inc_num = increment_num(mask_inf)
        temp_subnet[2] = inc_num
        subnet_for_subnet.append(temp_subnet)
        generate_list(subnet_for_subnet, net_ip)
    elif answer == 'h':
        subnet_for_host_num = int(input("¿Cuántas subredes de n-host desea obtener?\t(omitiendo repeticiones)\n#R: "))
        temp_subnet_list = [0] * subnet_for_host_num
        
        while i < subnet_for_host_num:
            host_num = int(input("Ingrese el numero de hosts que desea obtener para la red núm. {}: ".format(i+1)))
            subnet_num = int(input("¿Cuántas subredes de {} hosts desea obtener?\n#R: ".format(host_num)))
            
            temp_subnet = [0] * 4
            host_data = get_hosts(host_num)
            temp_subnet[0] = subnet_num
            temp_subnet[1] = host_data[1][1]
            temp_subnet[2] = host_data[2]
            temp_subnet[3] = host_num
            temp_subnet_list[i] = temp_subnet
            i += 1

        print("\n#################################################################################################")
        
        #Sorting the subnet list to descending form
        i = 0
        sorted_subnet_list = sorted(temp_subnet_list, key = itemgetter(3), reverse = True) 
        final_subnet_list = [0] * subnet_for_host_num
        
        while i < subnet_for_host_num:
            temp_subnet = [0] * 3
            temp_subnet[0] = sorted_subnet_list[i][0]
            temp_subnet[1] = sorted_subnet_list[i][1]
            temp_subnet[2] = sorted_subnet_list[i][2]
            final_subnet_list[i] = temp_subnet
            i += 1

        generate_list(final_subnet_list, net_ip)

################################################################################
signal(SIGINT, signal_handler)

fp = open("banner.ban", "r", encoding='UTF-8')

print(fp.read())
answer = input("\n--------------->¿Desea obtener subredes o hosts? \n--------------->Subredes = s\tHosts = h\n#R: ")
while True:
    if answer == 'h' or answer == 's':
        break
    else:
        print("Dato de entrada incorrecto.")
        answer = input(
            "\n--------------->¿Desea obtener subredes o hosts? \n--------------->Subredes = s\tHosts = h\n#R: ")

questions(answer)
