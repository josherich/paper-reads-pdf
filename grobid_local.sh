# assume grobid is running
foldername=web.stanford.edu
uri=http://web.stanford.edu/class/cs369g/lectures.html
# scp -r chenjosh@35.232.191.2:/home/chenjosh/app/paper-reads-pdf/data/${foldername} ./data
python main.py --page_uri=${uri} --skip_to_meta
scp -r ./data/${foldername}.meta chenjosh@35.232.191.2:/home/chenjosh/app/paper-reads-pdf/data/
# npx babel-node dist/scripts/import.js ../../paper-reads-pdf/data/w6113.github.io ./public/