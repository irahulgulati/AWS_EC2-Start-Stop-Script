import boto3
ec2=boto3.client('ec2')
resultedZones=[]
resulted_ids=[]
def intro():
    print("Welcome to simplified python script for starting or stopping EC2 instance")
    print("Created By: irahulgulati[github.com/irahulgulati]")

def available_zone():
    region_name=input("Enter Your region:")
    print("Fetching Availability-Zones..")
    response=ec2.describe_availability_zones(
    Filters=[
        {
            'Name': 'region-name',
            'Values':[
                region_name,

            ]
        },
    ],
    AllAvailabilityZones=True,
    DryRun=False
                                            )
    # print(response["AvailabilityZones"][0]["ZoneName"])
    # print (response)
    for i in range(len(response["AvailabilityZones"])):
        resultedZones.append(response["AvailabilityZones"][i]["ZoneName"])
    if(len(resultedZones)>0):
        print("Available availability-zones are:")
        print(resultedZones)
        getInstanceid()
    else:
        print("No availability zones are available in this region")
        print("Please choose another region")
        available_zone()    
    

def getInstanceid():
    z=input("Choose one availability-zone:")
    if z in resultedZones:
        try:
            response = ec2.describe_instances(
            Filters=[
                {
                    'Name': 'availability-zone',
                    'Values': [
                        z,
                    ]
                },
            ],
            DryRun=False,
                                            )
            for i in range(len(response['Reservations'])):
                resulted_ids.append(response['Reservations'][i]['Instances'][0]['InstanceId'])
                # print(len(response['Reservations'][0]['Instances']))
            if(len(resulted_ids)>0):
                print(resulted_ids)
                getInstanceStatus()
                
            else:
                print("There are no instances available in: " + z)
                print("Please choose another availability-zone")
                getInstanceid()
                
        except:
            print("hmm, something is wrong")
    else:
        print("Please enter correct avaiability zone")
        getInstanceid()

def getInstanceStatus():
    getId=input("Please enter one instance id")
    if getId in resulted_ids:
        response = ec2.describe_instance_status(
            InstanceIds=[getId,],IncludeAllInstances=True
        )
        status=response['InstanceStatuses'][0]['InstanceState']['Name']
        getpreference(status,getId)
    else:
        print("Please enter correct instance id")
        getInstanceStatus()

def getpreference(status,instId):
    if status == "running":
        print("Instance is in running state")
        pref=input("Do you want to STOP instance [yes/no] : ")
        if pref == "yes":
            stopInstance(instId)
    elif status == "stopped":
        print("instance is in stopped state")
        start_input=input("Do you want to restart it? [yes/no] : ")
        if start_input == "yes":
            startInstance(instId)
        elif start_input == "no":
            print("Thank you for running the script")
        else:
            print("Wrong input")

    else:
        print("Instance might be terminated. Please log into console")
    

def stopInstance(id):
    print("Instance: "+ id + " has been stopped" )
    response = ec2.stop_instances(
    InstanceIds=[
        id,
    ],
) 
def startInstance(id):
    print("Instance: "+ id + " has been started" )
    response = ec2.start_instances(
    InstanceIds=[
        id,
    ],
)                 

def main():
    available_zone()


if __name__ == "__main__":
    intro()
    main()

