import csv
import logging
from pathlib import Path

from .test_name import TestName
from .disciplines import Discipline
from log_saver.log_saver import Log

__all__ = ['Student']

# ������ ��������� ���������
_DISCIPLINES = ["����������",
                "������",
                "�����",
                "�������",
                "����������",
                ]

# ��������� �����������
_LOG_FILE = 'student.log'
_LOG_LEVEL = logging.INFO


class Student:
    """����� �������."""
    family = TestName()
    name = TestName()
    second_name = TestName()

    def __init__(self, family: str, name: str, second_name: str):
        """������������� ����������."""
        self.family = family  # �������
        self.name = name  # ���
        self.second_name = second_name  # ��������
        self._progress = []  # ������������ �� ��������� ������ �� Discipline
        self._load_progress()

    @property
    def progress(self):
        """�������� �������� ������ ���������, ���������� ����� ���������� ����� ����� append_to_progress"""
        return self._progress

    @property
    def short_name(self):
        """�������� ��� ��������� ��������� ����� ��������."""
        return f"{self.family} {self.name[0]}.{self.second_name[0]}."

    def __str__(self):
        """������������� ���������� � ���� ������."""
        return f'{self.family} {self.name} {self.second_name}'

    def __repr__(self):
        """������������� � ���� ������ ��������� ���������� ������."""
        return f'Student({self.family}, {self.name}, {self.second_name})'

    def _load_progress(self):
        """������ ������������ �� ���������. ���� � �������� ��� ������ ������ �� ������������ - ���������
        ������ ��������� �� ������ ������ ��������� ����.
        """
        file_name = self.short_name + 'csv'
        if Path(file_name).exists():
            with open(file_name, "r", encoding="UTF-8") as file:
                csv_reader = csv.reader(file, dialect="excel", quoting=csv.QUOTE_NONNUMERIC)
                for row in csv_reader:
                    new_discipline = Discipline(row[0], int(row[1]), int(row[2]))
                    self.append_to_progress(new_discipline)

    @Log(_LOG_FILE, __name__, _LOG_LEVEL)
    def save_progress(self):
        """���������� ���������� �� ������������ ��������."""
        file_name = self.short_name + 'csv'
        with open(file_name, "w", encoding="UTF-8", newline='') as file:
            csv_writer = csv.writer(file, dialect="excel", quoting=csv.QUOTE_NONNUMERIC)
            for discipline in self._progress:
                csv_writer.writerow([discipline.name, discipline.rate_value, discipline.test_value])

    def show_progress(self):
        """����������� ������������."""
        result = "--------------------------------\n" \
                 "     �������    | ������ | ���� \n" \
                 "--------------------------------\n"
        for discipline in self._progress:
            result += f"{discipline.name:16}|{discipline.rate_value:7} |{discipline.test_value:5}\n"
        result += "--------------------------------"
        return result

    def find_discipline_in_progress(self, discipline: Discipline) -> bool:
        """����� ���������� � ������ ������������ ��������."""
        result = False
        for disc in self._progress:
            if discipline == disc:
                result = True
                break

        return result

    @Log(_LOG_FILE, __name__, _LOG_LEVEL)
    def append_to_progress(self, discipline: Discipline):
        """���������� ����� ���������� � ������ ������������ ��������.
        ���� ���������� ����� ������������ ��� ��� ������������ � ������ - �������� ValueError
        """
        if discipline.name in _DISCIPLINES and not self.find_discipline_in_progress(discipline):
            self._progress.append(discipline)
        else:
            raise ValueError(f"{discipline.name} - ������������ ����������, ��� ��� ���� � ������!")


if __name__ == '__main__':
    student_1 = Student('�������', '��������', '���������')
    student_2 = Student('�������', '�����', '����������')

    print(student_1.short_name)
    print(student_2)