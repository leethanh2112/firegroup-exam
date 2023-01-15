#!/usr/bin/env python3
from flask import Flask
import json
import time
import boto3
import request

asg_client = boto3.client('autoscaling')
ec2_client = boto3.client('ec2')

app = Flask(__name__)

@app.route('/exam')
def exam(request):
    asg = request.forms.get("asg-name")
    asg_response = asg_client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg])
    instance_ids = []
    for i in asg_response['AutoScalingGroups']:
        for k in i['Instances']:
            instance_ids.append(k['InstanceId'])

    old_lc = []
    for i in asg_response['AutoScalingGroups']:
        old_lc.append(i['LaunchConfigurationName'])

    new_ami = ec2_client.create_image(
        Description='new AMI for InstanceId',
        InstanceId = instance_ids[0],
        Name=time.strftime("%Y%m%d-%H%M"),
        NoReboot=True,
    )

    lc_response = asg_client.describe_launch_configurations(LaunchConfigurationNames=old_lc)

    old_lc_KeyName = []
    for i in lc_response['LaunchConfigurations']:
        old_lc_KeyName.append(i['KeyName'])

    old_lc_SecurityGroups = []
    for i in lc_response['LaunchConfigurations']:
        for k in i['SecurityGroups']:
            old_lc_SecurityGroups.append(k)

    old_lc_InstanceType = []
    for i in lc_response['LaunchConfigurations']:
        old_lc_InstanceType.append(i['InstanceType'])

    old_lc_UserData = []
    for i in lc_response['LaunchConfigurations']:
        old_lc_UserData.append(i['UserData'])

    old_lc_IamInstanceProfile = []
    for i in lc_response['LaunchConfigurations']:
        old_lc_IamInstanceProfile.append(i['IamInstanceProfile'])

    lc_new = asg_client.create_launch_configuration(
        IamInstanceProfile = old_lc_IamInstanceProfile[0],
        ImageId = new_ami['ImageId'],
        InstanceType = old_lc_InstanceType[0],
        LaunchConfigurationName = time.strftime("%Y%m%d-%H%M"),
        SecurityGroups= old_lc_SecurityGroups,
    )

    lc_new_response = asg_client.describe_launch_configurations(LaunchConfigurationNames=[time.strftime("%Y%m%d-%H%M")])

    new_lc_Name = []
    for i in lc_new_response['LaunchConfigurations']:
        new_lc_Name.append(i['LaunchConfigurationName'])    

    update_asg = asg_client.update_auto_scaling_group(
        AutoScalingGroupName = asg,
        LaunchConfigurationName = new_lc_Name[0],
    )
    
    i = new_lc_Name[0]
    if i in new_lc_Name:
        return[i, "true"]
    else:
        return("false")

if __name__ == "__main__":
    app.run(
      host="0.0.0.0",
      port=5000,
      debug=True
)
