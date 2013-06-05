from distutils.core import setup, Command
import distutils.command.install
from subprocess import call

class NewInstall(distutils.command.install.install):
    def run(self):
        distutils.command.install.install.run(self)
        call(['/usr/bin/open', 
            'download_subtitles/Download Subtitles.workflow'])

setup(
    name='DownloadSubtitles',
    version='0.1',
    author='Humberto Henrique Campos Pinheiro',
    author_email='humbhenri@gmail.com',
    url='http://www.example.com',
    license='LICENSE.txt',
    description='Download subtitles by righ-clicking on file.',
    scripts=[
        'download_subtitles/download_subtitles.py'
    ],
    cmdclass={
        'install': NewInstall,
    },

)
