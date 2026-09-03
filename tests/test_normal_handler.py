import contextlib
import io
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

from dmconvert.convert import convert_xml_to_ass


class NormalDanmakuTests(unittest.TestCase):
    def convert(self, items, height=76, font_size=38, displayarea=1.0):
        root = ET.Element("i")
        for time, kind, text in items:
            ET.SubElement(root, "d", p="{},{},25,16777215".format(time, kind)).text = text
        with tempfile.TemporaryDirectory() as directory:
            xml_path = str(Path(directory) / "input.xml")
            ass_path = str(Path(directory) / "output.ass")
            ET.ElementTree(root).write(xml_path, encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                convert_xml_to_ass(
                    "Arial", font_size, 38, 1920, height, displayarea,
                    12, 5, 0.8, 0, 1.0, 0.0, xml_path, ass_path,
                )
            return [
                line for line in Path(ass_path).read_text(encoding="utf-8").splitlines()
                if line.startswith(("Dialogue:", "Comment:"))
            ]

    def test_unsorted_input_matches_chronological_input(self):
        for kind in (1, 4, 5):
            with self.subTest(kind=kind):
                items = [(30, kind, "late"), (0, kind, "first"), (15, kind, "middle")]
                lines = self.convert(items)
                self.assertEqual(lines, self.convert(sorted(items)))
                self.assertTrue(all(line.startswith("Dialogue:") for line in lines))

    def test_equal_times_preserve_input_order(self):
        lines = self.convert([(1, 5, "first"), (1, 5, "second")])
        self.assertTrue(lines[0].endswith("first"))
        self.assertTrue(lines[1].endswith("second"))
        self.assertIn(r"\pos(960,1)", lines[0])
        self.assertIn(r"\pos(960,39)", lines[1])

    def test_full_tracks_do_not_reuse_effect(self):
        for kind in (1, 4, 5):
            with self.subTest(kind=kind):
                lines = self.convert([(0, kind, "first"), (0, kind, "overflow")], height=38)
                self.assertTrue(lines[0].startswith("Dialogue:"))
                self.assertTrue(lines[1].startswith("Comment:"))
                self.assertNotIn(r"\pos", lines[1])
                self.assertNotIn(r"\move", lines[1])

    def test_full_tracks_do_not_inherit_other_type_effect(self):
        lines = self.convert([(0, 1, "rolling"), (0, 5, "fixed"), (0, 1, "overflow")], height=38)
        self.assertTrue(lines[2].startswith("Comment:"))
        self.assertNotIn(r"\pos", lines[2])

    def test_outside_display_area_becomes_comment(self):
        lines = self.convert([(0, 5, "first"), (0, 5, "hidden")], displayarea=0.5)
        self.assertTrue(lines[0].startswith("Dialogue:"))
        self.assertTrue(lines[1].startswith("Comment:"))

    def test_first_hidden_danmaku_does_not_raise(self):
        lines = self.convert([(0, 1, "hidden")], displayarea=0)
        self.assertTrue(lines[0].startswith("Comment:"))

    def test_unsupported_types_are_skipped(self):
        lines = self.convert([(0, 7, "unsupported"), (1, 5, "fixed"), (2, 8, "unsupported")])
        self.assertEqual(len(lines), 1)
        self.assertTrue(lines[0].endswith("fixed"))

    def test_track_count_uses_custom_font_size(self):
        lines = self.convert([(0, 5, str(i)) for i in range(4)], height=76, font_size=19)
        self.assertTrue(all(line.startswith("Dialogue:") for line in lines))
        self.assertIn(r"\pos(960,58)", lines[-1])


if __name__ == "__main__":
    unittest.main()
