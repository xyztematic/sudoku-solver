# sudoku-solver
Solves any solvable digital sudoku (browser or app) with user simulated input.

Currently supports Windows 10+ only.

## Dependencies
- Python (Tested with 3.10.4, may work with other versions) with the following libraries:
  - Pillow ```pip install pillow```
  - pyautogui ```pip install pyautogui```
  - pynput ```pip install pynput```
  - sudoku ```pip install py-sudoku```
  - pytesseract ```pip install pytesseract```
- Local install of Tesseract-OCR (https://github.com/tesseract-ocr/tesseract)
  - tesseract.exe is in PATH (check with ```tesseract --version```)
  - copy digits_comma.traineddata into /<your-tesseract-location>/tessdata

## Usage
- Go onto your desired sudoku website/app
- If you haven't already: Make sure that input is possible with a click on an emtpy sudoku cell followed by pressing a number key
- Wait until the puzzle is fully visible and input is possible
- ```python sudoku-solver.py```
- AFTER THE FOLLOWING STEP, YOU SHOULD NOT USE YOUR LEFT MOUSE BUTTON OTHER THAN INSTRUCTED:
  - Press any* key on your keyboard *(I recommend "ctrl")
- Left click the top left corner and then the bottom right corner of the sudoku precisely
- Don't move the mouse until the sudoku is solved (hopefully)
- You may operate your mouse again
