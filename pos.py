from pynput.mouse import Button, Controller as MController

mouse = MController()

if __name__ == '__main__':
    while True:
        print(mouse.position)
