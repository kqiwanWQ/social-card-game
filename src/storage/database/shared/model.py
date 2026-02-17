from sqlalchemy import BigInteger, Boolean, Column, DateTime, Double, ForeignKey, Integer, Numeric, PrimaryKeyConstraint, String, Table, Text, text
from sqlalchemy.dialects.postgresql import OID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
import datetime
from coze_coding_dev_sdk.database import Base
from sqlalchemy import func

from sqlalchemy import BigInteger, Boolean, Column, DateTime, Double, Integer, Numeric, PrimaryKeyConstraint, Table, Text, text
from sqlalchemy.dialects.postgresql import OID
from typing import Optional
import datetime

from sqlalchemy.orm import Mapped, mapped_column

class HealthCheck(Base):
    __tablename__ = 'health_check'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='health_check_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), server_default=text('now()'))


t_pg_stat_statements = Table(
    'pg_stat_statements', Base.metadata,
    Column('userid', OID),
    Column('dbid', OID),
    Column('toplevel', Boolean),
    Column('queryid', BigInteger),
    Column('query', Text),
    Column('plans', BigInteger),
    Column('total_plan_time', Double(53)),
    Column('min_plan_time', Double(53)),
    Column('max_plan_time', Double(53)),
    Column('mean_plan_time', Double(53)),
    Column('stddev_plan_time', Double(53)),
    Column('calls', BigInteger),
    Column('total_exec_time', Double(53)),
    Column('min_exec_time', Double(53)),
    Column('max_exec_time', Double(53)),
    Column('mean_exec_time', Double(53)),
    Column('stddev_exec_time', Double(53)),
    Column('rows', BigInteger),
    Column('shared_blks_hit', BigInteger),
    Column('shared_blks_read', BigInteger),
    Column('shared_blks_dirtied', BigInteger),
    Column('shared_blks_written', BigInteger),
    Column('local_blks_hit', BigInteger),
    Column('local_blks_read', BigInteger),
    Column('local_blks_dirtied', BigInteger),
    Column('local_blks_written', BigInteger),
    Column('temp_blks_read', BigInteger),
    Column('temp_blks_written', BigInteger),
    Column('shared_blk_read_time', Double(53)),
    Column('shared_blk_write_time', Double(53)),
    Column('local_blk_read_time', Double(53)),
    Column('local_blk_write_time', Double(53)),
    Column('temp_blk_read_time', Double(53)),
    Column('temp_blk_write_time', Double(53)),
    Column('wal_records', BigInteger),
    Column('wal_fpi', BigInteger),
    Column('wal_bytes', Numeric),
    Column('jit_functions', BigInteger),
    Column('jit_generation_time', Double(53)),
    Column('jit_inlining_count', BigInteger),
    Column('jit_inlining_time', Double(53)),
    Column('jit_optimization_count', BigInteger),
    Column('jit_optimization_time', Double(53)),
    Column('jit_emission_count', BigInteger),
    Column('jit_emission_time', Double(53)),
    Column('jit_deform_count', BigInteger),
    Column('jit_deform_time', Double(53)),
    Column('stats_since', DateTime(True)),
    Column('minmax_stats_since', DateTime(True))
)


t_pg_stat_statements_info = Table(
    'pg_stat_statements_info', Base.metadata,
    Column('dealloc', BigInteger),
    Column('stats_reset', DateTime(True))
)

# AI社交模拟卡牌游戏相关表

class Card(Base):
    """卡牌人物信息表"""
    __tablename__ = 'cards'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='cards_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="卡牌ID")
    photo_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, comment="照片URL")
    name: Mapped[str] = mapped_column(String(100), nullable=False, comment="姓名")
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True, comment="年龄")
    gender: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, comment="性别")
    occupation: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="职业")
    personality: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="性格(<100字)")
    ability: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="能力(<100字)")
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="个人简介(<200字)")
    network: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="人脉关系(<200字)")
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=func.now(), nullable=False, comment="创建时间")
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(True), onupdate=func.now(), nullable=True, comment="更新时间")

    # 关系
    interactions: Mapped[list["Interaction"]] = relationship("Interaction", back_populates="card", cascade="all, delete-orphan")
    strategy_reports: Mapped[list["StrategyReport"]] = relationship("StrategyReport", back_populates="card", cascade="all, delete-orphan")


class Interaction(Base):
    """互动记录表"""
    __tablename__ = 'interactions'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='interactions_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="互动记录ID")
    card_id: Mapped[int] = mapped_column(Integer, ForeignKey("cards.id", ondelete="CASCADE"), nullable=False, comment="关联卡牌ID")
    interaction_content: Mapped[str] = mapped_column(Text, nullable=False, comment="互动内容")
    interaction_date: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=func.now(), nullable=False, comment="互动日期")
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=func.now(), nullable=False, comment="创建时间")

    # 关系
    card: Mapped["Card"] = relationship("Card", back_populates="interactions")


class StrategyReport(Base):
    """社交策略报告表"""
    __tablename__ = 'strategy_reports'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='strategy_reports_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="策略报告ID")
    card_id: Mapped[int] = mapped_column(Integer, ForeignKey("cards.id", ondelete="CASCADE"), nullable=False, comment="关联卡牌ID")
    current_evaluation: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="当前评价")
    future_strategy: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="今后策略")
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(True), server_default=func.now(), nullable=False, comment="创建时间")

    # 关系
    card: Mapped["Card"] = relationship("Card", back_populates="strategy_reports")
