from pydantic import BaseModel


class PaymentSchema(BaseModel):
    card: int
    cvv: int


class RefundSchema(BaseModel):
    card: int
