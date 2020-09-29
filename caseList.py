import calendar
import time

Fake_case_20200702 = ["324", "329", "360", "381", "423", "430", "438", "439", "440", "452",
                      "453", "454", "469", "505", "513", "517", "527", "536"]

Fake_case_timestamp = [1581998400, 1582516800, 1583985600, 1585108800, 1587009600,
                       1587614400, 1588046400, 1588219200, 1588132800, 1588824000,
                       1588824000, 1588910400, 1589860800, 1591761600, 1558324800,
                       1592452800, 1593403200, 1593662400]

Real_case_20200702 = ["Real1", "Real2", "Real3", "Real4", "Real5", "Real6" , "Real7", "Real8", "Real9", "Real10",
                      "Real11", "Real12", "Real13", "Real14", "Real15", "Real16", "Real17", "Real18", "Real19", "Real20",
                      "Real21", "Real22", "Real23", "Real24", "Real25", "Real26", "Real27", "Real28", "Real29", "Real30",
                      "Real31", "Real32", "Real33", "Real34", "Real35", "Real36", "Real37", "Real38"]

ts = calendar.timegm(time.gmtime())
Real_case_timestamp = [ts] * len(Real_case_20200702)