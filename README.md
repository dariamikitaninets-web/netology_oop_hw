English | [Polski](README_PL.md) | [Français](README_FR.md)

# Python OOP: Students, Lecturers, and Reviewers

[![Python application](https://github.com/dariamikitaninets-web/netology_oop_hw/actions/workflows/python-app.yml/badge.svg)](https://github.com/dariamikitaninets-web/netology_oop_hw/actions/workflows/python-app.yml)

Object-oriented Python project modelling an educational platform with students, lecturers, and homework reviewers. The implementation demonstrates inheritance, object collaboration, validation rules, magic methods, grade aggregation, type hints, pytest integration, linting, and Continuous Integration with GitHub Actions.

The project was created as a Netology Object-Oriented Programming homework assignment and later extended with repository hygiene, a smoke test, and a CI workflow.

## Project purpose

The project was created to practise and demonstrate:

- class design and object-oriented modelling;
- inheritance and specialization;
- interactions between objects of different classes;
- validation of business rules before changing object state;
- storage of grades grouped by course;
- calculation of individual and course-level averages;
- custom string representations with `__str__`;
- comparison of objects through rich comparison methods;
- Python type hints;
- separation of reusable classes from demonstration code;
- basic automated testing with pytest;
- code checks and test execution in GitHub Actions.

## Domain model

The application represents four roles.

| Class | Responsibility |
|---|---|
| `Mentor` | Base class containing a mentor’s name, surname, and attached courses |
| `Lecturer` | Inherits from `Mentor`, receives lecture grades from students, calculates an average, and supports comparison with other lecturers |
| `Reviewer` | Inherits from `Mentor` and assigns homework grades to eligible students |
| `Student` | Tracks active and completed courses, receives homework grades, grades eligible lecturers, calculates an average, and supports comparison with other students |

## Inheritance structure

```text
Mentor
├── Lecturer
└── Reviewer

Student
```

`Lecturer` and `Reviewer` reuse the shared mentor attributes through inheritance. `Student` is a separate domain entity because it has a different responsibility and data model.

## Assignment implementation

### 1. Mentor hierarchy

The base `Mentor` class stores:

- `name`;
- `surname`;
- `courses_attached`.

`Lecturer` and `Reviewer` inherit these fields and extend the base behaviour.

### 2. Grade interactions

A `Reviewer` may grade a student’s homework only when:

- the target object is a `Student`;
- the course is attached to the reviewer;
- the course is currently studied by the student;
- the grade is within the implemented range from `0` to `10`.

A `Student` may grade a lecturer only when:

- the target object is a `Lecturer`;
- the course is in the student’s active courses;
- the course is attached to the lecturer;
- the grade is within the implemented range from `0` to `10`.

Successful operations append the grade to a course-specific list. Invalid operations return the Russian message `Ошибка` (`Error`) and leave grade collections unchanged.

### 3. String representations

The classes implement readable `__str__` output.

A lecturer representation includes:

- name;
- surname;
- average lecture grade.

A reviewer representation includes:

- name;
- surname.

A student representation includes:

- name;
- surname;
- average homework grade;
- courses currently in progress;
- completed courses.

The output labels remain in Russian because they follow the original assignment format.

### 4. Object comparisons

Students are compared with other students by their average homework grade.

Lecturers are compared with other lecturers by their average lecture grade.

The implementation supports:

```python
<
<=
>
>=
==
```

When the other object belongs to an incompatible class, the comparison method returns `NotImplemented`.

### 5. Course-level statistics

Two standalone functions aggregate grades across multiple objects:

```python
average_hw_grade_by_course(students, course)
average_lecture_grade_by_course(lecturers, course)
```

The first calculates the average homework grade for a selected course across students. The second calculates the average lecture grade for that course across lecturers.

If no matching grades are available, the shared `avg()` helper returns `0.0`.

## Example usage

```python
from main import Lecturer, Reviewer, Student

student = Student("Olga", "Alekhina", "F")
lecturer = Lecturer("Ivan", "Ivanov")
reviewer = Reviewer("Piotr", "Petrov")

student.courses_in_progress.append("Python")
lecturer.courses_attached.append("Python")
reviewer.courses_attached.append("Python")

student.rate_lecture(lecturer, "Python", 9)
reviewer.rate_hw(student, "Python", 10)

print(lecturer.average_grade())  # 9.0
print(student.average_grade())   # 10.0
```

## Demonstration script

The block protected by:

```python
if __name__ == "__main__":
```

creates sample students, lecturers, and reviewers and demonstrates:

- inheritance checks;
- valid and invalid grading attempts;
- stored grades;
- formatted object output;
- comparisons between two students and two lecturers;
- course-level average calculations.

Run it with:

```bash
python main.py
```

## Technology stack

- Python
- Object-Oriented Programming
- Pytest
- Flake8
- Git and GitHub
- GitHub Actions

## Project structure

```text
netology_oop_hw/
├── .github/
│   └── workflows/
│       └── python-app.yml
├── tests/
│   └── test_smoke.py
├── .gitignore
├── main.py
├── requirements.txt
├── README.md
├── README_PL.md
└── README_FR.md
```

### Main files

- `main.py` — domain classes, validation rules, comparison methods, average functions, and demonstration code.
- `tests/test_smoke.py` — minimal pytest smoke test used to verify that the test environment starts correctly.
- `requirements.txt` — pinned pytest and supporting packages.
- `.github/workflows/python-app.yml` — CI workflow running Flake8 and pytest.
- `.gitignore` — excludes Python cache files and local development artifacts.

## Requirements

- Python 3.10 or newer;
- Git, when cloning the repository.

The repository currently pins pytest 9, which requires Python 3.10 or newer.

## Installation

Clone the repository:

```bash
git clone https://github.com/dariamikitaninets-web/netology_oop_hw.git
cd netology_oop_hw
```

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

Install the dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Running the project

Run the demonstration:

```bash
python main.py
```

Run the current pytest suite:

```bash
pytest
```

Run with detailed output:

```bash
pytest -v
```

## Current automated test coverage

The repository currently contains one smoke test:

```python
def test_smoke():
    assert 1 + 1 == 2
```

Its purpose is to confirm that pytest is installed and that the CI test step can execute. It does **not** verify the educational platform’s business logic.

Therefore, a successful CI badge currently means:

- dependencies were installed;
- critical Flake8 checks did not detect syntax errors or undefined names;
- pytest started successfully;
- the smoke test passed.

It does not yet prove that grading, comparison, formatting, or average calculations are regression-tested.

## Continuous Integration

The `Python application` workflow runs on:

- pushes to `main`;
- pull requests targeting `main`.

The workflow:

1. checks out the repository;
2. configures Python 3.10;
3. upgrades pip;
4. installs Flake8, pytest, and `requirements.txt`;
5. runs critical Flake8 checks;
6. runs a non-blocking extended Flake8 report;
7. executes pytest.

[View GitHub Actions runs](https://github.com/dariamikitaninets-web/netology_oop_hw/actions)

The latest inspected workflow run completed successfully.

## Assignment compliance

| Assignment area | Implementation |
|---|---|
| Base `Mentor` class | Implemented |
| `Lecturer` inherits from `Mentor` | Implemented |
| `Reviewer` inherits from `Mentor` | Implemented |
| Reviewer grades student homework | Implemented with role, course, and grade validation |
| Student grades lecturer | Implemented with role, course, and grade validation |
| Grades stored by course | Implemented with dictionaries of lists |
| `__str__` for reviewer | Implemented |
| `__str__` for lecturer | Implemented with average |
| `__str__` for student | Implemented with average and course lists |
| Student comparison | Implemented by average homework grade |
| Lecturer comparison | Implemented by average lecture grade |
| Average homework grade by course | Implemented |
| Average lecture grade by course | Implemented |
| Example objects and calls | Included in the executable demonstration |
| CI and pytest | Added as a repository extension |

## Skills demonstrated

- object-oriented domain modelling;
- inheritance;
- polymorphic comparison behaviour;
- class collaboration;
- business-rule validation;
- state mutation through methods;
- dictionaries and lists for grouped data;
- magic methods;
- average aggregation;
- type annotations;
- pytest setup;
- basic CI configuration;
- static code checks with Flake8.

## Current limitations and improvement priorities

### Business logic is not unit-tested

The most important improvement is replacing or extending the smoke test with real tests for:

- valid and invalid homework grading;
- valid and invalid lecturer grading;
- grade boundary values;
- average calculations;
- empty-grade behaviour;
- string representations;
- student and lecturer comparisons;
- incompatible comparison types.

### Mixed languages in the source

The implementation contains Polish comments and Russian output strings. This reflects the learning context, but English comments and configurable output labels would make the repository more consistent for an international portfolio.

### Dependency cleanup

`requirements.txt` includes pytest and its transitive dependencies. A smaller direct-dependency file could contain only:

```text
pytest==9.0.3
```

Flake8 is installed directly inside the workflow rather than declared in the project dependency file.

### Minor code cleanup

The `dataclass` import is currently unused. Comparison methods are also repeated in both comparable classes and could later be simplified with `functools.total_ordering` or a shared comparison abstraction.

### GitHub Actions maintenance

The workflow still uses `actions/setup-python@v3`. GitHub currently reports a Node.js runtime deprecation warning for the action, so it should be upgraded to a newer supported release.

## Suggested next testing layer

A portfolio-ready suite should test the actual domain logic, for example:

```python
def test_reviewer_can_grade_student_for_shared_course():
    student = Student("Anna", "Nowak", "F")
    reviewer = Reviewer("Jan", "Kowalski")

    student.courses_in_progress.append("Python")
    reviewer.courses_attached.append("Python")

    result = reviewer.rate_hw(student, "Python", 10)

    assert result is None
    assert student.grades == {"Python": [10]}
```

This would turn the repository from an OOP homework with technical CI into a genuine unit-testing project.

## Author

**Daria Mikitaninets**

Python learning and QA portfolio project focused on OOP fundamentals, validation logic, pytest, and Continuous Integration.
