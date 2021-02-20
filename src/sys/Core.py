import src.tools.IPOp as IPOp

from operator import itemgetter

class System:
    _ip = None

    def __init__(self):
        super().__init__()
        self._ip = IPOp.IP()

    # According to the first question (subnet or host) make the respective operations
    def executeOp(self, Op: str, triada: list) -> None:
        # Subnet case
        if Op == 'i':
            # Temporal data array with the information of the subnet
            temp_subnet = [0] * 3
            # Number of subnets to generate
            while True:
                subnets_num = input(
                    " Number of subnets to print => Range (0, N)\n N: ")
                if subnets_num.isdigit() and int(subnets_num) >= 0:
                    break
                else:
                    print(" Error: Invalid number.")
            # Array with the data for print the list
            subnet_list = []
            # Number of subnets to generate
            temp_subnet[0] = int(subnets_num) + 1
            # Number of zeros which gonna change in the subnet mask.
            n = self._ip.get_n(int(subnets_num), 's')
            # Obtaining the subnet mask information
            mask_inf = self._ip.adapted_subnet_mask(triada[1], n)
            # Position of the last modified octet of 8 bits
            temp_subnet[1] = mask_inf[1]
            # Incremental number for the subnet
            inc_num = self._ip.incrementNo(mask_inf)
            temp_subnet[2] = inc_num
            # Save the temporal data array with the information of the subnet
            subnet_list.append(temp_subnet)
            # Generate and print the subnet list
            self._ip.generate_list(subnet_list, triada[0])
        # Host case
        elif Op == 'h':
            # Verifying the input data
            is_a_number = None
            while True:
                subnets_num = input(
                    " How many subnets of n-hosts do you want generate?\t(omitting repetitions)\n #: ")
                subnets_num, is_a_number = self._ip.number_request_verification(
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
                    hosts_no, is_a_number = self._ip.number_request_verification(
                        hosts_no)
                    if is_a_number == True:
                        break
                while True:
                    no_subnets_of_n_hosts = input(
                        " How many subnets of {} hosts do you want to obtain?\n #: ".format(hosts_no))
                    no_subnets_of_n_hosts, is_a_number = self._ip.number_request_verification(
                        no_subnets_of_n_hosts)
                    if is_a_number == True:
                        break
                # Temporal array for the every subnet information
                temp_subnet = [0] * 4
                # Array with host data
                host_data = [0] * 3
                # Number of zeros which gonna change in the subnet mask.
                host_data[0] = self._ip.get_n(int(hosts_no), 'h')
                # Obtaining the subnet mask information
                mask_inf = self._ip.adapted_subnet_mask_case_host(host_data[0])
                # Position of the last modified octet of 8 bits
                host_data[1] = mask_inf[1]
                # Incremental number for the subnet
                host_data[2] = self._ip.incrementNo(mask_inf)
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
            self._ip.generate_list(final_subnet_list, triada[0])

    # 
    def setTheMainOperation(self) -> str:
        while True:
            print("\n\n                    Generate: ")
            print("     i -> Subnets with an IP.")
            print("     h -> Subnets with a host number requirement.\n")
            opType = input(" #: ")
            if opType == 'h' or opType == 'i':
                break
            else:
                print("\n Error: invalid option.")
        return opType 

    # Function in case of the user press ctrl + c to exit   
    def signal_handler(self, signum, frame) -> None:
        print("\n\n Warning: Execution was interrupted.")
        print(" Killing process . . .\n (X_X) -> EXIT_CODE: 0xDEAD")
        exit()
