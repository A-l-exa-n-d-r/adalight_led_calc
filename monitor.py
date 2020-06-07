from core import array_line_generator
import core


class Monitor:
    def __init__(self, size_x: int, size_y: int, x0: int = 0, y0: int = 0):
        """
        create new monitor-object form calculation led's array
        :param size_x: width monitor px
        :param size_y: height monitor px
        :param x0: first coordinate left top angle
        :param y0: second coordinate left top angle
        """
        self.sizeX = size_x
        self.sizeY = size_y
        self.x0 = x0
        self.y0 = y0

        self.top = core.top
        self.right = core.right
        self.bottom = core.bottom
        self.left = core.left
        self.default_led_array_depth_coefficient = core.default_led_array_depth_coefficient
        self.clockwise = core.clockwise
        self.counterclockwise = core.counterclockwise
        self.positive = core.positive
        self.negative = core.negative

        self.top_left = core.top_left
        self.top_right = core.top_right
        self.bottom_right = core.bottom_right
        self.bottom_left = core.bottom_left

        self.side_coordinate = {
            0: self.y0,
            1: self.x0 + self.sizeX,
            2: self.y0 + self.sizeY,
            3: self.x0
        }

        self.side_width = {
            0: self.sizeX,
            1: self.sizeY,
            2: self.sizeX,
            3: self.sizeY
        }

    def led_line_create(self, alignment_side: int, count_led: int, first_led: int = 1, line_direction: int = 1,
                        alignment_coordinate=None, array_width=None, led_array_depth=None, start_coord=None):

        if alignment_coordinate is None:
            alignment_coordinate = self.side_coordinate[alignment_side]

        if array_width is None:
            array_width = self.side_width[alignment_side]

        if led_array_depth is None:
            led_array_depth = self.default_led_array_depth_coefficient

        if 0 < led_array_depth < 1:
            led_array_depth = int(led_array_depth * (self.sizeX if alignment_side in (1, 3) else self.sizeY))
        else:
            led_array_depth = int(led_array_depth)

        if start_coord is None:
            start_coord = (self.x0, self.y0)

        return array_line_generator(alignment_side, first_led, count_led, alignment_coordinate, array_width,
                                    led_array_depth, line_direction, start_coord)

    def full_perimeter_from_angle(self, count_led: tuple = (1, 1, 1, 1), first_led: int = 1,
                                  perimeter_direction: int = 1, angle: int = 2):

        if len(count_led) != 4:
            raise KeyError("use 4 int value in count_led")

        if perimeter_direction not in (-1, 1):
            raise KeyError("use only -1 or 1 in direction")

        if angle not in (0, 1, 2, 3):
            raise AttributeError("only 0, 1, 2, 3 in angle, not " + str(angle))

        now_led = first_led
        req_dict = {}

        for count_led_in_part in count_led:
            side = angle if perimeter_direction == 1 else (angle - 1) % 4

            req_dict.update(self.led_line_create(
                alignment_side=side,
                count_led=count_led_in_part,
                first_led=now_led,
                line_direction=perimeter_direction if side in (0, 1) else perimeter_direction * -1))
            now_led += count_led_in_part
            angle = (angle + perimeter_direction) % 4

        return req_dict
