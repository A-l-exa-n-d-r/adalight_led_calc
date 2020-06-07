build led config text from single 4k monitor 42x24 LED.
LED glued to right-down, clockwise(look from screen)
```
mon = Monitor(3840, 2160)
build = mon.full_perimeter_from_angle((42, 24, 42, 24))
print(get_profile_led_massive(build))
```

double 4k monitor with common LED-array
```
mon = Monitor(3840*2, 2160)
build = mon.full_perimeter_from_angle((42*2, 24, 42*2, 24))
print(get_profile_led_massive(build))
```

double monitor different size and individual LED-array:
```
mon1 = Monitor(3840, 2160)
mon2 = Monitor(1920, 1080, -1920, 0)
build = mon1.full_perimeter_from_angle((42, 24, 42, 24))
build.update(mon2.full_perimeter_from_angle((29, 16, 29, 16), max(build) + 1))
print(get_profile_led_massive(build))
```

copy some profile files to `my_profile` profile file and get path to them
```
print(core.copy_profiles(core.profiles_list[0], "my_profile"))
```

custom led array from 4k monitor
led starts on top-right angle, counterclockwise, 
top side = 84 led, bottom side = 42 led, left and right = 24 and 24 led
```
mon = Monitor(3840, 2160)
build = mon.full_perimeter_from_angle((84, 24, 42, 24),
                                      perimeter_direction=mon.counterclockwise,
                                      angle=mon.top_right)
print(get_profile_led_massive(build))
```