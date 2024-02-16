import numpy as np
import matplotlib
import matplotlib.cm
import matplotlib.figure
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import copy
import collections
import plotly
import plotly.subplots
import plotly.graph_objs as go

# PLOT_ENGINE = plt
PLOT_ENGINE = plotly


class TypedDict(collections.UserDict):
    def __init__(self, dict=None, required_type=None, **kwargs):
        super().__init__(None, **kwargs)
        self.data = {}  # Clear dict

        # Contains objects of a single type
        if isinstance(required_type, type):
            self._type = required_type
        else:
            self._type = object

        if dict is not None:
            self.update(dict)  # Implements type-checking through __setitem__

        if kwargs:
            self.update(kwargs)

    # Check type when adding an item
    def __setitem__(self, key, item):
        item_type = type(item)
        if self._type is item_type:
            self.data[key] = item
            return

        if self._type is object:
            self._type = item_type  # Restrict TypedDict to this data type
            self.data[key] = item
            return

        raise TypeError(f"Invalid Type: {type(item)} must be of type {self._type}")

    # Iterate on contents, not keys...
    def __iter__(self):
        return iter(self.data.values())

    # Object in TypedDict will also work...
    def __contains__(self, key):
        if type(key) is self._type:
            return key in self.data.values()
        return key in self.data

    def keys(self):
        return self.data.keys()  # Base class relies on __iter__ for keys

    def values(self):
        return self.data.values()  # Base class relies on __iter__ for values

    def items(self):
        return self.data.items()  # Base class relies on __iter__ for items

    def clear(self):
        super().clear()


class Lot(TypedDict):
    def __init__(self, name="", dict=None, **kwargs):
        super().__init__(dict=dict, required_type=Wafer)
        self._l = str(name).upper()

    def __len__(self):
        return len(self.data)

    @property
    def name(self):
        return self._l

    @name.setter
    def name(self, value):
        self._l = str(value).upper()

    @property
    def l(self):
        return self.name

    @l.setter
    def l(self, value):
        self.name = value

    # @property
    # def wafers(self):
    #     return super().data
    #
    # @wafers.setter
    # def wafers(self, value):
    #     self.data = value

    @property
    def wafer_ids(self):
        if not self: return None
        return super().keys()

    @property
    def die_count(self):
        if not len(self): return 0
        return sum(w.die_count for w in self)

    def add_wafer(self, wafer):
        if wafer not in self:
            self[wafer.w] = wafer
            wafer.lot = self
            # wafer.l = self.l

    def die_isbad_vector(self, bin=0):
        return np.array([wafer.die_isbad_vector(bin) for wafer in self.values()], dtype=np.bool)

    def die_bin_vector(self):
        return np.array([wafer.die_bin_vector() for wafer in self.values()], dtype=np.int)

    def die_param_vector(self):
        return np.array([wafer.die_param_vector() for wafer in self.values()])

    def clear(self):
        self.data.clear()

    def _calc_grid(self, n=0):
        if not n or n <= 0:
            n = len(self)

        # Defines desired aspect ratio for grid
        _x = 16
        _y = 9

        v = (n / _x * _y) ** 0.5
        y = int(round(v, 0))
        x = int(n / y)
        while n > y * x:
            x += 1
        # print(f"n: {n}  v: {v}  xy: {x} {y}")
        return x, y

    def plot(self, z='is_bad'):
        global PLOT_ENGINE
        if PLOT_ENGINE is plt: return self.plot_pyplot(z=z)
        if PLOT_ENGINE is plotly: return self.plot_plotly(z=z)
        raise ValueError(f"Plot engine not recognized: {PLOT_ENGINE}")

    def plot_pyplot(self, z='is_bad'):
        if not len(self):
            raise IndexError(f"Wafer {self._l} Wafers not defined.")

        x, y = self._calc_grid()

        # if not isinstance(ax, matplotlib.axes.Axes):
        #     raise TypeError(f"Argument 'ax' must be matplotlib Axes: {ax}")

        fig = plt.figure(figsize=(12, 6))
        fig.suptitle(f"Lot: {self.l}", fontsize=16)
        fig.subplots(y, x)
        for ax in fig.axes:
            ax.set_aspect(1., adjustable='box')
            ax.set_xticks([], [])
            ax.set_yticks([], [])

        #plt.axis('off')

        for i, w in enumerate(self):
            ax = fig.axes[i]
            ax.set_xlabel(f"Wafer {w.w}")
            w.plot(ax=ax)

        plt.draw_all()
        plt.tight_layout()
        # fig.canvas.draw()
        # fig.canvas.flush_events()
        return fig

    def plot_plotly(self, z='is_bad'):
        if not len(self):
            raise IndexError(f"Wafer {self._l} Wafers not defined.")

        x, y = self._calc_grid()

        # if not isinstance(ax, matplotlib.axes.Axes):
        #     raise TypeError(f"Argument 'ax' must be matplotlib Axes: {ax}")

        fig = plotly.subplots.make_subplots(rows=y, cols=x)

        #fig = plt.figure(figsize=(12, 6))
        fig.update_layout(dict(title=f"Lot: {self.l}", font=dict(size=16)))

        print(x, y)
        for i, wafer in enumerate(self.values()):
            _x = i % x + 1
            _y = i // x + 1

            wafer.plot(ax=go.Scatter(), coord=(_y, _x))

        return

        for ax in fig.axes:
            ax.set_aspect(1., adjustable='box')
            ax.set_xticks([], [])
            ax.set_yticks([], [])

        #plt.axis('off')

        for i, w in enumerate(self):
            ax = fig.axes[i]
            ax.set_xlabel(f"Wafer {w.w}")
            w.plot(ax=ax)

        plt.draw_all()
        plt.tight_layout()
        # fig.canvas.draw()
        # fig.canvas.flush_events()
        return fig



