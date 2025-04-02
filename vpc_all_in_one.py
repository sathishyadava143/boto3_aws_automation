#!/usr/bin/python3
import boto3
from botocore.exceptions import ClientError
vpc=boto3.client('ec2')
sts=boto3.client('sts')
def print_str():
    print("**"*50)
def aws_id_fun():
    print_str()
    id=sts.get_caller_identity()
    print(f"AWS_Account_Id: {id.get('Account')}")
def lst_vpc_fun():
    print_str()
    print("Listing VPCs...")
    lin=0
    try:
        lst_vpc=vpc.describe_vpcs()
        for i in lst_vpc.get('Vpcs'):
            lin+=1
            tags = i.get('Tags', [])
            vpc_name = next((tag['Value'] for tag in tags if tag['Key'] == 'Name'), ' - ')
            print(f"{lin}_vpc_id: {i.get('VpcId'):<25} Vpc_TAG: {vpc_name:<25} CIDR_Block: {i.get('CidrBlock')} ")
    except Exception as e:
        print(f"Error:\n {e}")
def lst_sub_fun():
    print_str()
    print("Listing Subnets...")
    lin=0
    try:
        lst_sub=vpc.describe_subnets()
        for i in lst_sub.get('Subnets'):
            lin+=1
            tag =i.get("Tags", [])
            lst_sub_tag= next((tag['Value'] for tag in tag if tag['Key'] == 'Name'), ' - ')
            print(f"{lin}_SubNet_id: {i.get('SubnetId'):<25} Subnet_Tag: {lst_sub_tag:<25} Vpc_Id: {i.get('VpcId'):<25}")
    except Exception as e:
        print(f"Error:\n {e}")
def lst_route_table_fun():
    print_str()
    print("Listing Routetables...")
    lin=0
    try:
        lst_route_table=vpc.describe_route_tables()
        #print(lst_route_table)
        for i in lst_route_table.get('RouteTables'):
            lin+=1
            route_table_id=i.get('RouteTableId')
            Vpc_id=i.get('VpcId')
            tag=i.get('Tags')
            tag_lst=next((tag['Value'] for tag in tag if tag['Key'] == 'Name'),' - ')
            ass_id = "N/A"
            state = "N/A"
            is_main = "No"
            for j in i.get('Associations'):
                ass_id=j.get('RouteTableAssociationId','N/A')
                state=j.get('AssociationState').get('State')
                is_main= "yes" if j.get('Main','False') else "No"
            print(f"{lin}_ Route_table_id: {route_table_id} | Vpc_Id: {Vpc_id} | Tag_Name: {tag_lst:<10} | Association_id: {ass_id} | Assosiation_State: {state} | Main: {is_main}")
    except Exception as e:
        print(f"Error:\n{e}")

def describe_internet_gateway_fun():
    print_str()
    print("Listing InternetGateways...")
    print_str()
    lin=0
    attached=[]
    detached=[]
    try:
        lst_internet_gateway=vpc.describe_internet_gateways()
        #print(lst_internet_gateway)
        for i in lst_internet_gateway.get('InternetGateways'):
            lin+=1
            tags=i.get('Tags')
            tag_value=next((tag['Value'] for tag in tags if tag['Key'] == 'Name'), ' - ')
            internet=i.get('InternetGatewayId')
            if i.get('Attachments'):
                for j in i.get('Attachments',[]):
                    vpc_id=j.get('VpcId',' - ')
                    print(f"{lin}) internet-gateway_id: {internet:<30} Tag_Name: {tag_value:<10} Vpc_Id: {vpc_id}")
            else:
                vpc_id= " - "
                print(f"{lin}) internet-gateway_id: {internet:<30} Tag_Name: {tag_value:<10} Vpc_Id: {vpc_id}")
    except Exception as e:
        print(f"Error:\n {e}")
def allocate_elastic_ip_fun():
    try:
        allocate_ip=vpc.allocate_address(
            Domain='vpc'
        )
        print(f"Elastic_ip allocated successfully!.")
    except Exception as e:
        print(f"Error:\n{e}")
def describe_elastic_ip_fun():
    print("Listing Elastic Ip's ...")
    lin=0
    try:
        lst_elastic_ip=vpc.describe_addresses()
        for i in lst_elastic_ip.get('Addresses'):
            lin+=1
            pub_ip=i.get('PublicIp')
            Allocation_id=i.get('AllocationId')
            if i.get("Tags"):
                for j in i.get('Tags'):
                    tag = j.get('Value'," - ")    
                    print(f"{lin}) Public_Ip: {pub_ip:<20} Allocation_Id: {Allocation_id:<20} Tag_Name: {tag}")
            else:
                print(f"{lin}) Public_Ip: {pub_ip:<20} Allocation_Id: {Allocation_id:<20} Tag_Name: N/A ")
    except Exception as e:
        print(f"Error:\n{e}") 
