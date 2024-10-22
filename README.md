  git checkout HEAD -- ./dataset
  to restore all data from the original 2020 repo

  the expected directory structure would be:
  
  ~/repo/ARC-solutions/
    ├── working/
    │   └── abstraction-and-reasoning-challenge/
    │       └── test/
    │           └── *.json files
    ├── input/
    │   └── arc-solution-source-files-by-icecuber/
    │       └── (contents including safe_run.py)
    └── absres-c-files/
        └── safe_run.py (copied from input directory)
