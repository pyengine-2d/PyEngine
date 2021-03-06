import unittest
from pyengine.Utils import *
import os


class OthersTests(unittest.TestCase):
    def test_clamp(self):
        self.assertEqual(clamp(1, 0, 2), 1)
        self.assertEqual(clamp(3, 0, 2), 2)
        self.assertEqual(clamp(-1, 0, 2), 0)
        self.assertEqual(clamp(1, 0), 1)
        self.assertEqual(clamp(-1, 0), 0)
        self.assertEqual(clamp(1, maxi=3), 1)
        self.assertEqual(clamp(4, maxi=3), 3)
        self.assertEqual(clamp(1), 1)

    def test_wrap_text(self):
        self.assertEqual(wrap_text("oui oui", Font(), 0), "")
        self.assertEqual(wrap_text("oui oui", Font(), 50), "oui oui")
        self.assertEqual(wrap_text("oui oui", Font(), 20), "oui\noui")


class ColorTests(unittest.TestCase):
    def setUp(self):
        self.color = Color()

    def test_color(self):
        self.assertEqual(self.color.get(), (255, 255, 255, 255))
        self.color = Color(1, 2, 3)
        self.assertEqual(self.color.get(), (1, 2, 3, 255))

    def test_to_hex(self):
        self.assertEqual(self.color.to_hex(), "#FFFFFFFF")
        self.color = Color(21, 66, 19)
        self.assertEqual(self.color.to_hex(), "#154213FF")

    def test_from_hex(self):
        with self.assertRaises(ValueError):
            self.color.from_hex("#13")
        self.color.from_hex("#154213")
        self.assertEqual(self.color.get(), (21, 66, 19, 255))

    def test_ope_arith(self):
        self.assertEqual(self.color.get(), (255, 255, 255, 255))
        self.color -= Color(255, 0, 0)
        self.assertEqual(self.color.get(), (0, 255, 255, 0))
        self.color += Color(125, 0, 0)
        self.assertEqual(self.color.get(), (125, 255, 255, 255))
        self.color += Color(0, 0, 1)
        self.assertEqual(self.color.get(), (125, 255, 255, 255))
        self.color -= Color(255, 0, 0)
        self.assertEqual(self.color.get(), (0, 255, 255, 0))

    def test_ope_log(self):
        self.assertTrue(self.color == Color())
        self.assertTrue(self.color != Color(1, 1, 1))

    def test_function(self):
        self.color = Color(150, 150, 150)
        self.assertEqual(self.color.lighter().get(), (160, 160, 160, 255))
        self.assertEqual(self.color.darker().get(), (140, 140, 140, 255))

    def test_enum(self):
        self.assertEqual(Colors.BLACK.value.get(), (0, 0, 0, 255))
        self.assertEqual(Colors.WHITE.value.get(), (255, 255, 255, 255))
        self.assertEqual(Colors.RED.value.get(), (255, 0, 0, 255))
        self.assertEqual(Colors.BLUE.value.get(), (0, 0, 255, 255))
        self.assertEqual(Colors.GREEN.value.get(), (0, 255, 0, 255))


class FontTests(unittest.TestCase):
    def setUp(self):
        self.font = Font()

    def test_name(self):
        self.assertEqual(self.font.name, "arial")
        self.font.name = "Lucida"
        self.assertEqual(self.font.name, "Lucida")

    def test_size(self):
        self.assertEqual(self.font.size, 15)
        self.font.size = 20
        self.assertEqual(self.font.size, 20)

    def test_bold(self):
        self.assertFalse(self.font.bold)
        self.font.bold = True
        self.assertTrue(self.font.bold)

    def test_italic(self):
        self.assertFalse(self.font.italic)
        self.font.italic = True
        self.assertTrue(self.font.italic)

    def test_ope_log(self):
        self.assertTrue(self.font == Font())
        self.assertTrue(self.font != Font("Lucida"))

    def test_rendered_size(self):
        self.assertEqual(self.font.rendered_size("test"), (24, 18))
        self.assertEqual(self.font.rendered_size("OUI"), (25, 18))


class Vec2Tests(unittest.TestCase):
    def setUp(self):
        self.vec = Vec2()

    def test_coords(self):
        self.assertEqual(self.vec.coords, (0, 0))
        self.vec.coords = [1, 1]
        self.assertEqual(self.vec.coords, (1, 1))

    def test_length(self):
        self.assertEqual(self.vec.length(), 0)
        self.vec.coords = [0, 1]
        self.assertEqual(self.vec.length(), 1)

    def test_normalized(self):
        with self.assertRaises(ValueError):
            self.vec.normalize()
        self.vec.coords = [0, 2]
        self.assertEqual(self.vec.normalize(), Vec2(0, 1))

    def test_ope_arith(self):
        self.assertEqual(self.vec + Vec2(1, 0), Vec2(1, 0))
        self.assertEqual(self.vec - Vec2(1, 0), Vec2(-1, 0))
        self.assertEqual(Vec2(2, 2) * Vec2(1, 0), 2.0)
        self.assertEqual(Vec2(2, 2) * 2, Vec2(4, 4))
        self.assertEqual(-Vec2(1, 1), Vec2(-1, -1))
        self.assertEqual(Vec2(2, 2) / 2, Vec2(1, 1))

    def test_ope_log(self):
        self.assertTrue(self.vec == Vec2())
        self.assertTrue(self.vec != Vec2(1, 0))

    def test_repr(self):
        self.assertEqual(self.vec.__repr__(), "<Vector2(0, 0)>")

    def test_iter(self):
        for i in self.vec:
            self.assertEqual(i, 0)


class LoggersTests(unittest.TestCase):
    def setUp(self):
        self.log = loggers.create_logger("Test", "logs/test.log", False)

    def test_loggers(self):
        with self.assertRaises(KeyError):
            loggers.get_logger("B")
        self.assertEqual(self.log, loggers.get_logger("Test"))

    def test_write(self):
        self.log.info("TEST")
        with open("logs/test.log") as f:
            self.assertEqual(f.readlines()[-1].split(" ")[-1], "TEST\n")
        loggers.get_logger("PyEngine").info("TEST")
        with open("logs/pyengine.log") as f:
            self.assertEqual(f.readlines()[-1].split(" ")[-1], "TEST\n")


class LangTests(unittest.TestCase):
    def setUp(self):
        self.lang = Lang("files/fr.lang")

    def test_lang(self):
        self.assertEqual(self.lang.get_translate("accueil", "OUI"), "Bonjour")
        self.assertEqual(self.lang.get_translate("wut", "OUI"), "OUI")
        self.lang.file = "files/en.lang"
        self.assertEqual(self.lang.get_translate("accueil", "OUI"), "Hello")
        self.assertEqual(self.lang.get_translate("wut", "OUI"), "OUI")


class ConfigTests(unittest.TestCase):
    def setUp(self):
        self.config = Config("config.conf")

    def test_create(self):
        self.config.create({"rep": "oui"})
        self.assertEqual(self.config.get("rep"), "oui")
        self.assertIsNone(self.config.get("wut"))
        self.config.set("rep", "non")
        self.assertEqual(self.config.get("rep"), "non")
        self.config.save()
        self.config.file = "config.conf"
        self.assertEqual(self.config.get("rep"), "non")
        self.assertIsNone(self.config.get("wut"))
        os.remove("config.conf")

