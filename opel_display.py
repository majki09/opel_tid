from enum import Enum


class OpelDisplayMessageType(Enum):
    MAIN_SCREEN_AUDIO = 0x03


class OpelDisplayMessageID(Enum):
    SONG_TITLE = 0x10


class FontSize(Enum):
    SMALL = 100     # b'd'
    NORMAL = 103    # b'g'


class OpelDisplayPayload:
    def __init__(self):
        self.song_title = ""
        self.song_title_length = 0
        self.song_title_decoded = ""
        self.texts = []

    def find_song_title(self, payload):
        """
        Finds "Song title" ID in the payload.
        :return:
        """
        self.song_title = payload.split(OpelDisplayMessageID.SONG_TITLE.value.to_bytes())[1]
        self.song_title_length = self.song_title[0]
        self.song_title_decoded = self.song_title[1:].decode("utf_16_be")

    def find_texts(self, song_title_decoded):
        """
        Finds "Texts" in "Song titles".
        :return:
        """
        return song_title_decoded.split("\x1b")

    def parse(self, payload):
        self.find_song_title(payload)

        for text in self.find_texts(self.song_title_decoded)[1:]:
            if len(text) > 3:
                self.texts.append(OpelDisplayMessage(message=text))

    def build(self, texts, size=FontSize.NORMAL):
        new_preamble = bytearray(b'\x1f\x00\x1b\x00[\x00c\x00m\x00\x1b\x00[\x00f\x00S\x00_\x00g\x00m')
        new_text = texts.encode("utf_16_be")
        ending = bytearray(b'\x00\x00')

        new_preamble[20] = size.value

        new_song_title = new_preamble + \
            new_text + \
            ending

        new_song_title_length = (len(new_song_title) - 1) // 2
        new_song_title[0] = new_song_title_length

        new_payload = bytearray(b"@\x00A\x03\x10") + new_song_title

        return new_payload


class OpelDisplayMessage:
    def __init__(self, message: str):
        self.message = message
        self.text = ""
        self.type = b""

        self.parse()

    def parse(self):
        self.type = self.message[4]
        self.text = self.message[6:].strip("\x00")


# FM  JEDYNKA
# payload = bytearray(b'\xc0\x007\x03\x10\x1a\x00\x1b\x00[\x00f\x00S\x00_\x00d\x00m\x00F\x00M\x00 \x00\x1b\x00[\x00f\x00S\x00_\x00g\x00m\x00 \x00J\x00E\x00D\x00Y\x00N\x00K\x00A\x00\x00')
# FM  TROJKA
# payload = bytearray(b'@\x003\x03\x10\x18\x00\x1b\x00[\x00f\x00S\x00_\x00d\x00m\x00F\x00M\x00 \x00\x1b\x00[\x00f\x00S\x00_\x00g\x00m\x00 \x00m\x00y\x00 \x00d\x00o\x00\x00')
# FM 18:03
# payload = bytearray(b'@\x007\x03\x10\x1a\x00\x1b\x00[\x00f\x00S\x00_\x00d\x00m\x00F\x00M\x00 \x00\x1b\x00[\x00f\x00S\x00_\x00g\x00m\x00 \x00 \x00 \x001\x008\x00:\x000\x003\x00\x00')

# CD
# payload = bytearray(b'@\x00%\x03\x10\x11\x00\x1b\x00[\x00c\x00m\x00\x1b\x00[\x00f\x00S\x00_\x00g\x00m\x00C\x00r\x00a\x00z\x00y\x00\x00@\x00%\x03\x90\x11\x00\x1b\x00[\x00c\x00m\x00\x1b\x00[\x00f\x00S\x00_\x00g\x00m\x00C\x00r\x00a\x00z\x00y\x00\x00')
#payload = bytearray(b'@\x00A\x03\x10\x1f\x00\x1b\x00[\x00c\x00m\x00\x1b\x00[\x00f\x00S\x00_\x00g\x00m\x00A\x00T\x00B\x00 \x00-\x00 \x00M\x00a\x00r\x00r\x00a\x00k\x00e\x00s\x00h\x00.\x00m\x00p\x003\x00\x00')
#odp = OpelDisplayPayload()
#odp.parse(payload)

#odp.build("Jasieczko!")

pass
