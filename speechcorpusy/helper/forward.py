"""Corpus archive file forwarding helpers"""


from pathlib import Path
from tempfile import NamedTemporaryFile

import fsspec

from speechcorpusy.components.download import download_gdrive_large_contents


def forward(source_adress: str, target_adress: str) -> None:
    """Forward the file at the source adress to the target adress with cache.

    Forward any_adress -> any_adress through fsspec (e.g. local, S3, GCP).
    Args:
        source_adress: The Forward origin adress.
        target_adrsss: Forward distination adress.
    """
    adress_cached_source = f"simplecache::{source_adress}"
    adress_cached_target = f"simplecache::{target_adress}"

    print("Forward: Reading from the adress...")
    with fsspec.open(adress_cached_source, "rb") as source:
        file = source.read()
    print("Forward: Read")

    print("Forward: Writing to the adress...")
    with fsspec.open(adress_cached_target, "wb") as target:
        target.write(file)
    print("Forward: Written")


def forward_from_gdrive(id_gdrive_contents: str, target_adress: str, size_gb: float) -> None:
    """Forward a file in Google Drive to specified adress.

    Forward GoogleDrive -> any_adress through fsspec (e.g. local, S3, GCP).

    Args:
        id_gdrive_contents: Google Drive contents ID
        target_adress: forward distination adress
        size_gb: File size [GB]
    """

    adress_cache_target = f"simplecache::{target_adress}"
    # TempFile for garbage-less forwarding
    with NamedTemporaryFile(delete=False) as tmp:
        temp_file_path = tmp.name
       
    download_gdrive_large_contents(id_gdrive_contents, Path(temp_file_path), size_gb)
    with open(temp_file_path, mode="rb") as tmp:
        tmp.seek(0)
        print("Forward: Writing to the adress...")
        with fsspec.open(adress_cache_target, "wb") as archive:
            archive.write(tmp.read())
        print("Forward: Written.")
    os.remove(temp_file_path)


if __name__ == "__main__":
    pass
