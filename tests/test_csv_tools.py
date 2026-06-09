import pytest
import mcp_server.src.tools.csv_tools as csv_tools


@pytest.fixture(autouse=True)
def reset_df():
    csv_tools._df = None


@pytest.fixture
def loaded_csv(tmp_path):
    # Create a small CSV file in tmp_path
    csv_file = tmp_path / "test_query.csv"
    csv_file.write_text(
        "age,running,colour\nAdult,True,Black\nAdult,False,Red\nYoung,False,Red\nYoung,True,Grey"
    )

    # Call load_csv to load csv file
    csv_tools.load_csv(str(csv_file))

    return csv_file


# Test 1
def test_load_csv_valid_file(tmp_path):
    # Create a small CSV file in tmp_path
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("name,age\nAlice,30\nBob,25")

    # Call load_csv with file path
    result = csv_tools.load_csv(str(csv_file))

    # Assert the results contain what we expect
    assert "2 rows" in result
    assert "2 columns" in result


# Test 2
def test_load_csv_file_not_found():
    # call load_csv with non existent file path
    result = csv_tools.load_csv("/nonexistent/path/file.csv")

    # Assert the result contains the error message we expect
    assert "Error: file not found" in result


# Test 3
def test_query_data_before_csv_loaded():
    # Call query_data with no csv file
    result = csv_tools.query_data("")

    # Assert the result contains error message we expect
    assert "Error: no CSV loaded. Call load_csv first." in result


# Test 4
# Query data with a valid filter
def test_query_data_with_valid_filter(loaded_csv):
    # Call query_data with file path
    result = csv_tools.query_data("running == True")

    # Assert the result contains what we expect
    assert "2 rows" in result
    assert "Adult" in result
    assert "Black" in result


# Test 5
# Query data with an invalid expression
def test_query_data_with_invalid_expression(loaded_csv):
    # Call query_data with invalid expression
    result = csv_tools.query_data("!!!!!")

    assert "Error" in result


# Test 6
# Call query_data that returns no matches
def test_query_data_with_no_matching_rows(loaded_csv):
    # Call query with no matching rows
    result = csv_tools.query_data("colour == 'Purple'")

    assert "No rows matched that query." in result
