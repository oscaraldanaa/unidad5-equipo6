from unittest.mock import Mock

import pytest

from src.application import OrderService
from src.domain import Order


def test_gateway_approved():
    gateway = Mock()
    gateway.charge.return_value = True
    assert OrderService(gateway).checkout(Order(100)) == 100
    gateway.charge.assert_called_once_with(100)

def test_gateway_rejected():
    gateway = Mock()
    gateway.charge.return_value = False
    with pytest.raises(RuntimeError):
        OrderService(gateway).checkout(Order(100))

def test_payment_rejected_vip_order():
    # Arrange: Configuramos el mock para que devuelva False (rechazado)
    gateway = Mock()
    gateway.charge.return_value = False
    
    service = OrderService(gateway)
    vip_order = Order(200, vip=True) # Pedido VIP de $200 -> cobra $170
    
    # Act & Assert: Verificamos que lance el RuntimeError y el monto exacto de la llamada
    with pytest.raises(RuntimeError, match="payment rejected"):
        service.checkout(vip_order)
        
    gateway.charge.assert_called_once_with(170)
