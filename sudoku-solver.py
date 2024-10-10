import time
from PIL import Image
from pytesseract import pytesseract
import pyautogui
from pynput import mouse, keyboard
from sudoku import Sudoku

def on_click(x, y, button, pressed):
    global clicks_monitored
    if pressed and button == mouse.Button.left:
        clicks_monitored.append([x, y])
        return False
    elif pressed and button in [mouse.Button.right, mouse.Button.middle, mouse.Button.unknown]:
        clicks_monitored = []
        exit()
        return False
    
def on_press(key):
    return False

# Disable pyautogui failsafe for faster clicking (risky, but it clicks 81 times max so not a big deal)
pyautogui.FAILSAFE = False

# Press any key on keyboard first (enables left clicking without script starting prematurely for navigating/starting new sudoku...)
clicks_monitored = []
listener = keyboard.Listener(on_press=on_press)
listener.start()
listener.join()

# Get the top left and bottom right position of the sudoku on screen through two consecutive left clicks
for i in range(2):
    listener = mouse.Listener(on_click=on_click)
    listener.start()
    listener.join()
    if len(clicks_monitored) == 0: exit()
print("Sudoku bounds: {}".format(clicks_monitored))

# Screenshot the full sudoku & size metrics
s1 = time.perf_counter_ns()
img_start_x = clicks_monitored[0][0]
img_start_y = clicks_monitored[0][1]
img_width = clicks_monitored[1][0] - img_start_x
img_height = clicks_monitored[1][1] - img_start_y
w_ninth = img_width // 9
h_ninth = img_height // 9
w_margin = img_width // 100
h_margin = img_height // 100
sudoku_img = pyautogui.screenshot(region=(clicks_monitored[0][0], clicks_monitored[0][1], img_width , img_height))
sudoku_img.quantize(colors=2, dither=0)
s2 = time.perf_counter_ns()

# Detect screenshotted digits and piece the sudoku together
s3 = time.perf_counter_ns()
sudoku_board = [[0,0,0,0,0,0,0,0,0] for _ in range(9)]
for j in range(9):
    for i in range(9):
        crop_img = sudoku_img.crop([w_ninth * i + w_margin, h_ninth * j + h_margin, w_ninth * (i+1) - w_margin, h_ninth * (j+1) - h_margin])
        result = str(pytesseract.image_to_string(crop_img, lang="digits_comma", config='-c tessedit_char_whitelist=123456789 --psm 6 --oem 3'))
        result = result.replace("\n", "")
        sudoku_board[j][i] = int(result[0]) if result.isdigit() else 0
s4 = time.perf_counter_ns()

# Solve the sudoku
s5 = time.perf_counter_ns()
sudoku = Sudoku(3, 3, board=sudoku_board)
#sudoku.show_full()
solution = sudoku.solve().board
s6 = time.perf_counter_ns()


# Input the solution digit for digit
s7 = time.perf_counter_ns()
for j in range(9):
    for i in range(9):
        if (sudoku_board[j][i] != 0): continue
        pyautogui.click(img_start_x + w_ninth * (i + 0.5), img_start_y + h_ninth * (j + 0.5), _pause=False)
        pyautogui.press(str(solution[j][i]))
s8 = time.perf_counter_ns()

# Stats
print("Screenshot: {} ms\nRead: {} ms\nSolve: {} ms\nInput: {} ms".format((s2-s1)/1e6,(s4-s3)/1e6,(s6-s5)/1e6,(s8-s7)/1e6))
print("SUM:",round((s8-s1)/1e9, 2),"seconds")