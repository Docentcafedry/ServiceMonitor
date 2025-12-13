from .conftest import client
from backend.db import add_domain_to_database


async def test_get_domains_empty(db_session):
    """
    GET /domains → empty list
    """
    res = client.get("/domains")
    assert res.status_code == 200
    assert res.json() == []


async def test_post_domain_success(db_session):
    """
    POST /add_domain → successfully add domain
    """
    res = client.post("/add_domain", json={"domain": "https://www.google.com/"})

    assert res.status_code == 201
    body = res.json()
    assert body["domain"] == "https://www.google.com/"
    assert "id" in body


async def test_post_domain_duplicate(db_session):
    """
    POST /add_domain → adding same domain twice raises error
    """
    await add_domain_to_database("https://www.google.com/", db_session)

    res = client.post("/add_domain", json={"domain": "https://www.google.com/"})

    assert res.status_code == 400
    assert res.json()["detail"] == "Domain already exists"


async def test_get_domains_nonempty(db_session):
    """
    GET /domains → returns existing domains
    """
    await add_domain_to_database("https://www.google.com/", db_session)

    res = client.get("/domains")

    assert res.status_code == 200
    body = res.json()

    assert isinstance(body, list)
    assert body[0]["domain"] == "google.com"


async def test_get_examinations_not_found(db_session):
    """
    GET /examinations/{domain} → domain does not exist
    """
    res = client.get("/examinations/some-domain.com")

    assert res.status_code == 404
    assert res.json()["detail"] == "Domain not found"


async def test_get_examinations_success(db_session):
    """
    GET /examinations/{domain} → returns domain + examinations
    """

    # create domain
    domain = await add_domain_to_database("https://www.google.com/", db_session)

    # add exam manually
    from backend.db import Examination as ExamModel
    import datetime

    exam = ExamModel(
        status_code=200,
        examination_time=datetime.datetime.now(),
        response_time=datetime.timedelta(milliseconds=200),
        domain_id=domain.id,
    )

    db_session.add(exam)
    await db_session.commit()

    res = client.get("/examinations/google.com")

    assert res.status_code == 200

    body = res.json()
    assert body["domain"] == "https://www.google.com/" or "google.com"
    assert len(body["examinations"]) == 1
    assert body["examinations"][0]["status_code"] == 200