def describe_nat_gateways_fun():
    print_str()
    print("Listing Nat_Gateways...")
    lin=0
    try:
        lst_nat=vpc.describe_nat_gateways()
        #print(lst_nat)
        for i in lst_nat.get('NatGateways'):
            lin+=1
            nat_id=i.get('NatGatewayId')
            sub_id=i.get('SubnetId')
            vpc_id=i.get('VpcId')
            state=i.get('State')
            if i.get('Tags'):
                for j in i.get('Tags'):
                    tag=j.get('Value')
                    print(f"{lin}) Tag_Name: {tag} | Nat_Gateway_Id: {nat_id:<25} | State: {state:<10}  | Subnet_Id: {sub_id:<25} | Vpc_Id: {vpc_id:<25} ")
            else:
                tag= " - "
                print(f"{lin}) Tag_Name: {tag} | Nat_Gateway_Id: {nat_id:<25} | State: {state:<25}  | Subnet_Id: {sub_id:<25} | Vpc_Id: {vpc_id:<25} ")
    except Exception as e:
        print(f"Error:\n{e}")
def describe_vpc_peering_connections_fun():
    print_str()
    print("Listing Vpc_peering Connections....")
    lin=0
    try:
        lst_vpc_peer_conn=vpc.describe_vpc_peering_connections()
        #print(lst_vpc_peer_conn)
        for i in lst_vpc_peer_conn.get('VpcPeeringConnections'):
            lin+=1
            req_vpc_id=i.get('RequesterVpcInfo').get('VpcId')
            req_owner_id=i.get('RequesterVpcInfo').get('OwnerId')
            accept_vpc_id=i.get('AccepterVpcInfo').get('VpcId')
            accept_owner_id=i.get('AccepterVpcInfo').get('OwnerId')
            vpc_peer_con_id=i.get('VpcPeeringConnectionId')
            if i.get('Tags'):
                for j in i.get('Tags'):
                    tag=j.get('Value')
                    print(f"{lin}) Vpc_Peering_conn_id: {vpc_peer_con_id} | peering_conn_Tag_Name: {tag} | req_vpc_id: {req_vpc_id:<25} | req_owner_id: {req_owner_id:<10} | accepter_vpc_id: {accept_vpc_id} | accepter_owner_id: {accept_owner_id} ")
                    print("****"*47)
            else:
                tag= " - "
                print(f"{lin}) Vpc_Peering_conn_id: {vpc_peer_con_id} | peering_conn_Tag_Name: {tag} | req_vpc_id: {req_vpc_id:<25} | req_owner_id: {req_owner_id:<25} | accepter_vpc_id: {accept_vpc_id} | accepter_owner_id: {accept_owner_id} ")
                print("****"*47)
    except Exception as e:
        print(f"Error:\n{e}")
