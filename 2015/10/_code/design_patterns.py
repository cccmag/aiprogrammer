#!/usr/bin/env python3
"""設計模式範例程式"""

from abc import ABC, abstractmethod


class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data):
        pass


class QuickSort(SortStrategy):
    def sort(self, data):
        print("Using QuickSort")
        return sorted(data)


class MergeSort(SortStrategy):
    def sort(self, data):
        print("Using MergeSort")
        return sorted(data)


class BubbleSort(SortStrategy):
    def sort(self, data):
        print("Using BubbleSort")
        result = list(data)
        n = len(result)
        for i in range(n):
            for j in range(0, n-i-1):
                if result[j] > result[j+1]:
                    result[j], result[j+1] = result[j+1], result[j]
        return result


class DataSorter:
    def __init__(self, strategy: SortStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def sort(self, data):
        return self.strategy.sort(data)


class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price


class Builder(ABC):
    @abstractmethod
    def build_header(self):
        pass

    @abstractmethod
    def build_body(self):
        pass

    @abstractmethod
    def build_footer(self):
        pass


class Report:
    def __init__(self):
        self.content = ""

    def add(self, text):
        self.content += text + "\n"


class HTMLReportBuilder(Builder):
    def __init__(self):
        self.report = Report()

    def build_header(self):
        self.report.add("<html><head><title>Report</title></head><body>")

    def build_body(self):
        self.report.add("<h1>Report Content</h1>")

    def build_footer(self):
        self.report.add("</body></html>")

    def get_result(self):
        return self.report


class PlainTextReportBuilder(Builder):
    def __init__(self):
        self.report = Report()

    def build_header(self):
        self.report.add("=" * 40)
        self.report.add("REPORT")
        self.report.add("=" * 40)

    def build_body(self):
        self.report.add("Report Content")
        self.report.add("-" * 20)

    def build_footer(self):
        self.report.add("=" * 40)

    def get_result(self):
        return self.report


class ReportDirector:
    def __init__(self, builder: Builder):
        self.builder = builder

    def construct(self):
        self.builder.build_header()
        self.builder.build_body()
        self.builder.build_footer()

    def get_report(self):
        return self.builder.get_result()


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


class Light:
    def on(self):
        print("Light is ON")

    def off(self):
        print("Light is OFF")


class LightOnCommand(Command):
    def __init__(self, light):
        self.light = light

    def execute(self):
        self.light.on()

    def undo(self):
        self.light.off()


class RemoteControl:
    def __init__(self):
        self.history = []

    def execute(self, command):
        command.execute()
        self.history.append(command)

    def undo(self):
        if self.history:
            command = self.history.pop()
            command.undo()


def demo():
    print("=" * 60)
    print("Design Patterns Demo")
    print("=" * 60)

    print("\n--- Strategy Pattern ---")
    data = [64, 34, 25, 12, 22, 11, 90]

    sorter = DataSorter(QuickSort())
    print(f"Result: {sorter.sort(data)}")

    sorter.set_strategy(BubbleSort())
    print(f"Result: {sorter.sort(data)}")

    print("\n--- Builder Pattern ---")
    html_builder = HTMLReportBuilder()
    director = ReportDirector(html_builder)
    director.construct()
    report = director.get_report()
    print(report.content)

    print("\n--- Command Pattern ---")
    light = Light()
    light_on = LightOnCommand(light)
    remote = RemoteControl()
    remote.execute(light_on)
    remote.undo()

    print("\n" + "=" * 60)
    print("All design pattern demos completed!")
    print("=" * 60)


if __name__ == "__main__":
    demo()