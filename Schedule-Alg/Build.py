import csv
import PDF_Scraper
import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

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
    
def search_igps_courses(search_term, subject=None, headless=True):
    """
    Search for courses on IU's iGPS website and return results
    Specifically for IU Bloomington campus and Fall 2025 term only
    
    Parameters:
    -----------
    search_term : str
        The search term to look for in course offerings
    subject : str, optional
        Subject area to filter by (e.g., 'CSCI' for Computer Science)
    headless : bool, default=True
        Whether to run browser in headless mode
        
    Returns:
    --------
    DataFrame containing course search results
    """
    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    
    # Navigate to iGPS search page
    # Note: You'll need to replace this URL with the actual iGPS URL
    driver.get("https://sisjee.iu.edu/sisigps-prd/web/igps/course/search/")
    
    try:
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search-term"))  # Assuming there's a search box with this ID
        )
        
        # Fill in search fields
        search_box = driver.find_element(By.ID, "search-term")
        search_box.clear()
        search_box.send_keys(search_term)
        
        # Set campus to IU Bloomington (automatically)
        campus_dropdown = driver.find_element(By.ID, "campus-select")  # Replace with actual ID
        # Select Bloomington option
        # This might need to be adjusted based on actual dropdown structure
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "campus-select"))
        )
        campus_dropdown.click()
        bloomington_option = driver.find_element(By.XPATH, "//option[contains(text(), 'Bloomington')]")
        bloomington_option.click()
        
        # Set term to Fall 2025 (automatically)
        term_dropdown = driver.find_element(By.ID, "term-select")  # Replace with actual ID
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "term-select"))
        )
        term_dropdown.click()
        fall_option = driver.find_element(By.XPATH, "//option[contains(text(), 'Fall 2025')]")
        fall_option.click()
        
        # Select subject if provided
        if subject:
            subject_dropdown = driver.find_element(By.ID, "subject-select")  # Replace with actual ID
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "subject-select"))
            )
            subject_dropdown.click()
            subject_option = driver.find_element(By.XPATH, f"//option[contains(text(), '{subject}')]")
            subject_option.click()
        
        # Submit search
        search_box.send_keys(Keys.RETURN)
        
        # Wait for results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "search-results"))  # Replace with actual class name
        )
        
        # Extract search results
        page_html = driver.page_source
        soup = BeautifulSoup(page_html, 'html.parser')
        
        # Parse results - this will depend on the actual structure of the results page
        results = []
        for course in soup.find_all('div', class_='course-item'):  # Replace with actual class
            course_data = {
                'title': course.find('h3').text.strip(),
                'code': course.find('span', class_='course-code').text.strip(),
                'credits': course.find('span', class_='credits').text.strip(),
                # No instructor name as specified
                'schedule': course.find('div', class_='schedule').text.strip(),
                'availability': course.find('div', class_='availability').text.strip()
            }
            results.append(course_data)
        
        # Convert results to DataFrame
        df = pd.DataFrame(results)
        return df
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
    finally:
        # Close the browser
        driver.quit()

def build_logic(txt):
    rqmts = PDF_Scraper.get_requirements(txt)

if __name__ == "__main__":
    # Search for Computer Science courses
    results = search_igps_courses(
        search_term="data structures",
        campus="Bloomington",
        term="Fall 2025",
        subject="CSCI"
    )

    if results is not None and not results.empty:
        print(f"Found {len(results)} courses:")
        print(results)
    else:
        print("No results found or an error occurred.")