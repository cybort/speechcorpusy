"""Corpus download handlers"""


from pathlib import Path
from typing import Optional

from tqdm import tqdm
import requests
import re
import os


def download_gdrive_large_contents(
    item_id: str,
    path_archive_local: Path,
    total_size_gb: float
) -> None:
    """Download large contents in Google Drive.

    Large contents in Google Drive needs special handling for virus check procedure.
    This utility wrap the procedure.

    Args:
        id: Google Drive contents ID.
        path_archive_local: Contents will be saved in this path.
        total_size_GB: Estimated contents size specified by yourself (hacky way).
    """
    path_archive_local.parent.mkdir(parents=True, exist_ok=True)
    #print(path_archive_local)
    has_write_permission = os.access(path_archive_local, os.W_OK)
    if not has_write_permission:
        raise PermissionError("no permission.")

    # Request cookies for big file download.
    url_for_cookies = f"https://drive.google.com/uc?export=download&id={item_id}"
    #print(url_for_cookies)
    res_dl = requests.get(url_for_cookies)
    code: Optional[str] = None
    #for cookie in res_dl.cookies:
    #    if "download_warning" in cookie.name:
    #        code = cookie.value
    code = re.search('confirm=([0-9A-Za-z_]+)', res_dl.text)
    if code is None:
        raise RuntimeError("download code is `None`. Please make issue in GitHub.")
    code = code.group(1)
    # Request corpus with cookies.
    url = f"{url_for_cookies}&confirm={code}"
    # Auto content-length acquisition do not work in GDrive.
    # file_size = int(requests.head(url, cookies=r.cookies).headers["content-length"])
    file_size = int(total_size_gb*1000*1000*1000)
    #res = requests.get(url, cookies=res_dl.cookies, stream=True)
    cookies_dict = requests.utils.dict_from_cookiejar(res_dl.cookies)
    res = requests.get(url, cookies=cookies_dict, stream=True)
    pbar = tqdm(total=file_size, unit="B", unit_scale=True)
    with open(path_archive_local, mode="wb") as file:
        for chunk in res.iter_content(chunk_size=1024):
            file.write(chunk)
            pbar.update(len(chunk))
        pbar.close()


if __name__ == "__main__":
    download_gdrive_large_contents(
        "1NyiZCXkYTdYBNtD1B-IMAYCVa-0SQsKX",
        Path("./jsss_auto.zip"),
        1.09
    )
