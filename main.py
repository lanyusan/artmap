# For local execution (does not require installing the library):

import sys; sys.path.append('../')

# parse args
import argparse

# Prettymaps
from prettymaps import *
# Vsketch
import vsketch
# OSMNX
import osmnx as ox
# Matplotlib-related
import matplotlib.font_manager as fm
from matplotlib import pyplot as plt
from descartes import PolygonPatch
# Shapely
from shapely.geometry import *
from shapely.affinity import *
from shapely.ops import unary_union

from plots import *

def main():
    print('running main')


def run(plotType, lat, log, radius, out):
    plots = [plot_1, plot_2, plot_3, plot_4, plot_5, plot_6, plot_7, plot_8, plot_9]
    if plotType < 0 or plotType > len(plots):
        print("Unsupported plot type: ", plotType)
        return
    plot = plots[plotType]
    plot(lat, log, radius, out)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("plotType", type=int, help="Plot type")
    parser.add_argument("lon", type=float, help="Longitude")
    parser.add_argument("lat", type=float, help="Latitude")
    parser.add_argument("radius", type=int, help="Radius")
    parser.add_argument("out", type=str, help="Radius in meters")
    parser.add_argument("-o", "--out", help="output file", default="")

    args = parser.parse_args()

    run(args.plotType - 1, args.lat, args.lon, args.radius, args.out)
