# We will focus on the following set of requirements while designing the parking lot:

# The parking lot should have multiple floors where customers can park their cars.
# The parking lot should have multiple entry and exit points.
# Customers can collect a parking ticket from the entry points and can pay the parking fee at the exit points on their way out.
# Customers can pay via both cash and credit cards.
# The system should not allow more vehicles than the maximum capacity of the parking lot. If the parking is full,
# the system should be able to show a message at the entrance panel and on the parking display board on the ground floor.
# Each parking floor will have many parking spots. The system should support multiple types of parking spots 
# such as Compact, Large, Handicapped, Motorcycle, etc.
# The system should support parking for different types of vehicles like car, truck, van, motorcycle, etc.
# Each parking floor should have a display board showing any free parking spot for each spot type.
# The system should support a per-hour parking fee model. For example, customers have to pay $4 for the first hour,
# $3.5 for the second and third hours, and $2.5 for all the remaining hours.


class ParkingSpot:
    def __init__(self, spot_type, is_occupied, spot_id):
        self.spot_type = spot_type
        self.is_occupied = is_occupied
        self.parking_spot_id = spot_id
        self.ticket = None
    
    def get_is_occupied(self):
        return self.is_occupied

    def set_is_occupied(self,is_occupied, ticket):
        self.ticket = ticket
        self.is_occupied = is_occupied

class Floor:
    def __init__(self, floor, parking_spot_locations):
        self.floor = floor
        self.parking_spots = self.parking_spots_init(parking_spot_locations)
        self.empty_slots = {}
        self.empty_count = 0
    
    def parking_spots_init(self, parking_spot_locations):
        spot_number = 1
        parking_spots = {}
        for val in parking_spot_locations:
            parking_spot = ParkingSpot(spot_type= val, spot_id = f'{self.floor}-{spot_number}') 
            if val not in self.empty_slots:
                self.empty_slots[val] = 0
            self.empty_slots[val] += 1
            self.empty_count += 1
            parking_spots[spot_number] = parking_spot
        return parking_spots
            
    def park(self, parking_spot, ticket, spot_type):
        floor, spot_number = parking_spot.split('-')
        parking_spot = self.parking_spots[spot_number]
        parking_spot.set_is_occupied(True, ticket)
        if not self.empty_count:
            raise Exception('No Spot to park')
        self.empty_count -= 1
        self.empty_slots[spot_type] -= 1
        return spot_number

    def unpark(self, parking_spot, ticket):
        floor, spot_number = parking_spot.split('-')
        parking_spot = self.parking_spots[spot_number]
        if parking_spot.ticket == ticket:
            parking_spot.set_is_occupied(False, None)
            self.empty_count += 1
            self.empty_slots[parking_spot.spot_type] +=1 
            return True
        return False
    
class ParkingManager:
    def __init__(self, parking_strategy, number_of_floors, parking_spot_locations, address, parking_manager_id, ticket_manager):
        self.address = address
        self.parking_manager_id = parking_manager_id
        self.parking_stratergy = parking_strategy
        self.parking_spot_locations = parking_spot_locations
        self.floors = self.initialize_floors(number_of_floors, parking_spot_locations)
        self.search_manager = {}
        self.ticketManager = ticket_manager
        self.total_count = 0
    
    def initialize_floors(self, number_of_floors, parking_spot_locations):
        floors = []
        for floor in number_of_floors:
            Floor(floor, parking_spot_locations=parking_spot_locations[floor])
            floors.append(floor)
            self.total_count  += 1
        return floor
    
    def park(self, parking_strategy,spot_type, license):
        if parking_strategy == 'find_first':
            for floor in self.floors:
                if floor.empty_count and len(floor.empty_slots[spot_type]):
                    for spot in floor.parking_spots:
                        if spot.spot_type == spot_type and not spot.get_is_occupied():
                            ticket  = self.ticket_manager.generate_ticket(spot.parking_spot_id)
                            floor.park(spot, ticket, spot_type)
                            self.total_count -= 1
                            self.search_manager[license] = ticket
    
    def unpark(self, ticket, license):
        if not ticket:
            ticket = self.search_manager[license]
        spot = ticket.parking_spot_id
        floor_number, spot = spot.split('-')
        floor = self.floors[floor_number]
        floor.unpark(spot, ticket)
        bill = self.ticketManager.generate_bill()
        self.total_count += 1
        del self.search_manager[license]
        return bill
        
class TicketManager:
    pass
    
    
                            
                    
        
        
        
    
        
        
        
        
        
    
    
