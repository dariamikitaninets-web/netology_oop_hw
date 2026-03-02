from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence


def avg(values: Sequence[int]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


class Mentor:
    def __init__(self, name: str, surname: str) -> None:
        self.name = name
        self.surname = surname
        self.courses_attached: List[str] = []

    def __str__(self) -> str:
        # Dla Mentor bazowego nie jest wymagane w zadaniu, ale nie szkodzi.
        return f"Имя: {self.name}\nФамилия: {self.surname}"


class Lecturer(Mentor):
    def __init__(self, name: str, surname: str) -> None:
        super().__init__(name, surname)
        self.grades: Dict[str, List[int]] = {}

    def average_grade(self) -> float:
        all_grades: List[int] = []
        for grades_list in self.grades.values():
            all_grades.extend(grades_list)
        return avg(all_grades)

    def __str__(self) -> str:
        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}\n"
            f"Средняя оценка за лекции: {self.average_grade():.1f}"
        )

    # Porównania tylko między Lecturer
    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.average_grade() < other.average_grade()

    def __le__(self, other: object) -> bool:
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.average_grade() <= other.average_grade()

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.average_grade() > other.average_grade()

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.average_grade() >= other.average_grade()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.average_grade() == other.average_grade()


class Reviewer(Mentor):
    def rate_hw(self, student: "Student", course: str, grade: int) -> Optional[str]:
        # Walidacje wg zadania: tylko Student, kurs musi być przypięty do reviewera
        # i student musi mieć kurs w trakcie.
        if (
            isinstance(student, Student)
            and course in self.courses_attached
            and course in student.courses_in_progress
            and 0 <= grade <= 10
        ):
            student.grades.setdefault(course, []).append(grade)
            return None
        return "Ошибка"

    def __str__(self) -> str:
        return f"Имя: {self.name}\nФамилия: {self.surname}"


class Student:
    def __init__(self, name: str, surname: str, gender: str) -> None:
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses: List[str] = []
        self.courses_in_progress: List[str] = []
        self.grades: Dict[str, List[int]] = {}

    def average_grade(self) -> float:
        all_grades: List[int] = []
        for grades_list in self.grades.values():
            all_grades.extend(grades_list)
        return avg(all_grades)

    def rate_lecture(self, lecturer: Lecturer, course: str, grade: int) -> Optional[str]:
        # Tylko Lecturer; kurs musi być u studenta w trakcie i u lecturera w courses_attached
        if (
            isinstance(lecturer, Lecturer)
            and course in self.courses_in_progress
            and course in lecturer.courses_attached
            and 0 <= grade <= 10
        ):
            lecturer.grades.setdefault(course, []).append(grade)
            return None
        return "Ошибка"

    def __str__(self) -> str:
        in_progress = ", ".join(self.courses_in_progress) if self.courses_in_progress else ""
        finished = ", ".join(self.finished_courses) if self.finished_courses else ""
        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}\n"
            f"Средняя оценка за домашние задания: {self.average_grade():.1f}\n"
            f"Курсы в процессе изучения: {in_progress}\n"
            f"Завершенные курсы: {finished}"
        )

    # Porównania tylko między Student
    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Student):
            return NotImplemented
        return self.average_grade() < other.average_grade()

    def __le__(self, other: object) -> bool:
        if not isinstance(other, Student):
            return NotImplemented
        return self.average_grade() <= other.average_grade()

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Student):
            return NotImplemented
        return self.average_grade() > other.average_grade()

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, Student):
            return NotImplemented
        return self.average_grade() >= other.average_grade()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Student):
            return NotImplemented
        return self.average_grade() == other.average_grade()


def average_hw_grade_by_course(students: Sequence[Student], course: str) -> float:
    grades: List[int] = []
    for s in students:
        grades.extend(s.grades.get(course, []))
    return avg(grades)


def average_lecture_grade_by_course(lecturers: Sequence[Lecturer], course: str) -> float:
    grades: List[int] = []
    for l in lecturers:
        grades.extend(l.grades.get(course, []))
    return avg(grades)


if __name__ == "__main__":
    # Zad. 1: sprawdzenie dziedziczenia
    lecturer = Lecturer("Иван", "Иванов")
    reviewer = Reviewer("Пётр", "Петров")
    print(isinstance(lecturer, Mentor))  # True
    print(isinstance(reviewer, Mentor))  # True
    print(lecturer.courses_attached)     # []
    print(reviewer.courses_attached)     # []

    # Zad. 2: interakcje i walidacje
    student = Student("Алёхина", "Ольга", "Ж")
    student.courses_in_progress += ["Python", "Java"]

    lecturer.courses_attached += ["Python", "C++"]
    reviewer.courses_attached += ["Python", "C++"]

    print(student.rate_lecture(lecturer, "Python", 7))    # None
    print(student.rate_lecture(lecturer, "Java", 8))      # Ошибка
    print(student.rate_lecture(lecturer, "C++", 8))       # Ошибка (bo student nie ma C++ w progress)
    # student.rate_lecture(reviewer, "Python", 6) -> Ошибка (bo reviewer nie jest Lecturer)
    print(student.rate_lecture(reviewer, "Python", 6))    # Ошибка

    print(lecturer.grades)  # {'Python': [7]}

    # Reviewer ocenia studentowi HW
    print(reviewer.rate_hw(student, "Python", 10))        # None
    print(reviewer.rate_hw(student, "Java", 9))           # Ошибка (reviewer nie ma Java attached)
    print(student.grades)                                  # {'Python': [10]}

    # Zad. 3: __str__
    print(reviewer)
    print(lecturer)
    print(student)

    # Zad. 3: porównania
    lecturer2 = Lecturer("Анна", "Сидорова")
    lecturer2.courses_attached += ["Python"]
    student2 = Student("Ирина", "Кузнецова", "Ж")
    student2.courses_in_progress += ["Python"]

    # Dodajemy oceny dla lecturer2 i student2
    student.rate_lecture(lecturer2, "Python", 9)
    student2.rate_lecture(lecturer2, "Python", 10)
    reviewer.courses_attached += ["Java"]
    student2.courses_in_progress += ["Java"]
    reviewer.rate_hw(student2, "Python", 8)
    reviewer.rate_hw(student2, "Java", 7)

    print(lecturer > lecturer2)
    print(student2 > student)

    # Zad. 4: średnie po kursie
    students_list = [student, student2]
    lecturers_list = [lecturer, lecturer2]
    print(average_hw_grade_by_course(students_list, "Python"))
    print(average_lecture_grade_by_course(lecturers_list, "Python"))