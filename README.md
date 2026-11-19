# Miles by KC

**[Download Miles by KC Test 0.1.3 for Android](https://github.com/kcmrshll9-ux/miles-by-kc-downloads/releases/download/v0.1.3-test.4/Miles-by-KC-0.1.3-Android-test.apk)**

Miles by KC records business mileage and trips. This public installer is the Android test version of the app originally named Uber Miles. It requires Android 8.0 or newer and opens directly on your phone without a GitHub account.

## What changed in 0.1.3

An isolated GPS jump used to leave a warning even when a good reading followed immediately. The recorder now skips that spike and continues from the last trusted location. A sustained outage still appears under **Trips → View GPS gaps**. The new behavior applies to new drives.

The Android tests replayed a route with 117 isolated spikes. It finished with zero gap alerts and the expected distance. A separate test with sustained conflicting positions produced one review interval.

## Install the test build

1. Open the download link above on your Android phone.
2. Open `Miles-by-KC-0.1.3-Android-test.apk` and tap **Install**.
3. If Android reports a signing conflict, remove the older **Miles by KC Test** build and install again. Removing the app erases its local records. To keep trips, end the active shift and save a full JSON backup from **Reports → Export full backup** before removing it.
4. Open **Miles by KC Test**. To restore saved trips, use **Reports → Import a backup → Choose backup**.

[Release notes and SHA-256 checksum](https://github.com/kcmrshll9-ux/miles-by-kc-downloads/releases/tag/v0.1.3-test.4) · [Verified public download](https://github.com/kcmrshll9-ux/miles-by-kc-downloads/actions/runs/44605033854)

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
