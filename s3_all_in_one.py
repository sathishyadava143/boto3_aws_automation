#!/usr/bin/python3
import boto3

s3=boto3.client('s3')
lst=[]
def lst_bucket_fun():
    lst_bucket=s3.list_buckets()
    count=0
    for i in lst_bucket.get('Buckets'):
        count+=1
        print(f"Bucket_{count}: {i.get('Name')}")
        print("**"*20)

def lst_obj_fun(print_flag=True):
    inp=input("Enter the Bucket_Name:\n")
    try:
        lst_obj=s3.list_objects(
            Bucket= inp
        )
        print("**"*20)
        no=0
        for i in lst_obj.get('Contents'):
            no+=1
            count_obj=i.get('Key')
            lst.append(count_obj)
            if print_flag:
                print (f"item_{no}: {count_obj}")
                print("**"*20)
    except Exception as e:
        print("No objects found in this Bucket")
print("Options:\n 1) list_buckets\n 2) list_objects\n 3) create_bucket\n 4) delete_bucket\n 5) put_object\n 6) get_object\n 7) delete_object")
inp=input("Enter the Option to perform:\n")
if (inp == "list_buckets"):
    lst_bucket_fun()
elif (inp == "list_objects"):
    lst_bucket_fun()
    print("**"*20)
    lst_obj_fun()
elif (inp == "create_bucket"):
    print("**"*60)
    print("Note: Enter the Bucket_Name as unique because of s3 in global not an region specfic and don't use special characters!")
    print("**"*60)
    inp_buck_name=input("Enter the Bucket_Name want to create:\n")
    create_buck=s3.create_bucket(
        Bucket=inp_buck_name,
        CreateBucketConfiguration= { 'LocationConstraint': 'ap-south-1'}
    )
    print(f"Bucket {inp_buck_name} created successfully!")
elif (inp == "delete_bucket"):
    lst_bucket_fun()
    inp_buk=input("Enter the Bucket_Name to delete an object:\n")
    try:
        del_buck=s3.delete_bucket(
            Bucket= inp_buk
        )
        print(f"{inp_buk} deleted successfully!.")
    except Exception as e:
        print(f"You want delete the objects first in this bucket {inp_buk}")
elif (inp == "put_object"):
    lst_bucket_fun()
    inp_buck_name_2=input("Enter the Bucket name to upload object:\n")
    obj_path=input("Enter the Object_Path to upload:\n")
    file_name = obj_path.split("/")[-1]
    put_obj=s3.put_object(
        Bucket= inp_buck_name_2,
        Key=file_name,
    )
    print(f"object uploaded successfully in the bucket {inp_buck_name_2}!.")
elif (inp == "get_object"):
    lst_bucket_fun()
    inp_buk=input("Enter the Bucket_Name to get an object:\n")
    lst_obj=s3.list_objects(
        Bucket= inp_buk
    )
    print("**"*20)
    no=0
    for i in lst_obj.get('Contents'):
        no+=1
        count_obj=i.get('Key')
        print (f"item_{no}: {count_obj}")
        print("**"*20)
    inp_object_name=input("enter the object_name to get:\n")
    inp_path=input("Enter the path to download:\n")
    get_obj=s3.download_file(inp_buk,inp_object_name,inp_path)
    print("file downloaded successfully!.")
elif (inp == "delete_object"):
    lst_bucket_fun()
    inp_buk=input("Enter the Bucket_Name to delete an object:\n")
    lst_obj=s3.list_objects(
        Bucket= inp_buk
    )
    print("**"*20)
    no=0
    for i in lst_obj.get('Contents'):
        no+=1
        count_obj=i.get('Key')
        print (f"item_{no}: {count_obj}")
        print("**"*20)
    inp_object_name=input("enter the object_name to delete:\n")
    obj_del=s3.delete_object(
        Bucket=inp_buk,
        Key=inp_object_name
    )
    print("object deleted successfully!.")
else:
    print("You Entered a Invalid Option!")
