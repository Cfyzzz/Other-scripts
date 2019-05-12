import simple_draw as sd
from median_filter import median_filter


def get_bright_map(color):
    return (0.299 * color[0] + 0.587 * color[1] + 0.114 * color[2]) / 255


def to_grayscale(original):
    sector = 1
    width = int(original.get_rect().width / sector)
    height = original.get_rect().height
    grayscale = []
    for i in range(width):
        grayscale.append([])
        for j in range(height):
            pixel = original.get_at((i, j))
            grayscale[-1].append(get_bright_map(pixel))

    return grayscale


def sobel_filter(g, sx):
    width = len(g)
    height = len(g[0])
    size_sx = len(sx)
    half_size_sx = (size_sx - 1) // 2
    my_new_surface = sd.pygame.Surface((width, height))

    for x in range(half_size_sx, width - half_size_sx):
        for y in range(half_size_sx, height - half_size_sx):
            gx = 0
            gy = 0
            for i in range(size_sx):
                for j in range(size_sx):
                    gx += sx[i][j] * g[x - half_size_sx + i][y - half_size_sx + j]
                    gy += sx[j][i] * g[x - half_size_sx + i][y - half_size_sx + j]

            color = int((gx ** 2 + gy ** 2) ** 0.5) * 10
            my_new_surface.set_at((x, y), (color, color, color))

    return my_new_surface


def main():
    sd.caption = "Фильтр Собеля"
    file_name = "photo_2019-01-05_23-42-32.jpg"
    img = sd.pygame.image.load(file_name)
    gray_image = to_grayscale(img)
    clear_image = median_filter(gray_image)
    result_image = sobel_filter(clear_image, [[-2, -2, -2, -2, -2], [-1, -1, -1, -1, -1], [0, 0, 0, 0, 0],
                                              [1, 1, 1, 1, 1], [2, 2, 2, 2, 2]])
    # result_gray_image = sobel_filter(gray_image, [[-2, -2, -2, -2, -2], [-1, -1, -1, -1, -1], [0, 0, 0, 0, 0],
    #                                               [1, 1, 1, 1, 1], [2, 2, 2, 2, 2]])

    sd.start_drawing()
    my_display = sd.pygame.display.set_mode((1200, 800))
    my_display.blit(img, (0, 0))
    # my_display.blit(result_gray_image, (200, 0))
    my_display.blit(result_image, (0, 0))
    sd.finish_drawing()

    sd.pause()


if __name__ == "__main__":
    main()
