# paper reads pdf

pdf pipeline for paper.mindynode.com

## Install
```
pip install -r requirements.txt
```

## Run

```
python main.py --page_uri=https://www.hackernewspapers.com/ --depth=2

// skip crawling
python main.py --page_uri=https://www.hackernewspapers.com/ --depth=2 --skip_crawl

// use original file names
python main.py --page_uri=https://www.hackernewspapers.com/ --depth=2 --keep_filename
```

5 steps are inlcuded
  1. crawl pdfs
  2. pdf to text
  3. screenshot thumbs
  4. analyze tdidf matrix
  5. extract meta using [grobid](https://github.com/kermitt2/grobid)

---

the code is based on:
  1. [arxiv-sanity-preserver](https://github.com/karpathy/arxiv-sanity-preserver)
  2. [pdf-crawler](https://github.com/SimFin/pdf-crawler)
  3. [grobid-client-python](https://github.com/kermitt2/grobid-client-python)
