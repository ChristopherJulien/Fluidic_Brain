"""Based on the Basic Set Pressure from Fluigent SDK
​Install locally the sdk with:
```bash
    python -m pip install fluigent_sdk-22.0.0.zip
```
"""

__author__ = "Louis-Justin Tallot and Alexia Allal and Anne Meeussen"
import numpy as np
import sys
import json
import matplotlib.pyplot as plt

import time
from contextlib import contextmanager
from contextvars import ContextVar

from Fluigent.SDK import fgt_init, fgt_close
from Fluigent.SDK import fgt_set_pressure, fgt_get_pressure, fgt_get_pressureRange, fgt_ERROR


p_min_0 = ContextVar('p_min_0')
p_max_0 = ContextVar('p_max_0')

p_min_1 = ContextVar('p_min_1')
p_max_1 = ContextVar('p_max_1')


@contextmanager
def setup_experiment(nb_controllers: int = 1):
    """Context manager to setup the experiment"""
    assert nb_controllers in [1, 2]

    # Initialize the session
    fgt_init()

    attempt = fgt_set_pressure(0, 0)
    if attempt != fgt_ERROR.OK:
        raise SystemExit("Failed to find the first controller")

    if nb_controllers == 2:
        attempt = fgt_set_pressure(1, 0)
        if attempt != fgt_ERROR.OK:
            raise SystemExit("Failed to find the second controller")

    error_code, _p_min_0, _p_max_0 = fgt_get_pressureRange(0, get_error=True)
    if error_code != fgt_ERROR.OK:
        raise SystemExit("Failed to find the first controller pressure range")
    p_min_0.set(_p_min_0)
    p_max_0.set(_p_max_0)

    if nb_controllers == 2:
        error_code, _p_min_1, _p_max_1 = fgt_get_pressureRange(
            1, get_error=True)
        if error_code != fgt_ERROR.OK:
            raise SystemExit(
                "Failed to find the second controller pressure range")
        p_min_1.set(_p_min_1)
        p_max_1.set(_p_max_1)

    print("Setup initialized")

    yield
    # Set pressure to 0 before closing
    fgt_set_pressure(0, 0)

    if nb_controllers == 2:
        fgt_set_pressure(1, 0)

    # Close the session
    fgt_close()
    print("Setup closed")


