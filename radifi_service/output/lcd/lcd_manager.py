import math

import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd


class LCDManager(object):
    """
    Handle the connection with a LCD module by using the Adafruit CircuitPython library.
    """

    def __init__(self):
        lcd_rs = digitalio.DigitalInOut(board.D25)
        lcd_en = digitalio.DigitalInOut(board.D24)
        lcd_d4 = digitalio.DigitalInOut(board.D23)
        lcd_d5 = digitalio.DigitalInOut(board.D17)
        lcd_d6 = digitalio.DigitalInOut(board.D27)
        lcd_d7 = digitalio.DigitalInOut(board.D22)

        self._lcd_columns = 16
        lcd_rows = 2

        self.__lcd = characterlcd.Character_LCD_Mono(
            lcd_rs,
            lcd_en,
            lcd_d4,
            lcd_d5,
            lcd_d6,
            lcd_d7,
            self._lcd_columns,
            lcd_rows)

        self.__lcd.cursor = False

        self.is_busy_lcd = False

        self._upper_txt = ""
        self._lower_txt = ""

    def _center_text(self, text_to_center:str) -> str:
        len_text = len(text_to_center)

        cursor_position = math.ceil((self._lcd_columns - len_text) / 2)
        return " " * cursor_position + text_to_center

    def get_upper_text(self) -> str:
        return self._upper_txt

    def get_lower_text(self) -> str:
        return self._lower_txt

    def print_message(self, upper_text: str, lower_text: str) -> None:
        """
        Clear the LCD screen and print a new message.

        ARGUMENTS
        ---------
         :param upper_text: The upper message to be printed.
         :param lower_text: The lower message to be printed.
        """

        self.__lcd.clear()

        if upper_text:
            self._upper_txt = self._center_text(upper_text)
        if lower_text:
            self._lower_txt = self._center_text(lower_text)

        self.__lcd.message = self._upper_txt + "\n" + self._lower_txt
