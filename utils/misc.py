from os import walk, path, sep, remove
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


def zip_it(zip_name, directory, ignore_extensions=['lock']):
    if path.exists(zip_name):
        remove(zip_name)

    src_path = Path(directory).expanduser().resolve(strict=True)
    with ZipFile(zip_name, 'w', ZIP_DEFLATED) as zf:
        files = [src_path] if src_path.is_file() else src_path.rglob('*')
        for file in files:
            if file.suffix[1:] not in ignore_extensions:
                zf.write(file, file.relative_to(src_path))
