from vehicle import Cargo, Route, Vehicle
import argparse

CARGO_START_LOCATION = 'Factory'


def cli_app():
    parser = argparse.ArgumentParser()
    parser.add_argument("cargo_destinations")
    args = parser.parse_args()

    result = transport(args.cargo_destinations)

    print(result)


def transport(cargo_destinations):

    cargos = _construct_cargos(cargo_destinations)
    vehicles = _construct_vehicles()

    time = _transport_core(cargos, vehicles)

    return time


def _construct_cargos(cargo_destinations):
    return [Cargo(CARGO_START_LOCATION, destination) for destination in cargo_destinations]


def _construct_vehicles():

    route_factory_to_port = Route(CARGO_START_LOCATION, 'Port', 1, downstream_destinations=['A'])
    route_factory_to_b = Route(CARGO_START_LOCATION, 'B', 5)
    route_port_to_a = Route('Port', 'A', 4)

    vehicles = [
        Vehicle(routes=[
                    route_factory_to_port,
                    route_factory_to_b
                ]),
        Vehicle(routes=[
                    route_factory_to_port,
                    route_factory_to_b
                ]),
        Vehicle(routes=[
                    route_port_to_a
                ]),
    ]

    return vehicles


def _transport_core(cargos, vehicles):
    time = 0
    while not _all_cargo_delivered(cargos):
        _step(cargos, vehicles)
        time += 1
    return time


def _all_cargo_delivered(cargos):
    return all(cargo.location is cargo.destination for cargo in cargos)


def _step(cargos, vehicles):
    """Synchronize vehicle activities to implement simulation assumptions:
     - drop and load does not take time
     - moving does take time
     - cargo is only moved by one vehicle during one step"""

    for vehicle in vehicles:
        vehicle.load(cargos)

    for vehicle in vehicles:
        vehicle.move()

    for vehicle in vehicles:
        vehicle.drop_cargo()


if __name__ == "__main__":
    cli_app()
