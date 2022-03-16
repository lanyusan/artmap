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

__all__ = ['plot_1', 'plot_2', 'plot_3', 'plot_4', 'plot_5', 'plot_6', 'plot_7', 'plot_8', 'plot_9']

def plot_1(lat, lon, radius, out):
    fig, ax = plt.subplots(figsize = (12, 12), constrained_layout = True)

    layers = plot(
        (lat, lon), radius = radius,

        ax = ax,
        layers = {
            'perimeter': {},
            'streets': {
                'custom_filter': '["highway"~"motorway|trunk|primary|secondary|tertiary|residential|service|unclassified|pedestrian|footway"]',
                'width': {
                    'motorway': 5,
                    'trunk': 5,
                    'primary': 4.5,
                    'secondary': 4,
                    'tertiary': 3.5,
                    'residential': 3,
                    'service': 2,
                    'unclassified': 2,
                    'pedestrian': 2,
                    'footway': 1,
                }
            },
            'building': {'tags': {'building': True, 'landuse': 'construction'}, 'union': False},
            'water': {'tags': {'natural': ['water', 'bay']}},
            'green': {'tags': {'landuse': 'grass', 'natural': ['island', 'wood'], 'leisure': 'park'}},
            'forest': {'tags': {'landuse': 'forest'}},
            'parking': {'tags': {'amenity': 'parking', 'highway': 'pedestrian', 'man_made': 'pier'}}
        },
        drawing_kwargs = {
            'background': {'fc': '#F2F4CB', 'ec': '#dadbc1', 'hatch': 'ooo...', 'zorder': -1},
            'perimeter': {'fc': '#F2F4CB', 'ec': '#dadbc1', 'lw': 0, 'hatch': 'ooo...',  'zorder': 0},
            'green': {'fc': '#D0F1BF', 'ec': '#2F3737', 'lw': 1, 'zorder': 1},
            'forest': {'fc': '#64B96A', 'ec': '#2F3737', 'lw': 1, 'zorder': 1},
            'water': {'fc': '#a1e3ff', 'ec': '#2F3737', 'hatch': 'ooo...', 'hatch_c': '#85c9e6', 'lw': 1, 'zorder': 2},
            'parking': {'fc': '#F2F4CB', 'ec': '#2F3737', 'lw': 1, 'zorder': 3},
            'streets': {'fc': '#2F3737', 'ec': '#475657', 'alpha': 1, 'lw': 0, 'zorder': 3},
            'building': {'palette': ['#FFC857', '#E9724C', '#C5283D'], 'ec': '#2F3737', 'lw': .5, 'zorder': 4},
        },

        osm_credit = False
    )

    if out != "":
        plt.savefig('prints/' + out)



