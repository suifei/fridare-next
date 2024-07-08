import re

# 示例字符串
sample_data = """
frida-16.4.1-cp37-abi3-freebsd_14_0_release_amd64.whl
frida-clr-16.4.1-windows-x86.dll.xz
frida-clr-16.4.1-windows-x86_64.dll.xz
frida-core-devkit-16.4.1-android-arm.tar.xz
frida-core-devkit-16.4.1-android-arm64.tar.xz
frida-core-devkit-16.4.1-android-x86.tar.xz
frida-core-devkit-16.4.1-android-x86_64.tar.xz
frida-core-devkit-16.4.1-freebsd-arm64.tar.xz
frida-core-devkit-16.4.1-freebsd-x86_64.tar.xz
frida-core-devkit-16.4.1-ios-arm64-simulator.tar.xz
frida-core-devkit-16.4.1-ios-arm64.tar.xz
frida-core-devkit-16.4.1-ios-arm64e.tar.xz
frida-core-devkit-16.4.1-ios-x86_64-simulator.tar.xz
frida-core-devkit-16.4.1-linux-arm64-musl.tar.xz
frida-core-devkit-16.4.1-linux-arm64.tar.xz
frida-core-devkit-16.4.1-linux-armhf.tar.xz
frida-core-devkit-16.4.1-linux-mips.tar.xz
frida-core-devkit-16.4.1-linux-mips64.tar.xz
frida-core-devkit-16.4.1-linux-mips64el.tar.xz
frida-core-devkit-16.4.1-linux-mipsel.tar.xz
frida-core-devkit-16.4.1-linux-x86.tar.xz
frida-core-devkit-16.4.1-linux-x86_64-musl.tar.xz
frida-core-devkit-16.4.1-linux-x86_64.tar.xz
frida-core-devkit-16.4.1-macos-arm64.tar.xz
frida-core-devkit-16.4.1-macos-arm64e.tar.xz
frida-core-devkit-16.4.1-macos-x86_64.tar.xz
frida-core-devkit-16.4.1-qnx-armeabi.tar.xz
frida-core-devkit-16.4.1-tvos-arm64-simulator.tar.xz
frida-core-devkit-16.4.1-tvos-arm64.tar.xz
frida-core-devkit-16.4.1-watchos-arm64-simulator.tar.xz
frida-core-devkit-16.4.1-watchos-arm64.tar.xz
frida-core-devkit-16.4.1-windows-x86.exe
frida-core-devkit-16.4.1-windows-x86.tar.xz
frida-core-devkit-16.4.1-windows-x86_64.exe
frida-core-devkit-16.4.1-windows-x86_64.tar.xz
frida-gadget-16.4.1-android-arm.so.xz
frida-gadget-16.4.1-android-arm64.so.xz
frida-gadget-16.4.1-android-x86.so.xz
frida-gadget-16.4.1-android-x86_64.so.xz
frida-gadget-16.4.1-freebsd-arm64.so.xz
frida-gadget-16.4.1-freebsd-x86_64.so.xz
frida-gadget-16.4.1-ios-simulator-universal.dylib.xz
frida-gadget-16.4.1-ios-universal.dylib.gz
frida-gadget-16.4.1-ios-universal.dylib.xz
frida-gadget-16.4.1-linux-arm64-musl.so.xz
frida-gadget-16.4.1-linux-arm64.so.xz
frida-gadget-16.4.1-linux-armhf.so.xz
frida-gadget-16.4.1-linux-mips.so.xz
frida-gadget-16.4.1-linux-mips64.so.xz
frida-gadget-16.4.1-linux-mips64el.so.xz
frida-gadget-16.4.1-linux-mipsel.so.xz
frida-gadget-16.4.1-linux-x86.so.xz
frida-gadget-16.4.1-linux-x86_64-musl.so.xz
frida-gadget-16.4.1-linux-x86_64.so.xz
frida-gadget-16.4.1-macos-universal.dylib.xz
frida-gadget-16.4.1-qnx-armeabi.so.xz
frida-gadget-16.4.1-tvos-arm64-simulator.dylib.xz
frida-gadget-16.4.1-tvos-arm64.dylib.xz
frida-gadget-16.4.1-watchos-arm64-simulator.dylib.xz
frida-gadget-16.4.1-watchos-arm64.dylib.xz
frida-gadget-16.4.1-windows-x86.dll.xz
frida-gadget-16.4.1-windows-x86_64.dll.xz
frida-gum-devkit-16.4.1-android-arm.tar.xz
frida-gum-devkit-16.4.1-android-arm64.tar.xz
frida-gum-devkit-16.4.1-android-x86.tar.xz
frida-gum-devkit-16.4.1-android-x86_64.tar.xz
frida-gum-devkit-16.4.1-freebsd-arm64.tar.xz
frida-gum-devkit-16.4.1-freebsd-x86_64.tar.xz
frida-gum-devkit-16.4.1-ios-arm64-simulator.tar.xz
frida-gum-devkit-16.4.1-ios-arm64.tar.xz
frida-gum-devkit-16.4.1-ios-arm64e.tar.xz
frida-gum-devkit-16.4.1-ios-x86_64-simulator.tar.xz
frida-gum-devkit-16.4.1-linux-arm64-musl.tar.xz
frida-gum-devkit-16.4.1-linux-arm64.tar.xz
frida-gum-devkit-16.4.1-linux-armhf.tar.xz
frida-gum-devkit-16.4.1-linux-mips.tar.xz
frida-gum-devkit-16.4.1-linux-mips64.tar.xz
frida-gum-devkit-16.4.1-linux-mips64el.tar.xz
frida-gum-devkit-16.4.1-linux-mipsel.tar.xz
frida-gum-devkit-16.4.1-linux-x86.tar.xz
frida-gum-devkit-16.4.1-linux-x86_64-musl.tar.xz
frida-gum-devkit-16.4.1-linux-x86_64.tar.xz
frida-gum-devkit-16.4.1-macos-arm64.tar.xz
frida-gum-devkit-16.4.1-macos-arm64e.tar.xz
frida-gum-devkit-16.4.1-macos-x86_64.tar.xz
frida-gum-devkit-16.4.1-qnx-armeabi.tar.xz
frida-gum-devkit-16.4.1-tvos-arm64-simulator.tar.xz
frida-gum-devkit-16.4.1-tvos-arm64.tar.xz
frida-gum-devkit-16.4.1-watchos-arm64-simulator.tar.xz
frida-gum-devkit-16.4.1-watchos-arm64.tar.xz
frida-gum-devkit-16.4.1-windows-x86.exe
frida-gum-devkit-16.4.1-windows-x86.tar.xz
frida-gum-devkit-16.4.1-windows-x86_64.exe
frida-gum-devkit-16.4.1-windows-x86_64.tar.xz
frida-gumjs-devkit-16.4.1-android-arm.tar.xz
frida-gumjs-devkit-16.4.1-android-arm64.tar.xz
frida-gumjs-devkit-16.4.1-android-x86.tar.xz
frida-gumjs-devkit-16.4.1-android-x86_64.tar.xz
frida-gumjs-devkit-16.4.1-freebsd-arm64.tar.xz
frida-gumjs-devkit-16.4.1-freebsd-x86_64.tar.xz
frida-gumjs-devkit-16.4.1-ios-arm64-simulator.tar.xz
frida-gumjs-devkit-16.4.1-ios-arm64.tar.xz
frida-gumjs-devkit-16.4.1-ios-arm64e.tar.xz
frida-gumjs-devkit-16.4.1-ios-x86_64-simulator.tar.xz
frida-gumjs-devkit-16.4.1-linux-arm64-musl.tar.xz
frida-gumjs-devkit-16.4.1-linux-arm64.tar.xz
frida-gumjs-devkit-16.4.1-linux-armhf.tar.xz
frida-gumjs-devkit-16.4.1-linux-mips.tar.xz
frida-gumjs-devkit-16.4.1-linux-mips64.tar.xz
frida-gumjs-devkit-16.4.1-linux-mips64el.tar.xz
frida-gumjs-devkit-16.4.1-linux-mipsel.tar.xz
frida-gumjs-devkit-16.4.1-linux-x86.tar.xz
frida-gumjs-devkit-16.4.1-linux-x86_64-musl.tar.xz
frida-gumjs-devkit-16.4.1-linux-x86_64.tar.xz
frida-gumjs-devkit-16.4.1-macos-arm64.tar.xz
frida-gumjs-devkit-16.4.1-macos-arm64e.tar.xz
frida-gumjs-devkit-16.4.1-macos-x86_64.tar.xz
frida-gumjs-devkit-16.4.1-qnx-armeabi.tar.xz
frida-gumjs-devkit-16.4.1-tvos-arm64-simulator.tar.xz
frida-gumjs-devkit-16.4.1-tvos-arm64.tar.xz
frida-gumjs-devkit-16.4.1-watchos-arm64-simulator.tar.xz
frida-gumjs-devkit-16.4.1-watchos-arm64.tar.xz
frida-gumjs-devkit-16.4.1-windows-x86.exe
frida-gumjs-devkit-16.4.1-windows-x86.tar.xz
frida-gumjs-devkit-16.4.1-windows-x86_64.exe
frida-gumjs-devkit-16.4.1-windows-x86_64.tar.xz
frida-inject-16.4.1-android-arm.xz
frida-inject-16.4.1-android-arm64.xz
frida-inject-16.4.1-android-x86.xz
frida-inject-16.4.1-android-x86_64.xz
frida-inject-16.4.1-freebsd-arm64.xz
frida-inject-16.4.1-freebsd-x86_64.xz
frida-inject-16.4.1-linux-arm64-musl.xz
frida-inject-16.4.1-linux-arm64.xz
frida-inject-16.4.1-linux-armhf.xz
frida-inject-16.4.1-linux-mips.xz
frida-inject-16.4.1-linux-mips64.xz
frida-inject-16.4.1-linux-mips64el.xz
frida-inject-16.4.1-linux-mipsel.xz
frida-inject-16.4.1-linux-x86.xz
frida-inject-16.4.1-linux-x86_64-musl.xz
frida-inject-16.4.1-linux-x86_64.xz
frida-inject-16.4.1-macos-arm64.xz
frida-inject-16.4.1-macos-arm64e.xz
frida-inject-16.4.1-macos-x86_64.xz
frida-inject-16.4.1-qnx-armeabi.xz
frida-inject-16.4.1-windows-x86.exe.xz
frida-inject-16.4.1-windows-x86_64.exe.xz
frida-portal-16.4.1-android-arm.xz
frida-portal-16.4.1-android-arm64.xz
frida-portal-16.4.1-android-x86.xz
frida-portal-16.4.1-android-x86_64.xz
frida-portal-16.4.1-freebsd-arm64.xz
frida-portal-16.4.1-freebsd-x86_64.xz
frida-portal-16.4.1-ios-arm64.xz
frida-portal-16.4.1-ios-arm64e.xz
frida-portal-16.4.1-linux-arm64-musl.xz
frida-portal-16.4.1-linux-arm64.xz
frida-portal-16.4.1-linux-armhf.xz
frida-portal-16.4.1-linux-mips.xz
frida-portal-16.4.1-linux-mips64.xz
frida-portal-16.4.1-linux-mips64el.xz
frida-portal-16.4.1-linux-mipsel.xz
frida-portal-16.4.1-linux-x86.xz
frida-portal-16.4.1-linux-x86_64-musl.xz
frida-portal-16.4.1-linux-x86_64.xz
frida-portal-16.4.1-macos-arm64.xz
frida-portal-16.4.1-macos-arm64e.xz
frida-portal-16.4.1-macos-x86_64.xz
frida-portal-16.4.1-qnx-armeabi.xz
frida-portal-16.4.1-windows-x86.exe.xz
frida-portal-16.4.1-windows-x86_64.exe.xz
frida-qml-16.4.1-linux-x86_64.tar.xz
frida-qml-16.4.1-macos-x86_64.tar.xz
frida-qml-16.4.1-windows-x86_64.tar.xz
frida-server-16.4.1-android-arm.xz
frida-server-16.4.1-android-arm64.xz
frida-server-16.4.1-android-x86.xz
frida-server-16.4.1-android-x86_64.xz
frida-server-16.4.1-freebsd-arm64.xz
frida-server-16.4.1-freebsd-x86_64.xz
frida-server-16.4.1-linux-arm64-musl.xz
frida-server-16.4.1-linux-arm64.xz
frida-server-16.4.1-linux-armhf.xz
frida-server-16.4.1-linux-mips.xz
frida-server-16.4.1-linux-mips64.xz
frida-server-16.4.1-linux-mips64el.xz
frida-server-16.4.1-linux-mipsel.xz
frida-server-16.4.1-linux-x86.xz
frida-server-16.4.1-linux-x86_64-musl.xz
frida-server-16.4.1-linux-x86_64.xz
frida-server-16.4.1-macos-arm64.xz
frida-server-16.4.1-macos-arm64e.xz
frida-server-16.4.1-macos-x86_64.xz
frida-server-16.4.1-qnx-armeabi.xz
frida-server-16.4.1-windows-x86.exe.xz
frida-server-16.4.1-windows-x86_64.exe.xz
frida-v16.4.1-electron-v123-freebsd-arm64.tar.gz
frida-v16.4.1-electron-v123-freebsd-x64.tar.gz
frida-v16.4.1-electron-v125-darwin-arm64.tar.gz
frida-v16.4.1-electron-v125-darwin-x64.tar.gz
frida-v16.4.1-electron-v125-linux-arm64.tar.gz
frida-v16.4.1-electron-v125-linux-x64.tar.gz
frida-v16.4.1-electron-v125-win32-x64.tar.gz
frida-v16.4.1-node-v108-darwin-arm64.tar.gz
frida-v16.4.1-node-v108-darwin-x64.tar.gz
frida-v16.4.1-node-v108-linux-arm64.tar.gz
frida-v16.4.1-node-v108-linux-armv7l.tar.gz
frida-v16.4.1-node-v108-linux-ia32.tar.gz
frida-v16.4.1-node-v108-linux-x64.tar.gz
frida-v16.4.1-node-v108-win32-x64.tar.gz
frida-v16.4.1-node-v115-darwin-arm64.tar.gz
frida-v16.4.1-node-v115-darwin-x64.tar.gz
frida-v16.4.1-node-v115-freebsd-arm64.tar.gz
frida-v16.4.1-node-v115-freebsd-x64.tar.gz
frida-v16.4.1-node-v115-linux-arm64.tar.gz
frida-v16.4.1-node-v115-linux-armv7l.tar.gz
frida-v16.4.1-node-v115-linux-ia32.tar.gz
frida-v16.4.1-node-v115-linux-x64.tar.gz
frida-v16.4.1-node-v115-win32-x64.tar.gz
frida-v16.4.1-node-v127-darwin-arm64.tar.gz
frida-v16.4.1-node-v127-darwin-x64.tar.gz
frida-v16.4.1-node-v127-linux-arm64.tar.gz
frida-v16.4.1-node-v127-linux-armv7l.tar.gz
frida-v16.4.1-node-v127-linux-ia32.tar.gz
frida-v16.4.1-node-v127-linux-x64.tar.gz
frida-v16.4.1-node-v127-win32-x64.tar.gz
frida-v16.4.1-node-v93-darwin-arm64.tar.gz
frida-v16.4.1-node-v93-darwin-x64.tar.gz
frida-v16.4.1-node-v93-linux-arm64.tar.gz
frida-v16.4.1-node-v93-linux-armv7l.tar.gz
frida-v16.4.1-node-v93-linux-ia32.tar.gz
frida-v16.4.1-node-v93-linux-x64.tar.gz
frida-v16.4.1-node-v93-win32-ia32.tar.gz
frida-v16.4.1-node-v93-win32-x64.tar.gz
frida_16.4.1_appletvos-arm64.deb
frida_16.4.1_iphoneos-arm.deb
frida_16.4.1_iphoneos-arm64.deb
gum-graft-16.3.3-macos-arm64.xz
gum-graft-16.3.3-macos-x86_64.xz
"""
# 分行处理样本数据
lines = sample_data.strip().split('\n')

