from data_showreal import data


def get_left_bottom(data):
    min_x = sorted(data, key=lambda x: x[0])[0][0]
    min_y = sorted(data, key=lambda x: x[1])[0][1]
    return [min_x, min_y]


def get_right_top(data):
    max_x = sorted(data, key=lambda x: x[0])[-1][0]
    max_y = sorted(data, key=lambda x: x[1])[-1][1]
    return [max_x, max_y]


def make_segments():
    segments = {}
    for seg_char, seg_data in data.items():
        left_bottom = get_left_bottom(seg_data)
        right_top = get_right_top(seg_data)
        new_data = [[d[0] - left_bottom[0], d[1] - left_bottom[1]] for d in seg_data]
        width = right_top[0] - left_bottom[0]
        height = right_top[1] - left_bottom[1]
        segments[seg_char] = dict(data=new_data, width=width, height=height)
    return segments


if __name__ == "__main__":
    segments = make_segments()
    print(segments)
