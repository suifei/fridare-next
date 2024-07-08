import re
from collections import defaultdict
import os
import requests
import subprocess
from packaging import version
from .settings import Settings
from .utils import get_default_download_dir

class FridaPatcher:
    def __init__(self):
        self.settings = Settings()
        self.current_version = "0.1"
        self.github_api_url = "https://api.github.com/repos/frida/frida/releases"
        self.download_dir = get_default_download_dir()
        
    def get_frida_releases(self, page=1, per_page=10):
        try:
            url = f"{self.github_api_url}?page={page}&per_page={per_page}"
            proxies = self.get_proxy_settings()
            response = requests.get(url, proxies=proxies)
            response.raise_for_status()
            return response.json(), None
        except requests.RequestException as e:
            return None, str(e)
        
    def get_proxy_settings(self):
        proxy = self.settings.get_setting("proxy")
        if proxy["enabled"]:
            return {
                "http": f"{proxy['type']}://{proxy['ip']}:{proxy['port']}",
                "https": f"{proxy['type']}://{proxy['ip']}:{proxy['port']}"
            }
        return None
    def parse_filename(self, filename):
        pattern = re.compile(r'(?P<module_type>frida[-_]?[a-zA-Z0-9\-]+)?[-_](?P<version>v?\d+\.\d+\.\d+)[-_](?P<os>[a-zA-Z0-9\-]+)[-_](?P<arch>[a-zA-Z0-9_]+)')
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
            return (module_type, version, os, arch, ext)
        return None

    def get_os_modules(self, assets):
        # 按名称排序
        assets = sorted(assets, key=lambda x: x['name'])
        os_modules = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
        for asset in assets:
            parsed = self.parse_filename(asset['name'])
            if parsed:
                module_type, version, os, arch, ext = parsed
                os_modules[module_type][os][arch].append(asset)
        return os_modules
    
    def download_file(self, url, filename):
        full_path = os.path.join(self.download_dir, filename)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            with open(full_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return full_path
        except requests.RequestException:
            return None

    def patch_frida(self, filename):
        # 这里实现打补丁的逻辑
        # 这是一个示例实现，实际的补丁逻辑需要根据具体需求来开发
        try:
            # 解压文件
            uncompressed_file = filename[:-3]  # 移除 .xz 扩展名
            subprocess.run(['xz', '-d', filename], check=True)
            
            # 修改二进制（这里需要实现具体的修改逻辑）
            # 例如，你可以使用 subprocess 运行一些命令来修改文件
            # subprocess.run(['some_command', uncompressed_file], check=True)

            # 重新压缩
            subprocess.run(['xz', uncompressed_file], check=True)
            
            return True
        except subprocess.CalledProcessError:
            return False

    # ... 其他方法保持不变 ...

    # TODO: Add other methods as needed
    def check_for_updates(self):
        try:
            response = requests.get(self.github_api_url)
            response.raise_for_status()
            latest_release = response.json()
            latest_version = latest_release['tag_name'].lstrip('v')
            
            if version.parse(latest_version) > version.parse(self.current_version):
                return latest_version, latest_release['html_url']
            else:
                return None, None
        except requests.RequestException:
            return None, None