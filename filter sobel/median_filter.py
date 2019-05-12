def median_filter(original):
    width = len(original)
    height = len(original[0])
    image_median_filtered = [[0 for _ in range(height)] for _ in range(width)]

    process_corners_image(original, image_median_filtered)
    process_edges_image(original, image_median_filtered)
    process_middle_image(original, image_median_filtered)

    return image_median_filtered


def process_middle_image(input_image, result_image):
    width = len(input_image)
    height = len(input_image[0])
    for i in range(width - 2):
        for j in range(height - 2):
            color = get_median_color(3, 3, input_image, i, j)
            result_image[i + 1][j + 1] = color


def process_edges_image(input_image, result_image):
    width = len(input_image)
    height = len(input_image[0])
    range_h = min(2, height)
    for i in range(width - 2):
        color = get_median_color(3, range_h, input_image, i, 0)
        result_image[i + 1][0] = color
        if height > 1:
            color = get_median_color(3, 2, input_image, i, height - 2)
            result_image[i + 1][height - 1] = color

    range_w = min(2, width)
    for j in range(height - 2):
        color = get_median_color(range_w, 3, input_image, 0, j)
        result_image[0][j + 1] = color
        if width > 1:
            color = get_median_color(2, 3, input_image, width - 2, j)
            result_image[width - 1][j + 1] = color


def process_corners_image(input_image, result_image):
    width = len(input_image)
    height = len(input_image[0])
    range_h = min(2, height)
    range_w = min(2, width)

    color = get_median_color(range_w, range_h, input_image, 0, 0)
    result_image[0][0] = color
    if width > 1:
        color = get_median_color(2, range_h, input_image, width - 2, 0)
        result_image[width - 1][0] = color

    if width > 1 and height > 1:
        color = get_median_color(2, 2, input_image, width - 2, height - 2)
        result_image[width - 1][height - 1] = color

    if height > 1:
        color = get_median_color(range_w, 2, input_image, 0, height - 2)
        result_image[0][height - 1] = color


def get_median_color(size_width, size_height, image, x, y):
    all_pixels = []
    for i in range(size_width):
        for j in range(size_height):
            all_pixels.append(image[x + i][y + j])

    return get_middle_number(all_pixels)


def get_middle_number(all_pixels):
    all_pixels.sort()
    half_length = len(all_pixels) // 2
    if half_length * 2 < len(all_pixels):
        return all_pixels[half_length]
    return (all_pixels[half_length] + all_pixels[half_length - 1]) / 2

