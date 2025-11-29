from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class PaymentMethod(enum.Enum):
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    CASH = "cash"
    PAYPAL = "paypal"


class PaymentStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class Payment(Base):
    """Payment model implementing polymorphic payment interface"""
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    reservation_id = Column(Integer, ForeignKey("reservations.id"), nullable=False, index=True)
    amount = Column(Float, nullable=False)
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False, index=True)

    # Payment details (abstracted)
    transaction_id = Column(String(255), unique=True, index=True)
    payment_details = Column(String(500))  # Encrypted card details or cash receipt info

    processed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    reservation = relationship("Reservation", back_populates="payments")

    # Polymorphic payment processing (abstraction)
    def process(self) -> bool:
        """Abstract payment processing interface"""
        if self.payment_method == PaymentMethod.CREDIT_CARD:
            return self._process_card_payment()
        elif self.payment_method == PaymentMethod.DEBIT_CARD:
            return self._process_card_payment()
        elif self.payment_method == PaymentMethod.CASH:
            return self._process_cash_payment()
        elif self.payment_method == PaymentMethod.PAYPAL:
            return self._process_paypal_payment()
        return False

    def _process_card_payment(self) -> bool:
        """Process card payment (simulated)"""
        self.status = PaymentStatus.PROCESSING
        # Simulate payment processing
        self.status = PaymentStatus.COMPLETED
        self.processed_at = datetime.utcnow()
        return True

    def _process_cash_payment(self) -> bool:
        """Process cash payment (simulated)"""
        self.status = PaymentStatus.COMPLETED
        self.processed_at = datetime.utcnow()
        return True

    def _process_paypal_payment(self) -> bool:
        """Process PayPal payment (simulated)"""
        self.status = PaymentStatus.PROCESSING
        # Simulate payment processing
        self.status = PaymentStatus.COMPLETED
        self.processed_at = datetime.utcnow()
        return True

    def refund(self) -> bool:
        """Refund payment"""
        if self.status == PaymentStatus.COMPLETED:
            self.status = PaymentStatus.REFUNDED
            return True
        return False
