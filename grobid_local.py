import os
import argparse
from urllib.parse import urlparse
from grobid.grobid_client import grobid_client

def run(site_uri):
  name = urlparse(site_uri).netloc
  output_dir = 'data'
  print(name)

  os.system(f"scp -r chenjosh@35.232.191.2:/home/chenjosh/app/paper-reads-pdf/data/{name} ./data")

  if not os.path.exists(os.path.join(output_dir, name+'.meta')):
    os.makedirs(os.path.join(output_dir, name+'.meta'))
  client = grobid_client(config_path='./grobid/config.json')
  client.process(os.path.join(output_dir, name), os.path.join(output_dir, name+'.meta'), 20, 'processHeaderDocument', True, True, True, True, False)

  os.system(f"scp -r ./data/{name}.meta chenjosh@35.232.191.2:/home/chenjosh/app/paper-reads-pdf/data/")

if __name__ == "__main__":

  # parse input arguments
  parser = argparse.ArgumentParser()
  parser.add_argument('--page_uri', type=str,
                      default='https://www.cs.cmu.edu/~odonnell/quantum18/',
                      help='website homepage to crawl')

  args = parser.parse_args()
  run(args.page_uri)