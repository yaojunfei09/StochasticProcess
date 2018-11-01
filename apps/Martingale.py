import time
import numpy as np
from apps.async_method import async


from apps.constants import *


# Avraham de Moivre martingale
class MartingaleStatistics(object):
    def __init__(self):
        self.counter = 0
        self.avm_martingale_list = []
        self.martingale_statistic_mean_list = [0, ] * len(martingale_statistic_list)
        self.martingale_statistic_count_list = [0, ] * len(martingale_statistic_list)
        self.martingale_statistic_mean_list2 = [0, ] * len(martingale_statistic_list)
        self.martingale_statistic_count_list2 = [0, ] * len(martingale_statistic_list)

    @staticmethod
    def get_martingale():
        martingale_x_list = np.random.uniform(0, 100, martingale_length).tolist()
        martingale_s_list = []
        martingale_s_sum = 0
        for martingale_x in martingale_x_list:
            if martingale_x < martingale_coefficient_p * 100:
                martingale_s_sum += 1
            else:
                martingale_s_sum += -1
            martingale_s_list.append(martingale_s_sum)

        martingale_avm_list = []
        for martingale_s in martingale_s_list:
            martingale_avm_list.append(pow(martingale_coefficient_q / martingale_coefficient_p, martingale_s))
        return martingale_avm_list

    @async
    def generate_martingale(self):
        while True:
            # build a martingale
            self.counter += 1
            self.avm_martingale_list = self.get_martingale()

            # calculate the conditional mean value mean value
            for i in range(len(martingale_statistic_list)):
                num = martingale_statistic_list[i]
                # all possible value of the 6th martingale shoule be in {-6, -4, -2, 0, 2, 4, 6}
                if abs(self.avm_martingale_list[5] - pow(martingale_coefficient_q / martingale_coefficient_p, num)) \
                        < 0.000001:
                    # get the next value and calculate the corresponding mean value
                    self.martingale_statistic_mean_list[i] = (self.martingale_statistic_mean_list[i] *
                                                              self.martingale_statistic_count_list[i] +
                                                              self.avm_martingale_list[6]) / \
                                                             (self.martingale_statistic_count_list[i] + 1)
                    self.martingale_statistic_count_list[i] += 1

                    # get the next value and calculate the corresponding mean value
                    self.martingale_statistic_mean_list2[i] = (self.martingale_statistic_mean_list2[i] *
                                                               self.martingale_statistic_count_list2[i] +
                                                               self.avm_martingale_list[19]) / \
                                                              (self.martingale_statistic_count_list2[i] + 1)
                    self.martingale_statistic_count_list2[i] += 1
                    break

            # set time interval
            time.sleep(1)

    def build_statistics_table(self):
        table_html = ""

        # counter table
        table_html += "<table border='1' style='font-size:18px;'>"
        table_html += "<tr><td style='width:150px;height:30px'>Counter</td>"
        table_html += "<td style='width:150px;height:30px'>%s</td></tr></table>" % str(self.counter)
        table_html += "<br>"

        # E(Y7) table
        table_html += "<table border='1' style='font-size:18px;'><tr>"
        table_html += "<td style='width:150px;height:30px'>Condition</td>"
        for i in range(7):
            table_html += "<td style='width:150px;height:30px'>S6=%s</td>" % str(martingale_statistic_list[i])
        table_html += "</tr><tr>"
        table_html += "<td style='width:150px;height:30px'></td>"
        for i in range(7):
            table_html += "<td style='width:150px;height:30px'>Y6=%.8f</td>" % \
                          pow(martingale_coefficient_q / martingale_coefficient_p, martingale_statistic_list[i])
        table_html += "</tr><tr>"

        table_html += "<td style='width:150px;height:30px'>E(Y7|condition(Y6))</td>"
        for i in range(7):
            table_html += "<td style='width:150px;height:30px'>%.8f</td>" % self.martingale_statistic_mean_list[i]
        table_html += "</tr></table><br>"

        # E(Y20) table
        table_html += "<table border='1' style='font-size:18px;'><tr>"
        table_html += "<td style='width:150px;height:30px'>Condition</td>"
        for i in range(7):
            table_html += "<td style='width:150px;height:30px'>S6=%s</td>" % str(martingale_statistic_list[i])
        table_html += "</tr><tr>"
        table_html += "<td style='width:150px;height:30px'></td>"
        for i in range(7):
            table_html += "<td style='width:150px;height:30px'>Y6=%.8f</td>" % \
                          pow(martingale_coefficient_q / martingale_coefficient_p, martingale_statistic_list[i])
        table_html += "</tr><tr>"

        table_html += "<td style='width:150px;height:30px'>E(Y20|condition(Y6))</td>"
        for i in range(7):
            table_html += "<td style='width:150px;height:30px'>%.8f</td>" % self.martingale_statistic_mean_list2[i]
        table_html += "</tr></table><br>"

        return table_html

if __name__ == "__main__":
    martingale_statistics = MartingaleStatistics()
    martingale_statistics.generate_martingale()



