from src.reports import spending_by_category


def test_spending_by_category_category(example_data):
    """Тест фильтрации по категории"""
    result = spending_by_category(example_data, category="Еда", date="01.12.2024 00:00:00")
    assert result
    assert "Еда" in result


def test_spending_by_category_no_date(example_data):
    """Тест, когда дата не передана (по умолчанию используется текущая дата)"""
    result = spending_by_category(example_data, category="Еда")
    assert result


def test_spending_by_category_negative_amount(example_data):
    """Тест на корректную работу с суммами"""
    result = spending_by_category(example_data, category="Еда", date="05.12.2024 16:00:00")
    assert result.count("-200") == 1
