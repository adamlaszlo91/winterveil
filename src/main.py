from gui import GUI
from core import Core


def main() -> None:
    core = Core()
    gui = GUI(core)
    gui.mainloop()


if __name__ == '__main__':
    main()
