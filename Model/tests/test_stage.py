# Dependences
import pandas as pd
import numpy as np
import os
import sys
import traceback

# radCAD
from radcad import Model, Simulation, Experiment
from radcad.engine import Engine, Backend


# Project dependences
# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go up one folder
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

# Append the parent directory to sys.path
sys.path.append(parent_dir)

from sys_params import *
import state_variables
import state_update_blocks
import sys_params
from parts.utils import *
from plots import *
from post_processing import *

import importlib
importlib.reload(state_variables)
importlib.reload(state_update_blocks)
importlib.reload(sys_params)

QTM_data_tables = pd.read_csv('./Quantitative_Token_Model_V1.88_radCad_integration - Data Tables.csv')

if __name__ == '__main__'   :
    MONTE_CARLO_RUNS = 1
    TIMESTEPS = 12*10

    model = Model(initial_state=state_variables.initial_state, params=sys_params.sys_param, state_update_blocks=state_update_blocks.state_update_block)
    simulation = Simulation(model=model, timesteps=TIMESTEPS, runs=MONTE_CARLO_RUNS)

    result = simulation.run()
    df = pd.DataFrame(result)

    # post processing
    data = postprocessing(df)

    # test vesting values
    print("\n------------------------------------")
    print("Testing vesting values of radCad timeseries simulation against QTM data tables...")
    # test all except for the market investors
    for i in range(len(stakeholder_names)-1):
        stakeholder = stakeholder_names[i]
        test_timeseries(data=data, data_key=stakeholder+"_tokens_vested", QTM_data_tables=QTM_data_tables, QTM_row=28+i, relative_tolerance=0.001)

    print("\n")
    print(u'\u2713'+" ALL TESTS PASSED!")
    print("\n------------------------------------")
        

