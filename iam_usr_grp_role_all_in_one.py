#!/usr/bin/python3
import boto3
import getpass
import sys
import json
lin=0
iam=boto3.client('iam')
def prt_star():
    print("**"*40)
def lst_usrs():
    lst_users=iam.list_users()
    lin=0
    for i in lst_users.get('Users'):
        lin+=1
        print(f'User_Name_{lin}: {i.get('UserName')}')
def lst_grps():
    lin=0
    lst_groups=iam.list_groups()
    lin+=1
    for i in lst_groups.get("Groups"):
        print(f'Group_Name_{lin}: {i.get('GroupName')}')
def lst_pol():
    lst_pol_1=iam.list_policies(
        Scope='All'
    )
    for i in lst_pol_1.get("Policies"):
        lin+=1
        print(f"Policy_Name_{lin} : {i.get('PolicyName'):<30} Policy_ARN: {i.get('Arn')}")
def lst_usr_attach_pol(inp_usr):
        prt_star()
        lin=0
        try:
            lst_policies=iam.list_attached_user_policies(
                UserName=inp_usr
            )
            if lst_policies.get('AttachedPolicies'):
                for i in lst_policies.get('AttachedPolicies'):
                    lin+=1
                    print(f"Plolicy_{lin} : {i.get('PolicyName'):<30} Policy_Arn: {i.get('PolicyArn')}")
                    return True
            elif not lst_policies.get('AttachedPolicies'):
                print(f"None of Policies to attached to the User {inp_usr}")
                return False
        except Exception as e:
            print(f"Error is occoured:\n{e}")
def lst_usr_inline_pol_fun(inp_usr):
        prt_star()
        lst_usr_policies=iam.list_user_policies(
            UserName=inp_usr
        )
        lin=0
        try:
            if lst_usr_policies.get('PolicyNames'):
                for i in lst_usr_policies.get('PolicyNames'):
                    lin+=1
                    print(f"Inline_Policy_{lin}: {i}")
            elif not lst_usr_policies.get('PolicyNames'):
                print(f"None of Inline _Policies Atteched to the User {inp_usr}")
        except Exception as e:
            print(f"Error Occoured:\n {e}")
def lst_grp_pol_fun(inp_grp):
        prt_star()
        lin=0
        try:
            lst_grp_inline_policy=iam.list_group_policies(
                GroupName=inp_grp
            )
            if lst_grp_inline_policy.get("PolicyNames"):
                for i in lst_grp_inline_policy.get("PolicyNames"):
                    lin+=1
                    print(f"Policy_{lin}: {i}")
            elif not lst_grp_inline_policy.get("PolicyNames"):
                print(f"None of Inline Policies Create By the Grp {inp_grp}")
        except Exception as e:
            print(f"Error is Occoured:\n{e}")
def lst_grp_attached_pol_fun(inp_grp):
        prt_star()
        lst_attatch_grp_policies=iam.list_attached_group_policies(
            GroupName=inp_grp
        )
        lin=0
        try:
            if lst_attatch_grp_policies.get('AttachedPolicies'):
                for i in lst_attatch_grp_policies.get('AttachedPolicies'):
                    lin+=1
                    print(f"Policy_{lin}: {i.get('PolicyName'):<50} PolicyARN: {i.get('PolicyArn')} ")
                return True
            elif not lst_attatch_grp_policies.get('AttachedPolicies'):
                print (f"None of Policies Attached to the Group {inp_grp}")
                return False
        except Exception as e:
            print(f"Error Occoured:\n {e}")
def lst_usr_grps_fun(inp_usr):
    try:
        lst_usr_grp=iam.list_groups_for_user(
            UserName=inp_usr
        )
        lin=0
        for i in lst_usr_grp.get('Groups'):
            lin+=1
            print(f"{lin}_GroupName: {i.get('GroupName')}")
    except iam.exceptions.NoSuchEntityException as e:
            print("Entered Wrong UserName")
    except Exception as e:
        print(f"Error:\n{e}")
def lst_aws_pol():
    lst_pol_1=iam.list_policies(
        Scope='All'
    )
    lin=0
    for i in lst_pol_1.get("Policies"):
        lin+=1
        print(f"Policy_Name_{lin}: {i.get('PolicyName'):<50} Policy_ARN: {i.get('Arn')}")
