## Download Android test version 0.1.2

**[Download Miles by KC Test for Android](https://github.com/kcmrshll9-ux/miles-by-kc-downloads/releases/download/v0.1.2-test.3/Miles-by-KC-0.1.2-Android-test.apk)** — 171.7 MB, Android 8.0 or newer. No GitHub account is required.

This update fixes the Trips screen filling with repeated GPS-review buttons. Miles by KC is the same project previously called Uber Miles.

## Back up before reinstalling

**This installer uses a different test signing key from 0.1.1. Save your records before uninstalling the old app.**

1. While parked, use **End shift** if a shift is active.
2. Open **Reports → Protect your records → Export full backup**. Use the share sheet to save the JSON outside the app. **Confirm the saved file is accessible before continuing.** Opening or dismissing the share sheet alone does not save it.
3. Uninstall the older **Miles by KC Test**, open the downloaded APK and install version 0.1.2. If Android asks, allow installation from the browser or file manager you used.
4. Open **Reports → Import a backup → Choose backup**, select the saved JSON, check the **Backup merged** result and inspect your trips. If conflicts are reported, review them; existing records are retained.

Uninstalling erases local app records. PDF and CSV reports are not full backups. **If export fails or you cannot find the saved JSON, keep the existing app installed.**

## What changed

- Trips now shows one counted GPS-review summary instead of hundreds of identical buttons.
- View GPS gaps groups warnings by trip, with local times, reasons and five intervals at a time.
- Rejected GPS jumps no longer replace the last trusted location. Overlapping warnings from one continuing loss of reliable GPS are combined; later separate outages remain separate.
- Delayed GPS events cannot reset newer recovered locations or move an interruption boundary backward.
- Opening the update preserves existing warnings and mileage. Any subsequent consolidation retains the original warning details in the audit history.
- Small-phone review dialogs remain usable at 320px with 200% text.
- Buy Me a Coffee remains near the top of Settings.

The support button opens [KC’s Buy Me a Coffee page](https://buymeacoffee.com/run4ourfun). Contributions remain optional.

## Reviewing old warnings

Existing warnings stay available after restoring your backup. Opening or paging the review screen does not dismiss them or recalculate mileage.

To resolve all open gaps for a trip whose entire distance you have independently verified, use **Trips → Review or edit**, or **View GPS gaps → Show intervals → Review affected trip**. Complete the trip details, enable **Correct the total miles**, enter the full distance in **Verified total for this trip (mi)** and explain the evidence in **Correction reason / supporting record**. Check **I verified this trip**, then select **Save review**.

If 60 miles were recorded and the verified full-trip total is 75 miles, enter **75**. Entering 15 would replace the total with 15. Do not guess mileage to clear warnings. Trips crossing a tax-year or mileage-rate boundary require separately verified dated records as prompted in the app.

## Verification

| Check | Result |
| --- | --- |
| Flutter analysis | Passed |
| Flutter data and phone user flows | 83 passed |
| Direct-download support link | 3 passed |
| Python regression suite | 52 passed |
| JavaScript regression suite | 14 passed |
| Android APK and store-format bundle | Built successfully |
| Android native capture and process recovery | Both passed |
| iPhone simulator and unsigned device builds | Built successfully |
| iPhone native capture and process recovery | Both passed |

The new data regressions failed against the old implementation and passed with the fix. Verification includes preserving and restoring 500 historical warning records, a screen with 200 warnings, and review dialogs at 320px width with 200% text.

Build evidence: [native workflow](https://github.com/kcmrshll9-ux/uber-miles/actions/runs/43676518775) · [regression workflow](https://github.com/kcmrshll9-ux/uber-miles/actions/runs/43676518782). The development repository is private.

An earlier 0.1.2 candidate timed out waiting for its first fresh Android GPS fix. This diagnostic follow-up passed the same real native capture and recovery assertions without a further production recording-code change. The earlier timeout’s cause remains unconfirmed; it was not omitted or treated as a pass.

## Build identity

- Application version: **0.1.2-test**, package `com.kcmrshll9.milesbykc.dev`.
- Source revision: `3af18975a5e7c7e7c6081696f5735731cb29459d`.
- CI checkout: `c700ffc7abaf1977ddc93e4907a6bbc6ced61424`; its source tree matches the revision above.
- APK size: **171656438 bytes**.
- APK SHA-256:

```text
a5d3abc9ab6a1c31869de7c75424d86a99bb23644b81636f742d9cf7ed44cf9d
```

[Checksum file](https://github.com/kcmrshll9-ux/miles-by-kc-downloads/releases/download/v0.1.2-test.3/Miles-by-KC-0.1.2-Android-test.sha256)

## Screen previews

These use synthetic sample records, not a user’s trip history.

- [Trips with 200 saved warnings](https://github.com/kcmrshll9-ux/miles-by-kc-downloads/releases/download/v0.1.2-test.3/Miles-by-KC-0.1.2-Trips-preview.png)
- [Grouped GPS interval review](https://github.com/kcmrshll9-ux/miles-by-kc-downloads/releases/download/v0.1.2-test.3/Miles-by-KC-0.1.2-GPS-review-preview.png)

## Test-build limits

This is a debug-signed Android test build, not a Google Play release. Physical-phone GPS accuracy, locked-screen recording and battery behavior still need hands-on acceptance. The unsigned iPhone build is not an installable TestFlight release. Full JSON backups retain their 100 MiB / 500,000 capture-record limits.

The APK is for Android only. Google Play distribution, production signing and signed iPhone installation remain separate release steps. GitHub’s generated “Source code” archives contain this downloads repository, not the private application repository.
