from seat_reservation_system.seat_store import SeatStore
from seat_reservation_system.seats import SEAT_IDS

# 0610_예약 코드 확인 및 취소, 재발급 추가_sj
HELP_TEXT = """Commands:
list                            - List all seats
reserve <seat_id> <name>        - Reserve a seat
cancel <seat_id> [name]         - Cancel a reservation
cancel_code <booking_code>      - Cancel a reservation by booking code

status <seat_id>                - Show seat status
check <booking_code>            - Show reservation by booking code
reissue <booking_code> <name>   - Reissue a booking code
stats                           - Show summary stats
help                            - Show this help
exit                            - Exit the program"""


def run_cli():
    store = SeatStore(SEAT_IDS)
    print("Seat Reservation System CLI")
    print("Type 'help' to see available commands.")
    while True:
        try:
            raw = input("seat> ").strip()
        except EOFError:
            print()
            break
        if not raw:
            continue

        parts = raw.split()
        command, args = parts[0].lower(), parts[1:]
        if command in {"exit", "quit"}:
            break
        if command == "help":
            print(HELP_TEXT)
            continue
        try:
            if command == "list":
                for seat_id, name in store.list_seats():
                    _print_seat(seat_id, name)

            # 0610_예약 안내 정보에 예약 코드 추가_sj
            elif command == "reserve":
                _require_args(command, args, 2)
                seat_id, name, code = store.reserve(int(args[0]), args[1])
                _print_seat(seat_id, name)
                print(f"Booking code: {code}")  # 예약 코드 출력

            elif command == "cancel":
                _require_args(command, args, 1)
                name = args[1] if len(args) > 1 else None
                seat_id, name = store.cancel(int(args[0]), name)
                _print_seat(seat_id, name)

            # 0610_예약 코드 확인 명령어 추가_sj
            elif command == "check":
                _require_args(command, args, 1)
                seat_id, name = store.check_code(args[0])
                _print_seat(seat_id, name)

            elif command == "status":
                _require_args(command, args, 1)
                seat_id, name = store.status(int(args[0]))
                _print_seat(seat_id, name)

            # 0610_예약 코드 취소 명령어 추가_sj
            elif command == "cancel_code":
                _require_args(command, args, 1)
                seat_id, name = store.cancel_by_code(args[0])
                _print_seat(seat_id, name)

            # 0610_예약 코드 재발급 명령어 추가_sj
            elif command == "reissue":
                _require_args(command, args, 2)
                seat_id, name, new_code = store.reissue_code(args[0], args[1])
                _print_seat(seat_id, name)
                print(f"New booking code: {new_code}")

            elif command == "stats":
                stats = store.stats()
                print(
                    "Total: {total}, Reserved: {reserved}, Available: {available}".format(
                        **stats
                    )
                )
            else:
                print("Unknown command. Type 'help' for commands.")
        except ValueError as exc:
            print(f"Error: {exc}")


def _print_seat(seat_id, name):
    label = f"reserved by {name}" if name else "available"
    print(f"Seat {seat_id}: {label}")


def _require_args(command, args, count):
    if len(args) < count:
        raise ValueError(f"Usage: {command} requires {count} argument(s).")
