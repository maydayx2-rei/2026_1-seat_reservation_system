class SeatStore:
    def __init__(self, seat_ids):
        self._seats = {seat_id: None for seat_id in seat_ids}

        # 0610_예약 확인 데이터 추가_sj
        self._seat_codes: dict[str, int] = {}  # 추가: code -> seat_id
        self._counter = 0                       # 추가: 코드 일련번호


   # 0610_코드 생성 기능 추가_sj
    def _generate_code(self, seat_id: int) -> str:
        self._counter += 1
        return f"SRS-{seat_id:03d}-{self._counter:03d}"
    
    def list_seats(self):
        return self._seats.items()

    def reserve(self, seat_id, name):
        current = self._get(seat_id)
        if current is not None:
            raise ValueError("Seat is already reserved.")
        
        # 0610_예약 시 예약 코드 추가_sj
        code = self._generate_code(seat_id) #코드 생성 호출
        self._seats[seat_id] = name
        self._seat_codes[code] = seat_id
        return seat_id, name, code

    def cancel(self, seat_id, name=None):
        current = self._get(seat_id)
        if current is None:
            raise ValueError("Seat is not reserved.")
        if name and current != name:
            raise ValueError("Name does not match the reservation.")
        
        # 0610_예약 취소 시 예약 코드 삭제 처리_sj
        self._seat_codes = {c: s for c, s in self._seat_codes.items() if s != seat_id}

        self._seats[seat_id] = None
        return seat_id, None

    # 0610_코드로 예약 조회 추가_sj
    def check_code(self, code: str):
        if code not in self._seat_codes:
            raise ValueError("Invalid booking code.")
        seat_id = self._seat_codes[code]
        return seat_id, self._seats[seat_id]
    
    def status(self, seat_id):
        return seat_id, self._get(seat_id)

    def stats(self):
        reserved = sum(1 for name in self._seats.values() if name)
        total = len(self._seats)
        return {"total": total, "reserved": reserved, "available": total - reserved}

    def _get(self, seat_id):
        if seat_id not in self._seats:
            raise ValueError("Seat does not exist.")
        return self._seats[seat_id]

