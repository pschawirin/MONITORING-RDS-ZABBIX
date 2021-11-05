#!/usr/bin/env python

# script that monitors CloudWatch stats for RDS instances.
#
# Requirements:
# - Boto (http://boto.s3.amazonaws.com/index.html)
#
# Plugin arguments:
# 1. DBInstanceIdentifier (name)
# 2. AWS Access Key
# 3. AWS Secret Access Key
# 4. RDS Metric
#

import datetime
import sys
from optparse import OptionParser
from boto.ec2.cloudwatch import CloudWatchConnection

### Arguments
parser = OptionParser()
parser.add_option("-i", "--instance-id", dest="instance_id",
                help="DBInstanceIdentifier")
parser.add_option("-a", "--access-key", dest="access_key",
                help="AWS Access Key")
parser.add_option("-k", "--secret-key", dest="secret_key",
                help="AWS Secret Access Key")
parser.add_option("-m", "--metric", dest="metric",
                help="RDS cloudwatch metric")

(options, args) = parser.parse_args()

if (options.instance_id == None):
    parser.error("-i DBInstanceIdentifier is required")
if (options.access_key == None):
    parser.error("-a AWS Access Key is required")
if (options.secret_key == None):
    parser.error("-k AWS Secret Key is required")
if (options.metric == None):
    parser.error("-m RDS cloudwatch metric is required")
###

### Actual code
metrics = {"CPUUtilization":{"type":"float", "value":None},
    "ReadLatency":{"type":"float", "value":None},
    "DatabaseConnections":{"type":"int", "value":None},
    "FreeableMemory":{"type":"float", "value":None},
    "ReadIOPS":{"type":"int", "value":None},
    "WriteLatency":{"type":"float", "value":None},
    "WriteThroughput":{"type":"float", "value":None},
    "WriteIOPS":{"type":"int", "value":None},
    "SwapUsage":{"type":"float", "value":None},
    "ReadThroughput":{"type":"float", "value":None},
    "DiskQueueDepth":{"type":"float", "value":None},
    "NetworkReceiveThroughput":{"type":"float", "value":None},
    "NetworkTransmitThroughput":{"type":"float", "value":None},
    "FreeStorageSpace":{"type":"float", "value":None}}

end = datetime.datetime.now()
start = end - datetime.timedelta(minutes=5)

conn = CloudWatchConnection(options.access_key, options.secret_key)
for k,vh in metrics.items():

    if (k == options.metric):

        try:
                res = conn.get_metric_statistics(60, start, end, k, "AWS/RDS", "Average", {"DBInstanceIdentifier": options.instance_id})
        except Exception, e:
                print "Error executing rds_stats: %s" % e.error_message
                sys.exit(1)
        average = res[-1]["Average"] # last item in result set
        if (k == "FreeStorageSpace" or k == "FreeableMemory"):
                average = average / 1024.0**3.0
        if vh["type"] == "float":
                metrics[k]["value"] = "%.4f" % average
        if vh["type"] == "int":
                metrics[k]["value"] = "%i" % average

        print "%s" % (vh["value"])
        break                                                                                                                                                                                                     1,1           Top
