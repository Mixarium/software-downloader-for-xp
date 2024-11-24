# software-downloader-for-xp
CLI tool that downloads software selected by the user, meant for Windows XP. Kind of like Ninite, except it doesn't automate the installation process.

# Compatibility
The program is compatible with Windows XP SP2 and above. Executable compiled using Pyinstaller and [Python 3.8.13, backported by cmalex](https://msfn.org/board/topic/183741-python-3813-for-windows-xp-sp3/), on [Windows XP Integral Edition](https://zone94.com/downloads/software/operating-systems/123-windows-xp-professional-sp3-x86-integral-edition).

# Compilation using pyinstaller

1. Download the [backported Python 3.8.13](https://www.4shared.com/web/directDownload/zN8_zoZofa/B8-gUmU2.bf85e3d1f4f32d78302b2ecc40144306) and follow its instructions, including how to install pip.
2. Install the packages mentioned in the requirements.txt file from this github repository. (pip install -r requirements.txt), as well as pyinstaller (pip install pyinstaller==4.10).

3. Run the following command, ensuring that sdfWinXP.py is present (PYTHONDIR is the directory to the python interpreter):
```
pyinstaller --onefile --noupx --add-data "C:\Python38\Lib\site-packages\ansicon\ANSI32.dll;." --copy-metadata readchar sdfWinXP.py --icon sdfWinXP_icon.ico
```
The executable should be saved in a 'dist' folder, created by pyinstaller.
