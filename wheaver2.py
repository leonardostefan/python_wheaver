import cv2
import tkinter
from tkinter import filedialog
from math import sin, cos, radians


def black(y_test, x_test, variable):
    color = [image.item(y_test, x_test, 0), image.item(y_test, x_test, 1), image.item(y_test, x_test, 2)]
    if color[0] == 0 and color[1] == 0 and color[2] == 0:
        variable += 1
        return int(variable)
    else:
        return int(variable)

# Escolha verifica qt  pixels na linha, se 'black_pixels' é absoluta, se black_pixels/total_pixels é relativo
def pixels_analysis(point_1, point_2):
    
    yd = point_2[0] - point_1[0]
    xd = point_2[1] - point_1[1]
    y_abs = abs(yd)
    x_abs = abs(xd)
    if y_abs > x_abs:
        step = y_abs
    else:
        step = x_abs
    black_pixels = 0
    total_pixels = 0
    for pixel in range(1, step):
        y_position = int(round(point_1[0] + (yd * (pixel / step))))
        x_position = int(round(point_1[1] + (xd * (pixel / step))))
        pxp = [x_position, y_position]
        color = [image.item(pxp[0], pxp[1], 0), image.item(pxp[0], pxp[1], 1), image.item(pxp[0], pxp[1], 2)]
        total_pixels += 1
        if color[0] == color[1] == color[2] == 0:
            black_pixels += 1
    return [(black_pixels/(total_pixels+1)), point_1, point_2]

# Escolha do melhor primeiro pixel 
def get_best(nail_positions):
    print('Encontrando melhor:')
    bigger = [0,0,0]
    for j in range(0, nail_number):
        actual_point= nail_positions[j]
        for i in range(0, nail_number):
            point_analysis = nail_positions[i]
            current_test = pixels_analysis(actual_point, point_analysis)
            if current_test[0] > bigger[0]:
                bigger = [current_test[0], current_test[1], current_test[2]]
    print('Encontrado')

    return bigger[2]

def clean_image():
    for y_axis in range(0, image.shape[0]):
        for x_axis in range(0, image.shape[1]):
            cleaned.itemset(y_axis, x_axis, 0, 255)
            cleaned.itemset(y_axis, x_axis, 1, 255)
            cleaned.itemset(y_axis, x_axis, 2, 255)

# Inicialização
root = tkinter.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()
image = cv2.imread(file_path)
cleaned = cv2.imread(file_path)
clean_image()
size = image.shape
# (Y,X)
center = [int(size[1] / 2), int(size[0] / 2)]
nail_number = int(input('nails number: '))
lines_number = int(input('lines number: '))

angle = 360 / nail_number
nail_positions = []
for i in range(0, nail_number):
    x = int(center[0] + ((center[0] - 1) * sin(-(radians(angle * i)))))
    y = int(center[1] + ((center[0] - 1) * cos(-(radians(angle * i)))))
    positions = [y, x]
    nail_positions.append(positions)

 
actual_point = nail_positions[0]
# actual_point = get_best(nail_positions)
segments = [0]
lines = 0
ctn = True


while ctn:
    bigger = [0, nail_positions[0], nail_positions[0]]
    # Encontra candidato com maior quantidade de pixels
    for i in range(0, nail_number):
        point_analysis = nail_positions[i]
        current_test = pixels_analysis(actual_point, point_analysis)
        if current_test[0] > bigger[0]:
            bigger = [current_test[0], current_test[1], current_test[2]]
    # Atualização da linha
    line = [bigger[1], bigger[2]]
    index = nail_positions.index(bigger[2])
    actual_point = bigger[2]
    segments.append(index)
    cv2.line(image, (line[1][0], line[1][1]), (line[0][0], line[0][1]), (255, 255, 255), 1)
    cv2.line(cleaned, (line[1][0], line[1][1]), (line[0][0], line[0][1]), (0, 0, 0), 1)
    image_output_1 = cv2.resize(image, (700, 700))
    image_output_2 = cv2.resize(cleaned, (700, 700))
    # cv2.imshow('output_1', image_output_1)
    cv2.imshow('output_2', image_output_2)
    cv2.waitKey(10)
    # print('.')
    lines += 1
    if bigger[0] <= 0.01 or lines >= lines_number:
        ctn=False
print('Finish')
image_output_2 = cv2.resize(cleaned, (700, 700))
cv2.imshow('output', image_output_2)
cv2.waitKey(0)
cv2.destroyAllWindows()
archive = [f'Finish, {lines} lines\n']
for i in range(1, len(segments)):
    archive.append(f'from {segments[(i - 1)]} to {segments[i]}\n')
cv2.destroyAllWindows()
file_type = [['text file', '*.txt']]
file_path = filedialog.asksaveasfilename(filetypes=file_type, defaultextension=file_type)
archive_txt = open(file_path, 'a')
archive_txt.writelines(archive)
archive_txt.close()
