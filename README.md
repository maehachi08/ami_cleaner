# ami_cleaner

```
$ python3 ami_cleaner.py --help
usage: ami_cleaner.py [-h] [--debug] [--dry-run] [--days DAYS]
                      [--region REGION] [--owner OWNER]
                      [--tag-filters TAG_FILTERS [TAG_FILTERS ...]]

optional arguments:
  -h, --help            show this help message and exit
  --debug               print debug log
  --dry-run             show of response describe-images that should be cleaned up
  --days DAYS           Clean up AMI images older than X days (default = 90 days)
  --region REGION       AWS region to watch for AMIs (default = ap-northeast-1)
  --owner OWNER         AWS account owner ID (default account number is getting from STS with boto3)
  --tag-filters TAG_FILTERS [TAG_FILTERS ...]
                        Specify the key of the tag in the  filter  name  and the value of the tag in the filter value.

```

## --debug option sample

```
$ python3 ami_cleaner.py --debug
2020-02-07 21:32:18,087 DEBUG    ami_cleaner:20   main             main startedi.
2020-02-07 21:32:18,088 DEBUG    ami_cleaner.libs.images:22   get_images_should_deregister function started
2020-02-07 21:32:18,088 DEBUG    ami_cleaner.libs.images:38   __get_client     function started
2020-02-07 21:32:18,220 DEBUG    ami_cleaner.libs.images:82   __get_images_should_deregister function started
2020-02-07 21:32:18,220 DEBUG    ami_cleaner.libs.images:73   __tag_filter_generate function started
2020-02-07 21:32:18,686 DEBUG    ami_cleaner.libs.images:90   __get_images_should_deregister describe_images response is...
2020-02-07 21:32:18,686 DEBUG    ami_cleaner.libs.images:91   __get_images_should_deregister {"Images": [], "ResponseMetadata": {"RequestId": "0fe7edaa-aed3-447f-8866-f98be24043dd", "HTTPStatusCode": 200, "HTTPHeaders": {"content-type": "text/xml;charset=UTF-8", "content-length": "219", "date": "Fri, 07 Feb 2020 12:33:14 GMT", "server": "AmazonEC2"}, "RetryAttempts": 0}}
2020-02-07 21:32:18,687 DEBUG    ami_cleaner.libs.images:102  __get_images_should_deregister The following images should be deregister.
2020-02-07 21:32:18,687 DEBUG    ami_cleaner.libs.images:103  __get_images_should_deregister []
```

#### with traceback

```
2020-02-07 21:17:38,909 DEBUG    ami_cleaner.libs.images:29   deregister_image function started
2020-02-07 21:17:38,909 DEBUG    ami_cleaner.libs.images:38   __get_client     function started
2020-02-07 21:17:38,915 DEBUG    ami_cleaner.libs.images:31   deregister_image deregister_image start(ami-0a47aa0bba5ab882e)
2020-02-07 21:17:39,364 ERROR    ami_cleaner:33   main             An error occurred (InvalidSnapshot.InUse) when calling the DeleteSnapshot operation: The snapshot snap-015cd56
f22227bac6 is currently in use by ami-0a47aa0bba5ab882e
Traceback (most recent call last):
  File "ami_cleaner.py", line 30, in main
    delete_image_snapshopt(args, image)
  File "/Users/maehachi08/work/git/ami_cleaner/libs/snapshots.py", line 8, in delete_image_snapshopt
    __delete_specified_snapshot(args, snapshot_id)
  File "/Users/maehachi08/work/git/ami_cleaner/libs/snapshots.py", line 15, in __delete_specified_snapshot
    SnapshotId=snapshot_id
  File "/Users/maehachi08/.local/lib/python3.6/site-packages/botocore/client.py", line 312, in _api_call
    return self._make_api_call(operation_name, kwargs)
  File "/Users/maehachi08/.local/lib/python3.6/site-packages/botocore/client.py", line 605, in _make_api_call
    raise error_class(parsed_response, operation_name)
botocore.exceptions.ClientError: An error occurred (InvalidSnapshot.InUse) when calling the DeleteSnapshot operation: The snapshot snap-015cd56f22227bac6 is currently in use by
ami-0a47aa0bba5ab882e
```
