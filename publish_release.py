#!/usr/bin/env python3
"""Publish one verified public APK; never build or copy application source."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener
import zipfile

ROOT = Path(__file__).resolve().parent
REPOSITORY = "kcmrshll9-ux/miles-by-kc-downloads"
RELEASE_ID = 445982208
TAG = "v0.1.2-test.3"
SOURCE = "3af18975a5e7c7e7c6081696f5735731cb29459d"
ARTIFACT_HOST = "sdmntprwestus3.oaiusercontent.com"
ZIP_SIZE = 88358066
ZIP_SHA = "fce1972fe4134c343264a5a8ea6a570f7e73ff672886ee21d23a9ba8d4f7da56"
APK_NAME = "Miles-by-KC-0.1.2-Android-test.apk"
APK_SIZE = 171656438
APK_SHA = "a5d3abc9ab6a1c31869de7c75424d86a99bb23644b81636f742d9cf7ed44cf9d"
PREVIEWS = {
    "Miles-by-KC-0.1.2-Trips-preview.png": (134819, "553b0b5527dfed084f5f30e86024986375b7bd000a440cef4b09ee3099953904"),
    "Miles-by-KC-0.1.2-GPS-review-preview.png": (149310, "ddc67fe2b6c4dd683c1ce3db9f51e3082bab9bdb03fee9ccaf8397fe2c1a0f42"),
}


class Refused(Exception):
    """Only fixed, URL-free messages are safe to expose in workflow logs."""


def mask(value: str) -> None:
    escaped = value.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
    print("::add-mask::" + escaped, flush=True)


def validate_url(value: str) -> str:
    try:
        parsed = urlsplit(value)
        valid = (value == value.strip() and 0 < len(value) <= 20000
                 and not any(ord(character) < 33 for character in value)
                 and parsed.scheme == "https" and parsed.hostname == ARTIFACT_HOST
                 and parsed.port in (None, 443) and parsed.username is None
                 and parsed.password is None and not parsed.fragment)
    except ValueError:
        valid = False
    if not valid:
        raise Refused("Artifact URL is not on the approved HTTPS host.")
    return value


def event_url() -> str:
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
    value = event.get("inputs", {}).get("artifact_url")
    if not isinstance(value, str):
        raise Refused("A signed artifact URL is required.")
    mask(value)  # Before validation or any request; never interpolate in shell.
    return validate_url(value)


class ApprovedRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        mask(newurl)
        validate_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def verified_copy(reader, target: Path, expected_size: int, expected_sha: str) -> None:
    digest, count = hashlib.sha256(), 0
    output = target.open("xb")
    try:
        with output:
            while chunk := reader.read(1024 * 1024):
                count += len(chunk)
                if count > expected_size:
                    raise Refused("Downloaded content exceeds the pinned size.")
                digest.update(chunk)
                output.write(chunk)
        if count != expected_size or digest.hexdigest() != expected_sha:
            raise Refused("Downloaded content does not match its pinned size and SHA-256.")
    except Exception:
        target.unlink(missing_ok=True)
        raise


def file_identity(path: Path) -> tuple[int, str]:
    digest, count = hashlib.sha256(), 0
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            count += len(chunk)
            digest.update(chunk)
    return count, digest.hexdigest()


def prepare_apk(url: str, work: Path) -> Path:
    archive = work / "verified-artifact.zip"
    opener = build_opener(ApprovedRedirects())
    try:
        with opener.open(Request(validate_url(url), headers={"Accept-Encoding": "identity"}), timeout=60) as response:
            verified_copy(response, archive, ZIP_SIZE, ZIP_SHA)
        with zipfile.ZipFile(archive) as bundle:
            files = [entry for entry in bundle.infolist() if not entry.is_dir()]
            if len(files) != 1 or not files[0].filename.lower().endswith(".apk"):
                raise Refused("The pinned artifact must contain exactly one APK and no other files.")
            if files[0].file_size != APK_SIZE:
                raise Refused("The archived APK has an unexpected size.")
            apk = work / APK_NAME
            # Read to our fixed filename; never extract an archive-provided path.
            with bundle.open(files[0]) as source:
                verified_copy(source, apk, APK_SIZE, APK_SHA)
            return apk
    except Refused:
        raise
    except Exception:
        raise Refused("Artifact download or ZIP validation failed; URL details are withheld.") from None


def gh(*arguments: str, body: dict | None = None) -> dict | None:
    command = ["gh", *arguments]
    if body is not None:
        command += ["--input", "-"]
    result = subprocess.run(command, input=json.dumps(body) if body is not None else None,
                            capture_output=True, text=True, timeout=600)
    if result.returncode:
        raise Refused("GitHub operation failed; remote error text is withheld.")
    return json.loads(result.stdout) if result.stdout.strip() and arguments[0] == "api" else None


def release() -> dict:
    value = gh("api", f"repos/{REPOSITORY}/releases/{RELEASE_ID}")
    if (not isinstance(value, dict) or value.get("id") != RELEASE_ID
            or value.get("tag_name") != TAG or value.get("prerelease") is not True
            or type(value.get("draft")) is not bool):
        raise Refused("Release identity, tag or prerelease status does not match.")
    return value


def verify_assets(value: dict, expected: dict[str, tuple[int, str]], *, complete: bool) -> set[str]:
    rows = value.get("assets")
    if not isinstance(rows, list):
        raise Refused("Release asset metadata is unavailable.")
    seen = set()
    for row in rows:
        name = row.get("name") if isinstance(row, dict) else None
        if name not in expected or name in seen:
            raise Refused("Unexpected or duplicate release asset; refusing publication.")
        size, sha = expected[name]
        if row.get("size") != size or row.get("digest") != "sha256:" + sha or row.get("state") != "uploaded":
            raise Refused("Existing asset differs or cannot be verified; it will not be overwritten.")
        seen.add(name)
    if complete and seen != set(expected):
        raise Refused("All four verified release assets are required before publication.")
    return seen


def publish(apk: Path, work: Path) -> None:
    notes = (ROOT / "release-notes.md").read_text()
    if SOURCE not in notes:
        raise Refused("Release notes do not identify the pinned application source.")
    files = {APK_NAME: apk}
    expected = {APK_NAME: (APK_SIZE, APK_SHA), **PREVIEWS}
    for name, identity in PREVIEWS.items():
        path = ROOT / name
        if file_identity(path) != identity:
            raise Refused("Preview image differs from the reviewed public image.")
        files[name] = path
    checksum_name = APK_NAME.removesuffix(".apk") + ".sha256"
    checksum = work / checksum_name
    checksum.write_text(f"{APK_SHA}  {APK_NAME}\n")
    files[checksum_name] = checksum
    expected[checksum_name] = file_identity(checksum)
    if file_identity(apk) != expected[APK_NAME]:
        raise Refused("The staged APK does not match the approved application.")
    current = release()
    existing = verify_assets(current, expected, complete=not current["draft"])
    if not current["draft"]:
        if current.get("body") != notes:
            raise Refused("Published release notes differ; refusing to edit an existing publication.")
        print("The release is already published with all four verified assets.")
        return
    for name, path in files.items():
        if name in existing:
            continue
        # No --clobber: an existing asset can never be replaced by this job.
        gh("release", "upload", TAG, str(path), "--repo", REPOSITORY)
        current = release()
        if not current["draft"]:
            raise Refused("Release changed during upload; refusing further edits.")
        verify_assets(current, expected, complete=False)
    current = release()
    if not current["draft"]:
        raise Refused("Release changed before the publication gate.")
    verify_assets(current, expected, complete=True)
    gh("api", "--method", "PATCH", f"repos/{REPOSITORY}/releases/{RELEASE_ID}",
       body={"body": notes, "draft": False, "prerelease": True})
    final = release()
    verify_assets(final, expected, complete=True)
    if final["draft"] or final.get("body") != notes:
        raise Refused("Publication response could not be verified.")
    print("Published the verified Android test release with all four public assets.")


def main() -> None:
    url = event_url()
    if (os.environ.get("GITHUB_ACTIONS") != "true"
            or os.environ.get("GITHUB_REPOSITORY") != REPOSITORY
            or not os.environ.get("GH_TOKEN")):
        raise Refused("Run this publisher only in the designated repository workflow.")
    with tempfile.TemporaryDirectory(prefix="verified-mileage-release-", dir=os.environ["RUNNER_TEMP"]) as directory:
        work = Path(directory)
        publish(prepare_apk(url, work), work)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        # Never print a traceback, subprocess output, request URL or token.
        print("Publication stopped: " + (str(error) if isinstance(error, Refused)
                                        else "unexpected failure; sensitive details withheld."), file=sys.stderr)
        sys.exit(1)
