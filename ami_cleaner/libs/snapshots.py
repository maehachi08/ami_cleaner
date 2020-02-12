import boto3


def delete_image_snapshopt(args, image):
    for device in image['BlockDeviceMappings']:
        if 'SnapshotId' in device['Ebs']:
            snapshot_id = device['Ebs']['SnapshotId']
            _delete_specified_snapshot(args, snapshot_id)


# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.delete_snapshot
def _delete_specified_snapshot(args, snapshot_id):
    client = _get_client(args.region)
    client.delete_snapshot(
        SnapshotId=snapshot_id
    )


def _get_client(region: str):
    return boto3.client('ec2', region)
