from sqlalchemy import (
    create_engine,
    Column,
    String,
    Integer,
    ForeignKey,
    DateTime,
    JSON,
    Boolean,
    Enum,
)
from sqlalchemy.orm import relationship, Session, declarative_base, sessionmaker
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime, UTC
import enum
import json
from typing import Dict, Any, Tuple
from pydantic import BaseModel

Base = declarative_base()

# directory specific


class ThomsonRecord(BaseModel):
    file_key: str
    other_data: Dict[str, Any]

    @classmethod
    def from_raw(cls, raw: dict) -> "ThomsonRecord":
        file_key = raw["file_key"]
        other_data = {k: v for k, v in raw.items() if k != "file_key"}
        return cls(file_key=file_key, other_data=other_data)

    def to_record_value(self) -> Dict[str, Any]:
        return {"file_key": self.file_key, **self.other_data}

    def diff(self, other: "ThomsonRecord") -> Dict[str, Tuple[Any, Any]]:
        return {
            k: (self.other_data.get(k), other.other_data.get(k))
            for k in set(self.other_data) | set(other.other_data)
            if self.other_data.get(k) != other.other_data.get(k)
        }


# ---------------- Models ----------------


class MarketRecord(Base):
    __tablename__ = "market_record"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    schema = Column(String)
    url_to_blob = Column(String)
    key_in_directory = Column(String)
    directory = Column(String)
    market_data_source = Column(String)
    record_id = Column(String)
    record_value = Column(JSON)

    node_market_records = relationship(
        "NodeMarketRecord", back_populates="market_record"
    )

    def as_dict(self) -> dict:
        """Convert this MarketRecord instance to a dictionary."""
        return {
            "id": str(self.id),
            "schema": self.schema,
            "url_to_blob": self.url_to_blob,
            "key_in_directory": self.key_in_directory,
            "directory": self.directory,
            "market_data_source": self.market_data_source,
            "record_id": str(self.record_id),
            "record_value": json.loads(str(self.record_value))
            if isinstance(self.record_value, dict)
            else self.record_value,
        }


class Node(Base):
    __tablename__ = "nodes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    country_code = Column(String, nullable=False)
    address = Column(JSON)
    institution_type = Column(String, nullable=True)
    office_type = Column(String, nullable=True)

    market_records = relationship("NodeMarketRecord", back_populates="node")
    external_identifiers = relationship("ExternalIdentifiers", back_populates="node")

    cre_time = Column(DateTime, nullable=True)
    mod_time = Column(DateTime, nullable=True)
    del_time = Column(DateTime, nullable=True)
    mod_user = Column(String, nullable=True)
    manual_override = Column(Boolean, default=False)


class NodeMarketRecord(Base):
    __tablename__ = "node_market_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    node_id = Column(UUID(as_uuid=True), ForeignKey("nodes.id"))
    market_record_id = Column(UUID(as_uuid=True), ForeignKey("market_record.id"))

    node = relationship("Node", back_populates="market_records")
    market_record = relationship("MarketRecord", back_populates="node_market_records")


class IdentifiersType(Base):
    __tablename__ = "identifiers_types"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String, nullable=False)
    attributes = Column(JSON)


class ExternalIdentifiers(Base):
    __tablename__ = "external_identifiers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    node_id = Column(UUID(as_uuid=True), ForeignKey("nodes.id"))
    value = Column(String)
    identifier_type_id = Column(UUID(as_uuid=True), ForeignKey("identifiers_types.id"))
    attributes = Column(JSON, nullable=True)

    node = relationship("Node", back_populates="external_identifiers")
    identifier_type = relationship("IdentifiersType")


class NodeRelationship(Base):
    __tablename__ = "node_relationships"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    from_node_id = Column(UUID(as_uuid=True), ForeignKey("nodes.id"))
    to_node_id = Column(UUID(as_uuid=True), ForeignKey("nodes.id"))

    from_node = relationship("Node", foreign_keys=[from_node_id])
    to_node = relationship("Node", foreign_keys=[to_node_id])

    features = relationship("RelationshipFeatures", back_populates="node_relationship")


class RelationshipFeatures(Base):
    __tablename__ = "relationship_features"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    node_relationship_id = Column(
        UUID(as_uuid=True), ForeignKey("node_relationships.id")
    )
    routing_number = Column(String, nullable=False)
    currency = Column(String, nullable=False)
    relation_code = Column(String, nullable=False)
    relation = Column(String, nullable=False)
    attributes = Column(JSON)

    node_relationship = relationship("NodeRelationship", back_populates="features")


### staing


class ActionType(enum.Enum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


class Status(enum.Enum):
    INITIATED = "initiated"
    PENDING_REVIEW = "pending review"
    UNDER_REVIEW = "under review"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class ChangeSource(enum.Enum):
    THOMPON = "THOMSON"
    IDALL = "IDALL"
    USER = "USER"


# The staging area table: each change (like a Git commit) is recorded here.
class Staging(Base):
    __tablename__ = "staging"
    id = Column(Integer, primary_key=True)
    changeset_id = Column(String, nullable=False)
    record_id = Column(String, nullable=False)
    directory = Column(String, nullable=False)
    action = Column(Enum(ActionType), nullable=False)
    market_record_json_new = Column(JSON, nullable=True)
    market_record_json_gs = Column(JSON, nullable=True)
    change_source = Column(Enum(ChangeSource), nullable=False)
    status = Column(Enum(Status), default=Status.INITIATED, nullable=False)
    business_justification = Column(String, nullable=True)
    revision = Column(Integer, default=1, nullable=False)
    created_by = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now(UTC), nullable=False)
