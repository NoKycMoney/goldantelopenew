"""Offline regression checks; never connect to Telegram or start collectors."""
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image
import qrcode

ROOT = Path(__file__).resolve().parents[1]


def load_module(name, relative_path):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DependencyUpgradeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.collector = load_module("collector_under_test", "hf_baza_app.py")
        cls.finance = load_module("finance_under_test", "hf_finance_space/app.py")

    def test_collector_page_and_status(self):
        client = self.collector.app.test_client()
        page = client.get("/")
        self.assertEqual(page.status_code, 200)
        self.assertIn(b"TG Deep Collector", page.data)
        response = client.get("/status")
        self.assertEqual(response.json["status"], self.collector.get_st())
        self.assertEqual(response.json["log"], self.collector.get_log())
        self.assertEqual(response.headers["Cache-Control"], "no-store")

    def test_collector_start_requires_control_token(self):
        client = self.collector.app.test_client()
        with patch.object(self.collector, "start", return_value="started") as start:
            self.assertEqual(client.get("/start").status_code, 405)
            self.assertEqual(client.post("/start").status_code, 403)
            self.assertEqual(client.post("/start", headers={"X-Control-Token": "invalid"}).status_code, 403)
            start.assert_not_called()
            response = client.post("/start", headers={
                "X-Control-Token": self.collector._control_token,
            })
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {"message": "started"})
            start.assert_called_once_with()

    def test_collector_download_missing_and_available(self):
        client = self.collector.app.test_client()
        with tempfile.TemporaryDirectory() as directory:
            result = Path(directory) / "result.json"
            with patch.object(self.collector, "RESULT", str(result)):
                self.assertEqual(client.get("/download").status_code, 404)
                result.write_text('{"test": true}')
                response = client.get("/download")
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.json, {"test": True})
                self.assertIn("attachment", response.headers["Content-Disposition"])
                response.close()

    def test_finance_page_refresh_and_log(self):
        client = self.finance.app.test_client()
        page = client.get("/")
        self.assertEqual(page.status_code, 200)
        self.assertIn(b"setInterval(refresh, 10000)", page.data)
        with patch.object(self.finance, "STATUS_LOG", ["<script>untrusted</script>"]):
            response = client.get("/status")
            self.assertEqual(response.json["log"], "<script>untrusted</script>")
            self.assertEqual(response.headers["Cache-Control"], "no-store")
        # Log strings are assigned with textContent, never interpreted as HTML.
        self.assertIn(b'.textContent = (await response.json()).log', page.data)

    def test_pillow_resize_and_qrcode(self):
        image = Image.new("RGB", (20, 20), "white")
        image.thumbnail((10, 10))
        output = io.BytesIO()
        image.save(output, format="JPEG")
        output.seek(0)
        self.assertEqual(Image.open(output).size, (10, 10))
        qr = qrcode.make("offline-regression-check")
        output = io.BytesIO()
        qr.save(output, format="PNG")
        output.seek(0)
        self.assertEqual(Image.open(output).format, "PNG")


if __name__ == "__main__":
    unittest.main()