class Ramp:
    def __init__(self, nb_controllers: int = 1, exp_name: str = None) -> None:
        self.nb_controllers = nb_controllers
        self.exp_name = exp_name
        self.time = 0
        self.times_list = []
        self.inputs_list = []

    def perform_one_ramp_one_controller(self, start_p, end_p, nb_steps, plateau_time) -> None:
        """Performs a pressure ramp with one controller
        from 'start_p' to 'end_p' with 'nb_steps' steps
​
        Args:
            start_p1 (float): Start pressure in mbar
            end_p1 (float): End pressure in mbar
            nb_steps (int): Number of steps
            plateau_time (float): Time spend on each pressure value in s
        """
        nb_controllers = self.nb_controllers
        assert p_min_0.get() <= start_p, "Start pressure must be greater than minimum pressure"
        assert p_min_0.get() <= end_p, "End pressure must be greater than minimum pressure"
        assert start_p <= p_max_0.get(), "Start pressure must be lower than maximum pressure"
        assert end_p <= p_max_0.get(), "End pressure must be lower than maximum pressure"
        assert nb_controllers == 1, "Should be one controller"

        p_range = np.linspace(start_p, end_p, nb_steps)
        # print(p_range)
        # return None
        for p_0 in p_range:
            fgt_set_pressure(0, p_0)
            print(f'Set pressure to p_0 = {p_0:.1f} mbar', end="\r")
            self.inputs_list.append([p_0])
            self.times_list.append(self.time)
            time.sleep(plateau_time)
            self.time += plateau_time

    def perform_ramp_two_controllers(self,
                                     start_p1: float = 0, end_p1: float = 0, nb_steps1: float = 0,
                                     start_p2: float = 0, end_p2: float = 0, nb_steps2: float = 0,
                                     plateau_time: float = 30,
                                     zigzag_p2: bool = False, nb_big_ramp_controller: int = 0
                                     ) -> None:
        """Performs a pressure ramps with two pressure controllers
        from 'start_p1' to 'end_p1' with 'nb_steps1' step size for the first contoller
        from 'start_p2' to 'end_p2' with 'nb_steps2' step size for the second contoller
​
        Args:
            start_p1 (float): Start pressure for the first controller in mbar
            end_p1 (float): End pressure for the first controller in mbar
            nb_steps1 (int): Number of steps for the first controller
            start_p2 (float): Start pressure for the second controller in mbar
            end_p2 (float): End pressure for the second controller in mbar
            nb_steps2 (int): Number of steps for the second controller
            plateau_time (float): Time spend on each pressure value in s
            zigzag_p2 (bool): If we want to reverse the direction of the ramp everytime
            nb_big_ramp_controller (int): The controller that is going to have only one big ramp
        """

        assert p_min_0.get() <= start_p1 and p_min_1.get(
        ) <= start_p2, "Start pressure must be greater than minimum pressure"
        assert p_min_0.get() <= end_p1 and p_min_1.get(
        ) <= end_p2, "End pressure must be greater than minimum pressure"
        assert start_p1 <= p_max_0.get() and start_p2 <= p_max_1.get(
        ), "Start pressure must be lower than maximum pressure"
        assert end_p1 <= p_max_0.get() and end_p2 <= p_max_1.get(
        ), "End pressure must be lower than maximum pressure"
        assert self.nb_controllers == 2, "Should be two controllers"
        assert nb_big_ramp_controller in [
            0, 1], " The controller for the big ramp should be 0 or 1"

        p_range1 = np.linspace(start_p1, end_p1, nb_steps1)
        p_range2 = np.linspace(start_p2, end_p2, nb_steps2)
        nb_many_ramps_controller = int(1 - nb_big_ramp_controller)

        for p_0 in [p_range1, p_range2][nb_big_ramp_controller]:
            # reset pressure to 0 to avoid hysteresis
            # fgt_set_pressure(nb_big_ramp_controller, 0)
            # time.sleep(plateau_time)

            fgt_set_pressure(nb_big_ramp_controller, p_0)

            for p_1 in [p_range1, p_range2][nb_many_ramps_controller]:
                # reset pressure to 0 to avoid hysteresis
                # fgt_set_pressure(nb_many_ramps_controller, 0)
                # time.sleep(plateau_time)

                fgt_set_pressure(nb_many_ramps_controller, p_1)

                if nb_big_ramp_controller == 0:
                    print(
                        f'Set pressure to p_0 = {p_0:.1f} mbar and p_1 = {p_1:.1f} mbar', end="\r")
                    self.inputs_list.append([p_0, p_1])
                else:
                    print(
                        f'Set pressure to p_0 = {p_1:.1f} mbar and p_1 = {p_0:.1f} mbar', end="\r")
                    self.inputs_list.append([p_1, p_0])
                self.times_list.append(self.time)
                time.sleep(plateau_time)
                self.time += plateau_time

            if zigzag_p2:
                if nb_big_ramp_controller == 0:
                    p_range2 = p_range2[::-1]
                else:
                    p_range1 = p_range1[::-1]  # invert direction every time

        print("Ramp finished !")

    def create_json_file(self) -> None:
        with open(f'{self.exp_name}.json', 'w') as fp:
            protocol = {
                "name": self.exp_name,
                "times": self.times_list,
                "input_pressures": self.inputs_list
            }
            json.dump(protocol, fp)

    def plot_intputs(self):
        fig, ax = plt.subplots(1, 1, figsize=[2.5, 2.5])
        self.inputs_list = np.array(self.inputs_list)
        if self.nb_controllers == 1:
            ax.plot(self.times_list, self.inputs_list, label="ctrl 1", marker='o',
                    color=[0, 0, 0])
        else:
            ax.plot(self.times_list, self.inputs_list[:, 0], label="ctrl 1", marker='o',
                    color=[0, 0, 0])
            ax.plot(self.times_list, self.inputs_list[:, 1], label="ctrl 2", marker='o',
                    color=[.5, .5, .5])
        ax.legend()
        ax.set_title(f"Inputs - {self.exp_name}")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Input pressures (mbar)")
        plt.tight_layout()
        fig.savefig(f"{self.exp_name}_figure.png")
        plt.show()


