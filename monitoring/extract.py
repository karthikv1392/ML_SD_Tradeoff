import argparse
from loguru import logger

import monitoring.services as services

parser = argparse.ArgumentParser()
parser.add_argument("--id", type=str)
parser.add_argument("--f", type=str)
parser.add_argument("--type", type=str)


args = parser.parse_args()

if args.id is None or args.f is None or args.type is None:
    logger.error("Error. Please provide all the requested args")
    exit(1)

if args.type == "rt":
    logger.debug(f"Extracting rt csv at folder '{args.f}' of workload with id '{args.id}'")
    services.generate_rt_csv_by_workload_id(args.id, args.f)

elif args.type == "cpu":
    logger.debug(f"Extracting cpu csv at folder '{args.f}' of workload with id '{args.id}'")
    services.generate_cpu_csv_by_workload_id(args.id, args.f)

else:
    logger.error("Bad type params. Valid options are 'rt' and 'cpu'")
    exit(1)