def plot_2(lat, lon, radius, out):
# Style parameters
    palette = ['#433633', '#FF5E5B']
    background_c = '#F2F4CB'
    dilate = 100

    # Setup figure
    fig, ax = plt.subplots(figsize = (10, 10), constrained_layout = True)

    # Plot
    layers = plot(
        (lat, lon), radius = radius,
        ax = ax,
        layers = {
            'perimeter': {'circle': False, 'dilate': dilate},
            'streets': {
                'width': {
                    'primary': 5,
                    'secondary': 4,
                    'tertiary': 3,
                    'residential': 2,
                    'footway': 1,
                },
                'circle': False,
                'dilate': dilate
            },
            'building': {
                'tags': {'building': True},
                'union': False,
                'circle': False,
                'dilate': dilate
            },
            'green': {
                'tags': {
                    'landuse': ['grass', 'village_green'],
                    'leisure': 'park'
                },
                'circle': False,
                'dilate': dilate
            },
        },
        drawing_kwargs = {
            'background': {'fc': '#F2F4CB', 'ec': '#dadbc1', 'hatch': 'ooo...', 'zorder': -1},
            'perimeter': {'fill': False, 'lw': 0, 'zorder': 0},
            'green': {'fc': '#8BB174', 'ec': '#2F3737', 'hatch_c': '#A7C497', 'hatch': 'ooo...', 'lw': 1, 'zorder': 1},
            'water': {'fc': '#a8e1e6', 'ec': '#2F3737', 'hatch_c': '#9bc3d4', 'hatch': 'ooo...', 'lw': 1, 'zorder': 3},
            'streets': {'fc': '#2F3737', 'ec': '#475657', 'alpha': 1, 'lw': 0, 'zorder': 4},
            'building': {'palette': palette, 'ec': '#2F3737', 'lw': .5, 'zorder': 5},
        },
        osm_credit = False
    )

    # Set bounds
    xmin, ymin, xmax, ymax = layers['perimeter'].bounds
    dx, dy = xmax-xmin, ymax-ymin
    ax.set_xlim(xmin-.06*dx, xmax+.06*dx)
    ax.set_ylim(ymin-.06*dy, ymax+.06*dy)

    # Draw left text
    # ax.text(
    #     xmin-.06*dx, ymin+.5*dy,
    #     'Barcelona, Spain',
    #     color = '#2F3737',
    #     rotation = 90,
    #     fontproperties = fm.FontProperties(fname = 'assets/Permanent_Marker/PermanentMarker-Regular.ttf', size = 35),
    # )
    # # Draw top text
    # ax.text(
    #     xmax-.35*dx, ymax+.02*dy,
    #     "41° 23′ N, 2° 11′ E",
    #     color = '#2F3737',
    #     fontproperties = fm.FontProperties(fname = 'assets/Permanent_Marker/PermanentMarker-Regular.ttf', size = 20),
    # )

    if out != "":
        plt.savefig('prints/' + out)


def plot_3(lat, lon, radius, out):
    dilate = 100

    class Sketch(vsketch.SketchClass):
        def draw(self, vsk: vsketch.Vsketch) -> None:

            vsk.size("a4", landscape = True)

            global layers
            layers = plot(
                (lat,lon), radius = radius,
                vsketch = vsk,
                layers = {
                    'perimeter': {'circle': False, 'dilate': dilate},
                    'streets': {
                        'width': {
                            'primary': 5,
                            'secondary': 4,
                            'tertiary': 3,
                            'residential': 2,
                            'footway': 1,
                        },
                        'circle': False,
                        'dilate': dilate
                    },
                    'building': {
                        'tags': {'building': True},
                        'union': False,
                        'circle': False,
                        'dilate': dilate
                    },
                    'green': {
                        'tags': {
                            'landuse': ['grass', 'village_green'],
                            'leisure': 'park'
                        },
                        'circle': False,
                        'dilate': dilate
                    },
                },

                scale_x = .65,
                scale_y = -.65,

                drawing_kwargs = {
                    'perimeter': {'draw': False},
                    'streets': {'stroke': 1, 'fill': 1, 'penWidth': 2},
                    'buildings': {'stroke': 2},
                },
            )

            vsk.save('prints/' + out)

        def finalize(self, vsk: vsketch.Vsketch) -> None:
            vsk.vpype("linemerge linesimplify reloop linesort")

    sketch = Sketch()
    sketch.display()

