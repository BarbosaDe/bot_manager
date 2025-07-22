import os
import uuid

import aiohttp

from database import Transaction


class Payment:
    @staticmethod
    async def create_qr(payer_id: int, server_id: int, price: int) -> dict:
        headers = {
            "x-idempotency-key": uuid.uuid4().hex,
            "Authorization": f"Bearer {os.getenv('MP_ACCESS_TOKEN')}",
        }
        payment_data = {
            "transaction_amount": price,
            "description": "lorem ipsom",
            "payment_method_id": "pix",
            "payer": {"email": "foo@gmail.com", "first_name": payer_id},
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

                await Transaction.create(
                    payer_id=payer_id,
                    price=price,
                    payment_id=payment_id,
                    server_id=server_id,
                )

                return {
                    "qr_code_base64": qr_code_base64,
                    "qr_code": qr_code_str,
                }

    @staticmethod
    async def get(payment_id: int) -> dict:
        headers = {
            "Authorization": f"Bearer {os.getenv('MP_ACCESS_TOKEN')}",
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.mercadopago.com/v1/payments/{payment_id}", headers=headers
            ) as response:
                return await response.json()
