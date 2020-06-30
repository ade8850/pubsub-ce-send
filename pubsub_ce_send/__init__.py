import argparse
import sys
import io
import os

from google.cloud import pubsub_v1
from google.oauth2 import service_account


parser = argparse.ArgumentParser(description="Send cloudevents to pubsub")
parser.add_argument("--type", dest="type", nargs="?", help="type", required=True)
parser.add_argument("--subject", dest="subject", nargs="?", help="subject", required=True)
pgroup = parser.add_mutually_exclusive_group(required=False)
pgroup.add_argument("--payload", dest="payload", nargs="?", help="payload", default=b"{}")
pgroup.add_argument("--payload-from", dest="payload", nargs="?", help="payload from file", type=argparse.FileType())
parser.add_argument("--gcp-credentials-from", dest="credentials", nargs="?", help="google cloud credentials file")
parser.add_argument("--topic", dest="topic", nargs="?", help="pubsub topic", required=True)
parser.add_argument("--attrs", dest="attrs", nargs="+", help="extended attributes", default=[])
""
def main():
    args = parser.parse_args()
    payload = str(args.payload)
    if isinstance(args.payload, io.TextIOWrapper):
        payload = args.payload.read()
    #payload=json.loads(payload)
    gcp_credentials = args.credentials
    if gcp_credentials is None:
        gcp_credentials = os.environ.get("GOOGLE_CLOUD_CREDENTIALS")
    if gcp_credentials is None:
        parser.print_help()
        print("NO GOOGLE CLOUD CREDENTIALS", file=sys.stderr)
        sys.exit(1)

    attrs = {}
    for k, v in [attr.split("=") for attr in args.attrs]:
        attrs[k] = v

    print(f"gcp credentials: {args.credentials}")
    print(f"pubsub topic: {args.topic}")
    print(f"type: {args.type}", file=sys.stderr)
    print(f"subject: {args.subject}", file=sys.stderr)
    print(f"payload: {payload}", file=sys.stderr)
    print(f"attrs: {attrs}", file=sys.stderr)

    attrs.update({'subject': args.subject, 'type': args.type})

    credentials = service_account.Credentials.from_service_account_file(args.credentials)
    publisher = pubsub_v1.PublisherClient(credentials=credentials)
    topic_path = publisher.topic_path(credentials.project_id, args.topic)
    future = publisher.publish(topic_path, data=payload.encode("utf-8"), **attrs, contentType="text/json")
    future.add_done_callback(lambda x: print(x.result()))

