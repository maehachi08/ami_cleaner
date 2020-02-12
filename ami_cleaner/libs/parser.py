import argparse
from argparse import RawTextHelpFormatter

from libs.sts import get_account_id


# input
#   tag_filters=[{'Name': 'hoge'}, {'Env': 'development'}]
#
# output
#   tag_filters={'Name': 'hoge', 'Env': 'development'}
def tag_filters_chain(args):
    _tag_filters = {}
    for kv in args.tag_filters:
        for k, v in kv.items():
            _tag_filters[k] = v

    args.tag_filters = _tag_filters
    return args


def create_parser():
    arg_parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)

    arg_parser.add_argument(
        '--debug',
        action='store_true',
        help='print debug log'
    )

    arg_parser.add_argument(
        '--dry-run',
        action='store_true',
        help='show of response describe-images that should be cleaned up'
    )

    arg_parser.add_argument(
        '--days',
        default=90,
        type=int,
        help='Clean up AMI images older than X days (default = 90 days)',
    )

    arg_parser.add_argument(
        '--region',
        default='ap-northeast-1',
        type=str,
        help='AWS region to watch for AMIs (default = ap-northeast-1)',
    )

    arg_parser.add_argument(
        '--owner',
        default=get_account_id(),
        type=str,
        help='AWS account owner ID \
                (default account number is getting from STS with boto3)',
    )

    # --tag-filters
    # e.g.
    # --tag-filters Name=hoge --tag-filters Env=development
    arg_parser.add_argument(
        '--tag-filters',
        default=[{}],
        type=lambda kv: dict(x.split("=") for x in kv.split(" +")),
        nargs="+",
        dest='tag_filters',
        help=f'Specify the key of the tag in the filter name and the value \
                 of the tag in the filter value.'
             f'\n\n',
    )

    return arg_parser
