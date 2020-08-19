import tempfile
import shutil

from pathlib import Path

from sync import sync

def test_when_file_exists_in_source_but_not_in_destination():
    try:
        source = tempfile.mkdtemp()
        dest = tempfile.mkdtemp()

        content = 'I am a very useful file'
        (Path(source) / 'my-file').write_text(content)

        sync(source, dest)

        expected_path = Path(dest) / 'my-file'

        assert expected_path.exists()
        assert expected_path.read_text() == content
    finally:
        shutil.rmtree(source)
        shutil.rmtree(dest)


def test_when_file_renamed_in_source():
    try:
        source = tempfile.mkdtemp()
        dest = tempfile.mkdtemp()

        content = 'I am a file that was renamed'

        source_path = Path(source) / 'source-filename'
        dest_path = Path(dest) / 'dest-filename'

        expected_path = Path(dest) / 'source-filename'

        source_path.write_text(content)
        dest_path.write_text(content)

        sync(source, dest)

        assert dest_path.exists() is False
        assert expected_path.read_text() == content
    finally:
        shutil.rmtree(source)
        shutil.rmtree(dest)
