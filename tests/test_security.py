from datetime import UTC, datetime, timedelta

from src.security import can_cancel


def test_owner_within_24h():
    now = datetime.now(UTC)
    assert can_cancel("NEW", 1, 1, False, now - timedelta(hours=1), now)

def test_stranger_denied():
    now = datetime.now(UTC)
    assert not can_cancel("NEW", 1, 2, False, now, now)

def test_shipped_denied_even_admin():
    now = datetime.now(UTC)
    assert not can_cancel("SHIPPED", 1, 1, True, now, now)

def test_expired_denied():
    now = datetime.now(UTC)
    assert not can_cancel("NEW", 1, 1, False, now - timedelta(hours=25), now)



def test_admin_can_cancel_other_user_new():
    # Un administrador (is_admin=True) cancela un pedido NEW de otro usuario (user_id=2, owner_id=1)
    created = datetime(2026, 5, 1, 10, 0, 0, tzinfo=UTC)
    now = datetime(2026, 5, 1, 12, 0, 0, tzinfo=UTC)
    assert can_cancel("NEW", 2, 1, True, created, now)

def test_owner_cannot_cancel_at_exact_24_hours():
    # El propietario (user_id=1, owner_id=1) intenta cancelar exactamente a las 24 horas (is_admin=False)
    created = datetime(2026, 5, 1, 10, 0, 0, tzinfo=UTC)
    now = created + timedelta(hours=24)
    assert not can_cancel("NEW", 1, 1, False, created, now)