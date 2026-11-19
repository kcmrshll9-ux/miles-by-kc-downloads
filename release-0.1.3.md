# Miles by KC 0.1.3 for Android

[Download the Android test APK](https://github.com/kcmrshll9-ux/miles-by-kc-downloads/releases/download/v0.1.3-test.4/Miles-by-KC-0.1.3-Android-test.apk)

This update fixes repeated GPS gap alerts during a drive. When an isolated location spike is followed promptly by a good reading, the recorder discards the spike and continues measuring from the last trusted location. A sustained GPS outage still creates a review interval. The change applies to new recordings.

In the regression test, 117 isolated spikes produced zero gap alerts and preserved the expected route distance. All 85 app tests passed. The Android emulator passed recording and process recovery. Road performance still needs testing on a physical phone.

**Installing the test build.** Download and open the APK on Android 8 or newer. If Android reports a signing conflict, remove the older Miles by KC Test build before installing. Uninstalling clears its local records. To keep trips, end the active shift and save a full JSON backup from Reports first. With disposable test data you can start fresh.

Version 0.1.3, build 4. Package `com.kcmrshll9.milesbykc.dev`. Android test source `38e8d82f122f0f9e92296d10490aa289c21af2da`, private build run `44590502939`.