def lst_rol_fun():
        print("Listing Roles...")
        lst_rol=iam.list_roles()
        lin=0
        for i in lst_rol.get('Roles'):
            lin+=1
            print(f"{lin}_Role: {i.get('RoleName')}")
def lst_attached_rol_fun(inp_rol):
    lst_rol_policies=iam.list_attached_role_policies(
            RoleName=inp_rol
        )
    lin=0
    if lst_rol_policies.get('AttachedPolicies'):
        for i in lst_rol_policies.get('AttachedPolicies'):
            lin+=1
            print(f"{lin}_Policy_Name: {i.get('PolicyName'):<30} PolicyArn: {i.get('PolicyArn')}")
    elif not lst_rol_policies.get('AttachedPolicies'):
        print(f"None of Policies Attached to the Role!.")
def lst_role_inline_policies_fun(inp_rol):
    lst_role_inline_pol=iam.list_role_policies(
        RoleName=inp_rol
    )
    #print(lst_role_inline_pol)
    lin=0
    try:
        if lst_role_inline_pol.get('PolicyNames'):
            for i in lst_role_inline_pol.get('PolicyNames'):
                lin+=1
                print(f"Inline_Policy_{lin}: {i}")
        elif not lst_role_inline_pol.get('PolicyNames'):
            print(f"None of Inline _Policies Atteched to the User {inp_rol}")
    except Exception as e:
        print(f"Error Occoured:\n {e}")
def list_instance_profile_for_role(inp_rol):
        try:
            list_instance_profile=iam.list_instance_profiles_for_role(
                RoleName=inp_rol
            )
            lin=0
            for i in list_instance_profile.get('InstanceProfiles'):
                lin+=1
                print(f"{lin}) Profile_Name: {i.get('InstanceProfileName')}")
        except Exception as e:
            print(f"Error:\n {e}")
