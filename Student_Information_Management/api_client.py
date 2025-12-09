import requests

API = "http://127.0.0.1:8000"



def admin_add_student():
    print("\nADD STUDENT")
    sid = input("ID: ")
    name = input("Name: ")
    age = int(input("Age: "))
    program = input("Program: ")
    payload = {"id": sid, "name": name, "age": age, "program": program}
    print(requests.post(API + "/admin/add_student", json=payload).json())


def admin_list_students():
    r = requests.get(API + "/admin/list_students").json()
    print("\nSTUDENTS:")
    for s in r["students"]:
        print(s)


def admin_view_student():
    sid = input("Student ID: ")
    print(requests.get(API + "/admin/get_student", params={"id": sid}).json())


def admin_update_student():
    sid = input("ID to update: ")
    name = input("New name: ")
    age = int(input("New age: "))
    program = input("New program: ")
    payload = {"id": sid, "name": name, "age": age, "program": program}
    print(requests.put(API + "/admin/update_student", json=payload).json())


def admin_delete_student():
    sid = input("Delete ID: ")
    print(requests.delete(API + "/admin/delete_student", params={"id": sid}).json())


def admin_menu():
    print("\nADMIN MENU")
    print("1. Add Student")
    print("2. List Students")
    print("3. View Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Back to Main Menu")


def admin_panel():
    while True:
        admin_menu()
        c = input("Choice: ")
        if c == "1":
            admin_add_student()
        elif c == "2":
            admin_list_students()
        elif c == "3":
            admin_view_student()
        elif c == "4":
            admin_update_student()
        elif c == "5":
            admin_delete_student()
        elif c == "6":
            break
        else:
            print("Invalid choice!")



def student_login():
    while True:
        sid = input("Enter your Student ID: ").strip()
        r = requests.get(API + "/admin/get_student", params={"id": sid}).json()
        if r.get("found"):
            print("\nLogin Successful!")
            print("Welcome", r["student"]["name"])
            return sid
        else:
            print("Student ID not found. Please try again.")
            main()


def student_add_course(sid):
    print("\nADD COURSE")
    cid = input("Course ID: ")
    title = input("Title: ")
    credits = int(input("Credits: "))
    payload = {"course_id": cid, "title": title, "credits": credits, "student_id": sid}
    print(requests.post(API + "/student/add_course", json=payload).json())


def student_my_courses(sid):
    r = requests.get(API + "/student/my_courses", params={"student_id": sid}).json()
    print("\nMY COURSES:")
    for c in r["courses"]:
        print(c)


def student_update_course(sid):
    print("\nUPDATE COURSE")
    cid = input("Course ID: ")
    title = input("New title: ")
    credits = int(input("New credits: "))
    payload = {"course_id": cid, "title": title, "credits": credits, "student_id": sid}
    print(requests.put(API + "/student/update_course", json=payload).json())


def student_delete_course(sid):
    cid = input("Course ID to delete: ")
    print(
        requests.delete(
            API + "/student/delete_course",
            params={"course_id": cid, "student_id": sid},
        ).json()
    )


def student_menu():
    print("\nSTUDENT MENU")
    print("1. Add Course")
    print("2. My Courses")
    print("3. Update Course")
    print("4. Delete Course")
    print("5. Logout")


def student_panel():
    sid = student_login()
    while True:
        student_menu()
        c = input("Choice: ")
        if c == "1":
            student_add_course(sid)
        elif c == "2":
            student_my_courses(sid)
        elif c == "3":
            student_update_course(sid)
        elif c == "4":
            student_delete_course(sid)
        elif c == "5":
            break
        else:
            print("Invalid choice!")



def main():
    while True:
        print("\n=======================")
        print("      MAIN MENU")
        print("=======================")
        print("1. Admin Panel")
        print("2. Student Panel")
        print("3. Exit")

        choice = input("Choice: ")

        if choice == "1":
            admin_panel()
        elif choice == "2":
            student_panel()
        elif choice == "3":
            print("\nExiting system...")
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
