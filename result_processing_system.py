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
    
    results = []
    for i in range(10):
        name = input('enter student name: ')
        score = [int(x.strip()) for x in input('enter scores (assignment,test,exam): ').split(',')]
        print('')
        results.append({
        "name": name,
        "assignment": score[0],
        "test": score[1],
        "examination": score[2],
        "total": 0,
        "grade": "",
    })

    processor = ResultProcessor()
    processor.load(results)
    processor.process()
    processor.display()