print("Options:\n 0) create_login_profile\n 1) list_users\n 2) list_groups\n 3) list_usr_inline_policies\n 4) delete_user\n 4) delete_group\n 5) list_usr_attached_policies\n 6) list_group_inline_policies\n 7) list_attached_grp_policies\n 8) create_user\n 9) create_group\n 10) update_login_profile\n 11) add_usr_to_grp\n 12) rm_usr_from_grp\n 13) list_grps_for_usr\n 14) attach_usr_policy\n 15) attach_grp_policy\n 16) detach_usr_policy\n 17) detach_grp_policy\n 18) delete_inline_policicy\n 19) grp_inline_policy\n 20) create_role\n 21) lst_roles\n 22) attch_rol_pol\n 23) lst_attached_role_policies\n 24) lst_role_inline_policies\n 25) detach_attached_rol_pol\n 26) delete_role_inline_policy\n 27) delete_role\n 28) list_instance_profile_for_role\n 29) rm_rol_from_instance_profile")
inp=input("Enter the Option to Perform:\n")
prt_star()
match inp:
    case "list_users": ##list_iam_usrs
        lst_usrs()
    case "list_groups": ##list_groups
        lst_grps()
    case "list_usr_inline_policies": ##list_iam_usr_inline_policies
        print("Listing Users...")
        lst_usrs()
        inp_usr=input("Enter the User_Name to list_usr_inline_policies:\n")
        lst_usr_inline_pol_fun(inp_usr)
    case "delete_user": ##deleting a iam_usr case
        lst_usrs()
        prt_star()
        inp_usr=input("Enter the User_Name to delete:\n")
        prt_star()
        try:
            user_del_login=iam.delete_login_profile(
                UserName=inp_usr
            )
            usr_del=iam.delete_user(
                UserName=inp_usr
            )
            print(f"User {inp_usr} deleted successfully!.")
        except iam.exceptions.DeleteConflictException as e:
            print(f"the user{inp_usr} have Policies to delete that policies or Assioated  with groups please detach it!.")
        except Exception as e:
            print(f"Error:\n {e}")
    case "delete_group":
        lst_grps()
        prt_star()
        inp_grp=input("Enter the Group_Name want to delete:\n")
        prt_star()
        try:
            del_grp=iam.delete_group(
                GroupName=inp_grp
            )

            print(f"Group {inp_grp} is deleted Successfully!.")
        except Exception as e:
            print(f" The group {inp_grp} is attached to users to detach the users from this group then try again!")
    case "list_usr_attached_policies":
        print("Listing_Users....")
        lst_usrs()
        inp_usr=input("Enter the User_Name to list_usr_direct_policies:\n")
        lst_usr_attach_pol(inp_usr)
    case "list_group_inline_policies":
        print("Listing Groups...")
        lst_grps()
        prt_star()
        inp_grp=input("Enter the Group_Name to List_Inlines_policies:\n")
        lst_grp_pol_fun(inp_grp)
    case "list_attached_grp_policies":
        lst_grps()
        prt_star()
        inp_grp=input("Enter the Group_Name to list Attached Policies:\n")
        lst_grp_attached_pol_fun(inp_grp)
    case "create_user":
        inp_usr=input("Enter the User_Name Want to be Create:\n")
        print("Note: passwd should have Alphabets,numbers,special characters,min lenth is 8")
        inp_passwd=getpass.getpass("Enter the Passwd to set:\n")
        prt_star()
        try:
            create_usr=iam.create_user(
                UserName=inp_usr
            )
            print(f"User {inp_usr} created Successfully!.")
            set_pass=iam.create_login_profile(
                UserName=inp_usr,
                Password=inp_passwd,
                PasswordResetRequired=True
            )
            print(f"User {inp_usr} and password set successfully!.")
        except iam.exceptions.EntityAlreadyExistsException as e:
            print(f"Error: User '{inp_usr}' already exists.")
        except iam.exceptions.PasswordPolicyViolationException as e:
            print(f"Passwd not met Conditions,Please try Again!.")
            print("Note: passwd should have Alphabets,numbers,special characters,min lenth is 8")
            inp_pass=getpass.getpass("Enter the Passwd to set:\n")
            set_pass_1=iam.create_login_profile(
                UserName=inp_usr,
                Password=inp_pass,
                PasswordResetRequired=True
            )
            print(f"User {inp_usr} and password set successfully!.")
        except Exception as e:
            print(f"Error:\n {e}")
    case "create_group":
        inp_grp=input("Enter the Group_Name Want to be Create:\n")
        prt_star()
        try:
            grp_create=iam.create_group(
                GroupName=inp_grp
            )
            print(f"Group {inp_grp} created successfully!.")
        except iam.exceptions.EntityAlreadyExistsException as e:
            print(f"Error: Group {inp_grp} is already exist")
        except Exception as e:
            print(f"Error:\n {e}")
    case "update_login_profile":
        print("Listing_Users...")
        prt_star()
        lst_usrs()
        prt_star()
        inp_usr=input("Enter the User_Name:\n")
        inp_passwd=getpass.getpass("Enter the Passwd to set:\n")
        prt_star()
        try:
            update_login_passwd=iam.update_login_profile(
                UserName=inp_usr,
                Password=inp_passwd,
                PasswordResetRequired=True
            )
            print(f"Passwd Updated Successfully for the User {inp_usr}")
        except iam.exceptions.EntityTemporarilyUnmodifiableException as e:
            print(f"login_profile_updation service temporarily unmodifiable")
        except iam.exceptions.PasswordPolicyViolationException as e:
            print("Password Violation Error")
        except Exception as e:
            print(f"Error:\n {e}")
    case "add_usr_to_grp":
        print("Listing_users...")
        lst_usrs()
        prt_star()
        inp_usr=input("Enter the User_Name to add to Group:\n")
        prt_star()
        print("Listing_groups:")
        lst_grps()
        prt_star()
        inp_grp=input("Enter the Group_Name want to be add:\n")
        prt_star()
        try:
            usr_to_grp=iam.add_user_to_group(
                UserName=inp_usr,
                GroupName=inp_grp
            )
            print(f"User {inp_usr} to added the Group {inp_grp} Successfully!.")
        except iam.exceptions.NoSuchEntityException as e:
            print(f"User or Group not Exisit")
        except Exception as e:
            print(f"Error:\n {e}")
    case "rm_usr_from_grp":
        print("Listing_users:")
        lst_usrs()
        prt_star()
        inp_usr=input("Enter the UserName to remove from the group:\n")
        prt_star()
        lst_usr_grps_fun(inp_usr)
        inp_grp=input("Enter the group Name:\n")
        try:
            rm_usr_from_grp=iam.remove_user_from_group(
                UserName=inp_usr,
                GroupName=inp_grp
            )
            print(f"User {inp_usr} Removed Successfully  From {inp_grp} Group!.")
        except iam.exceptions.NoSuchEntityException as e:
            print(f"Entered User or Group is Not Valid!.")
        except Exception as e:
            print(f"Error:\n {e}")
    case "list_grps_for_usr":
        print(f"Listing Users...")
        lst_usrs()
        inp_usr=input("Enter the UserName to list the Groups:\n")
        prt_star()
        lst_usr_grps_fun(inp_usr)
    case "attach_usr_policy":
        lst_usrs()
        prt_star()
        inp_usr=input("Enter the Username to attach Policy:\n")
        prt_star()
        lst_aws_pol()
        inp_arn=input("Enter the Policy_ARN:\n")
        try:
            attach_pol=iam.attach_user_policy(
                UserName=inp_usr,
                PolicyArn=inp_arn
            )
            print(f"Policy attached Sccessfully to the User{inp_usr}")
        except iam.exceptions.NoSuchEntityException as e:
            print(f"User {inp_usr} is not Available in IAM")
        except iam.exceptions.InvalidInputException as e:
            print(f"Invalid ARN provided")
        except iam.exceptions.PolicyNotAttachableException:
            print(f"This policy Not Attchable to the User {inp_usr}")
        except iam.exceptions.LimitExceededException as e:
            print(f"the User {inp_usr} had Exceeded the Limit to Attach Policies")
        except Exception as e:
            print(f"Error:\n {e}")
    case "attach_grp_policy":
        print("Listing_Groups...")
        prt_star()
        lst_grps()
        inp_grp=input("Enter the GroupName to attach a Policy:\n")
        prt_star()
        print("Listing_ALL_Available_Policies...")
        prt_star()
        lst_aws_pol()
        inp_arn=input("Enter the Policy Arn to attach the Group:\n")
        try:
            attach_grp_pol=iam.attach_group_policy(
                GroupName=inp_grp,
                PolicyArn=inp_arn
            )
            print(f"Policy is attached successfully to the group {inp_grp}")
        except iam.exceptions.NoSuchEntityException as e:
            print(f"User {inp_grp} is not Available in IAM")
        except iam.exceptions.InvalidInputException as e:
            print(f"Invalid ARN provided")
        except iam.exceptions.PolicyNotAttachableException:
            print(f"This policy Not Attchable to the User {inp_grp}")
        except iam.exceptions.LimitExceededException as e:
            print(f"the User {inp_grp} had Exceeded the Limit to Attach Policies")
        except Exception as e:
            print(f"Error:\n {e}")
    case "detach_usr_policy":
        print("Listing_Users....")
        lst_usrs()
        prt_star()
        inp_usr=input("Enter the User_Name to list_usr_direct_policies:\n")
        condition_1=lst_usr_attach_pol(inp_usr)
        if condition_1:
            inp_arn=input(f"Enter the Policy Arn to detach from the User {inp_usr}:\n")
            prt_star()
            try:
                detach_usr_pol=iam.detach_user_policy(
                        UserName=inp_usr,
                        PolicyArn=inp_arn
                    )
                print(f"Policy Detach Successfully from the user {inp_usr}")
            except iam.exceptions.NoSuchEntityException as e:
                print(f"User {inp_usr} is not Available in IAM")
            except iam.exceptions.InvalidInputException as e:
                print(f"Invalid ARN provided")
            except Exception as e:
                print(f"Error:\n {e}")
        elif not condition_1:
            sys.exit(0)
    case "detach_grp_policy":
        print("Listing_Groups....")
        lst_grps()
        prt_star()
        inp_grp=input("Enter the Group_Name to list Attached Policies:\n")
        condition_1=lst_grp_attached_pol_fun(inp_grp)
        if condition_1:
            inp_arn=input(f"Enter the Policy Arn to detach from the group {inp_grp}:\n")
            try:
                detach_grp_pol=iam.detach_group_policy(
                    GroupName=inp_grp,
                    PolicyArn=inp_arn
                )
                print(f"Policy Detached Successfully From the Group {inp_grp}!.")
            except iam.exceptions.NoSuchEntityException as e:
                print(f"User {inp_grp} is not Available in IAM")
            except iam.exceptions.InvalidInputException as e:
                print(f"Invalid ARN provided")
            except Exception as e:
                print(f"Error:\n {e}")

        elif not condition_1:
            sys.exit(0)
    case "delete_inline_policicy":
        print("Listing Users...")
        lst_usrs()
        inp_usr=input("Enter the User_Name to list_usr_inline_policies:\n")
        lst_usr_inline_pol_fun(inp_usr)
        prt_star()
        inp_pol=input("Enter the POlicy Name to Delete:")
        try:
            del_inline_pol=iam.delete_user_policy(
                UserName=inp_usr,
                PolicyName=inp_pol
            )
            print(f"Policy {inp_pol} deleted successfully!.")
        except iam.exceptions.NoSuchEntityException as e:
            print(f"User {inp_usr} or policy {inp_pol} is not found ,plese Enter Valid Input !.")
        except Exception as e:
            print(f"Error:\n{e}")
    case "grp_inline_policy":
        print("Listing Groups")
        lst_grps()
        prt_star()
        inp_grp=input("Enter the GroupName to list_usr_inline_policies:\n")
        lst_grp_pol_fun(inp_grp)
        prt_star()
        inp_pol=input("Enter the POlicy Name to Delete:")
        try:
            del_inline_pol=iam.delete_group_policy(
                GroupName=inp_grp,
                PolicyName=inp_pol
            )
            print(f"Policy {inp_pol} deleted successfully!.")
        except iam.exceptions.NoSuchEntityException as e:
            print(f"Group {inp_grp} policy {inp_pol} is not found ,plese Enter Valid Input !.")
        except Exception as e:
            print(f"Error:\n{e}")
    case "create_role":
        inp_rol=input("Enter the Role_Name Want to create:\n")
        prt_star()
        print("Note: (example_serviceNames) eks.amazonaws.com, ec2.amazonaws.com, elasticbeanstalk.amazonaws.com")
        inp_Service=input("Enter the Sevice to access via iam_role:\n")
        trust_policy={
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"Service": inp_Service},
                    "Action": "sts:AssumeRole"
                }
            ]
        }
        inp_des=input("Enter the Role_Description:\n")
        try:
            rol_create=iam.create_role(
                RoleName= inp_rol,
                AssumeRolePolicyDocument=json.dumps(trust_policy),
                Description=inp_des
            )
            print(f"Role {inp_rol} created Successfully!.")
        except iam.exceptions.EntityAlreadyExistsException as e:
            print(f"Role {inp_rol} is already Exists!.")
        except iam.exceptions.MalformedPolicyDocumentException as e:
            print(f"You Entered a Invalid Service Name!.")
        except Exception as e:
            print(f"Error:\n {e}")
    case "lst_roles":
        lst_rol_fun()
    case "attch_rol_pol":
        lst_rol_fun()
        prt_star()
        inp_rol=input("Enter the Role Name to Attach Policy:\n")
        prt_star()
        print("Listing Policies...")
        lst_aws_pol()
        prt_star()
        inp_arn=input("Enter the Policy Arn to attach:\n")
        try:
            attach_pol_rol=iam.attach_role_policy(
                RoleName=inp_rol,
                PolicyArn=inp_arn
            )
            print(f"Policy attached Successfully to the Role {inp_rol} !.")
        except iam.exceptions.NoSuchEntityException as e:
            print(f" Entered Invalid Role {inp_rol}!.")
        except iam.exceptions.InvalidInputException as e:
            print(f"Entered Invalid ARN!.")
        except iam.exceptions.PolicyNotAttachableException as e:
            print(f"Policy is not Attachable!.")
        except Exception as e:
            print(f"Error:\n {e}")
    case "lst_attached_role_policies":
        lst_rol_fun()
        prt_star()
        inp_rol=input("Enter the Role Name to list_policies:\n")
        prt_star()
        lst_attached_rol_fun(inp_rol) 
    case "lst_role_inline_policies":
        lst_rol_fun()
        prt_star()
        inp_rol=input("Enter the Role Name to list_inline_policies:\n")
        prt_star()
        lst_role_inline_policies_fun(inp_rol)
    case "detach_attached_rol_pol":
        lst_rol_fun()
        prt_star()
        inp_rol=input("Enter the Role Name to list_policies:\n")
        prt_star()
        lst_attached_rol_fun(inp_rol)
        prt_star()
        inp_pol_arn=input("Enter the Policy Arn:\n")
        try:
            detach_attached_pol=iam.detach_role_policy(
                RoleName=inp_rol,
                PolicyArn=inp_pol_arn
            )
            print(f"Policy Detached Successfully from the role {inp_rol}!.")
        except iam.exceptions.NoSuchEntityException as e:
            print(f"Entered Invalid Role_Name")
        except iam.exceptions.InvalidInputException as e:
            print(f"Entered Invalid PolicyArn")
        except Exception as e:
            print(f"Error:\n {e}")
    case "delete_role_inline_policy":
        lst_rol_fun()
        prt_star()
        inp_rol=input("Enter the Role Name to list_policies:\n")
        prt_star()
        lst_role_inline_policies_fun(inp_rol)
        prt_star()
        inp_pol=input("Enter Policy Name:\n")
        try:
            del_inline_pol=iam.delete_role_policy(
                RoleName=inp_rol,
                PolicyName=inp_pol
            )
            print(f"{inp_pol} Deleted Successfully!.")
        except iam.exceptions.NoSuchEntityException as e:
            print(f"Entered Role Name is InValid!.")
        except iam.exceptions.UnmodifiableEntityException as e:
            print(f"Role Inline Policy Cannot Remove!.")
        except Exception as e:
            print(f"Error:\n {e}")
    case "delete_role":
        lst_rol_fun()
        prt_star()
        inp_rol=input("Enter the Role Name want to delete:\n")
        prt_star()
        try:
            del_role=iam.delete_role(
                RoleName=inp_rol
            )
            print(f"Role {inp_rol} deleted Successfully!.")
        except iam.exceptions.NoSuchEntityException as e:
            print(f"Entered Invalid Role Name")
        except iam.exceptions.DeleteConflictException as e:
            print(f"Role {inp_rol} have Policies or instanceprofiles to delete them!")
        except Exception as e:
            print(f"Error:\n {e}")
    case "create_login_profile":
        print("Listing Users...")
        lst_usrs()
        prt_star()
        inp_usr=input("Enter the UserName:\n")
        try:
            inp_pass=getpass.getpass("Enter the Passwd to set:\n")
            set_pass_1=iam.create_login_profile(
                    UserName=inp_usr,
                    Password=inp_pass,
                    PasswordResetRequired=True
            )
            print(f"User {inp_usr} created profile successfully!.")
        except iam.exceptions.NoSuchEntityException as e:
            print(f"Entered Username  Dosn't Exist in Iam")
        except iam.exceptions.PasswordPolicyViolationException as e:
            print(f"Passwd not met Conditions,Please try Again!.")
            print("Note: passwd should have Alphabets,numbers,special characters,min lenth is 8")
            inp_pass=getpass.getpass("Enter the Passwd to set:\n")
            set_pass_2=iam.create_login_profile(
                UserName=inp_usr,
                Password=inp_pass,
                PasswordResetRequired=True
            )
            print(f"User {inp_usr} and password set successfully!.")
        except Exception as e:
            print(f"Error:\n {e}")
    case "list_instance_profile_for_role":
        lst_rol_fun()
        prt_star()
        inp_rol=input("Enter the Role Name:\n")
        prt_star()
        list_instance_profile_for_role(inp_rol)
    case "rm_rol_from_instance_profile":
        lst_rol_fun()
        prt_star()
        inp_rol=input("Enter the Role Name:\n")
        prt_star()
        list_instance_profile_for_role(inp_rol)
        inp_pr=input("Enter the instance_profile_Name:\n")
        try:
            rm_instance_profile=iam.remove_role_from_instance_profile(
                RoleName=inp_rol,
                InstanceProfileName=inp_pr

            )
            print(f"Instance_Policy removed Successfully!.")
        except Exception as e:
            print(f"Error:\n {e}") 
    case _:
        print("Entered Invalid Option!.")
