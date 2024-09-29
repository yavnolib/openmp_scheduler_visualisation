import argparse
import os
import warnings
from pathlib import Path

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

warnings.filterwarnings("ignore")
sns.set(style="darkgrid")


class Distribution:
    def __init__(self, key, value):
        self.value_repr = ", ".join(value.split("\n")[:-1]).rstrip(", ")
        self.key = key
        self.value = value

        self.chunk = self.key[1]
        self.name = self.key[0]

        data = np.array(
            [list(map(int, i.split("<->"))) for i in self.value_repr.split(", ")]
        )
        self.iters = data[:, 0]
        self.threads = data[:, 1]

    def __repr__(self) -> str:
        return (
            f"<Distribution> {self.key} with chunksize={self.chunk} : {self.value_repr}"
        )

    def get_iterations_threads(self) -> list[list[int], list[int]]:
        return self.iters, self.threads


class Plotter:
    def __init__(
        self, log_file="logs.txt", output_dir="./distributions", remove_log_file=True
    ):
        self.log_file = log_file
        self.output_dir = output_dir
        self.remove_log_file = remove_log_file

        logs: list[str] = self.read_log_file(log_file)
        iter_distribution: dict = self.parse_logs(logs)
        self.distrs: list[Distribution] = self.distrs_from_array(iter_distribution)

    def read_log_file(self, log_file):
        if not Path(log_file).exists():
            raise OSError(
                f"Log-file does not exists. Path: {str(Path(log_file))}.\n"
                f"Current directory: {str(Path('.').resolve())}\n"
            )
        with open(log_file) as f:
            logs = f.read()
        logs = logs.split(":::")
        return logs

    def parse_logs(self, logs):
        iter_distribution = {}
        for log in logs:
            if "schedule" in log:
                name = log.split("schedule")[0].strip()
                chunk = None
                if "chunk" in log:
                    chunk = int(log.split("chunk=")[1].split(":")[0])
            else:
                if (name, chunk) in iter_distribution:
                    prev = iter_distribution[(name, chunk)]
                    iter_distribution.update({(name, chunk): prev + log})
                else:
                    iter_distribution.update({(name, chunk): log})
        return iter_distribution

    def distrs_from_array(self, iter_distribution) -> list[Distribution]:
        distrs = []
        for key, value in iter_distribution.items():
            distrs.append(Distribution(key, value))
        return distrs

    def plot_distributions(self):
        Path(self.output_dir).resolve().mkdir(exist_ok=True, parents=True)

        if self.remove_log_file:
            os.remove(self.log_file)

        for distr in self.distrs:
            iterations = distr.iters
            threads = distr.threads
            unique_threads = sorted(set(threads))
            colors = plt.cm.get_cmap("tab10", len(unique_threads))
            square_size = 0.5

            _, ax = plt.subplots(figsize=(18, 12))

            for i, (iter_num, thread_num) in enumerate(zip(iterations, threads)):
                color = colors(unique_threads.index(thread_num))
                rect = patches.Rectangle(
                    (i, thread_num - square_size / 2),
                    1,
                    square_size,
                    facecolor=color,
                    edgecolor="black",
                )
                ax.add_patch(rect)

                text_color = "green"
                if iter_num > 0.9 * len(iterations):
                    text_color = "black"
                elif iter_num > 0.75 * len(iterations):
                    text_color = "red"
                elif iter_num > 0.5 * len(iterations):
                    text_color = "yellow"

                ax.text(
                    i + 0.5,
                    thread_num,
                    str(iter_num),
                    fontweight="bold",
                    ha="center",
                    va="center",
                    fontsize=10,
                    rotation=90,
                    color=text_color,
                )

            plt.yticks(sorted(set(threads)))
            plt.xticks(
                range(len(iterations)), range(len(iterations))
            )
            plt.xlabel("Порядок итераций")
            plt.ylabel("Номер потока")
            plt.title("Выполнение итераций потоков")
            plt.ylim((-1, max(threads) + 1))
            plt.xlim((-1, max(iterations) + 2))
            plt.grid(True)

            xticks = np.arange(0, len(iterations), 5)
            plt.xticks(xticks, xticks)  # Итерации для подписей
            plt.savefig(f"{self.output_dir}/distr_{distr.name}_chunk={distr.chunk}.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Программа для работы с логами.")
    parser.add_argument(
        "--log_file",
        type=str,
        default="logs.txt",
        help="Путь к файлу логов (по умолчанию: logs.txt)",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="./distributions",
        help="Путь к файлу логов (по умолчанию: ./distributions)",
    )
    args = parser.parse_args()

    plotter = Plotter(
        log_file=args.log_file, output_dir=args.output_dir, remove_log_file=True
    )
    plotter.plot_distributions()
