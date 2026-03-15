from pathlib import Path
from tqdm import tqdm
DATA_PATH = Path("../dumps/13032026184550_ftm150rasp_i2c_capture.txt")
r_bar='| {n:.1f}MB/{total:.1f}MB [{elapsed}<{remaining}, ' '{rate_fmt}{postfix}]'
PBARDESC = f"{{l_bar}}{{bar}}{r_bar}"

B_IN_MB = 1024**2


def main():
    contents, num_lines = read_dumpfile()
    print(num_lines)

def read_dumpfile() -> tuple[list, int]:
    filesizembytes = DATA_PATH.stat().st_size / B_IN_MB
    file_contents = []
    num_lines = 0
    with (open(DATA_PATH, "r") as f,
          tqdm(desc="Reading dump from file: ", total=filesizembytes, unit=' bytes', bar_format=PBARDESC) as tq
          ):
        tq.format_num(.3)
        for line in f:
            file_contents.append(line)
            linesizembytes = len(line) / B_IN_MB
            tq.update(linesizembytes)
            num_lines += 1
        tq.update(filesizembytes - tq.n)
    return file_contents, num_lines


if __name__ == "__main__":
    main()