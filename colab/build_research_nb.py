"""rca_research_src.py (percent format: '# %%' code cells, '# %% [markdown]' text cells) -> rca_research.ipynb."""
import json
import pathlib
import re

here = pathlib.Path(__file__).parent
src = (here / "rca_research_src.py").read_text(encoding="utf-8")
cells = []
for block in re.split(r"^# %%", src, flags=re.M)[1:]:
    head, _, body = block.partition("\n")
    if head.strip() == "[markdown]":
        text = "\n".join(l[2:] if l.startswith("# ") else l.lstrip("#") for l in body.strip("\n").splitlines())
        cells.append({"cell_type": "markdown", "metadata": {}, "source": text.splitlines(True)})
    else:
        cells.append({"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": body.strip("\n").splitlines(True)})
nb = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "name": "python3"}, "language_info": {"name": "python"},
                                   "colab": {"provenance": [], "toc_visible": True}}, "nbformat": 4, "nbformat_minor": 5}
(here / "rca_research.ipynb").write_text(json.dumps(nb, indent=1), encoding="utf-8")
print("cells:", len(cells))
