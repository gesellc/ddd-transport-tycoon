from dataclasses import dataclass, field


@dataclass
class Cargo:
    location: str
    destination: str


@dataclass
class Route:
    home: str
    destination: str
    distance: int
    downstream_destinations: list = field(default_factory=list)


class Vehicle:

    def __init__(self, routes):
        self._routes = routes
        self._cargo = None
        self._current_route = None
        self._next_location = self._routes[0].home
        self._time_until_arrival = 0

    @property
    def _destinations(self):
        destinations = []
        for route in self._routes:
            destinations.append(route.destination)
            destinations.extend(route.downstream_destinations)
        return destinations

    @property
    def _location(self):
        if self._time_until_arrival is 0:
            return self._next_location
        return None

    def load(self, cargos):
        if self._is_ready_to_load_cargo():
            viable_cargo = self._get_viable_cargo(cargos)
            if viable_cargo:
                self._really_load(viable_cargo)
                self._start_trip_to_cargo_destination()

    def _is_ready_to_load_cargo(self):
        return self._location and not self._cargo

    def _get_viable_cargo(self, cargos):
        for cargo in cargos:
            if cargo.location is self._location and cargo.destination in self._destinations:
                return cargo
        return None

    def _really_load(self, cargo):
        self._cargo = cargo
        self._cargo.location = None

    def _start_trip_to_cargo_destination(self):
        self._current_route = self._find_route_for(self._cargo)
        self._next_location = self._current_route.destination
        self._time_until_arrival = self._current_route.distance

    def _find_route_for(self, cargo):
        for route in self._routes:
            if cargo.destination in [route.destination] + route.downstream_destinations:
                return route

    def move(self):
        self._time_until_arrival = max(self._time_until_arrival - 1, 0)

    def drop_cargo(self):
        if self._is_ready_to_drop_cargo():
            self._really_drop_cargo()
            self._start_trip_back_to_base()

    def _is_ready_to_drop_cargo(self):
        return self._cargo and self._location is self._current_route.destination

    def _really_drop_cargo(self):
        self._cargo.location = self._location
        self._cargo = None

    def _start_trip_back_to_base(self):
        self._next_location = self._current_route.home
        self._time_until_arrival = self._current_route.distance