print(" 1) create_vpc\n 2) list_vpcs\n 3) delete_vpc\n 4) create_subnet\n 5) list_subnets\n 6) delete_subnet\n 7) create_route_table\n 8) list_route_tables\n 9) delete_route_table \n 10) create_internet_gateway\n 11) describe_internet_gateway\n 12) delete_internet_gateway\n 13) attach_internet_gateway\n 14) detach_internet_gateway\n 15) associate_route_table\n 16) disassociate_route_table\n 17) create_route\n 18) create_natgateway\n 19) describe_nat_gatways\n 20) allocate_elastic_ip\n 21) describe_addresses\n 22) delete_nat_gateway\n 23) delete_route\n 24) create_vpc_peering\n 25) describe_vpc_peering_connections\n 26) accept_vpc_peering_connection\n 27) reject_vpc_peering_connection\n 28) delete_vpc_peering_connection")
print_str()
inp=input("Enter the Option:\n")
match inp:
    case "create_vpc":
        inp_vpc_Name=input("Enter the Vpc Tag Name:\n")
        inp_cidr=input("Enter the cidr value for Vpc:\n")
        try:
            creation_vpc=vpc.create_vpc(
                CidrBlock=inp_cidr,
                TagSpecifications=[{'ResourceType':'vpc',
                'Tags':[{'Key':'Name','Value':inp_vpc_Name}]
                }]
            )
            print(f"Vpc Created Successfully!.")
        except Exception as e:
            print(f"Error:\n {e}")
    case "list_vpcs":
        lst_vpc_fun()
    case "delete_vpc":
        lst_vpc_fun()
        inp_vpc_id=input("Enter the Vpc Id want to delete:\n")
        print_str()
        try:
            del_vpc=vpc.delete_vpc(
                VpcId=inp_vpc_id
            )
            print(f"Deleted the {inp_vpc_id} successfully!.")
        except ClientError as e:
            if e.response['Error']['Code'] == 'DependencyViolation':
                print(f"the {inp_vpc_id} have Dependencies ,please delete the dependencies !.")
            else:
                print(f"Error:\n {e}")

    case "create_subnet":
        lst_vpc_fun()
        inp_vpc_id=input("Enter the vpc_id:\n")
        inp_sub_cidr=input("Enter the subnet CIDR_Value:\n")
        inp_tag=input("Enter teh Tag_Name:\n")
        try:
            create_subnet=vpc.create_subnet(
                VpcId=inp_vpc_id,
                CidrBlock=inp_sub_cidr,
                TagSpecifications=[{
                    'ResourceType':'subnet',
                    'Tags':[{'Key':'Name','Value':inp_tag}]
                }]
            )
            print(f"Subnet {inp_tag} created Successfully!.")
        except Exception as e:
            print(f"Error:\n{e}")
    case "list_subnets":
        lst_sub_fun()
    case "delete_subnet":
        lst_sub_fun()
        print_str()
        inp_sub_id=input("Enter the Subnet_Id to delete:\n")
        print_str()
        try:
            del_sub=vpc.delete_subnet(
                SubnetId=inp_sub_id
            )
            print(f"{inp_sub_id} deleted Successfully!.")
        except ClientError as e:
            if e.response['Error']['Code'] == "DependencyViolation":
                print(f"{inp_sub_id} have dependencies,please Delete the Dependencies!.")
            else:
                print(f"Error:\n {e}")
    case "create_route_table":
        lst_vpc_fun()
        print_str()
        inp_vpc_id=input("Enter the Vpc_Id:\n")
        print_str()
        inp_tag=input("Enter the Tag_Name:\n")
        print_str()
        try:
            create_route=vpc.create_route_table(
                VpcId=inp_vpc_id,
                TagSpecifications=[{
                    'ResourceType':'route-table',
                    'Tags':[{'Key':'Name','Value':inp_tag}]
                }]
            )
            print(f"{inp_tag} created Successfully!.")
        except ClientError as e:
            print(f"Error:\n{e}")
    case "list_route_tables":
        lst_route_table_fun()
    case "delete_route_table":
        lst_route_table_fun()
        print_str()
        inp_route_id=input("Enter the Route_Table_Id:\n")
        print_str()
        try:
            del_route_table=vpc.delete_route_table(
                RouteTableId=inp_route_id
            )
            print(f"{inp_route_id} deleted Successfully!.")
        except ClientError as e:
            if e.response['Error']['Code'] == "DependencyViolation" :
                print(f"{inp_route_id} have dependencies,please Delete the Dependencies!.")
            else:
                print(f"Error:\n{e}")
    case ("create_internet_gateway"):
        inp_internet_gateway=input("Enter the internet_gateway_tag_name:\n")
        try:
            internet_gat_create=vpc.create_internet_gateway(
                TagSpecifications=[{
                    'ResourceType':'internet-gateway',
                    'Tags':[{'Key':'Name','Value':inp_internet_gateway}]
                }]
            )
            print(f"{inp_internet_gateway} is created Successfully!.")
        except Exception as e:
            print(f"Error:\n{e}")
    case ("describe_internet_gateway"):
        describe_internet_gateway_fun()
    case ("delete_internet_gateway"):
        describe_internet_gateway_fun()
        print_str()
        delete_internet_gateway=input("Enter the Internet_Gateway_Id:\n")
        print_str()
        try:
            del_internet_gateway=vpc.delete_internet_gateway(
                InternetGatewayId=delete_internet_gateway
            )
            print(f"{delete_internet_gateway} deleted Successfully!.")
        except ClientError as e:
            if e.response['Error']['Code'] == "DependencyViolation":
                print(f"{delete_internet_gateway} have dependencies,please Delete the Dependencies!.")
    case ("attach_internet_gateway"):
        describe_internet_gateway_fun()
        print_str()
        attach_internet_gateway=input("Enter the Internet_Gateway_Id:\n")
        print_str()
        lst_vpc_fun()
        print_str()
        inp_vpc=input("Enter the Vpc_Id:\n")
        try:
            att_internet_gateway=vpc.attach_internet_gateway(
                InternetGatewayId=attach_internet_gateway,
                VpcId=inp_vpc

            )
            print(f"{attach_internet_gateway} to attached {inp_vpc} Successfully!.")
        except Exception as e:
            print(f"Error:\n{e}")
    case ("detach_internet_gateway"):
        describe_internet_gateway_fun()
        print_str()
        detach_internet_gateway=input("Enter the Internet_Gateway_Id:\n")
        lst_vpc_fun()
        print_str()
        inp_vpc=input("Enter the Vpc_Id:\n")
        print_str()
        try:
            detach_igw_from_vpc=vpc.detach_internet_gateway(
                InternetGatewayId=detach_internet_gateway,
                VpcId=inp_vpc
            )
            print(f"{detach_internet_gateway} detached Successfully!.")
        except Exception as e:
            print(f"Error:\n{e}")
    case ("associate_route_table"):
        lst_route_table_fun()
        print_str()
        inp_route_id=input("Enter the Route_Table_Id:\n")
        lst_sub_fun()
        print_str()
        inp_subnet_id=input("Enter the Subnet_id:\n")
        print_str()
        try:
            associate_route_table=vpc.associate_route_table(
                RouteTableId=inp_route_id,
                SubnetId=inp_subnet_id
            )
            print(f"routetable {inp_route_id} associated {inp_subnet_id} successfully!.")
        except Exception as e:
            print(f"Error:\n{e}")
    case ("disassociate_route_table"):
        lst_route_table_fun()
        print_str()
        inp_ass_id=input("Enter the Association_Id:\n")
        print_str()
        try:
            dis_associate_route_table=vpc.disassociate_route_table(
                AssociationId=inp_ass_id
            )
            print(f"{inp_ass_id} disassociated successfully!.")
        except Exception as e:
            print(f"Error:\n{e}")
    case ("create_route"):
        lst_route_table_fun()
        print_str()
        inp_route=input("Enter the Routetable_Id:\n")
        print_str()
        inp_opt=input(" 1) internet_gateway\n 2) nat_gateway\n 3) vpc_peering_connection\n")
        try:
            match inp_opt:
                case "internet_gateway":
                    describe_internet_gateway_fun()
                    print_str()
                    print(f"---Note: Here Displays InternetGatway and Nat Gatways which Gateway you want can select---")
                    inp_igw_id=input("Enter the Igw_Id:\n")
                    print_str()
                    print("---Note:( 0.0.0.0/0 is accept all connection through internet)---")
                    inp_cidr=input("Enter the target_cidr:\n")
                    crt_route=vpc.create_route(
                        GatewayId=inp_igw_id,
                        RouteTableId=inp_route,
                        DestinationCidrBlock=inp_cidr
                    )
                    print(f"routed Created successfully!.")
                case "nat_gateway":
                    describe_nat_gateways_fun()
                    print_str()
                    inp_nat_id=input("Enter the nat_Id:\n")
                    print_str()
                    print("---Note:( 0.0.0.0/0 is accept all connection through internet)---")
                    inp_cidr=input("Enter the target_cidr:\n")
                    crt_route=vpc.create_route(
                        GatewayId=inp_nat_id,
                        RouteTableId=inp_route,
                        DestinationCidrBlock=inp_cidr
                    )
                    print(f"routed Created successfully!.")
                case "vpc_peering_connection":
                    describe_vpc_peering_connections_fun()
                    print_str()
                    inp_vpc_peer=input("enter the Vpc_peering id:\n")
                    print_str()
                    print("---Note:( 0.0.0.0/0 is accept all connection through internet)---")
                    inp_cidr=input("Enter the target_cidr:\n")
                    crt_route=vpc.create_route(
                        RouteTableId=inp_route,
                        DestinationCidrBlock=inp_cidr,
                        VpcPeeringConnectionId=inp_vpc_peer
                    )
                    print(f"routed Created successfully for vpc_peering!.")
        except Exception as e:
            print(f"Error:\n{e}")
    case ("create_natgateway"):
        inp_tag=input("Enter the Tag_Name:\n")
        lst_sub_fun()
        print_str()
        inp_sub_id=input("Enter the Subnet_id:\n")
        print_str()
        describe_elastic_ip_fun()
        print_str()
        inp_all_id=input("Enter the Allocation_Id:\n")
        print_str()
        try:
            create_nat=vpc.create_nat_gateway(
                SubnetId=inp_sub_id,
                AllocationId=inp_all_id,
                TagSpecifications=[{
                    'ResourceType':'natgateway',
                    'Tags': [
                        {
                            'Key':'Name','Value':inp_tag
                        },
                    ]
                },
            ]
            )
            print(f"{inp_tag} created successfully!.")
        except Exception as e:
            print(f"Error:\n{e}")
    case ("describe_nat_gatways"):
        describe_nat_gateways_fun()
    case ("allocate_elastic_ip"):
        allocate_elastic_ip_fun()
    case ("describe_addresses"):
        describe_elastic_ip_fun()
    case ("delete_nat_gateway"):
        describe_nat_gateways_fun()
        print_str()
        inp_nat=input("Enter the Nat_gateway_id:\n")
        try:
            del_nat=vpc.delete_nat_gateway(
                NatGatewayId=inp_nat
            )
            print(f"{inp_nat} deleted Successfully!.")
        except ClientError as e:
         if e.response['Error']['Code'] == "DependencyViolation":
            print(f"This Natgateway have dependencies,Please delete it!.")
        except Exception as e:
            print(f"Error:\n{e}")
    case ("delete_route"):
        lst_route_table_fun()
        print_str()
        inp_route=input("Enter the Routetable_Id:\n")
        print_str()
        inp_dest=input("Enter the destination_cidr want to delete:\n")
        print_str()
        try:
            del_route=vpc.delete_route(
                RouteTableId=inp_route,
                DestinationCidrBlock=inp_dest
            )
            print(f"Route Deleted Successfully!.")
        except Exception as e:
            print("Error:\n{e}")
    case ("create_vpc_peering"):
        lst_vpc_fun()
        print_str()
        inp_src_vpc_id=input("Enter the Requester_Vpc_Id:\n")
        print_str()
        inp_dest_vpc_id=input("Enter the Accepter_Vpc_Id:\n")
        print_str()
        inp_tag=input("Enter the Peering_Tag_Name:\n")
        print_str()
        print("Below shows Sender Owner_Account if you Mention other AWS Another Owner Account Id Also applicable!.")
        aws_id_fun()
        print_str()
        acc_id=input("Enter the Destination_Account_Id:\n")
        print_str()
        inp_reg=input("Enter the Destination AWS_Region:\n")
        print_str()
        try:
            vpc_peering=vpc.create_vpc_peering_connection(
                PeerRegion=inp_reg,
                TagSpecifications=[{
                    'ResourceType': 'vpc-peering-connection',
                    'Tags':[{'Key':'Name','Value':inp_tag}]
                }],
                VpcId=inp_src_vpc_id,
                PeerVpcId=inp_dest_vpc_id,
                PeerOwnerId=acc_id
            )
            print("Vpc-peering Created Successfully!.")
        except Exception as e:
            print(f"Error:\n{e}")
    case ("describe_vpc_peering_connections"):
        describe_vpc_peering_connections_fun()
    case ("accept_vpc_peering_connection"):
        describe_vpc_peering_connections_fun()
        inp_conn_id=input("Enter the vpc_connection_id :\n")
        print_str()
        try:
            acc_vpc_peer=vpc.accept_vpc_peering_connection(
                VpcPeeringConnectionId=inp_conn_id
            )
            print("vpc_peering Accepted Successfully!.")
        except Exception as e:
            print(f"Error:\n{e}")
    case ("reject_vpc_peering_connection"):
        describe_vpc_peering_connections_fun()
        inp_conn_id=input("Enter the vpc_connection_id :\n")
        print_str()
        try:
            rej_vpc_peer=vpc.reject_vpc_peering_connection(
                VpcPeeringConnectionId=inp_conn_id
            )
            print("vpc_peering Rejected Successfully!.")
        except Exception as e:
            print(f"Error:\n{e}")
    case ("delete_vpc_peering_connection"):
        describe_vpc_peering_connections_fun()
        inp_conn_id=input("Enter the vpc_connection_id :\n")
        print_str()
        try:
            del_vpc_peer=vpc.delete_vpc_peering_connection(
                VpcPeeringConnectionId=inp_conn_id
            )
            print("vpc_peering Deleted Successfully!.")
        except Exception as e:
            print(f"Error:\n{e}")
    case _:
        print("Entered Invalid Option!.")