class Wafer(TypedDict):
    def __init__(self, lot: (Lot, str) = None, wafer: int = None):
        super().__init__(dict=None, required_type=Die)

        if lot is None:
            lot = ""
        if wafer is None:
            wafer = np.random.randint(100, 999)

        if isinstance(lot, Lot):
            self._lot = lot
            self._l = lot.l
        else:
            self._lot = None
            self._l = str(lot).upper()
        self._w = int(wafer)
        self.radius = 150.
        self.edge_exclusion = 3.
        self.center = (0., 0.)
        self.x_range = None
        self.y_range = None
        self.y_min = None
        self.y_max = None
        self.x_min = None
        self.x_max = None

    def __str__(self):
        result = ""
        result += f"Wafer lw: {self._l} {self._w}\n"
        result += f"  Total Dice: {len(self)}\n"
        result += f"  Usable/Total Diameter: {2 * (self.radius - self.edge_exclusion)} / {2 * self.radius}\n"
        result += f"  Center: {self.center}\n"
        if len(self):
            die = self[0, 0]
            result += f"  Die size: {die.x_size} x {die.y_size}: {die.area} cm\u00b2\n"
        if self.x_range:
            result += f"  x: {min(self.x_range)} : {max(self.x_range)} \n"
        if self.y_range:
            result += f"  y: {min(self.y_range)} : {max(self.y_range)} \n"
        return result

    def __repr__(self):
        if not len(self) or not self.x_range or not self.y_range:
            return f"Undefined {int(2 * self.radius)}mm wafer, lw: {self._l} {self._w}"

        result = "\n"
        for y in self.y_range:
            chars = []
            for x in self.x_range:
                char = ""
                if (x, y) in self.keys():
                    if 0 == x == y:
                        char += '\x1b[96m'  # Cyan text

                    # Black rectangle for Good die, White rectangle for Bad die
                    char += "\u25AF" if self[x, y].is_good else "\u25AE"

                    if 0 == x == y:
                        char += '\x1b[0m'  # Default color
                else:
                    char = "\u2001"  # "Em Quad" space (same width as rectangles)
                    # result += " \u25AF"
                chars.append(char)
            result += " ".join(chars) + "\n"
        return result

    def __copy__(self):
        new_wafer = Wafer(self._l, self._w)
        new_wafer.center = self.center
        new_wafer.die = copy.copy(self.die)
        return new_wafer

    def __deepcopy__(self, memo=None):
        new_wafer = Wafer(self._l, self._w)
        new_wafer.radius = self.radius
        new_wafer.edge_exclusion = self.edge_exclusion
        new_wafer.center = copy.deepcopy(self.center)
        new_wafer.data = copy.deepcopy(self.data)
        return new_wafer

    def __len__(self):
        return super().__len__()

    def __iter__(self):
        return super().__iter__()

    # def __next__(self):
    #     return super().__next__()

    @property
    def lot(self):
        return self._lot

    @lot.setter
    def lot(self, value):
        if isinstance(value, Lot):
            self._lot = value
        else:
            raise TypeError("Lot must be of Class: Lot")

    @property
    def l(self):
        if self.lot: return self.lot.recipes
        return self._l

    @l.setter
    def l(self, value):
        self._l = str(value).upper()

    @property
    def w(self):
        return self._w

    @w.setter
    def w(self, value):
        self._w = value

    @property
    def name(self):
        return self._w

    # def __getitem__(self, item):
    #     return super().__getitem__(item)
    #
    # def __setitem__(self, key, value):
    #     super().__setitem__(key, value)

    def clear(self):
        self.data.clear()

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)

        self.x_min = min(d.x for d in self.values())
        self.x_max = max(d.x for d in self.values())
        self.x_range = range(self.x_min, self.x_max + 1)

        self.y_min = min(d.y for d in self.values())
        self.y_max = max(d.y for d in self.values())
        self.y_range = range(self.y_max, self.y_min - 1, -1)  # Descending for easy maps in console

    @property
    def die_count(self):
        return len(self)

    def die_isbad_vector(self, bin=0):
        if bin and bin > 0:  # Positive Integer
            return np.array([die.bin == bin for die in self.values()], dtype=np.bool)

        return np.array([die.is_bad for die in self.values()], dtype=np.bool)

    def die_bin_vector(self):
        return np.array([die.bin for die in self.values()], dtype=np.int)

    def die_param_vector(self):
        return np.array([die.param for die in self.values()])

    def set_param_vector(self, value):
        if isinstance(value, collections.Mapping):
            # Dict-like container, then match keys
            if set(super().keys()) == set(value.keys()):
                #print("dict-like update")
                for key in value.keys():
                    self[key].param = value[key]
                return
        elif len(value) == super().__len__():
            # print(f"arr-like update: {len(value)} == {super().__len__()}")
            # Array-like.  Trust they are still in order
            for die, val in zip(self.values(), value):
                die.param = val
            return
        raise IndexError(f"Incorrect array length: {len(value)} != {len(self)}")

    def plot(self, z="is_bad", ax=None):
        global PLOT_ENGINE
        if PLOT_ENGINE is plt:
            result = self.plot_pyplot(z=z, ax=ax)
            if ax is None: plt.show()
            return result

        if PLOT_ENGINE is plotly:
            result = self.plot_plotly(z=z, ax=ax)
            if ax is None:
                print(result)
                plotly.offline.plot(result)
            return result

        raise ValueError(f"Plot engine not recognized: {PLOT_ENGINE}")

    def plot_pyplot(self, z="is_bad", ax=None):
        if not len(self):
            raise KeyError(f"Wafer {self._l} {self._w} Die not defined.")

        if ax is None:
            fig = plt.figure(figsize=(6, 6))
            fig.suptitle(f"Lot Wafer: {self.l} {self.w}", fontsize=16)
            fig.subplots(1, 1)
            ax = fig.axes[0]
            plt.draw_all()
            plt.tight_layout()
            # ax.set_xticks([], [])
            # ax.set_yticks([], [])
            # plt.axis('off')
            # plt.tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='off', right='off', left='off',
            #             labelleft='off')

        if not isinstance(ax, matplotlib.axes.Axes):
            raise TypeError(f"Argument 'ax' must be matplotlib Axes: {ax}")

        # Circles for edge of wafer and edge exclusion zone
        ax.add_patch(patches.Circle(xy=(0, 0), radius=self.radius))
        ax.add_patch(patches.Circle(xy=(0, 0), radius=self.radius - self.edge_exclusion, color='0.75'))
        ax.autoscale()  # Do now, since Circles define the outer edge

        show_empty = True
        die = self[0, 0]
        x_size_mm = die.x_size * 10
        y_size_mm = die.y_size * 10

        # Force square plots
        ax.set_aspect(1., adjustable='box')

        if z == 'param':
            z_min = np.min(self.die_param_vector())
            z_max = np.max(self.die_param_vector())

        for y in self.y_range:
            for x in self.x_range:
                die = self.get((x, y), None)
                x_corner = (x - self.center[0]) * x_size_mm - x_size_mm / 2
                y_corner = (y - self.center[1]) * y_size_mm - y_size_mm / 2

                if not die:
                    color = '0.6'
                    fill = False
                elif 0 == x == y:
                    color = 'blue'
                    fill = die.__getattribute__(z)
                else:
                    color = 'black'
                    fill = die.__getattribute__(z)

                if fill is not False and z == 'param':
                    # Filled rectangles, color based on parameter value
                    # print(x, y, fill)
                    z_color = matplotlib.cm.jet(100 * (fill - z_min) / (z_max - z_min))
                    ax.add_patch(patches.Rectangle(xy=(x_corner, y_corner),
                                                   width=x_size_mm * .98, height=y_size_mm * .98,
                                                   edgecolor=color, Fill=True, facecolor=z_color
                                                   ))
                    plt.title(f"z: [{z_min},{z_max}]")

                elif die or show_empty:
                    # Empty rectangles, color based on parameter value
                    ax.add_patch(patches.Rectangle(xy=(x_corner, y_corner),
                                                   width=x_size_mm * .98, height=y_size_mm * .98,
                                                   edgecolor=color, Fill=fill))

        return ax

    def plot_plotly(self, z="is_bad", ax=None, coord=None):
        """
            Wafer plot using plotly
        """

        # Color names reference:
        # https://developer.mozilla.org/en-US/docs/Web/CSS/color_value

        if not len(self):
            raise KeyError(f"Wafer {self._l} {self._w} Die not defined.")

        if ax is None or coord is None:
            fig = go.Figure()

            fig.update_layout(
                title=f"Lot Wafer: {self.l} {self.w}",
                font=dict(size=18)
            )
            # fig.update_layout(width=800, height=800)
            ax = go.Scatter()
            # fig.suptitle(f"Lot Wafer: {self.l} {self.w}", fontsize=16)
            # fig.subplots(1, 1)
            # ax = fig.axes[0]
            # plt.draw_all()
            # plt.tight_layout()

            # ax.set_xticks([], [])
            # ax.set_yticks([], [])
            # plt.axis('off')
            # plt.tick_params(axis='both', which='both', bottom='off', top='off', labelbottom='off', right='off', left='off',
            #             labelleft='off')
        else:
            if not isinstance(ax, go.Scatter):
                raise TypeError(f"Argument 'ax' must be Plotly Scatter: {ax}")

            if not isinstance(coord, tuple) or len(coord) != 2:
                raise TypeError(f"Argument 'coord' must be 2-tuple row, col: {coord}")

            fig = ax

        r = self.radius
        fig.update_xaxes(range=[-r, r], zeroline=False)
        fig.update_yaxes(range=[-r, r])

        # Outer circle for full wafer
        fig.add_shape(type='circle', fillcolor='RoyalBlue', line_width=0,
                      x0=-r, y0=-r, x1=r, y1=r,
        )

        # Inner circle for edge exclusion
        ree = self.radius - self.edge_exclusion
        fig.add_shape(type='circle', fillcolor='Silver', line_width=0,
                      x0=-ree, y0=-ree, x1=ree, y1=ree,
         )

        # scaleanchor='x' forces square plots
        fig.update_layout(
            xaxis=dict(showgrid=False, zeroline=False),
            yaxis=dict(showgrid=False, zeroline=False, scaleanchor='x'),
        )

        show_empty = True
        die = self[0, 0]
        x_size_mm = die.x_size * 10
        y_size_mm = die.y_size * 10

        if z == 'param':
            z_min = np.min(self.die_param_vector())
            z_max = np.max(self.die_param_vector())

        for y in self.y_range:
            for x in self.x_range:
                die = self.get((x, y), None)
                x_corner = (x - self.center[0]) * x_size_mm - x_size_mm / 2
                y_corner = (y - self.center[1]) * y_size_mm - y_size_mm / 2

                if not die:
                    color = 'Gray'
                    fill = False
                elif 0 == x == y:
                    color = 'RoyalBlue'
                    fill = die.__getattribute__(z)
                else:
                    color = 'Black'
                    fill = die.__getattribute__(z)

                if fill is not False and z == 'param':
                    # Filled rectangles, color based on parameter value
                    # print(x, y, fill)
                    # z_color = matplotlib.cm.jet(100 * (fill - z_min) / (z_max - z_min))
                    # ax.add_patch(patches.Rectangle(xy=(x_corner, y_corner),
                    #                                width=x_size_mm * .98, height=y_size_mm * .98,
                    #                                edgecolor=color, Fill=True, facecolor=z_color
                    #                                ))
                    # plt.title(f"z: [{z_min},{z_max}]")
                    fig.add_shape(
                        type='rect',
                        x0=x_corner, y0=y_corner,
                        x1=x_corner + x_size_mm * .98, y1=y_corner + y_size_mm * .98,
                        line=dict(color=color),
                    )

                elif die or show_empty:
                    # Empty rectangles, color based on parameter value
                    # ax.add_patch(patches.Rectangle(xy=(x_corner, y_corner),
                    #                                width=x_size_mm * .98, height=y_size_mm * .98,
                    #                                edgecolor=color, Fill=fill))
                    fig.add_shape(
                        type='rect',
                        x0=x_corner, y0=y_corner,
                        x1=x_corner + x_size_mm * .98, y1=y_corner + y_size_mm * .98,
                        line=dict(color=color),
                    )

        return fig

    def in_wafer(self, x_mm, y_mm):
        return (x_mm ** 2 + y_mm ** 2) ** 0.5 < self.radius - self.edge_exclusion

    def generate_array_map(self, x_size, y_size):
        if x_size <= 0. or y_size <= 0.:
            raise ValueError(f"Invalid die dimensions: {x_size} x {y_size}")

        centers = ((0., 0.), (0., .5), (.5, 0.), (.5, .5))

        if False:
            centers = (centers[2],)

        x_size_mm = x_size * 10
        y_size_mm = y_size * 10
        wafer_map = []
        zero_center = None
        for center in centers:
            dice = TypedDict(required_type=Die)
            x_min = int(center[0] - self.radius / x_size_mm - 1)
            x_max = int(center[0] + self.radius / x_size_mm + 1)
            y_min = int(center[1] - self.radius / y_size_mm - 1)
            y_max = int(center[1] + self.radius / y_size_mm + 1)
            # print(f"min/max x: {x_min}/{x_max}  y: {y_min}/{y_max}")

            for y in range(y_min, y_max + 1):
                for x in range(x_min, x_max + 1):
                    # print(f"xy: {x}, {y}")
                    x_center = (x - center[0]) * x_size_mm
                    y_center = (y - center[1]) * y_size_mm
                    # corners of die: nw, ne, sw, se
                    nw = (x_center - x_size_mm / 2, y_center + y_size_mm / 2)
                    ne = (x_center + x_size_mm / 2, y_center + y_size_mm / 2)
                    se = (x_center + x_size_mm / 2, y_center - y_size_mm / 2)
                    sw = (x_center - x_size_mm / 2, y_center - y_size_mm / 2)

                    if all([self.in_wafer(*coord) for coord in (nw, ne, sw, se)]):
                        dice[x, y] = Die(wafer=self, x=x, y=y, x_size=x_size, y_size=y_size)
                        #print(f"FIT: Center: {center} {x},{y} Corners: {nw} {ne} {se} {sw}")
                        #print(len(dice))
                    else:
                        #print(f"NO:  Center: {center} {x},{y} Corners: {nw} {ne} {se} {sw}")
                        pass

            if len(dice) > len(wafer_map):
                wafer_map = dice
                zero_center = center

        if len(wafer_map):
            self.clear()
            # print(f"After clear should be zero: {len(self)}")
            self.update(wafer_map.data)
            self.center = zero_center
        else:
            raise ValueError(f"Unable to generate array map for x/y (in cm): {x_size}, {y_size}")


