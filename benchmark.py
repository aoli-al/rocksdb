import subprocess
import os
import shutil
from pathlib import Path

DB_BASE="/data/db/"
WAL_BASE="/data/wal/"
OUT_BASE="/data/out/"


class Benchmark():
    def __init__(self, name, has_duration=True, args=[], env={}):
        self.name = name
        self.has_duration = has_duration
        self.args = args
        self.env = env

    def prepare_dir(self, path):
        path = os.path.join(path, self.name)
        if os.path.exists(path):
            shutil.rmtree(path)
        Path(path).mkdir(parents=True, exist_ok=True)
        return path

    def run(self, cwd, t):
        env = {
            "NUM_KEYS": "900000000",
            "CACHE_SIZE": "6442450944",
            "DB_DIR": self.prepare_dir(os.path.join(DB_BASE, t)),
            "WAL_DIR": self.prepare_dir(os.path.join(WAL_BASE, t)),
            "OUTPUT_DIR": self.prepare_dir(os.path.join(OUT_BASE, t)),
            **self.env
        }
        if self.has_duration:
            env["DURATION"] = "5400"

        subprocess.run("./tools/benchmark.sh" + " " + self.name + " " + " ".join(self.args), shell=True, env=env, cwd=cwd)

bms = [
    Benchmark("bulkload", False),
    Benchmark("readrandom"),
    Benchmark("multireadrandom", args=["--multiread_batched"]),
    Benchmark("fwdrange"),
    Benchmark("revrange"),
    Benchmark("overwrite"),
    Benchmark("readwhilewriting", env={"MB_WRITE_PER_SEC": "2"}),
    Benchmark("fwdrangewhilewriting", env={"MB_WRITE_PER_SEC": "2"}),
    Benchmark("revrangewhilewriting", env={"MB_WRITE_PER_SEC": "2"}),
]

def main():
    ori_path = "../rocksdb"
    cur_path = "."
    for bm in bms:
        bm.run(ori_path, "ori")
    for bm in bms:
        bm.run(cur_path, "cst")


if __name__ == '__main__':
    main()

