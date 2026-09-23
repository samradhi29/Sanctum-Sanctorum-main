class TestOrderMixedRestrictedItems:
    def test_one_restricted_item_blocks_whole_order(self, client, make_member, make_book):
        member = make_member(tier="apprentice")
        normal_book = make_book(restricted=False)
        restricted_book = make_book(restricted=True)
        body = {
            "member_id": member["id"],
            "items": [
                {"book_id": normal_book["id"], "quantity": 1},
                {"book_id": restricted_book["id"], "quantity": 1},
            ],
        }
        response = client.post("/orders", json=body)
        assert response.status_code == 403
        assert client.get(f"/books/{normal_book['id']}").json()["stock"] == 10


class TestBookSearchWildcardEscaping:
    def test_percent_in_query_is_treated_literally(self, client, make_book):
        make_book(title="100% Magic")
        make_book(title="Totally Unrelated")
        response = client.get("/books", params={"q": "100%"})
        assert response.json()["total"] == 1


class TestPatchEmptyBody:
    def test_empty_patch_body_changes_nothing(self, client, make_book):
        book = make_book()
        response = client.patch(f"/books/{book['id']}", json={})
        assert response.status_code == 200
        assert response.json() == book


# class TestMemberPagination:
#     def test_total_reflects_all_members_not_just_page(self, client, make_member):
#         for _ in range(5):
#             make_member()
#         response = client.get("/members", params={"limit": 2, "offset": 0})
#         assert response.status_code == 200
#         body = response.json()
#         assert len(body["items"]) == 2
#         assert body["total"] >= 5


class TestCancelOrderStockRestore:
    def test_cancel_restores_exact_stock(self, client, make_member, make_book):
        book = make_book(stock=10)
        member = make_member()
        body = {"member_id": member["id"], "items": [{"book_id": book["id"], "quantity": 4}]}
        order = client.post("/orders", json=body).json()

        assert client.get(f"/books/{book['id']}").json()["stock"] == 6

        cancel_response = client.post(f"/orders/{order['id']}/cancel")
        assert cancel_response.status_code == 200
        assert client.get(f"/books/{book['id']}").json()["stock"] == 10