import sys
from pathlib import Path
import subprocess

def run(*args):
    arglist = [str(a) for a in args]
    print('+', *arglist)
    subprocess.check_call(arglist)

HEADER = """\
<!doctype html>
<meta charset="utf-8">
<style>
body { background: #222 }
.gallery li { list-style: none; float: left; width: 300px; height: 300px; margin: 5px }
.gallery a { display: block; text-align: center; height: 100% }
.gallery a:before { content: ""; display: inline-block; height: 100%; vertical-align: middle }
.gallery img { display: inline-block; max-width: 300px; max-height: 300px; outline: 1px solid #444; vertical-align: middle }
</style>
<body>
<ul class="gallery">
"""

IMG = """\
<li><a href="photos/{full.name}"><img src="photos/{thumb.name}"></a></li>
"""

FOOTER = """\
</ul>
"""

photos = Path('photos')
if not photos.exists():
    photos.mkdir()

with open('index.html', 'w') as index:
    index.write(HEADER)
    for name in sys.argv[1:]:
        orig = Path(name)
        full = photos / (orig.stem.lower() + orig.suffix.lower())
        thumb = photos / (orig.stem.lower() + '-thumb' + orig.suffix.lower())
        run('convert', orig, '-thumbnail', '600x600', '-auto-orient', thumb)
        run('convert', orig, '-resize', '2000x2000', '-auto-orient', full)
        index.write(IMG.format(full=full, thumb=thumb))
    index.write(FOOTER)
