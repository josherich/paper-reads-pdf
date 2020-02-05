import os
import argparse
import crawler
from parse_pdf_to_text import pdf_to_text
from urllib.parse import urlparse
from analyze import analyze
from thumb_pdf import thumb_pdf
from grobid.grobid_client import grobid_client

def run(site_uri, depth, output_dir, skip_crawl, keep_filename, skip_to_meta):
  name = urlparse(site_uri).netloc

  if not skip_to_meta:
    if not skip_crawl:
      crawler.crawl(url=site_uri, depth=depth, output_dir=output_dir, method="normal", keep_filename=keep_filename)
    pdf_to_text(os.path.join(output_dir, name), os.path.join(output_dir, 'parsed-txt'))
    thumb_pdf(os.path.join(output_dir, name), os.path.join(output_dir, name+'.thumb'))
    analyze(os.path.join(output_dir, 'list.csv'), os.path.join(output_dir, 'parsed-txt'))

  if not os.path.exists(os.path.join(output_dir, name+'.meta')):
    os.makedirs(os.path.join(output_dir, name+'.meta'))
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
  parser.add_argument("--keep_filename", action="store_true", help="use hashed filename as default")
  parser.add_argument("--skip_to_meta", action="store_true", help="skip to grobid meta parsing")

  args = parser.parse_args()
  run(args.page_uri, args.depth, args.output_dir, args.skip_crawl, args.keep_filename, args.skip_to_meta)