def plot_4(lat, lon, radius, out):
    # Style parameters
    fig, ax = plt.subplots(figsize = (3*3000/300, 3000/300), constrained_layout = True, dpi = 300)
    fig.patch.set_facecolor('#FFEDDF')

    layers = plot(
        # City name
        (lat, lon),
        radius = radius,
        # Matplotlib 'ax'
        ax = ax,
        # Layers to plot & their kwargs
        layers = {
            'perimeter': {},
            'streets':      {
                'width': {
                    'motorway':     12,
                    'trunk':        12,
                    'primary':      11,
                    'secondary':    10,
                    'tertiary':     9,
                    'residential':  8,
                }
            },
            'park':         {'tags': {'leisure': 'park', 'landuse': 'golf_course', 'landuse': 'meadow', 'leisure': 'nature_reserve', 'boundary': 'protected_area', 'place': 'square', 'natural': 'grassland', 'landuse': 'military', 'amenity': 'hospital'}},
            'grass':        {'tags': {'landuse': 'grass', 'natural': 'wood'}},
            'wetland':      {'tags': {'natural': 'wetland', 'natural': 'scrub'}},
            'beach':        {'tags': {'natural': 'beach'}},
            'water':        {'tags': {'natural': 'water'}},
            'pedestrian':   {'tags': {'area:highway': 'pedestrian'}},
            'building':     {'tags': {'building': True}}
        },
        drawing_kwargs = {
            'perimeter':    {'ec': '#0F110C', 'fill': False, 'lw': 0},
            'park':         {'fc': '#AAD897', 'ec': '#8bc49e', 'lw': 0, 'zorder': 1, 'hatch': 'ooo...'},
            'grass':        {'fc': '#72C07A', 'ec': '#64a38d', 'lw': 0, 'zorder': 1, 'hatch': 'ooo...'},
            'wetland':      {'fc': '#D2D68D', 'ec': '#AEB441', 'lw': 0, 'zorder': 3, 'hatch': 'ooo...'},
            'water':        {'fc': '#6CCFF6', 'ec': '#59adcf', 'lw': 0, 'zorder': 2, 'hatch': 'ooo...'},
            'beach':        {'fc': '#F2E3BC', 'ec': '#EBD499', 'lw': 0, 'zorder': 2, 'hatch': 'ooo...'},
            'pedestrian':   {'fc': '#7BC950', 'ec': '#638475', 'lw': 0, 'zorder': 2, 'hatch': 'ooo...'},
            'streets':      {'fc': '#898989', 'ec': '#706f6f', 'zorder': 3, 'lw': 0, 'hatch': 'ooo...'},
            'building':     {'fc': '#E7A89C', 'ec': '#E7A89C', 'lw': 0, 'zorder': 0},
        },

        osm_credit = False
    )

    # Add meadows, parks & scrubs
    for tags, kwargs in [
            ({'landuse': 'meadow'}, {'fc': '#AAD897', 'ec': '#8bc49e', 'lw': 0, 'zorder': 1, 'hatch': 'ooo...'}),
            ({'leisure': 'park'}, {'fc': '#AAD897', 'ec': '#8bc49e', 'lw': 0, 'zorder': 1, 'hatch': 'ooo...'}),
            ({'natural': 'scrub'}, {'fc': '#D2D68D', 'ec': '#AEB441', 'lw': 0, 'zorder': 3, 'hatch': 'ooo...'}),
    ]:
        ax.add_patch(PolygonPatch(
            unary_union(
                ox.project_gdf(
                    ox.geometries_from_point(
                        (-22.9926, -43.4152),
                        tags = tags,
                        dist = 1000
                    )
                ).geometry
            ),
            **kwargs
        ))

        # Add 'sea'
    sea = max(layers['perimeter'].convex_hull.difference(layers['perimeter']), key = lambda x: x.area).buffer(20)
    sea = sea.difference(translate(scale(sea, 1.05, 1), 0, -200)).difference(layers['perimeter'])[0]
    ax.add_patch(PolygonPatch(sea, fc = '#59A5D8', ec = '#386FA4', hatch = 'ooo...'))

    # Set bounds
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    dx = xmax-xmin
    dy = ymax-ymin
    ax.set_xlim(xmin+.3*dx, xmax-.3*dx)
    ax.set_ylim(ymin+.3*dy, ymax-.0*dy)

    plt.savefig('prints/' + out)

