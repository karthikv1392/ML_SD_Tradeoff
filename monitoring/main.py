from monitoring.config import DMON_NETWORK_TOPIC, DMON_STRUCTURE_TOPIC, DMON_MERGED_TOPIC
from monitoring.core import RedisMonitor, live
import argparse
from loguru import logger
import monitoring.services as services
from multiprocessing import Process

parser = argparse.ArgumentParser()
parser.add_argument("--m", type=str)
parser.add_argument("--ts_init", type=str)
parser.add_argument("--ts_end", type=str)
parser.add_argument("--days_count", type=str)
parser.add_argument("--day_duration", type=str)
parser.add_argument("--label", type=str)
parser.add_argument("--live", type=bool)

args = parser.parse_args()


def main_live():
    p_rt = Process(target=live, args=(DMON_NETWORK_TOPIC,))
    p_rt.start()
    p_cpu = Process(target=live, args=(DMON_STRUCTURE_TOPIC,))
    p_cpu.start()

    p_rt.join()
    p_cpu.join()


if __name__ == '__main__':
    if args.m == "test":
        service_monitor = RedisMonitor()
        service_monitor.test(DMON_MERGED_TOPIC)
    elif args.m == "live_monitoring":
        main_live()
    elif args.m == "response_time":
        service_monitor = RedisMonitor()
        service_monitor.start_monitoring(DMON_NETWORK_TOPIC, live=args.live)
    elif args.m == "api":
        import uvicorn

        uvicorn.run('monitoring.app:app', host='0.0.0.0', port=8003, reload=True)
    elif args.m == "cpu_utilization":
        service_monitor = RedisMonitor()
        service_monitor.start_monitoring(DMON_STRUCTURE_TOPIC, live=args.live)
    elif args.m == "save_workload":
        if args.ts_init is None or args.ts_end is None or args.days_count is None or args.day_duration is None or args.label is None:
            logger.error("Error. Please provide all the requested args")
            exit(1)
        services.store_workload(args.ts_init, args.ts_end, args.days_count, args.day_duration, args.label)
    else:
        logger.debug("Invalid value for arg --m")
