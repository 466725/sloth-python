import pytest


# Test Amazon homepage begins here
@pytest.mark.ui
def test_homepage(selenium):
    my_elenium.get("https://www.amazon.com/")
    print(my_elenium.title)
    print(my_elenium.page_source)
    assert my_elenium.title != None
