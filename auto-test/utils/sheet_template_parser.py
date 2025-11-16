def parse_input_string(input_str):
    """
    Parse chuỗi input từ Google Sheet thành dictionary

    Format: "action: param1=value1, param2=value2"
    Example: "login: username=test@gmail.com, password=123456"

    Returns:
        dict: {
            'action': 'login',
            'params': {
                'username': 'test@gmail.com',
                'password': '123456'
            }
        }
    """
    if not input_str or ':' not in input_str:
        return None

    # Split action và parameters
    parts = input_str.split(':', 1)
    action = parts[0].strip()
    params_str = parts[1].strip() if len(parts) > 1 else ''

    # Parse parameters
    params = {}
    if params_str:
        # Handle list values: products=[iPhone,Samsung]
        if '[' in params_str and ']' in params_str:
            for item in params_str.split(','):
                if '=' in item:
                    key, value = item.split('=', 1)
                    key = key.strip()
                    value = value.strip()

                    # Parse list values
                    if value.startswith('[') and value.endswith(']'):
                        value = [v.strip() for v in value[1:-1].split(',')]

                    params[key] = value
        else:
            # Regular key=value pairs
            for param in params_str.split(','):
                if '=' in param:
                    key, value = param.split('=', 1)
                    params[key.strip()] = value.strip()

    return {
        'action': action,
        'params': params
    }


def parse_sheet_to_test_cases(rows):
    """
    Parse Google Sheet rows thành list test cases

    Args:
        rows: List of rows from Google Sheet
        Format: [STT, Input, Output, Expected Result, Result, Phân loại chức năng, Mức độ, Status, Round]

    Returns:
        list: List of test case dictionaries
    """
    test_cases = []

    # Skip header row
    for row in rows[1:]:
        if len(row) < 9:
            continue

        stt, input_str, output, expected, result, function_type, priority, status, round_num = row[:9]

        # Skip empty rows
        if not input_str.strip():
            continue

        parsed_input = parse_input_string(input_str)
        if not parsed_input:
            continue

        test_case = {
            'stt': stt,
            'action': parsed_input['action'],
            'params': parsed_input['params'],
            'expected_result': expected.strip(),
            'function_type': function_type.strip(),
            'priority': priority.strip(),
            'round': round_num.strip() if round_num else '1',
            'row_index': rows.index(row) + 1  # For updating back to sheet
        }

        test_cases.append(test_case)

    return test_cases


def group_test_cases_by_action(test_cases):
    """
    Group test cases theo action để dễ xử lý

    Returns:
        dict: {
            'login': [...],
            'add_to_cart': [...],
            'checkout': [...]
        }
    """
    grouped = {}
    for tc in test_cases:
        action = tc['action']
        if action not in grouped:
            grouped[action] = []
        grouped[action].append(tc)

    return grouped


class TestResultWriter:
    """Class để ghi kết quả test về Google Sheet"""

    def __init__(self, worksheet):
        self.worksheet = worksheet
        self.results = []

    def add_result(self, row_index, output, result_status):
        """
        Thêm kết quả test

        Args:
            row_index: Index của row trong sheet (1-based)
            output: Actual output từ test
            result_status: PASS/FAIL/BLOCKED/SKIP
        """
        self.results.append({
            'row': row_index,
            'output': output,
            'status': result_status
        })

    def write_results(self):
        """Ghi tất cả kết quả về Google Sheet"""
        for result in self.results:
            row = result['row']

            # Column C (3) = Output, Column E (5) = Result, Column H (8) = Status
            self.worksheet.update_cell(row, 3, result['output'])  # Output
            self.worksheet.update_cell(row, 5, result['status'])  # Result
            self.worksheet.update_cell(row, 8, result['status'])  # Status

            # Set background color based on status
            if result['status'] == 'PASS':
                self._set_cell_color(row, 5, (0.7, 1.0, 0.7))  # Light green
                self._set_cell_color(row, 8, (0.7, 1.0, 0.7))
            elif result['status'] == 'FAIL':
                self._set_cell_color(row, 5, (1.0, 0.7, 0.7))  # Light red
                self._set_cell_color(row, 8, (1.0, 0.7, 0.7))
            elif result['status'] == 'BLOCKED':
                self._set_cell_color(row, 5, (1.0, 1.0, 0.7))  # Light yellow
                self._set_cell_color(row, 8, (1.0, 1.0, 0.7))

    def _set_cell_color(self, row, col, rgb):
        """Set màu nền cho cell"""
        try:
            self.worksheet.format(
                f"{chr(64 + col)}{row}",
                {
                    "backgroundColor": {
                        "red": rgb[0],
                        "green": rgb[1],
                        "blue": rgb[2]
                    }
                }
            )
        except Exception as e:
            print(f"Warning: Could not set cell color: {e}")


def create_test_summary(test_results):
    """
    Tạo summary từ kết quả test

    Args:
        test_results: List of test results

    Returns:
        dict: Summary statistics
    """
    total = len(test_results)
    passed = sum(1 for r in test_results if r.get('status') == 'PASS')
    failed = sum(1 for r in test_results if r.get('status') == 'FAIL')
    blocked = sum(1 for r in test_results if r.get('status') == 'BLOCKED')
    skipped = sum(1 for r in test_results if r.get('status') == 'SKIP')

    return {
        'total': total,
        'passed': passed,
        'failed': failed,
        'blocked': blocked,
        'skipped': skipped,
        'pass_rate': (passed / total * 100) if total > 0 else 0
    }


# Example usage:
"""
# Parse test cases from sheet
rows = worksheet.get_all_values()
test_cases = parse_sheet_to_test_cases(rows)
grouped_tests = group_test_cases_by_action(test_cases)

# Run tests and collect results
result_writer = TestResultWriter(worksheet)

for action, tests in grouped_tests.items():
    for test in tests:
        # Run test...
        actual_output = run_test(test)
        status = 'PASS' if actual_output == test['expected_result'] else 'FAIL'

        result_writer.add_result(
            row_index=test['row_index'],
            output=actual_output,
            result_status=status
        )

# Write all results back to sheet
result_writer.write_results()

# Print summary
summary = create_test_summary(result_writer.results)
print(f"Test Summary: {summary}")
"""
