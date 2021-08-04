import psutil as ps
from datetime import datetime
from utilities import get_logger
from utilities import LOG_FILE_NAME

logger = get_logger(__name__, LOG_FILE_NAME)


class Metrics(object):

    def __init__(self):
        logger.info("First collecting of metrics")

        self.time = datetime.now()
        vm = ps.virtual_memory()
        disks = ps.disk_usage('/')
        net = ps.net_io_counters()

        self.cpu_percent = ps.cpu_percent()
        self.cpu_current_freq = ps.cpu_freq()[0]

        self.virtual_memory_percent = vm[2]
        self.virtual_memory_used = vm[3]
        self.virtual_memory_free = vm[4]
        self.virtual_memory_available = vm[1]

        self.disk_percent = disks[3]
        self.disk_used = disks[1]
        self.disk_free = disks[2]

        self.network_bytes_sent = net[0]
        self.network_bytes_recv = net[1]
        self.network_err_in = net[4]
        self.network_err_out = net[5]

        self.disk_percent = disks[3]
        self.disk_used = disks[1]
        self.disk_free = disks[2]
        self.cpu_min_freq = ps.cpu_freq()[1]
        self.cpu_max_freq = ps.cpu_freq()[2]
        self.cpu_count = ps.cpu_count()
        self.virtual_memory_total = vm[0]
        self.disk_total = disks[0]

    def refresh(self):
        logger.info("Refresh metrics")
        self.time = datetime.now()
        vm = ps.virtual_memory()
        disks = ps.disk_usage('/')
        net = ps.net_io_counters()

        self.cpu_percent = ps.cpu_percent()
        self.cpu_current_freq = ps.cpu_freq()[0]
        # self.cpu_stats = ps.cpu_stats()
        # self.cpu_times = ps.cpu_times()

        self.virtual_memory_percent = vm[2]
        self.virtual_memory_used = vm[3]
        self.virtual_memory_free = vm[4]
        self.virtual_memory_available = vm[1]

        self.disk_percent = disks[3]
        self.disk_used = disks[1]
        self.disk_free = disks[2]

        self.network_bytes_sent = net[0]
        self.network_bytes_recv = net[1]
        self.network_err_in = net[4]
        self.network_err_out = net[5]

    def metrics_list(self):
        return [self.time,

                self.cpu_percent,
                self.cpu_current_freq,
                # self.cpu_stats,
                # self.cpu_times,

                self.virtual_memory_percent,
                self.virtual_memory_used,
                self.virtual_memory_free,
                self.virtual_memory_available,

                self.disk_percent,
                self.disk_used,
                self.disk_free,

                self.network_bytes_sent,
                self.network_bytes_recv,
                self.network_err_in,
                self.network_err_out
                ]

    def static_metrics(self):
        return [self.cpu_min_freq,
                self.cpu_max_freq,
                self.cpu_count,
                self.virtual_memory_total,
                self.disk_total]
