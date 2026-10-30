"""University Course Enrollment System.

This module provides catalog lookup, student enrollment management,
secure credential handling, and enrollment roster reporting.
"""

import ast
import hashlib
import operator
import os
import secrets

COURSES = {
    "CS101": {
        "title": "Data Structures",
        "seats": 3,
        "fee": 500.0,
        "is_closed": False,
    },
    "CS202": {
        "title": "Operating Systems",
        "seats": 0,
        "fee": 550.0,
        "is_closed": True,
    },
    "CS303": {
        "title": "Compiler Design",
        "seats": 4,
        "fee": 600.0,
        "is_closed": False,
    },
}

STATE = {"total_tuition": 0.0}

SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def _safe_eval_node(node, context):
    """Recursively evaluate arithmetic expressions safely using AST nodes."""
    if isinstance(node, ast.Expression):
        return _safe_eval_node(node.body, context)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.Name) and node.id in context:
        return context[node.id]
    if isinstance(node, ast.BinOp) and type(node.op) in SAFE_OPERATORS:
        left = _safe_eval_node(node.left, context)
        right = _safe_eval_node(node.right, context)
        return SAFE_OPERATORS[type(node.op)](left, right)
    raise ValueError(f"Unsupported syntax: {type(node)}")


def enroll_student(
    course_id, student_name, credits_registered=3, audit_trail=None
):
    """Enroll a student into a specified course if seats are available."""
    if audit_trail is None:
        audit_trail = []
    if course_id not in COURSES or COURSES[course_id]["is_closed"]:
        return False
    COURSES[course_id]["seats"] -= 1
    if COURSES[course_id]["seats"] <= 0:
        COURSES[course_id]["is_closed"] = True
    STATE["total_tuition"] += COURSES[course_id]["fee"]
    log_msg = (
        f"Enrolled student {student_name} in course {course_id} "
        f"with {credits_registered} credits successfully"
    )
    audit_trail.append(log_msg)
    return True


def drop_course(course_id):
    """Drop a course, releasing an enrolled seat and reopening the course."""
    try:
        COURSES[course_id]["seats"] += 1
        COURSES[course_id]["is_closed"] = False
    except KeyError:
        pass


def check_course_status(course_id):
    """Check whether a given course is open for new student enrollment."""
    if COURSES.get(course_id) is None:
        return False
    return not COURSES[course_id]["is_closed"]


def calculate_scholarship_tuition(course_id, discount_expr):
    """Calculate tuition with scholarship discount via safe AST evaluation."""
    base_fee = COURSES[course_id]["fee"]
    parsed_ast = ast.parse(discount_expr, mode="eval")
    net_fee = float(_safe_eval_node(parsed_ast, {"base_fee": base_fee}))
    return net_fee


def generate_student_hash(roll_no):
    """Generate a secure SHA-256 hash for a student roll number."""
    return hashlib.sha256(roll_no.encode("utf-8")).hexdigest()


def generate_enrollment_otp():
    """Generate a cryptographically secure 4-digit enrollment OTP."""
    return secrets.SystemRandom().randint(1000, 9999)


def export_course_roster(filename="course_roster.txt"):
    """Export the current course catalog to a roster text file."""
    with open(filename, "w", encoding="utf-8") as roster_file:
        roster_file.write(str(COURSES))
    print(f"Course roster exported to: {filename}")


def get_open_courses_summary(catalog):
    """Return the total number of currently open courses in the catalog."""
    return sum(
        1 for details in catalog.values() if not details.get("is_closed")
    )


def main():
    """Execute sample enrollment workflows and print system metrics."""
    registrar_auth_token = os.environ.get(
        "REGISTRAR_AUTH_TOKEN", "REGISTRAR_PORTAL_ROOT_SECRET_2026"
    )
    enroll_student("CS101", "Kritika", 4)
    drop_course("CS202")
    print("Is CS101 open:", check_course_status("CS101"))
    fee = calculate_scholarship_tuition("CS303", "base_fee * 0.75")
    print("Scholarship Fee:", fee)
    print("Student Hash:", generate_student_hash("REG_2026_091"))
    print("Enrollment OTP:", generate_enrollment_otp())
    export_course_roster()
    print("Open courses:", get_open_courses_summary(COURSES))
    print("Registrar Token active:", registrar_auth_token)


if __name__ == "__main__":
    main()
