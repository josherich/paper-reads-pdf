import os
import argparse
import crawler
from parse_pdf_to_text import pdf_to_text
from urllib.parse import urlparse
from analyze import analyze
from thumb_pdf import thumb_pdf
from grobid.grobid_client import grobid_client

def run(site_uri, depth, output_dir, skip_crawl):
  if not skip_crawl:
    crawler.crawl(url=site_uri, depth=depth, output_dir=output_dir, method="normal")
  name = urlparse(site_uri).netloc
  pdf_to_text(os.path.join(output_dir, name), os.path.join(output_dir, name+'.txt'))
  thumb_pdf(os.path.join(output_dir, name), os.path.join(output_dir, name+'.thumb'))
  analyze(os.path.join(output_dir, name, 'list.csv'), os.path.join(output_dir, name))

  client = grobid_client(config_path='./grobid/config.json')
  client.process(os.path.join(output_dir, name), os.path.join(output_dir, name+'.meta'), 20, 'processHeaderDocument', True, True, True, True, False)


if __name__ == "__main__":

  # parse input arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('--page_uri', type=str,
                      default='https://www.cs.cmu.edu/~odonnell/quantum18/',
                      help='website homepage to crawl')
  parser.add_argument('--depth', type=int, default=3, help='crawling depth')
  parser.add_argument('--output_dir', type=str, default='data', help='output dir')
  parser.add_argument("--skip_crawl", action="store_true", help="set to skip crawl")

  args = parser.parse_args()
  run(args.page_uri, args.depth, args.output_dir, args.skip_crawl)