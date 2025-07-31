import os
import uuid
from abc import ABC, abstractmethod

import aiohttp

from database.models import Plan, Transaction
from database.repository import TransactionRepository


class BasePayment(ABC):
    @abstractmethod
    async def create(self, payer: int, server_id: int, plan: Plan) -> dict: ...

    @abstractmethod
    async def get(self, payment_id: int) -> dict: ...


class MercadoPagoDriver(BasePayment):
    async def create(self, payer_id: int, server_id: int, plan: Plan) -> dict:
        headers = {
            "x-idempotency-key": uuid.uuid4().hex,
            "Authorization": f"Bearer {os.getenv('MP_ACCESS_TOKEN')}",
        }
        payment_data = {
            "transaction_amount": plan.price,
            "description": "lorem ipsom",
            "payment_method_id": "pix",
            "payer": {"email": "foo@gmail.com"},
            "notification_url": os.getenv("WEBHOOK_URL"),
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.mercadopago.com/v1/payments",
                headers=headers,
                json=payment_data,
            ) as resp:
                response = await resp.json()

                payment_id = response["id"]

                qr_code_base64 = response["point_of_interaction"]["transaction_data"][
                    "qr_code_base64"
                ]

                qr_code_str = response["point_of_interaction"]["transaction_data"][
                    "qr_code"
                ]

                transaction = Transaction(
                    payment_id=payment_id,
                    payer_id=payer_id,
                    server_id=server_id,
                    plan=plan.id,
                    price=plan.price,
                )

                await TransactionRepository.insert(transaction)

                return {
                    "qr_code_base64": qr_code_base64,
                    "qr_code": qr_code_str,
                }

    async def get(self, payment_id: int) -> dict:
        headers = {
            "Authorization": f"Bearer {os.getenv('MP_ACCESS_TOKEN')}",
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.mercadopago.com/v1/payments/{payment_id}", headers=headers
            ) as response:
                return await response.json()


class PaymentService:
    def __init__(self, service: BasePayment):
        self.service = service

    async def create(self, payer: int, server_id: int, plan: Plan):
        return await self.service.create(payer, server_id, plan)

    async def get(self, payment_id: int):
        return await self.service.get(payment_id)


payment_service = PaymentService(MercadoPagoDriver())