def experiment_cycle_single_controller(filename="20230208_quick",
                                       start_p=0, max_p=300, min_p=-100, step_size=25,
                                       plateau_time=30):
    """Time : 12*30s = 6min"""
    ramp = Ramp(nb_controllers=1, exp_name=filename)
    with setup_experiment(nb_controllers=ramp.nb_controllers):

        nstep_up1 = int((max_p - start_p)/step_size)+1
        max_p = start_p + step_size*(nstep_up1-1)
        nstep_down1 = int((max_p - min_p)/step_size)
        min_p = max_p - step_size*(nstep_down1)
        nstep_up2 = - nstep_up1 + nstep_down1+1

        # print(max_p, min_p, nstep_up2)
        # nstep_down = 1
        # nstep_up2 = 1
        ramp.perform_one_ramp_one_controller(
            start_p=start_p, end_p=max_p, nb_steps=nstep_up1, plateau_time=plateau_time
        )
        ramp.perform_one_ramp_one_controller(
            start_p=max_p-step_size, end_p=min_p, nb_steps=nstep_down1, plateau_time=plateau_time
        )
        ramp.perform_one_ramp_one_controller(
            start_p=min_p + step_size, end_p=0, nb_steps=nstep_up2, plateau_time=plateau_time
        )
        # ramp.create_json_file()
        # print(ramp.inputs_list)
        # ramp.plot_intputs()


def experiment_cycle_double_controller(filename="20230208_quick",
                                       start_p1=0, max_p1=30, min_p1=-10, nb_steps1=10,
                                       start_p2=0, max_p2=30, min_p2=-10, nb_steps2=10,
                                       plateau_time=5):
    ramp = Ramp(nb_controllers=2, exp_name=filename)
    with setup_experiment(nb_controllers=ramp.nb_controllers):
        nstep1_up1 = int((max_p1 - start_p1)/nb_steps1)+1
        max_p1 = start_p1 + nb_steps1*(nstep1_up1-1)
        nstep1_down1 = int((max_p1 - min_p1)/nb_steps1)
        min_p1 = max_p1 - nb_steps1*(nstep1_down1)
        nstep1_up2 = - nstep1_up1 + nstep1_down1+1

        nstep2_up1 = int((max_p2 - start_p2)/nb_steps2)+1
        max_p2 = start_p2 + nb_steps2*(nstep2_up1-1)
        nstep2_down1 = int((max_p2 - min_p2)/nb_steps2)
        min_p2 = max_p2 - nb_steps2*(nstep2_down1)
        nstep2_up2 = - nstep2_up1 + nstep2_down1+1

        ramp.perform_ramp_two_controllers(
            start_p1=start_p1, end_p1=max_p1, nb_steps1=nstep1_up1,
            start_p2=start_p2, end_p2=max_p2, nb_steps2=nstep2_up1,
            plateau_time=plateau_time,
        )
        ramp.perform_ramp_two_controllers(
            start_p1=max_p1-nb_steps1, end_p1=min_p1, nb_steps1=nstep1_down1,
            start_p2=max_p2-nb_steps2, end_p2=min_p2, nb_steps2=nstep2_down1,
            plateau_time=plateau_time,
        )
        ramp.perform_ramp_two_controllers(
            start_p1=min_p1+nb_steps1, end_p1=0, nb_steps1=nstep1_up2,
            start_p2=min_p2+nb_steps2, end_p2=0, nb_steps2=nstep2_up2,
            plateau_time=plateau_time,
        )


if __name__ == "__main__":

    # experiment_cycle_single_controller(r'./test/input_ramp', min_p=0,
    #                                    max_p=30, step_size=30,
    #                                    plateau_time=5)
    experiment_cycle_double_controller(r'./test/input_ramp', start_p1=0, max_p1=30, min_p1=-10, nb_steps1=10,
                                       start_p2=0, max_p2=30, min_p2=-10, nb_steps2=10,
                                       plateau_time=5)
