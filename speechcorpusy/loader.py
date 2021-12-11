"""Corpus Loaders"""

from typing import Optional

from speechcorpusy.interface import AbstractCorpus, ConfCorpus
from speechcorpusy import presets


def load_preset(
    name: str,
    root: Optional[str] = None,
    download: Optional[bool] = None,
    conf: Optional[ConfCorpus] = None,
    ) -> AbstractCorpus:
    """Load preset corpus.

    Args:
        name: Preset corpus name
        root: Adress of the directory under which the corpus archive is found or downloaded
        download: Whether to download original corpus if it is not found in `root`
        conf: (Advanced) Corpus configuration containing both `root` and `download`
    """

    # Design Notes:
    #     ConfCorpus is verbose wrapper, but useful when used with config manager.
    #     For both purpose, we provide both way.
    #     As a result, loader become dirty, but it is good for user.

    # Check config inconsistency
    # Both `root` and `conf` are provided, but different value
    if root and conf and (root is not conf.root):
        raise Exception(f"'root' and 'conf.root' is inconsistent: {root} vs {conf.root}")
    # Both `download` and `conf` are provided, but different value
    if (download is not None) and conf and (download is not conf.download):
        msg = f"'download' and 'conf.download' is inconsistent: {download} vs {conf.download}"
        raise Exception(msg)

    checked_conf = conf or ConfCorpus(root, download or False)

    # Load corpus safely
    if name in presets.corpus_list:
        corpus_cls: AbstractCorpus = getattr(presets, name)
        corpus = corpus_cls(checked_conf)
    else:
        msg1 = f"Corpus '{name}' is not supported by 'speechcurpusy'. "
        msg2 = f"Supported presets: {presets.corpus_list}"
        raise Exception(msg1+msg2)

    return corpus