def plot_5(lat, lon, radius, out):
   # General style parameters
   palette = ['#433633', '#FF5E5B']
   background_c = '#F2F4CB'
   dilate = 100

   # Setup plot
   fig, ax = plt.subplots(figsize = (12, 12), constrained_layout = True)

   layers = plot(
       (lat, lon),
       radius = radius,
       ax = ax,

       layers = {
               'perimeter': {},
               'streets': {
                   'width': {
                       'motorway': 5,
                       'trunk': 5,
                       'primary': 4.5,
                       'secondary': 4,
                       'tertiary': 3.5,
                       'cycleway': 3.5,
                       'residential': 3,
                       'service': 2,
                       'unclassified': 2,
                       'pedestrian': 2,
                       'footway': 1,
                   },
                   'circle': False, 'dilate': dilate
               },
               'building': {'tags': {'building': True, 'landuse': 'construction'}, 'union': True, 'circle': False, 'dilate': dilate},
               'water': {'tags': {'natural': ['water', 'bay']}, 'circle': False, 'dilate': dilate},
               'forest': {'tags': {'landuse': 'forest'}, 'circle': False, 'dilate': dilate},
               'green': {'tags': {'landuse': ['grass', 'orchard'], 'natural': ['island', 'wood'], 'leisure': 'park'}, 'circle': False, 'dilate': dilate},
               'beach': {'tags': {'natural': 'beach'}, 'circle': False, 'dilate': dilate},
               'parking': {'tags': {'amenity': 'parking', 'highway': 'pedestrian', 'man_made': 'pier'}, 'circle': False}
           },
           drawing_kwargs = {
               'perimeter': {'fill': False, 'lw': 0, 'zorder': 0},
               'background': {'fc': background_c, 'zorder': -1},
               'green': {'fc': '#8BB174', 'ec': '#2F3737', 'hatch_c': '#A7C497', 'hatch': 'ooo...', 'lw': 1, 'zorder': 1},
               'forest': {'fc': '#64B96A', 'ec': '#2F3737', 'lw': 1, 'zorder': 2},
               'water': {'fc': '#a8e1e6', 'ec': '#2F3737', 'hatch_c': '#9bc3d4', 'hatch': 'ooo...', 'lw': 1, 'zorder': 3},
               'beach': {'fc': '#FCE19C', 'ec': '#2F3737', 'hatch_c': '#d4d196', 'hatch': 'ooo...', 'lw': 1, 'zorder': 3},
               'parking': {'fc': background_c, 'ec': '#2F3737', 'lw': 1, 'zorder': 3},
               'streets': {'fc': '#2F3737', 'ec': '#475657', 'alpha': 1, 'lw': 0, 'zorder': 4},
               'building': {'palette': palette, 'ec': '#2F3737', 'lw': .5, 'zorder': 5},

           },

           osm_credit = False
   )

   # Set bounds
   xmin, ymin, xmax, ymax = layers['perimeter'].bounds
   dx, dy = xmax-xmin, ymax-ymin
   a = .2
   ax.set_xlim(xmin+a*dx, xmax-a*dx)
   ax.set_ylim(ymin+a*dy, ymax-a*dy)

   plt.savefig('prints/' + out)

def plot_6(lat, lon, radius, out):

   palette = ['#FFC857', '#E9724C', '#C5283D']

   fig, ax = plt.subplots(figsize = (12, 12), constrained_layout = True)

   def postprocessing(layers):
       boundary = Polygon(layers['green'].buffer(5)[0].exterior).buffer(0)
       layers['building'] = layers['building'].buffer(0).intersection(boundary)
       layers['streets'] = layers['streets'].buffer(0).intersection(boundary)
       return layers

   layers = plot(
       (lat, lon), radius = radius,

       ax = ax,

       postprocessing = postprocessing,

       layers = {
               'perimeter': {},
               'streets': {
                   'width': {
                       'motorway': 5,
                       'trunk': 5,
                       'primary': 4.5,
                       'secondary': 4,
                       'tertiary': 3.5,
                       'residential': 3,
                       'service': 2,
                       'unclassified': 2,
                       'pedestrian': 2,
                       'footway': 1,
                       'track': 1,
                       'bridleway': 1
                   }
               },
               'building': {'tags': {'building': True, 'landuse': 'construction'}, 'union': False},
               'water': {'tags': {'natural': ['water', 'bay']}},
               'green': {'tags': {'landuse': 'grass', 'natural': ['island', 'wood'], 'leisure': 'park'}},
               'scrub': {'tags': {'natural': 'scrub'}},
               'walls': {'tags': {'historic': 'citywalls'}},
               'pedestrian_way': {'tags': {'highway': 'pedestrian'}},
           },
           drawing_kwargs = {
               'background': {'fc': '#F2F4CB', 'ec': '#dadbc1', 'hatch': 'ooo...', 'zorder': -1},
               'perimeter': {'fc': '#F2F4CB', 'ec': '#dadbc1', 'lw': 0, 'hatch': 'ooo...',  'zorder': 0},
               'green': {'fc': '#D0F1BF', 'ec': '#2F3737', 'hatch_c': '#b3cfa5', 'hatch': 'ooo...', 'lw': 1, 'zorder': 1},
               'scrub': {'fc': '#89d689', 'ec': '#2F3737', 'hatch_c': '#75bd75', 'hatch': 'ooo...', 'lw': 1, 'zorder': 1},
               'water': {'fc': '#a1e3ff', 'ec': '#2F3737', 'lw': 1, 'zorder': 2},
               'streets': {'fc': '#2F3737', 'ec': '#475657', 'alpha': 1, 'lw': 0, 'zorder': 3},
               'walls': {'fc': '#2F3737', 'ec': '#475657', 'alpha': 1, 'lw': 0, 'zorder': 3},
               'building': {'palette': palette, 'ec': '#2F3737', 'lw': .5, 'zorder': 4},
               'pedestrian_way': {'fc': '#dfe8d3', 'ec': '#2F3737', 'lw': 1, 'zorder': 4},
           },

           osm_credit = False
   )

   plt.savefig('prints/' + out)