# 提取信息的正则表达式，考虑不同版本格式
# pattern = re.compile(r'(?P<module_type>frida[-_]?[a-zA-Z0-9\-]+)?[-_](?P<version>v?\d+\.\d+\.\d+)[-_](?P<os>[a-zA-Z0-9\-]+)[-_](?P<arch>[a-zA-Z0-9_]+)')

pattern = re.compile(r'(?P<module_type>frida[-_]?[a-zA-Z0-9\-]+)?[-_](?P<version>v?\d+\.\d+\.\d+)[-_](?P<os>[a-zA-Z0-9\-]+)[-_](?P<arch>[a-zA-Z0-9_]+)')


# 解析每一行并打印信息
for filename in lines:
    match = pattern.search(filename)
    if match:
        module_type = match.group('module_type') or 'N/A'
        version = match.group('version')
        os = match.group('os')
        arch = match.group('arch')
        if '.' in filename:
            ext = filename.split('.')[-1]
        else:
            ext = 'N/A'
        # 特殊处理
        # if module_type == 'N/A':
        #     if "cp37-abi3" in filename:
        #         module_type = "frida-python"
        #     elif "electron" in filename:
        #         module_type = "frida-electron"
        #     elif "node" in filename:
        #         module_type = "frida-" + filename.split('-')[3]
        #     elif "iphoneos" in filename or "appletvos" in filename:
        #         module_type = "frida-deb"

        if '64' == arch:
            arch = 'x86_64'
        elif '_' in arch:
            arch = arch.split('_')[-1]
        if os.startswith('cp') and '-' in os:
            os_info = os.split('-')
            os = os_info[-1]
            module_type = 'frida-python-' + os_info[0] + '-' + os_info[1]
        elif 'node-' in os:
            os_info = os.split('-')
            os = os_info[-1]
            module_type = 'frida-' + os_info[0] + '-' + os_info[1]
        elif 'electron-' in os:
            os_info = os.split('-')
            os = os_info[-1]
            module_type = 'frida-' + os_info[0] + '-' + os_info[1]
        elif '-' in os:
            os = os.split('-')[0]

        if 'N/A' == module_type and 'deb' in filename:
            module_type = 'frida-' + os + '-deb'
        elif 'N/A' == module_type and 'gum-graft' in filename:
            module_type = 'gum-graft'
            os = filename.split('-')[-2]
            arch = filename.split('-')[-1].split('.')[0]

        print(f"Module_type: {module_type}, Version: {version}, OS: {os}, Arch: {arch}, Filename: {filename}, Extension: {ext}")
    else:
        print(f"Filename: {filename}\nNo match found\n")