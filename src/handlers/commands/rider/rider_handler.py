"""
Rider command and query handlers have been moved to their canonical locations.

Query:   src/handlers/queries/rider/get_rider_profile.py  → GetRiderProfileQueryHandler
Command: src/handlers/commands/rider/update_rider_profile.py → UpdateRiderProfileCommandHandler
Service: src/core/services/rider.py  → RiderService (get_or_provision, update_profile)
"""