def plot_7(lat, lon, radius, out):
  palette = ['#FFC857', '#E9724C', '#C5283D']

  fig, ax = plt.subplots(figsize = (12, 12), constrained_layout = True)

  layers = plot(
      (lat, lon), radius = radius,

      ax = ax,

      layers = {
              'perimeter': {},
              'streets': {
                  'width': {
                      'motorway': 5,
                      'trunk': 5,
                      'primary': 4.5,
                      'secondary': 4,
                      'tertiary': 3.5,
                      'residential': 3,
                      'living_street': 2,
                      'pedestrian': 1,
                      'footway': 1,
                      'track': 1,
                      'bridleway': 1
                  }
              },
              'building': {'tags': {'building': True, 'landuse': 'construction'}, 'union': False},
              'water': {'tags': {'natural': ['water', 'bay']}},
              'green': {'tags': {'landuse': 'grass', 'natural': ['island', 'wood'], 'leisure': 'park'}},
              'scrub': {'tags': {'natural': 'scrub'}},
              'walls': {'tags': {'manmade': 'embankment'}},
          },
          drawing_kwargs = {
              'background': {'fc': '#F2F4CB', 'ec': '#dadbc1', 'hatch': 'ooo...', 'zorder': -1},
              'perimeter': {'fc': '#F2F4CB', 'ec': '#dadbc1', 'lw': 0, 'hatch': 'ooo...',  'zorder': 0},
              'green': {'fc': '#D0F1BF', 'ec': '#2F3737', 'hatch_c': '#b3cfa5', 'hatch': 'ooo...', 'lw': 1, 'zorder': 1},
              'scrub': {'fc': '#89d689', 'ec': '#2F3737', 'hatch_c': '#75bd75', 'hatch': 'ooo...', 'lw': 1, 'zorder': 1},
              'water': {'fc': '#a1e3ff', 'ec': '#2F3737', 'lw': 1, 'zorder': 2},
              'streets': {'fc': '#2F3737', 'ec': '#475657', 'alpha': 1, 'lw': 0, 'zorder': 3},
              'walls': {'fc': '#2F3737', 'ec': '#475657', 'alpha': 1, 'lw': 0, 'zorder': 3},
              'building': {'palette': palette, 'ec': '#2F3737', 'lw': .5, 'zorder': 4},
          },

          osm_credit = False
  )

  plt.savefig('prints/' + out)

