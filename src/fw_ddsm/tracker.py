from pandas import DataFrame as df
from src.fw_ddsm.common.parameter import *
from src.fw_ddsm.functions.custom_functions import average, bisect_left


class Tracker:

    def __init__(self, ):
        self.data = dict()
        self.name = "name"

    def new(self, name=""):
        self.name = name
        # self.par_weight = par_cost_weight

        for key in [s_starts, s_demand, s_demand_max, s_demand_total, s_demand_reduction, s_par,
                    s_penalty, s_obj, p_prices, p_cost, p_cost_reduction, p_step, t_time, b_profile, s_debugger]:
            self.data[key] = dict()

    def read(self, existing_tracker):
        self.data = dict()
        self.data = existing_tracker.copy()
        # self.par_weight = par_cost_weight

    def update(self, num_record, tracker_data=None, demands=None, prices=None, penalty=None, par=None, obj=None,
               run_time=None, cost=None, step=None, init_demand_max=None, init_cost=None, tasks_starts=None,
               battery_profile=None, obj_par=True, obj_max=True, debugger=None):
        obj2 = 0
        if tracker_data is None:
            tracker_data = self.data
        if step is not None:
            tracker_data[p_step][num_record] = round(step, 4)
        if prices is not None:
            tracker_data[p_prices][num_record] = prices
        if cost is not None:
            cost2 = round(cost, 2)
            tracker_data[p_cost][num_record] = cost2
            obj2 += cost2
            if init_cost is not None:
                tracker_data[p_cost_reduction][num_record] = round((init_cost - cost) / init_cost, 2)
        if penalty is not None:
            penalty2 = round(penalty, 2)
            tracker_data[s_penalty][num_record] = penalty2
            obj2 += penalty2
        if demands is not None:
            demand_max = round(max(demands), 2)
            obj2 += int(obj_max) * demand_max
            tracker_data[s_demand][num_record] = demands
            tracker_data[s_demand_max][num_record] = demand_max
            tracker_data[s_demand_total][num_record] = round(sum(demands), 2)
            if par is None:
                par = round(demand_max / average(demands), 2)
            tracker_data[s_par][num_record] = par
            obj2 += int(obj_par) * par
            if init_demand_max is not None:
                tracker_data[s_demand_reduction][num_record] \
                    = round((init_demand_max - demand_max) / init_demand_max, 2)
        if run_time is not None:
            tracker_data[t_time][num_record] = round(run_time, 4)
        if tasks_starts is not None:
            tracker_data[s_starts][num_record] = tasks_starts
        if battery_profile is not None:
            tracker_data[b_profile][num_record] = battery_profile
        if debugger is not None:
            tracker_data[s_debugger][num_record] = debugger
        if obj is not None:
            tracker_data[s_obj][num_record] = obj
        else:
            tracker_data[s_obj][num_record] = obj2

        return tracker_data

    def extract_data(self):

        demands = self.data[s_demand]
        batteries = self.data[b_profile]
        prices = self.data[p_prices]
        others = {k: self.data[k]
                  for k in [s_par, s_demand_reduction, p_cost_reduction, s_penalty,
                            s_demand_total, s_demand_max, p_cost, s_obj, t_time, p_step]}
        debugger = self.data[s_debugger]
        return demands, batteries, prices, others, debugger

    def write_to_file(self, folder, print_demands=True, print_prices=True, print_others=True,
                      print_batteries=True, print_debugger=True):
        demands, batteries, prices, others, debugger = self.extract_data()
        if print_demands:
            df_demands = df.from_dict(demands).div(1000)
            df_demands.to_csv(r"{}{}_demands.csv".format(folder, self.name))
        if print_prices:
            df_prices = df.from_dict(prices)
            df_prices.to_csv(r"{}{}_prices.csv".format(folder, self.name))
        if print_others:
            df_others = df.from_dict(others)
            df_others.to_csv(r"{}{}_others.csv".format(folder, self.name))
        if print_batteries:
            df_batteries = df.from_dict(batteries)
            df_batteries.to_csv(r"{}{}_batteries.csv".format(folder, self.name))
        if print_debugger:
            df_debugger = df.from_dict(debugger)
            df_debugger.to_csv(r"{}{}_debugger.csv".format(folder, self.name))

