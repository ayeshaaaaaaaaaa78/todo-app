import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

BASE_URL = "http://127.0.0.1:5000"

def get_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    return driver

class TestTodoApp(unittest.TestCase):

    def setUp(self):
        self.driver = get_driver()
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def test_01_page_loads(self):
        self.driver.get(BASE_URL)
        self.assertIn("Todo", self.driver.title)

    def test_02_page_heading(self):
        self.driver.get(BASE_URL)
        h1 = self.driver.find_element(By.TAG_NAME, "h1")
        self.assertEqual(h1.text, "My Todo List")

    def test_03_input_field_present(self):
        self.driver.get(BASE_URL)
        input_field = self.driver.find_element(By.ID, "title")
        self.assertTrue(input_field.is_displayed())

    def test_04_add_button_present(self):
        self.driver.get(BASE_URL)
        btn = self.driver.find_element(By.ID, "add-btn")
        self.assertTrue(btn.is_displayed())

    def test_05_add_task(self):
        self.driver.get(BASE_URL)
        self.driver.find_element(By.ID, "title").send_keys("Test Task One")
        self.driver.find_element(By.ID, "add-btn").click()
        time.sleep(1)
        body = self.driver.find_element(By.TAG_NAME, "body").text
        self.assertIn("Test Task One", body)

    def test_06_add_multiple_tasks(self):
        self.driver.get(BASE_URL)
        for task in ["Task A", "Task B", "Task C"]:
            self.driver.find_element(By.ID, "title").send_keys(task)
            self.driver.find_element(By.ID, "add-btn").click()
            time.sleep(0.5)
        body = self.driver.find_element(By.TAG_NAME, "body").text
        self.assertIn("Task A", body)
        self.assertIn("Task B", body)
        self.assertIn("Task C", body)

    def test_07_empty_task_not_added(self):
        self.driver.get(BASE_URL)
        before = self.driver.find_element(By.TAG_NAME, "body").text
        self.driver.find_element(By.ID, "add-btn").click()
        time.sleep(1)
        after = self.driver.find_element(By.TAG_NAME, "body").text
        self.assertEqual(before, after)

    def test_08_complete_task(self):
        self.driver.get(BASE_URL)
        self.driver.find_element(By.ID, "title").send_keys("Task To Complete")
        self.driver.find_element(By.ID, "add-btn").click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, "Complete").click()
        time.sleep(1)
        body = self.driver.find_element(By.TAG_NAME, "body").text
        self.assertIn("Undo", body)

    def test_09_undo_task(self):
        self.driver.get(BASE_URL)
        self.driver.find_element(By.ID, "title").send_keys("Task To Undo")
        self.driver.find_element(By.ID, "add-btn").click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, "Complete").click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, "Undo").click()
        time.sleep(1)
        body = self.driver.find_element(By.TAG_NAME, "body").text
        self.assertIn("Complete", body)

    def test_10_delete_task(self):
        import time as t
        unique = "DeleteMe" + str(int(t.time()))
        self.driver.get(BASE_URL)
        self.driver.find_element(By.ID, "title").send_keys(unique)
        self.driver.find_element(By.ID, "add-btn").click()
        time.sleep(1)
        delete_links = self.driver.find_elements(By.LINK_TEXT, "Delete")
        delete_links[-1].click()
        time.sleep(1)
        body = self.driver.find_element(By.TAG_NAME, "body").text
        self.assertNotIn(unique, body)

    def test_11_edit_link_present(self):
        self.driver.get(BASE_URL)
        self.driver.find_element(By.ID, "title").send_keys("Task To Edit")
        self.driver.find_element(By.ID, "add-btn").click()
        time.sleep(1)
        edit_link = self.driver.find_element(By.LINK_TEXT, "Edit")
        self.assertTrue(edit_link.is_displayed())

    def test_12_edit_page_loads(self):
        self.driver.get(BASE_URL)
        self.driver.find_element(By.ID, "title").send_keys("Editable Task")
        self.driver.find_element(By.ID, "add-btn").click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, "Edit").click()
        time.sleep(1)
        self.assertIn("Edit", self.driver.title)

    def test_13_edit_task(self):
        self.driver.get(BASE_URL)
        self.driver.find_element(By.ID, "title").send_keys("Old Task Name")
        self.driver.find_element(By.ID, "add-btn").click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, "Edit").click()
        time.sleep(1)
        edit_input = self.driver.find_element(By.ID, "edit-title")
        edit_input.clear()
        edit_input.send_keys("New Task Name")
        self.driver.find_element(By.ID, "save-btn").click()
        time.sleep(1)
        body = self.driver.find_element(By.TAG_NAME, "body").text
        self.assertIn("New Task Name", body)

    def test_14_cancel_edit(self):
        self.driver.get(BASE_URL)
        self.driver.find_element(By.ID, "title").send_keys("Cancel Test Task")
        self.driver.find_element(By.ID, "add-btn").click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, "Edit").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "cancel-btn").click()
        time.sleep(1)
        self.assertEqual(self.driver.current_url, BASE_URL + "/")

    def test_15_todo_list_present(self):
        self.driver.get(BASE_URL)
        todo_list = self.driver.find_element(By.ID, "todo-list")
        self.assertTrue(todo_list.is_displayed())

if __name__ == "__main__":
    unittest.main()