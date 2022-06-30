import argparse
from loguru import logger

import monitoring.services as services

parser = argparse.ArgumentParser()
parser.add_argument("--f", type=str)  # folder
parser.add_argument("--type", type=str)


args = parser.parse_args()

if args.f is None or args.type is None:
    logger.error("Error. Please provide all the requested args")
    exit(1)

id_start = int(input("Enter starting id: "))
id_end = int(input("Enter ending id: "))

ids = range(id_start, id_end+1)

logger.debug(f"Will be generated csv for these ids: {ids}")

if args.type == "rt":
    logger.debug(f"Extracting rt csv at folder '{args.f}'")
    for i in ids:
        services.generate_rt_csv_by_workload_id(i, args.f)

elif args.type == "cpu":
    logger.debug(f"Extracting cpu csv at folder '{args.f}'")
    for i in ids:
        services.generate_cpu_csv_by_workload_id(i, args.f)

else:
    logger.error("Bad type params. Valid options are 'rt' and 'cpu'")
    exit(1)
