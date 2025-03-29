#!/usr/bin/python3
import boto3

ec2=boto3.client('ec2')

def lst():
    lst_instances=ec2.describe_instances()
    for i in lst_instances.get('Reservations',[]):
        for j in i.get('Instances',[]):
            for k in j.get('Tags',[]):
                if k.get('Key')=="Name":
                    print(f"Instance_Name: {k.get('Value')}")
            print(f"Instance_Id: {j.get('InstanceId')}")
            ins_state=j.get('State').get('Name')
            if ins_state == "running":
                print(f"instance_State: {ins_state}")
                if j.get("PublicIpAddress") is not None:
                    print(f"Public_IpAddress: {j.get("PublicIpAddress")}")
            elif ins_state == "stopped":
                print (f"Instance_State: {ins_state}")
            elif ins_state == "stopping":
                print(f"instance_State: {ins_state}")
            elif(ins_state == "terminated"):
                print(f"instance_State: {ins_state}")
            else:
                print(f"this server is private server")
            print(f"Private_IpAddress: {j.get('PrivateIpAddress')}")
            print('**'*40)
#Options
print(f"Options:\n 1) list_instances\n 2) create_instance\n 3) stop_instances\n 4) start_instances\n 5) terminate_instances")
inp=input("Enter the Action to perform:\n")
print('**'*40)
match inp:
    case "create_instance":
        inp_name=input("Enter the Instance_Name:\n")
        inp_img_id=input("Enter the Image_id:\n")
        inp_subnet_id=input("Enter the Subnet_id:\n")
        inp_security_group=input("Enter the Security_Id:\n")
        inp_keypair=input("Enter the key-pair name:\n")
        inp_min=int(input("Enter the Minimum number instances want create:\n"))
        inp_max=int(input("Enter the Maximum number instances want create:\n"))
        inp_instance_type=input("Enter the instance-type:\n")
        create_ec2=ec2.run_instances(
            ImageId=inp_img_id,
            InstanceType=inp_instance_type,
            KeyName=inp_keypair,
            SubnetId=inp_subnet_id,
            SecurityGroupIds=[inp_security_group],
            MinCount=inp_min,
            MaxCount=inp_max,
            TagSpecifications=[{
                'ResourceType':'instance',
                'Tags':[{
                    'Key':'Name','Value':inp_name
                }]
            }]
        )
    case "list_instances":
        lst()
    case "stop_instances":
        lst()
        stp_instance_id=input("Enter the Instance-Id want to stop:\n")
        stp_instances=ec2.stop_instances(
            InstanceIds= [stp_instance_id]
        )
    case "start_instances":
        lst()
        inp_start=input("Enter the instance_is want to start:\n")
        strt_instance=ec2.start_instances(
            InstanceIds=[inp_start]
        )
    case "terminate_instances":
        lst()
        inp_terminate=input("Enter the Instance_Id want to Terminate:\n")
        terminate_inst=ec2.terminate_instances(
            InstanceIds=[inp_terminate]    
        )
    case _:
        print(f"Entered wrong option {inp}.")
    
     
