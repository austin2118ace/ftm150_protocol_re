import datetime
from pathlib import Path
from tqdm import tqdm
from pybuspirate import BusPirate

OUTPUT_DIR = "/opt/dev/HAM/FTM150_protocol_re/dumps/"
SNIFF_TIME = 15
def main():

    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = datetime.datetime.now().strftime("%d%m%Y%H%M%S_ftm150rasp_i2c_capture")
    addition = input("Insert filename addition, such as what is being sniffed/recorded:")
    filename = filename + "_" + addition

    output_path = output_dir / filename


    # Connect to the Bus Pirate
    bp = BusPirate('/dev/ttyACM1',115200, 1)
    bp.start()
    # Change to I2C mode
    bp.change_mode("I2C")
    bp.send("sniff")
    print(f"Scanning BUS with a {SNIFF_TIME} timeout...")
    results = bp.receive_all(silence_timeout=SNIFF_TIME)
    bp.stop()

    txt_file = output_path.with_suffix(".txt")
    with open(txt_file, "w") as txt_file:
        print("Writing to txt file...")
        for result in tqdm(results):
            txt_file.write(f"{result}\n")



if __name__ == "__main__":
    main()