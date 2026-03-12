"""
Ride command and query handlers have been moved to their canonical CQRS locations.

Commands:
  src/handlers/commands/ride/request_ride.py   → RequestRideCommandHandler
  src/handlers/commands/ride/assign_pod.py     → AssignPodCommandHandler
  src/handlers/commands/ride/board_ride.py     → BoardRideCommandHandler
  src/handlers/commands/ride/complete_ride.py  → CompleteRideCommandHandler
  src/handlers/commands/ride/cancel_ride.py    → CancelRideCommandHandler

Queries:
  src/handlers/queries/ride/get_ride.py        → GetRideQueryHandler
  src/handlers/queries/ride/list_my_rides.py   → ListMyRidesQueryHandler

Service:
  src/core/services/ride.py                    → RideService (all business rules)
"""

