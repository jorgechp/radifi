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

        lcd_columns = 16
        lcd_rows = 2

        self.__lcd = characterlcd.Character_LCD_Mono(
            lcd_rs,
            lcd_en,
            lcd_d4,
            lcd_d5,
            lcd_d6,
            lcd_d7,
            lcd_columns,
            lcd_rows)

        self.__lcd.cursor = False

        self.is_busy_lcd = False

    def print_message(self, message_to_print: str) -> None:
        """
        Clear the LCD screen and print a new message.

        ARGUMENTS
        ---------
         :param message_to_print: The new message to be printed.
        """

        self.__lcd.clear()
        self.__lcd.message = message_to_print
