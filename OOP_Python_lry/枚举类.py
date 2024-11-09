from enum import Enum
class Gender(Enum):
    MALE = 1
    FEMALE =2
class Student:
    def __init__(self,gender: Gender):
        self.gender = gender


def main():
    print(type(Gender))
    print(type(Gender.MALE))
    print(type(Gender.FEMALE))
    print("***************************************************")
    print(Gender.MALE.name)
    print(Gender.MALE.value)
    print(Gender.FEMALE.name)
    print(Gender.FEMALE.value)
    print("***************************************************")
    student = Student(Gender.MALE)
    if student.gender == Gender.MALE:
        print("this student is a male")
    else:
        print("this student is a female")

    s_gender = "FEMALE"
    student.gender = Gender[s_gender]
    print(student.gender)

    i_gender = 2
    print(Gender(i_gender))

    for gg in Gender:
        print(gg.name)


if __name__ == '__main__':
    main()