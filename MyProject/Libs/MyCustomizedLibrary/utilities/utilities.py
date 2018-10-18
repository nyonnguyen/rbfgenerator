import re

class Utilities():

    def _convert_rgb_to_hex(self, rgb_string):
        color_tuple = rgb_string.replace("rgb(", "").replace("rgba(", "").replace(")", "").replace(" ", "")
        color_tuple = color_tuple.split(",")
        rgb = (int(color_tuple[0]), int(color_tuple[1]), int(color_tuple[2]))
        hex_str = rgb_to_hex(rgb)
        return hex_str

    def _is_rgb_color(self, color_str):
        r = r"rgb\((\d+),\s*(\d+),\s*(\d+)\)"
        r2 = r"rgba\((\d+),\s*(\d+),\s*(\d+),\s*(\d+)\)"
        return re.match(r, color_str) or re.match(r2, color_str)