class Die(object):
    def __init__(self, wafer: Wafer, x: int, y: int, x_size: float, y_size: float):
        if isinstance(wafer, Wafer):
            self._lot = wafer.lot
            self._l = wafer.l
        else:
            self._lot = None
            self._l = ''
        self._wafer = wafer
        self._x = int(x)
        self._y = int(y)
        self.x_size = x_size
        self.y_size = y_size
        self._bin = 1
        self._param = 0.

    @property
    def __name__(self):
        return f"Die: {self.l} {self.w} {self.x},{self.y}"

    def __repr__(self):
        return self.__name__

    def __copy__(self):
        new_die = Die(self.wafer, self.x, self.y, self.x_size, self.y_size)
        new_die.bin = self._bin
        new_die.param = self._param
        return new_die

    def __deepcopy__(self, memo=None):
        return self.__copy__()

    @property
    def wafer(self):
        return self._wafer

    @property
    def l(self):
        if self.lot: return self.lot.recipes
        if self.wafer: return self.wafer.l
        return self._l

    @property
    def w(self):
        if self.wafer: return self.wafer.w
        return self._w

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def coord(self):
        return (self.x, self.y)

    @property
    def area(self):
        # Area in cm2, from x, y in cm
        return self.x_size * self.y_size

    @property
    def bin(self):
        return self._bin

    @bin.setter
    def bin(self, value):
        self._bin = value

    @property
    def param(self):
        return self._param

    @param.setter
    def param(self, value):
        self._param = value

    @property
    def is_good(self):
        return self.bin <= 6

    @property
    def is_bad(self):
        return not self.is_good

    @property
    def aspect_ratio(self):
        if self.x_size == 0:
            raise ValueError(f"Invalid x_size: {self.x_size}")
        return self.y_size / self.x_size

