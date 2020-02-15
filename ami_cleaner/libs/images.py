import json
import boto3
from datetime import datetime, timedelta
from prettytable import PrettyTable
from logging import getLogger

logger = getLogger('ami_cleaner').getChild(__name__)


def print_tableview(images):
    logger.debug('function started')
    pt = PrettyTable()
    pt.field_names = ['ImageId', 'Name', 'CreationDate']

    for image in images['Images']:
        pt.add_row([image['ImageId'], image['Name'], image['CreationDate']])

    print(pt)


def get_images_should_deregister(args):
    logger.debug('function started')
    client = _get_client(args.region)
    images = _get_images_should_deregister(client, args)
    return images


def deregister_image(args, image_id):
    logger.debug('function started')
    client = _get_client(args.region)
    logger.debug(f'deregister_image start({image_id})')
    client.deregister_image(
        ImageId=image_id,
    )


def _get_client(region: str):
    logger.debug('function started')
    return boto3.client('ec2', region)


def _is_using_image(args, image) -> bool:
    logger.debug('function started')
    flag = True
    image_id = image['ImageId']
    client = _get_client(args.region)
    response = _get_inatances_specific_image_id(client, image_id)

    instances = response['Reservations']
    if not instances:
        flag = False

    return flag


def _is_creation_date_expire_limit(args, image) -> bool:
    logger.debug('function started')
    days_count = args.days
    ami_age_limit = _get_datetime_now() - timedelta(days=days_count)

    date_string = image['CreationDate']
    image_dt = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')

    # print(f"AMI({image['ImageId']}): {image_dt} < {ami_age_limit}")
    if image_dt < ami_age_limit:
        # print(f"AMI({image['ImageId']}) should will be deregister.")
        return True

    return False


def _get_datetime_now():
    return datetime.now()


def _tag_filter_generate(args):
    logger.debug('function started')
    items = []
    for k, v in args.tag_filters.items():
        items.append({'Name': f'tag:{k}', 'Values': [v]})
    return items


# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_images
def _get_images_should_deregister(client, args):
    logger.debug('function started')
    images = []
    response = client.describe_images(
        Owners=[
            args.owner
        ],
        Filters=_tag_filter_generate(args)
    )
    logger.debug('describe_images response is...')
    logger.debug(json.dumps(response))

    for image in response['Images']:
        is_limit = _is_creation_date_expire_limit(args, image)
        is_using = _is_using_image(args, image)

        if is_limit and not is_using:
            logger.debug('this image should deregister.')
            logger.debug(json.dumps(image))
            images.append(image)

    logger.debug('The following images should be deregister.')
    logger.debug(json.dumps(images))
    return {'Images': images}


# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instances
def _get_inatances_specific_image_id(client, image_id):
    logger.debug('function started.')
    response = client.describe_instances(
        Filters=[
            {
                'Name': 'image-id',
                'Values': [image_id]
            }
        ]
    )
    logger.debug('describe_instances response is...')
    logger.debug(json.dumps(response))
    return response
