import time
import numpy as np

from apps.constants import *
from apps.async_method import *


class BrownianStatistics(object):
    def __init__(self):
        self.counter = 0
        self.brownian_motion_list = []
        self.brownian_mean_list = [0, ] * statistics_count
        self.brownian_multiple_mean_list = [0, ] * (statistics_count - 1)

    @staticmethod
    def get_brownian_motion(norm_distribution_list):
        brownian_motion_list = [0, ]
        norm_sum = 0
        for norm_value in norm_distribution_list:
            norm_sum += norm_value
            brownian_motion_list.append(norm_sum)
        return brownian_motion_list

    @async
    def generate_brownian_motion(self):
        while True:
            # generate brownian motion
            norm_distribution_list = list(np.random.normal(0, 1, brownian_motion_length))
            self.brownian_motion_list = self.get_brownian_motion(norm_distribution_list)

            # get mean of brownian motion
            for i in range(statistics_count):
                brownian_mean = (self.brownian_mean_list[i] * self.counter + self.brownian_motion_list[(i + 1) * 20]) \
                                / (self.counter + 1)
                self.brownian_mean_list[i] = brownian_mean

            # get mean of brownian motion multiple
            for i in range(statistics_count - 1):
                brownian_multiple_mean = (self.brownian_multiple_mean_list[i] * self.counter +
                                          self.brownian_motion_list[(i + 1) * 20] * self.brownian_motion_list
                                          [(i + 2) * 20]) / (self.counter + 1)
                self.brownian_multiple_mean_list[i] = brownian_multiple_mean
            self.counter += 1

            # set time interval
            time.sleep(1)

    def build_statistics_table(self):
        table_html = ""

        # counter table
        table_html += "<table border='1' style='font-size:18px;'>"
        table_html += "<tr><td style='width:150px;height:30px'>counter</td>"
        table_html += "<td style='width:150px;height:30px'>%s</td></tr></table>" % str(self.counter)
        table_html += "<br>"

        # EBn table
        table_html += "<table border='1' style='font-size:18px;'><tr>"
        for i in range(statistics_count):
            table_html += "<td style='width:150px;height:30px'>E(B%s)</td>" % str((i + 1) * statistics_interval)
        table_html += "</tr><tr>"
        for i in range(statistics_count):
            table_html += "<td style='width:150px;height:30px'>%.8f</td>" % self.brownian_mean_list[i]
        table_html += "</tr></table><br>"

        # EBn*Bm
        table_html += "<table border='1' style='font-size:18px;'><tr>"
        for i in range(statistics_count - 1):
            table_html += "<td style='width:150px;height:30px'>E(B%s * B%s)</td>" % (
            str((i + 1) * statistics_interval),
            str((i + 2) * statistics_interval))
        table_html += "</tr><tr>"
        for i in range(statistics_count - 1):
            table_html += "<td style='width:150px;height:30px'>%.8f</td>" % self.brownian_multiple_mean_list[i]
        table_html += "</tr></table><br>"

        return table_html

