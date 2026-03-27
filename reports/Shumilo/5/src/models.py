from sqlalchemy import Column, Integer, String, Boolean, Date, Numeric, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship
from db import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    inn = Column(String(12), unique=True)
    kpp = Column(String(9))
    created_at = Column(TIMESTAMP, server_default=func.now())

    documents = relationship("Document", back_populates="company")


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True)
    code = Column(String(20), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)

    debit_postings = relationship("Posting", foreign_keys="Posting.debit_account_id")
    credit_postings = relationship("Posting", foreign_keys="Posting.credit_account_id")


class Counterparty(Base):
    __tablename__ = "counterparties"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    inn = Column(String(12))
    kpp = Column(String(9))
    type = Column(String(20), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    documents = relationship("Document", back_populates="counterparty")


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    counterparty_id = Column(Integer, ForeignKey("counterparties.id"))
    doc_number = Column(String(50), nullable=False)
    doc_date = Column(Date, nullable=False)
    doc_type = Column(String(30), nullable=False)
    total_amount = Column(Numeric(14, 2), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    company = relationship("Company", back_populates="documents")
    counterparty = relationship("Counterparty", back_populates="documents")
    postings = relationship("Posting", back_populates="document")


class Posting(Base):
    __tablename__ = "postings"

    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    debit_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    credit_account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    amount = Column(Numeric(14, 2), nullable=False)
    description = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.now())

    document = relationship("Document", back_populates="postings")
