# Tkinter — სასწავლო საფუძვლები

**დანიშნულება:** ეს ფაილი ხსნის Python-ის GUI-ის საბაზისო პრინციპებს. ქვემოთ მოცემული მაგალითები **სასწავლოა** და არ არის KLAVA-ს მოქმედი `trainer.py`-ის ასლები.

## რას წარმოადგენს Tkinter

Tkinter არის Python-ის სტანდარტულ ბიბლიოთეკაში არსებული ინტერფეისი Tk გრაფიკულ ინსტრუმენტებთან. მისი საშუალებით იქმნება ფანჯრები, ტექსტი, მენიუ, ღილაკები და მოვლენებზე რეაქცია.

## ფანჯრის მინიმალური მაგალითი

```python
import tkinter as tk

root = tk.Tk()
root.title("გამარჯობა")
label = tk.Label(root, text="ჩემი პირველი ფანჯარა")
label.pack()
root.mainloop()
```

**Inputs:** ტექსტი და GUI გარემო.  
**Steps:** `Tk()` ქმნის ძირითად ფანჯარას; `Label` ქმნის ტექსტის ელემენტს; `pack()` ათავსებს მას; `mainloop()` ამუშავებს მოვლენებს.  
**Output:** ფანჯარა წარწერით.  
**Educational rationale:** ვიზუალური ელემენტის შექმნა და მისი ჩვენება განსხვავებული ნაბიჯებია.

## მოვლენა და callback

```python
import tkinter as tk

def clicked() -> None:
    """ღილაკზე დაჭერის შემდეგ ცვლის წარწერას."""
    label.config(text="დაჭერილია")

root = tk.Tk()
label = tk.Label(root, text="დააჭირე ღილაკს")
label.pack()
tk.Button(root, text="დაჭერა", command=clicked).pack()
root.mainloop()
```

`command=clicked` გადასცემს ფუნქციის ბმულს და არა გამოძახების შედეგს. მოვლენა გამოიწვევს `clicked()`-ის შესრულებას.

## Canvas — ხატვის ზედაპირი

```python
import tkinter as tk

root = tk.Tk()
canvas = tk.Canvas(root, width=400, height=200, bg="white")
canvas.pack()
canvas.create_text(200, 100, text="KLAVA", font=("Arial", 24))
root.mainloop()
```

KLAVA-ში ვიზუალური ხატვის ფუნქციები თავმოყრილია `ui/canvas.py`-სა და `ui/keyboard.py`-ში.

## KLAVA-სთან დაკავშირება

- `main.py` ქმნის `Tk` ფანჯარას და იწყებს მოვლენების ციკლს.
- `trainer.py` აკავშირებს სესიას, მენიუს, სავარჯიშოსა და ფანჯრის მოვლენებს.
- `exercises/typing.py` ამჟამად იღებს `tk.Event`-ს და ამუშავებს კლავიშის მნიშვნელობას.
- `logic/engine.py` Tkinter-ზე არ არის დამოკიდებული.

**Known limitation:** მოცემული მაგალითები ცალკე უნდა გაუშვათ და არ უნდა ჩაისვას პირდაპირ `trainer.py`-ში. GUI-ის სამუშაოდ საჭიროა გრაფიკული გარემო.
