# Copyright (c) 2020 by Fraunhofer Institute for Energy Economics
# and Energy System Technology (IEE), Kassel. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be found in the LICENSE file.
import pandapipes
import pytest


@pytest.fixture
def net_plotting():
    net = pandapipes.create_empty_network(fluid="lgas")

    # create network elements, such as junctions, external grid, pipes, valves, sinks and sources
    junction1 = pandapipes.create_junction(net, pn_bar=1.05, tfluid_k=293.15,
                                           name="Connection to External Grid", geodata=(0, 0))
    junction2 = pandapipes.create_junction(net, pn_bar=1.05, tfluid_k=293.15, name="Junction 2",
                                           geodata=(2, 0))
    junction3 = pandapipes.create_junction(net, pn_bar=1.05, tfluid_k=293.15, name="Junction 3",
                                           geodata=(7, 4))
    junction4 = pandapipes.create_junction(net, pn_bar=1.05, tfluid_k=293.15, name="Junction 4",
                                           geodata=(7, -4))
    junction5 = pandapipes.create_junction(net, pn_bar=1.05, tfluid_k=293.15, name="Junction 5",
                                           geodata=(5, 3))
    junction6 = pandapipes.create_junction(net, pn_bar=1.05, tfluid_k=293.15, name="Junction 6",
                                           geodata=(5, -3))
    junction7 = pandapipes.create_junction(net, pn_bar=1.05, tfluid_k=293.15, name="Junction 7",
                                           geodata=(9, -4))
    junction8 = pandapipes.create_junction(net, pn_bar=1.05, tfluid_k=293.15, name="Junction 7",
                                           geodata=(9, 4))

    pandapipes.create_ext_grid(net, junction=junction1, p_bar=1.1, t_k=293.15,
                               name="Grid Connection")
    pandapipes.create_pipe_from_parameters(net, from_junction=junction1, to_junction=junction2,
                                           length_km=10, diameter_m=0.3, name="Pipe 1",
                                           geodata=[(0, 0), (2, 0)])
    pandapipes.create_pipe_from_parameters(net, from_junction=junction2, to_junction=junction3,
                                           length_km=2, diameter_m=0.3, name="Pipe 2",
                                           geodata=[(2, 0), (2, 4), (7, 4)])
    pandapipes.create_pipe_from_parameters(net, from_junction=junction2, to_junction=junction4,
                                           length_km=2.5, diameter_m=0.3, name="Pipe 3",
                                           geodata=[(2, 0), (2, -4), (7, -4)])
    pandapipes.create_pipe_from_parameters(net, from_junction=junction3, to_junction=junction5,
                                           length_km=1, diameter_m=0.3, name="Pipe 4",
                                           geodata=[(7, 4), (7, 3), (5, 3)])
    pandapipes.create_pipe_from_parameters(net, from_junction=junction4, to_junction=junction6,
                                           length_km=1, diameter_m=0.3, name="Pipe 5",
                                           geodata=[(7, -4), (7, -3), (5, -3)])
    pandapipes.create_pipe_from_parameters(net, from_junction=junction7, to_junction=junction8,
                                           length_km=1, diameter_m=0.3, name="Pipe 6",
                                           geodata=[(9, -4), (9, 4)])
    pandapipes.create_valve(net, from_junction=junction5, to_junction=junction6, diameter_m=0.05,
                            opened=True)
    pandapipes.create_heat_exchanger(net, junction3, junction8, diameter_m=0.3, qext_w=20000)
    pandapipes.create_sink(net, junction=junction4, mdot_kg_per_s=0.545, name="Sink 1")
    pandapipes.create_source(net, junction=junction3, mdot_kg_per_s=0.234)
    pandapipes.create_pump_from_parameters(net, junction4, junction7, 'P1')

    return net
