# Miles by KC

**Business mileage & trip records — Android test downloads**

Miles by KC is the renamed **Uber Miles** project. This is the public installer page for that same app; development and its history remain in the private application repository.

## Before updating an earlier test build

**Save your trips first.** End any active shift, open **Reports → Export full backup**, and save the JSON file outside the app through the share sheet. Confirm the file is actually saved and accessible before uninstalling. These early test installers use temporary signing keys. The 0.1.2 installer uses a different signing key from 0.1.1 and requires removing the earlier test build before installation.

Uninstall the older **Miles by KC Test** only after the JSON backup is saved. Uninstalling erases local app records. After installing 0.1.2, use **Reports → Import a backup → Choose backup** to restore the saved file. Check the **Backup merged** result and your trips. A PDF or CSV is a report, not a full backup. If exporting fails, keep the existing app installed.

## Install version 0.1.2

**[Download Miles by KC Test 0.1.2 for Android](https://github.com/kcmrshll9-ux/miles-by-kc-downloads/releases/download/v0.1.2-test.3/Miles-by-KC-0.1.2-Android-test.apk)**

1. Open the download link on your Android phone.
2. Open the downloaded `Miles-by-KC-0.1.2-Android-test.apk`.
3. If Android asks, allow installation from the browser or file manager you used, then tap **Install**.
4. Open **Miles by KC Test** and restore your JSON backup if updating.

Requires **Android 8.0 or newer**. No GitHub account or app account is required.

[Release notes, checksums and screen previews](https://github.com/kcmrshll9-ux/miles-by-kc-downloads/releases/tag/v0.1.2-test.3)

[Verified publication results](https://github.com/kcmrshll9-ux/miles-by-kc-downloads/actions/runs/43714022325). The public APK has been checked without a GitHub login; its bytes match the tested build.

## GPS warnings are easier to review

Version **0.1.2** fixes the crowded Trips screen. One counted summary leads to **View GPS gaps**, where warnings are grouped by trip and paged with their individual local times and reasons.

The update also corrects rejected-location and delayed-event handling that could generate extra warnings or disturb a recovered location. Existing warnings and recorded mileage are not rewritten merely by opening the updated app. If continued capture combines overlapping warnings, their original details remain in the audit history. Reviewing the list does not automatically dismiss warnings or invent missing miles.

## Buy Me a Coffee

Open **Settings** and tap the gold **Buy Me a Coffee** button just below the heading. It opens [KC's support page](https://buymeacoffee.com/run4ourfun) in the phone's browser. Contributions are optional; every mileage feature remains available without payment.

## What to test on your phone

- Open Trips with your restored history; confirm the GPS summary keeps actual trips easy to reach.
- Open **View GPS gaps** and check individual times/reasons against your records.
- Start and end a shift while parked, review the completed trip and compare its total with independent vehicle records.
- Check PDF/CSV reports and a full JSON backup.

This is a debug-signed prerelease for hands-on testing. Its exact source revision and automated results are recorded in the release notes. Physical-phone road accuracy, locked-screen recording and battery behavior still need acceptance. Current full JSON archives are limited to 100 MiB / 500,000 captured records.

Google Play distribution and signed iPhone installation are still being prepared. This Android APK cannot be installed on an iPhone.

## Privacy and ownership

The app stores its mileage records on the device. This public repository contains installers and release information. GitHub's automatically generated **Source code** archives contain this download repository's files, not the private application source.

Original application copyright © 2026 KC. Third-party components retain their own licenses, available in the app's Settings. Miles by KC is independent and is not affiliated with Uber or the IRS.
