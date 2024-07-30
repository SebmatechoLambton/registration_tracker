import warnings
import schedule
import time
from utils import run_report
warnings.filterwarnings("ignore")


if __name__ == '__main__':
    # # schedule.every(30).seconds.do(run_report)
    schedule.every(30).minutes.do(run_report)
    run_report()
    while True:
        schedule.run_pending()
        time.sleep(1)

	