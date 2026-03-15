import pickle
from pathlib import Path
from tqdm import tqdm
DATA_PATH = Path("../dumps/13032026184550_ftm150rasp_i2c_capture.txt")
r_bar='| {n:.1f}MB/{total:.1f}MB [{elapsed}<{remaining}, ' '{rate_fmt}{postfix}]'
PBARDESC = f"{{l_bar}}{{bar}}{r_bar}"

B_IN_MB = 1024**2
CHUNKS_TO_SKIP = ["\n", "[S]", "[P]", 'ADDR', '']

class Packet:
    def __init__(self, line: str, num: int):
        self._line = line
        self._chunked_line = self.chunk_line(self._line)
        self.packet_num = num
        self.addr = self._chunked_line[0]
        self.read_write = self._chunked_line[1]
        self.data = self._chunked_line[2:]

    def __str__(self):
        return (f"FTM150 Packet: {self.packet_num}\n"
                f"Address: {self.addr}\n"
                f"Address Bits: {bin(int(self.addr, 16))}\n"
                f"Read/Write: {self.read_write}\n"
                f"Data: {self.data}")

    def __eq__(self, other):
        return (
                self.packet_num == other.packet_num and
                self.addr == other.addr and
                self.read_write == other.read_write and
                self.data == other.data
                )

    @staticmethod
    def chunk_line(line):
        return [chunk for chunk in line.split(" ")[:-1] if chunk not in CHUNKS_TO_SKIP]
        # split at spaces and drop the newline


def main():
    packets = []

    try:
        packets = load_packets(DATA_PATH)
    except (IOError, OSError, FileNotFoundError) as e:
        print(f"{DATA_PATH} has not been parsed into packets")
    if not packets:
        contents, num_lines = read_dumpfile()
        packets = dumpfile_to_packets(contents)
        save_packets(packets, DATA_PATH)



def packet_filepath(data_path: Path) -> Path:
    return data_path.parent.joinpath(data_path.stem + "_packets.pkl")


def load_packets(data_path: Path) -> list[Packet]:
    with open(packet_filepath(data_path), "rb") as f:
        return pickle.load(f)


def save_packets(packets: list[Packet], data_path: Path):
    with open(packet_filepath(data_path), "wb") as f:
        pickle.dump(packets, f)


def dumpfile_to_packets(dumpfile_contents: list):
    packets = []
    packet_num = 0
    for line in tqdm(dumpfile_contents):
        if 'I2C' in line or 'x' not in line:
            # Skip the lines from the Bus Pirate and blank lines without an address
            continue
        packet_num += 1
        packets.append(Packet(line, packet_num))

    return packets


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