import os

from sqlalchemy import (
    CheckConstraint,
    Column,
    Date,
    ForeignKey,
    Integer,
    Text,
    create_engine,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()


class Admin(Base):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    company = Column(Text, nullable=False)

    managers = relationship("Manager", back_populates="admin")


class Manager(Base):
    __tablename__ = "manager"

    id = Column(Integer, primary_key=True)
    admin_id = Column(Integer, ForeignKey("admin.id"), nullable=False, index=True)
    name = Column(Text, nullable=False)

    admin = relationship("Admin", back_populates="managers")
    learners = relationship("Learner", back_populates="manager")


class Learner(Base):
    __tablename__ = "learner"

    id = Column(Integer, primary_key=True)
    manager_id = Column(Integer, ForeignKey("manager.id"), nullable=False, index=True)
    name = Column(Text, nullable=False)

    manager = relationship("Manager", back_populates="learners")
    plans = relationship("Plan", back_populates="learner")
    check_ins = relationship("CheckIn", back_populates="learner")


class Plan(Base):
    __tablename__ = "plan"

    id = Column(Integer, primary_key=True)
    learner_id = Column(Integer, ForeignKey("learner.id"), nullable=False, index=True)
    text = Column(Text, nullable=False)
    date_created = Column(Date, nullable=False, server_default="CURRENT_DATE")
    status = Column(Text, nullable=False, server_default="active")
    source = Column(Text, nullable=False)

    __table_args__ = (
        CheckConstraint("status IN ('active', 'completed', 'abandoned')", name="plan_status_check"),
        CheckConstraint("source IN ('curated', 'ai_suggested')", name="plan_source_check"),
    )

    learner = relationship("Learner", back_populates="plans")
    check_ins = relationship("CheckIn", back_populates="plan")


class CheckIn(Base):
    __tablename__ = "check_in"

    id = Column(Integer, primary_key=True)
    learner_id = Column(Integer, ForeignKey("learner.id"), nullable=False, index=True)
    plan_id = Column(Integer, ForeignKey("plan.id"), nullable=False, index=True)
    date = Column(Date, nullable=False, server_default="CURRENT_DATE")
    score = Column(Integer, nullable=False)
    comment = Column(Text)

    __table_args__ = (
        CheckConstraint("score BETWEEN 1 AND 5", name="check_in_score_check"),
    )

    learner = relationship("Learner", back_populates="check_ins")
    plan = relationship("Plan", back_populates="check_ins")


def get_engine():
    return create_engine(
        os.environ["DATABASE_URL"],
        pool_pre_ping=True,
        pool_recycle=300,
    )


def get_session():
    return sessionmaker(bind=get_engine())()
