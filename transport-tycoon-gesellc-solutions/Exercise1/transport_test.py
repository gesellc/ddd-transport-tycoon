from unittest import TestCase

from transport import CARGO_START_LOCATION, _construct_cargos, _transport_core, transport
from vehicle import Cargo, Route, Vehicle


class TransportExercise1Test(TestCase):

    def test_A(self):
        self.assertEqual(5, transport('A'))

    def test_AB(self):
        self.assertEqual(5, transport('AB'))

    def test_BB(self):
        self.assertEqual(5, transport('BB'))

    def test_ABB(self):
        self.assertEqual(7, transport('ABB'))

    def test_AABABBAB(self):
        self.assertEqual(29, transport('AABABBAB'))


class TransportCoreSingleVehicleTest(TestCase):

    def setUp(self):
        route_to_a = Route(CARGO_START_LOCATION, 'A', 5)
        route_to_b = Route(CARGO_START_LOCATION, 'B', 5)
        route_to_c = Route(CARGO_START_LOCATION, 'C', 5)

        self.vehicles = [
            Vehicle(routes=[
                        route_to_a,
                        route_to_b,
                        route_to_c,
                    ]),
        ]

    def test_one_trip_delivery(self):
        cargos = _construct_cargos('A')
        self.assertEqual(5, _transport_core(cargos, self.vehicles))

    def test_multiple_cargos_same_route(self):
        cargos = _construct_cargos('AA')
        self.assertEqual(15, _transport_core(cargos, self.vehicles))

    def test_multiple_cargos_multiple_routes(self):
        cargos = _construct_cargos('ABC')
        self.assertEqual(25, _transport_core(cargos, self.vehicles))


class TransportCoreDifferentRouteDistancesTest(TestCase):

    def setUp(self):
        route_to_port = Route(CARGO_START_LOCATION, 'Port', 1)
        route_to_b = Route(CARGO_START_LOCATION, 'B', 5)

        self.vehicles = [
            Vehicle(routes=[
                        route_to_port,
                        route_to_b,
                    ]),
        ]

    def test_one_vehicle_different_route_distances(self):
        cargos = [
            Cargo(CARGO_START_LOCATION, 'Port'),
            Cargo(CARGO_START_LOCATION, 'Port'),
            Cargo(CARGO_START_LOCATION, 'B'),
        ]
        self.assertEqual(9, _transport_core(cargos, self.vehicles))


class TransportCoreMultipleVehiclesTest(TestCase):

    def setUp(self) -> None:
        route_to_a = Route(CARGO_START_LOCATION, 'A', 5)
        route_to_b = Route(CARGO_START_LOCATION, 'B', 5)
        route_to_c = Route(CARGO_START_LOCATION, 'C', 5)

        self.vehicles = [
            Vehicle(routes=[
                        route_to_a,
                        route_to_b,
                    ]),
            Vehicle(routes=[
                        route_to_a,
                        route_to_b,
                    ]),
            Vehicle(routes=[
                        route_to_c,
                    ]),
        ]

    def test_cargo_stays_at_start_position(self):
        cargos = [
            Cargo(CARGO_START_LOCATION, CARGO_START_LOCATION)
        ]
        self.assertEqual(0, _transport_core(cargos, self.vehicles))

    def test_cargo_already_delivered(self):
        cargos = [
            Cargo('A', 'A')
        ]
        self.assertEqual(0, _transport_core(cargos, self.vehicles))

    def test_one_trip_delivery(self):
        cargos = _construct_cargos('A')
        self.assertEqual(5, _transport_core(cargos, self.vehicles))

    def test_multiple_cargos_same_route(self):
        cargos = _construct_cargos('AA')
        self.assertEqual(5, _transport_core(cargos, self.vehicles))

    def test_multiple_cargos_multiple_routes(self):
        cargos = _construct_cargos('ABCC')
        self.assertEqual(15, _transport_core(cargos, self.vehicles))
