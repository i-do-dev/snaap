import uuid
from sqlalchemy import Column, String, Text, Numeric, ForeignKey, TIMESTAMP, text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.types import UUID
from src.adapters.db.base import Base

class User(Base):
    """SQLAlchemy User model"""

    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=False, unique=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)  # Hashed password stored
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


# ─── AMMS Models ────────────────────────────────────────────────────────────

class Ribbonway(Base):
    """SQLAlchemy model for snaap_ribbonways table"""

    __tablename__ = "snaap_ribbonways"
    rbn_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rbn_created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    rbn_name = Column(String, nullable=True)
    rbn_description = Column(Text, nullable=True)
    rbn_geofence_location = Column(JSON, nullable=True)
    # Relationships
    portals = relationship("RibbonwayPortal", back_populates="ribbonway")
    pods = relationship("Pod", back_populates="ribbonway")


class RibbonwayPortal(Base):
    """SQLAlchemy model for snaap_ribbonway_portals table"""

    __tablename__ = "snaap_ribbonway_portals"
    ptl_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ptl_created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    ptl_name = Column(String, nullable=True)
    ptl_description = Column(Text, nullable=True)
    ptl_geofence_location = Column(JSON, nullable=True)
    rbn_id = Column(UUID(as_uuid=True), ForeignKey("snaap_ribbonways.rbn_id"), nullable=True)
    # Relationships
    ribbonway = relationship("Ribbonway", back_populates="portals")
    docks = relationship("PortalDock", back_populates="portal")
    ride_requests = relationship("RideRequest", back_populates="portal")


class PortalDock(Base):
    """SQLAlchemy model for snaap_portal_docks table"""

    __tablename__ = "snaap_portal_docks"
    dck_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dck_created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    dck_name = Column(String, nullable=True)
    dck_description = Column(Text, nullable=True)
    dck_geofence_location = Column(JSON, nullable=True)
    ptl_id = Column(UUID(as_uuid=True), ForeignKey("snaap_ribbonway_portals.ptl_id"), nullable=False)
    # Relationships
    portal = relationship("RibbonwayPortal", back_populates="docks")


class Pod(Base):
    """SQLAlchemy model for snaap_pods table"""

    __tablename__ = "snaap_pods"
    pod_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pod_created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    pod_name = Column(String, nullable=True)
    pod_description = Column(Text, nullable=True)
    pod_configuration = Column(String, nullable=True)
    pod_current_status = Column(String, nullable=True)
    pod_current_location = Column(String, nullable=False)
    rbn_id = Column(UUID(as_uuid=True), ForeignKey("snaap_ribbonways.rbn_id"), nullable=True)
    # Relationships
    ribbonway = relationship("Ribbonway", back_populates="pods")
    ride_requests = relationship("RideRequest", back_populates="pod")


class Rider(Base):
    """SQLAlchemy model for snaap_riders table"""

    __tablename__ = "snaap_riders"
    rdr_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rdr_created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    rdr_first_name = Column(String, nullable=True)
    rdr_last_name = Column(String, nullable=True)
    rdr_email = Column(String, nullable=True)
    rdr_phone_number = Column(String, nullable=True)
    rdr_password = Column(String, nullable=True)
    rdr_avatar = Column(String, nullable=True)
    # Relationships
    ride_requests = relationship("RideRequest", back_populates="rider")


class RideRequest(Base):
    """SQLAlchemy model for snaap_ride_requests table"""

    __tablename__ = "snaap_ride_requests"
    rde_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rde_created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    rde_boarding_time = Column(TIMESTAMP(timezone=True), nullable=True)
    rde_dropoff_time = Column(TIMESTAMP(timezone=True), nullable=True)
    rde_amount_charged = Column(Numeric, nullable=True)
    rde_currency_charged = Column(String, nullable=True)
    rdr_id = Column(UUID(as_uuid=True), ForeignKey("snaap_riders.rdr_id"), nullable=True)
    ptl_id = Column(UUID(as_uuid=True), ForeignKey("snaap_ribbonway_portals.ptl_id"), nullable=True)
    pod_id = Column(UUID(as_uuid=True), ForeignKey("snaap_pods.pod_id"), nullable=True)
    rde_starting_dock = Column(UUID(as_uuid=True), nullable=True)
    rde_ending_dock = Column(UUID(as_uuid=True), nullable=True)
    # Relationships
    rider = relationship("Rider", back_populates="ride_requests")
    portal = relationship("RibbonwayPortal", back_populates="ride_requests")
    pod = relationship("Pod", back_populates="ride_requests")
