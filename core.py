import math
import os
from shutil import copy2

top = 0
right = 1
bottom = 2
left = 3
default_led_array_depth_coefficient = 0.15
clockwise = 1
counterclockwise = -1
positive = 1
negative = -1

top_left = 0
top_right = 1
bottom_right = 2
bottom_left = 3

profiles_path = os.path.join(os.environ["USERPROFILE"], "Prismatik", "Profiles")
profiles_list = list()

for i in os.listdir(profiles_path):
    filename, ini = os.path.splitext(i)
    if ini == ".ini":
        profiles_list.append(filename)

led_block = """[LED_{led_num}]
IsEnabled={IsEnabled}
Position=@Point({PointX} {PointY})
Size=@Size({SizeX} {SizeY})
CoefRed={CoefRed}
CoefGreen={CoefGreen}
CoefBlue={CoefBlue}

"""


def array_line_generator(alignment_side: int, first_led: int, count_leds: int,
                         alignment_coordinate: int, array_width: int, led_array_depth: int,
                         line_direction=1, start_coord=(0, 0)):
    """
    :param alignment_side: 0-top, 1-right, 2-bottom, 3-left
    :param first_led: first led_id in line
    :param count_leds: count led's in line
    :param alignment_coordinate: general coordinate line
    :param array_width: width line array
    :param led_array_depth: probably 0.15 * (size non alignment side)
    :param line_direction: -1-negative(to left/up), 1-positive(to right/down)
    :param start_coord: up-left coordinate display from single display = (0, 0)
    :return: tuple with "SizeX", "SizeY", "PointX", "PointY" change led's
    """
    if line_direction not in (-1, 1):
        raise AttributeError("only -1, 1 in direction, not " + str(line_direction))
    req = {}
    x0_window, y0_window = start_coord
    for led in range(first_led, first_led+count_leds):
        i_led = led - first_led
        req[led] = {}
        if alignment_side in (0, 2):
            req[led]["SizeX"] = math.ceil(array_width / count_leds)
            req[led]["SizeY"] = led_array_depth
            req[led]["PointX"] = int(x0_window + (array_width / count_leds) * i_led if line_direction == 1 else
                                     (x0_window + array_width) - ((array_width / count_leds) * (i_led + 1)))
            req[led]["PointY"] = alignment_coordinate if alignment_side == 0 else alignment_coordinate - led_array_depth
        elif alignment_side in (1, 3):
            req[led]["SizeX"] = led_array_depth
            req[led]["SizeY"] = math.ceil(array_width / count_leds)
            req[led]["PointX"] = alignment_coordinate if alignment_side == 3 else alignment_coordinate - led_array_depth
            req[led]["PointY"] = int(y0_window + (array_width / count_leds) * i_led if line_direction == 1 else
                                     (y0_window + array_width) - ((array_width / count_leds) * (i_led + 1)))
        else:
            raise AttributeError("only 0, 1, 2, 3 in alignment_side, not " + str(alignment_side))
    return req


def copy_profiles(from_profile: str, to_profile: str):
    """
    :param from_profile: file name copied profile
    :param to_profile: file name new profile file
    :return: path to new profile file
    """
    os.chdir(profiles_path)
    req_file_name = os.path.abspath(to_profile + ".ini")
    copy2(from_profile + ".ini", req_file_name)
    return req_file_name


def get_profile_led_massive(led_dict: dict, max_led: int = 511,
                            coef_red: int = 1, coef_green: int = 1, coef_blue: int = 1):
    """
    :param led_dict: tuple with "SizeX", "SizeY", "PointX", "PointY" change led's
    :param max_led: max change led's in configuration, in Prismatik = 511
    :param coef_red: general red coef
    :param coef_green: general green coef
    :param coef_blue: general blue coef
    :return: str with configuration led's
    """
    count_led = max(led_dict)
    req_str = ""
    for led_id in range(1, max_led+1):
        try:
            req_str += led_block.format(
                led_num=led_id,
                IsEnabled=str(led_id <= count_led).lower(),
                PointX=led_dict[led_id]["PointX"],
                PointY=led_dict[led_id]["PointY"],
                SizeX=led_dict[led_id]["SizeX"],
                SizeY=led_dict[led_id]["SizeY"],
                CoefRed=coef_red,
                CoefGreen=coef_green,
                CoefBlue=coef_blue
            )
        except KeyError:
            req_str += led_block.format(
                led_num=led_id,
                IsEnabled=str(led_id <= count_led).lower(),
                PointX=0,
                PointY=0,
                SizeX=0,
                SizeY=0,
                CoefRed=coef_red,
                CoefGreen=coef_green,
                CoefBlue=coef_blue
            )
    return req_str
