import hashlib
import io
import json
from contextlib import redirect_stdout
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import publish_release as publisher


class PublisherTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def test_copy_rejects_wrong_size_and_hash_without_leaving_output(self):
        expected = hashlib.sha256(b"approved").hexdigest()
        for data, size in ((b"short", 8), (b"toolong-content", 8), (b"tampered", 8)):
            with self.subTest(data=data):
                target = self.root / "download"
                with self.assertRaises(publisher.Refused):
                    publisher.verified_copy(io.BytesIO(data), target, size, expected)
                self.assertFalse(target.exists())
        target = self.root / "approved"
        publisher.verified_copy(io.BytesIO(b"approved"), target, 8, expected)
        self.assertEqual(target.read_bytes(), b"approved")

    def test_signed_url_is_masked_before_validation_and_wrong_host_refused(self):
        url = "https://unapproved.invalid/file?signature=do-not-log"
        event = self.root / "event.json"
        event.write_text(json.dumps({"inputs": {"artifact_url": url}}))
        with patch.dict(publisher.os.environ, {"GITHUB_EVENT_PATH": str(event)}), \
                patch.object(publisher, "mask") as mask:
            with self.assertRaises(publisher.Refused) as refused:
                publisher.event_url()
        mask.assert_called_once_with(url)
        self.assertNotIn(url, str(refused.exception))
        self.assertEqual(publisher.validate_url("https://" + publisher.ARTIFACT_HOST + "/file?signature=opaque"),
                         "https://" + publisher.ARTIFACT_HOST + "/file?signature=opaque")
        for bad in ("http://" + publisher.ARTIFACT_HOST + "/file",
                    "https://user@" + publisher.ARTIFACT_HOST + "/file",
                    "https://" + publisher.ARTIFACT_HOST + ".attacker.invalid/file"):
            with self.assertRaises(publisher.Refused):
                publisher.validate_url(bad)

    def test_publication_gate_refuses_missing_mismatched_and_duplicate_assets(self):
        expected = {"approved.apk": (8, "a" * 64)}
        valid = {"name": "approved.apk", "size": 8, "digest": "sha256:" + "a" * 64, "state": "uploaded"}
        for assets in ([], [{**valid, "size": 9}], [{**valid, "digest": None}],
                       [{**valid, "state": "new"}], [valid, valid], [{**valid, "name": "unknown.zip"}]):
            with self.subTest(assets=assets), self.assertRaises(publisher.Refused):
                publisher.verify_assets({"assets": assets}, expected, complete=True)
        self.assertEqual(publisher.verify_assets({"assets": [valid]}, expected, complete=True), {"approved.apk"})

    def staged_files(self):
        apk = self.root / publisher.APK_NAME
        apk.write_bytes(b"synthetic approved APK")
        sha = hashlib.sha256(apk.read_bytes()).hexdigest()
        previews = {}
        for name in publisher.PREVIEWS:
            path = self.root / name
            path.write_bytes(b"synthetic preview " + name.encode())
            previews[name] = publisher.file_identity(path)
        (self.root / "release-notes.md").write_text("Reviewed source " + publisher.SOURCE)
        return apk, sha, previews

    def test_successful_upload_commands_cannot_bypass_missing_asset_gate(self):
        apk, sha, previews = self.staged_files()
        draft = {"id": publisher.RELEASE_ID, "tag_name": publisher.TAG, "draft": True,
                 "prerelease": True, "assets": []}
        calls = []
        def fake_gh(*args, **kwargs):
            calls.append((args, kwargs))
            return draft if args[0] == "api" else None
        with patch.multiple(publisher, ROOT=self.root, APK_SIZE=apk.stat().st_size, APK_SHA=sha, PREVIEWS=previews), \
                patch.object(publisher, "gh", side_effect=fake_gh), redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(publisher.Refused, "All four verified"):
                publisher.publish(apk, self.root)
        self.assertEqual(sum(args[:2] == ("release", "upload") for args, _ in calls), 4)
        self.assertFalse(any("PATCH" in args for args, _ in calls))
        self.assertFalse(any("--clobber" in args for args, _ in calls))

    def test_all_four_verified_assets_are_required_before_patch_and_rerun_is_read_only(self):
        apk, sha, previews = self.staged_files()
        state = {"id": publisher.RELEASE_ID, "tag_name": publisher.TAG, "draft": True,
                 "prerelease": True, "assets": []}
        calls = []
        def fake_gh(*args, body=None):
            calls.append(args)
            if args[:2] == ("release", "upload"):
                path = Path(args[3])
                size, digest = publisher.file_identity(path)
                state["assets"].append({"name": path.name, "size": size,
                                        "digest": "sha256:" + digest, "state": "uploaded"})
            if "PATCH" in args:
                self.assertEqual(len(state["assets"]), 4)
                state.update(body)
            return state.copy() if args[0] == "api" else None
        with patch.multiple(publisher, ROOT=self.root, APK_SIZE=apk.stat().st_size, APK_SHA=sha, PREVIEWS=previews), \
                patch.object(publisher, "gh", side_effect=fake_gh), redirect_stdout(io.StringIO()):
            publisher.publish(apk, self.root)
            self.assertFalse(state["draft"])
            self.assertEqual(sum("PATCH" in args for args in calls), 1)
            calls.clear()
            publisher.publish(apk, self.root)
        self.assertTrue(calls)
        self.assertTrue(all(args[0] == "api" and "PATCH" not in args for args in calls))


if __name__ == "__main__":
    unittest.main()
