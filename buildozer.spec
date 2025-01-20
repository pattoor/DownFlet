[app]
title = AllDownloader
package.name = alldownloader
package.domain = org.example
source.dir = src
source.include_exts = py
version = 0.1
requirements = python3, flet, yt-dlp, requests, pillow
orientation = portrait
android.permissions = INTERNET
android.sdk = 33
android.ndk = 25b
android.api = 33
android.platform = android-33  # en buildozer.spec, en la parte de android
android.build_tools_version = 33.0.2  # Esta versión debería ser compatible

[buildozer]
log_level = 2
