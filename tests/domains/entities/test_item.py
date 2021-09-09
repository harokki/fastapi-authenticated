from app.domains.entities.item import Item


def test_initialize_item():
    item = Item(id=1234, title="title", description="description", owner_id=1234)

    assert item.id == 1234
    assert item.title == "title"
    assert item.description == "description"
    assert item.owner_id == 1234
    assert item.owner is None
