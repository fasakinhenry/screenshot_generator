 #!/usr/bin/env python3

# NAME:
# MATRIC NO:
# DEPARTMENT:
# TITLE: STUDENT RESULT PROCESSING SYSTEM
# QUESTION NO: 1

class ResultProcessor:
    def __init__(self):
        self.results = []
        self.highest_score = 0
        self.lowest_score = 0

    def load(self, results: list):
        self.results.extend(results)

    def add_student(self):
        """Add a single student interactively."""
        name = input("Enter student name: ").strip()
        assignment = int(input("Enter assignment score (max 20): "))
        test = int(input("Enter test score (max 30): "))
        examination = int(input("Enter examination score (max 50): "))

        student = {
            "name": name,
            "assignment": assignment,
            "test": test,
            "examination": examination,
            "total": 0,
            "grade": "",
        }
        self.results.append(student)

    def process(self):
        """Calculate totals and grades for all students."""
        for item in self.results:
            total = item["assignment"] + item["test"] + item["examination"]
            item["total"] = total

            if total >= 70:
                item["grade"] = "A"
            elif total >= 60:
                item["grade"] = "B"
            elif total >= 50:
                item["grade"] = "C"
            elif total >= 45:
                item["grade"] = "D"
            elif total >= 40:
                item["grade"] = "E"
            else:
                item["grade"] = "F"

        self.highest_score = max(self.results, key=lambda x: x["total"])["total"]
        self.lowest_score = min(self.results, key=lambda x: x["total"])["total"]

    def display(self):
        """Display all results."""
        print("\n" + "=" * 50)
        print("       STUDENT RESULT REPORT")
        print("=" * 50)

        for item in self.results:
            
            print(f"\n  Name:  {item['name']}")
            print(f"  Assignment: {item['assignment']}")
            print(f"  Test:       {item['test']}")
            print(f"  Exam:       {item['examination']}")
            print(f"  Total:      {item['total']}")
            print(f"  Grade:      {item['grade']}")
            print("-" * 50)

        
        print("\n" + "=" * 50)
        print("       SUMMARY")
        print("=" * 50)
        print(f"  Total Students: {len(self.results)}")
        print(f"  Highest Score:  {self.highest_score}")
        print(f"  Lowest Score:   {self.lowest_score}")
        print(f"  Average Score:  {self.average_score:.2f}")
        print("=" * 50)

    @property
    def average_score(self) -> float:
        if not self.results:
            return 0
        return sum(x["total"] for x in self.results) / len(self.results)


if __name__ == "__main__":
    
    results = [
    {
        "name": "John Doe",
        "assignment": 18,
        "test": 25,
        "examination": 45,
        "total": 0,
        "grade": "",
    },
    {
        "name": "Jane Smith",
        "assignment": 15,
        "test": 20,
        "examination": 30,
        "total": 0,
        "grade": "",
    },
    {
        "name": "Bob Johnson",
        "assignment": 20,
        "test": 28,
        "examination": 48,
        "total": 0,
        "grade": "",
    },
    {
        "name": "Alice Brown",
        "assignment": 10,
        "test": 15,
        "examination": 10,
        "total": 0,
        "grade": "",
    },
    {
        "name": "Charlie Wilson",
        "assignment": 12,
        "test": 18,
        "examination": 25,
        "total": 0,
        "grade": "",
    },
    {
        "name": "Diana Prince",
        "assignment": 19,
        "test": 27,
        "examination": 42,
        "total": 0,
        "grade": "",
    },
    {
        "name": "Edward King",
        "assignment": 14,
        "test": 22,
        "examination": 35,
        "total": 0,
        "grade": "",
    },
    {
        "name": "Fiona Adams",
        "assignment": 16,
        "test": 19,
        "examination": 28,
        "total": 0,
        "grade": "",
    },
    {
        "name": "George Clark",
        "assignment": 8,
        "test": 12,
        "examination": 20,
        "total": 0,
        "grade": "",
    },
    {
        "name": "Hannah Davis",
        "assignment": 17,
        "test": 26,
        "examination": 40,
        "total": 0,
        "grade": "",
    },
]

    processor = ResultProcessor()
    processor.load(results)
    processor.process()
    processor.display()