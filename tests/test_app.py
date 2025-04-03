import pytest
from app import app as dash_app
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def test_header_exists(dash_duo):
    dash_duo.start_server(dash_app)
    dash_duo.wait_for_element("#header", timeout=20)

def test_visualization_exists(dash_duo):
    dash_duo.start_server(dash_app)
    dash_duo.wait_for_element("#sales-chart", timeout=20)

def test_region_picker_exists(dash_duo):
    dash_duo.start_server(dash_app)
    dash_duo.wait_for_element("#region-filter", timeout=20)

def test_data_updates(dash_duo):
    dash_duo.start_server(dash_app)

    # Wait for initial render of the chart
    WebDriverWait(dash_duo.driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#sales-chart .js-plotly-plot"))
    )

    # Verify RadioItems are present
    WebDriverWait(dash_duo.driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[value='north']"))
    )

    # Click on North region filter
    north_radio = dash_duo.find_element("input[value='north']")
    north_radio.click()

    # Wait for chart update
    WebDriverWait(dash_duo.driver, 20).until(
        EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#sales-chart .gtitle"), "Sales Trend - North Region")
    )

    # Verify updated traces
    updated_traces = dash_duo.find_elements("#sales-chart .js-plotly-plot .scatterlayer .trace")
    assert len(updated_traces) > 0