import numpy as np
import matplotlib.cm
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import copy
import collections


class TypedDict(collections.UserDict):
    def __init__(self, dict=None, required_type=None, **kwargs):
        super().__init__(None, **kwargs)
        self.data = {}

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


class Lot(object):
    def __init__(self, lot):
        self._l = str(lot).upper()
        self._wafers = TypedDict(required_type=Wafer)

    def __len__(self):
        return len(self._wafers)

    @property
    def l(self):
        return self._l

    @property
    def name(self):
        return self._l

    @l.setter
    def l(self, value):
        self._l = str(value).upper()

    @property
    def wafers(self):
        return self._wafers

    @wafers.setter
    def wafers(self, value):
        self._wafers = value

    @property
    def wafer_ids(self):
        if not self._wafers: return None
        return self._wafers.keys()

    @property
    def die_count(self):
        if not self.wafers: return 0
        return sum(w.die_count for w in self.wafers)

    def add_wafer(self, wafer):
        if wafer not in self.wafers:
            self.wafers[wafer._w] = wafer
            wafer.lot = self
            wafer.l = self.l

    def die_isbad_vector(self, bin=0):
        return np.array([wafer.die_isbad_vector(bin) for wafer in self.wafers], dtype=np.bool)

    def die_bin_vector(self):
        return np.array([wafer.die_bin_vector() for wafer in self.wafers], dtype=np.int)

    def die_param_vector(self):
        return np.array([wafer.die_param_vector() for wafer in self.wafers])


class Wafer(object):
    def __init__(self, lot: (Lot, str), wafer: int):
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
        self._die = TypedDict(required_type=Die)
        self.x_range = None
        self.y_range = None
        self.y_min = None
        self.y_max = None
        self.x_min = None
        self.x_max = None

    def __str__(self):
        result = ""
        result += f"Wafer lw: {self._l} {self._w}\n"
        result += f"  Total Dice: {self._die and len(self._die) or 0}\n"
        result += f"  Usable/Total Diameter: {2 * (self.radius - self.edge_exclusion)} / {2 * self.radius}\n"
        result += f"  Center: {self.center}\n"
        if self._die:
            die = self._die[(0, 0)]
            result += f"  Die size: {die.x_size} x {die.y_size}: {die.area} cm\u00b2\n"
        if self.x_range:
            result += f"  x: {min(self.x_range)} : {max(self.x_range)} \n"
        if self.y_range:
            result += f"  y: {min(self.y_range)} : {max(self.y_range)} \n"
        return result

    def __repr__(self):
        if not self._die or not self.x_range or not self.y_range:
            return f"Undefined {int(2 * self.radius)}mm wafer, lw: {self._l} {self._w}"

        result = "\n"
        for y in self.y_range:
            chars = []
            for x in self.x_range:
                char = ""
                if (x, y) in self._die:
                    if 0 == x == y:
                        char += '\x1b[96m'  # Cyan text

                    # Black rectangle for Good die, White rectangle for Bad die
                    char += "\u25AF" if self._die[(x, y)].is_good else "\u25AE"

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
        new_wafer.die = copy.deepcopy(self.die)
        return new_wafer

    def __len__(self):
        return len(self._die)

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

    @property
    def die(self):
        return self._die

    @die.setter
    def die(self, die):
        self._die = die
        if die:
            self.x_min = min(d.x for d in die.values())
            self.x_max = max(d.x for d in die.values())
            self.x_range = range(self.x_min, self.x_max + 1)

            self.y_min = min(d.y for d in die.values())
            self.y_max = max(d.y for d in die.values())
            self.y_range = range(self.y_max, self.y_min - 1, -1)  # Descending for easy maps in console

    @property
    def die_count(self):
        if not self.die: return 0
        return len(self.die)

    def die_isbad_vector(self, bin=0):
        if bin and bin > 0:  # Positive Integer
            return np.array([die.bin == bin for die in self.die.values()], dtype=np.bool)

        return np.array([die.is_bad for die in self.die.values()], dtype=np.bool)

    def die_bin_vector(self):
        return np.array([die.bin for die in self.die.values()], dtype=np.int)

    def die_param_vector(self):
        return np.array([die.param for die in self.die.values()])

    def set_param_vector(self, value):
        if isinstance(value, collections.Mapping):
            for key, val in value.items():
                self.die[key].param = val
            return
        if len(value) == len(self.die):
            # Trust they are still in order
            for val, die in zip(value, self.die):
                die.param = val
            return
        raise IndexError(f"Incorrect array length: {len(value)} != {len(self.die)}")

    def plot(self, z="is_bad"):
        if not self._die:
            raise KeyError(f"Wafer {self._l} {self._w} Die not defined.")

        fig = plt.figure(figsize=(6, 6))
        fig.subplots(1, 1)
        ax = fig.axes[0]

        # Circles for edge of wafer and edge exclusion zone
        ax.add_patch(patches.Circle(xy=(0, 0), radius=self.radius))
        ax.add_patch(patches.Circle(xy=(0, 0), radius=self.radius - self.edge_exclusion, color='0.75'))
        ax.autoscale()  # Do now, since Circles define the outer edge

        show_empty = True
        die = self._die[(0, 0)]
        aspect_ratio = die.aspect_ratio
        x_size_mm = die.x_size * 10
        y_size_mm = die.y_size * 10

        if z == 'param':
            z_min = np.min(self.die_param_vector())
            z_max = np.max(self.die_param_vector())

        for y in self.y_range:
            for x in self.x_range:
                die = self._die.get((x, y), None)
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
                    # print(x, y, fill)
                    z_color = matplotlib.cm.jet(100 * (fill - z_min) / (z_max - z_min))
                    ax.add_patch(patches.Rectangle(xy=(x_corner, y_corner),
                                                   width=x_size_mm * .98, height=y_size_mm * .98,
                                                   edgecolor=color, Fill=True, facecolor=z_color
                                                   ))
                    plt.title(f"z: [{z_min},{z_max}]")
                else:
                    ax.add_patch(patches.Rectangle(xy=(x_corner, y_corner),
                                                   width=x_size_mm * .98, height=y_size_mm * .98,
                                                   edgecolor=color, Fill=fill))

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

            for y in np.arange(y_min, y_max + 1):
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
                        dice[(x, y)] = Die(self, x, y, x_size, y_size)
                        # print(f"FIT: Center: {center} Corners: {nw} {ne} {se} {sw}")
                    else:
                        # print(f"NO:  Center: {center} Corners: {nw} {ne} {se} {sw}")
                        pass

            if len(dice) > len(wafer_map):
                wafer_map = dice
                zero_center = center

        if len(wafer_map):
            self.die = wafer_map
            self.center = zero_center
        else:
            raise ValueError(f"Unable to generate array map for x/y (in cm): {x_size}, {y_size}")


class Die(object):
    def __init__(self, wafer: Wafer, x: int, y: int, x_size: float, y_size: float):
        self._wafer = wafer
        self._x = int(x)
        self._y = int(y)
        self.x_size = x_size
        self.y_size = y_size
        self._bin = 1
        self._param = 0.

    def __repr__(self):
        return f"Die: {self.l} {self.w} {self.x},{self.y}"

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
        return self._wafer._l

    @property
    def w(self):
        return self._wafer._w

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

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
