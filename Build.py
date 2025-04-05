import csv
import PDF_Scraper
import re

# finds and rates a class a difficulty score 1-10
def class_rater(class_code):
    with open('class_distribution.csv', mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        reader.fieldnames = [field.strip() for field in reader.fieldnames]  # strip spaces from headers

        target_code = re.sub(r'\s+', '', class_code).upper()

        for row in reader:
            subject = row.get("Course Subject", "").strip()
            catalog_number = row.get("Catalog Number", "").strip()

            full_code = f"{subject}{catalog_number}"
            full_code = re.sub(r'\s+', '', full_code).upper()

            if full_code == target_code:
                avg = row.get("Avg Class Grade", "").strip()
                other = row.get("All Other Grades #", "").strip()

                if avg in ("NR", "NOT AVAILABLE - SMALL CLASS SIZE") or \
                   other in ("NR", "NOT AVAILABLE - SMALL CLASS SIZE"):
                    return "Insufficient data"

                try:
                    avg_grade = float(avg)
                    other_grades = int(other)

                    grade_component = (4.0 - avg_grade) / 4.0
                    other_component = min(other_grades / 20, 1.0)

                    score = (0.7 * grade_component + 0.3 * other_component) * 10
                    return max(1, round(score, 1))


                except ValueError:
                    return "Invalid numeric format"

        return "Class Not Found"

if __name__ == "__main__":
    pdf_path = 'example.pdf'
    output_txt = 'example.txt'
    PDF_Scraper.pdf_to_text(pdf_path, output_txt)
    classes_taken = PDF_Scraper.get_classes(output_txt, "List of all courses taken", "F,X,I,W,P,R")
    unsuitable_classes = PDF_Scraper.get_classes(output_txt, "Unsuitable grades that do not fulfill requirements", "GPA, TOTAL HOURS AND 300/400 LEVEL COURSES (RG 11776)")
    for cls in classes_taken:
        if cls not in unsuitable_classes:
            print(f"{cls}: {class_rater(cls)}")
         