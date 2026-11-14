# Miles by KC

**Business mileage & trip records — Android test downloads**

Miles by KC is the renamed **Uber Miles** project. This repository is the public installer page for that same app. Development and its existing history remain in the private application repository.

## Install the Android test build

**[Download Miles by KC Test for Android](https://github.com/kcmrshll9-ux/miles-by-kc-downloads/releases/download/v0.1.1-test.2/Miles-by-KC-0.1.1-Android-test.apk)**

1. Open the download link on your Android phone.
2. Open the downloaded `Miles-by-KC-0.1.1-Android-test.apk` file.
3. If Android asks, allow installation from the browser or file manager you used, then tap **Install**.
4. Open **Miles by KC Test**. Manual trips work without location access; grant location and notifications when testing GPS recording.

Requires **Android 8.0 or newer**. The download is approximately **164 MiB**. No GitHub account or app account is required.

[Release notes and checksum](https://github.com/kcmrshll9-ux/miles-by-kc-downloads/releases/tag/v0.1.1-test.2)

## Buy Me a Coffee

Version **0.1.1** restores the missing button. Open **Settings** and tap the gold **Buy Me a Coffee** button just below the heading. It opens [KC's support page](https://buymeacoffee.com/run4ourfun) in the phone's browser. Contributions are optional; every mileage feature remains available without payment.

## Updating an earlier test build

**Save your trips first:** end any active shift, open **Reports → Export full backup**, and save the JSON file outside the app. This 0.1.1 installer uses a different test signing key from 0.1.0. To update 0.1.0, uninstall the older **Miles by KC Test** only after saving your backup, install this version, then use **Reports → Import a backup**. Uninstalling erases local app records; a PDF or CSV is not a full backup.

## What to test

- Start and end a shift while parked, review the trip and add its purpose and places.
- Add a manual trip from actual vehicle odometer readings.
- Correct a record, review classifications and try Undo after deleting a test trip.
- Export a PDF/CSV report and a JSON backup; restore the backup and check the records.

This is a debug-signed prerelease for hands-on testing. It has passed the published automated suites and Android compilation; real-phone road accuracy, locked-screen recording and battery behavior still need testing. Keep independent vehicle records and export a JSON backup before changing builds. Current full JSON archives are limited to 100 MiB / 500,000 captured records.

Google Play distribution and signed iPhone installation are still being prepared. This Android APK cannot be installed on an iPhone.

## Privacy and ownership

The app stores its mileage records on the device. This public repository contains installers and release information. GitHub's automatically generated **Source code** archives contain this download repository's files, not the private application source.

Original application copyright © 2026 KC. Third-party components retain their own licenses, available in the app's Settings. Miles by KC is independent and is not affiliated with Uber or the IRS.
