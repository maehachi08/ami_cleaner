import sys
import traceback

from libs.parser import create_parser
from libs.parser import tag_filters_chain
from libs.images import get_images_should_deregister
from libs.images import deregister_image
from libs.images import print_tableview
from libs.snapshots import delete_image_snapshopt
from libs.logger import get_logger


def main():
    try:
        arg_parser = create_parser()
        _args = arg_parser.parse_args()
        args = tag_filters_chain(_args)

        logger = get_logger(args)
        logger.debug('main startedi.')

        images = get_images_should_deregister(args)
        if args.dry_run:
            if images['Images']:
                print_tableview(images)
            return

        for image in images['Images']:
            image_id = image['ImageId']
            logger.info(f'AMI: {image_id} start.')
            deregister_image(args, image_id)
            delete_image_snapshopt(args, image)
            logger.info(f'AMI: {image_id} end.')

    except Exception as e:
        logger.error(str(e))
        traceback.print_exc(file=sys.stdout)


if __name__ == "__main__":
    main()