def plot_8(lat, lon, radius, out):
  def postprocessing(layers):
      layers['perimeter'] = layers['perimeter'].buffer(10)
      return layers

  fig, ax = plt.subplots(figsize = (15, 12), constrained_layout = True)

  layers = plot(
      (lat, lon),
      radius = radius,
      ax = ax,
      postprocessing = postprocessing,

      layers = {
              'perimeter': {},
              'streets': {
                  'width': {
                      #'motorway': 8,
                      'trunk': 6,
                      'primary': 6,
                      'secondary': 5,
                      'tertiary': 4,
                      'residential': 3,
                      #'living_street': 3,
                      'pedestrian': 1.5,
                      'footway': 1.5,
                      #'track': 1,
                      #'bridleway': 1
                  }
              },
              'building': {'tags': {'building': True}, 'union': False},
              'water': {'tags': {'natural': ['water', 'bay']}},
              'green': {'tags': {'landuse': 'grass', 'natural': ['island', 'wood'], 'leisure': 'park'}},
          },
          drawing_kwargs = {
              'background': {'fc': '#F7F3F5', 'ec': '#EFE7EB', 'hatch': 'ooo...', 'zorder': -1},
              'perimeter': {'fc': '#F7F3F5', 'ec': '#2F3737', 'lw': 3, 'hatch': 'ooo...', 'hatch_c': '#EFE7EB',  'zorder': 0},
              'green': {'fc': '#AABD8C', 'ec': '#2F3737', 'hatch_c': '#b3cfa5', 'hatch': 'ooo...', 'lw': 0, 'zorder': 1},
              'water': {'fc': '#a1e3ff', 'hatch': 'ooo...', 'hatch_c': '#80bed9', 'lw': 0, 'zorder': 2},
              'streets': {'fc': '#3b4545', 'lw': 0, 'zorder': 3},
              'building': {'palette': ['#433633', '#FF5E5B'], 'ec': '#2F3737', 'hatch': 'ooo...', 'hatch_c': '#b3504f', 'lw': 0, 'zorder': 4},
          },

          osm_credit = False
  )

  plt.savefig('prints/' + out)

def plot_9(lat, lon, radius, out):
  fig, ax = plt.subplots(figsize = (15, 12), constrained_layout = True)
  fig.patch.set_facecolor('#F9F8F8')

  places = {
      (lat, lon): ['#EEE4E1', '#E7D8C9', '#E6BEAE'],
      # 'Cidade Baixa, Porto Alegre': ['#49392C', '#77625C', '#B2B1CF', '#E1F2FE', '#98D2EB'],
      # 'Bom Fim, Porto Alegre': ['#BA2D0B', '#D5F2E3', '#73BA9B', '#F79D5C'],
  }

  for i, (place, palette) in enumerate(places.items()):
      plot(
          place,
          radius = radius,
          ax = ax,

          layers = {
              'perimeter': {},
              'streets': {
                  'width': {
                      'trunk': 6,
                      'primary': 6,
                      'secondary': 5,
                      'tertiary': 4,
                      'residential': 3.5,
                      'pedestrian': 3,
                      'footway': 3,
                      'path': 3,
                  }
              },
              'building': {'tags': {'building': True, 'leisure': ['track', 'pitch']}, 'union': False},
              'water': {'tags': {'natural': ['water', 'bay']}},
              'park': {'tags': {'leisure': 'park'}},
              'forest': {'tags': {'landuse': 'forest'}},
              'garden': {'tags': {'leisure': 'garden'}},
          },
          drawing_kwargs = {
              'perimeter': {'fill': False, 'lw': 0, 'zorder': 0},
              'park': {'fc': '#AABD8C', 'ec': '#87996b', 'lw': 1, 'zorder': 1},
              'forest': {'fc': '#78A58D', 'ec': '#658a76', 'lw': 1, 'zorder': 1},
              'garden': {'fc': '#a9d1a9', 'ec': '#8ab58a', 'lw': 1, 'zorder': 1},
              'water': {'fc': '#92D5F2', 'ec': '#6da8c2', 'lw': 1, 'zorder': 2},
              'streets': {'fc': '#F1E6D0', 'ec': '#2F3737', 'lw': 1.5, 'zorder': 3},
              'building': {'palette': palette, 'ec': '#2F3737', 'lw': 1, 'zorder': 4},
          },

          osm_credit = False
      )

  ax.autoscale()

  plt.savefig('prints/' + out)
