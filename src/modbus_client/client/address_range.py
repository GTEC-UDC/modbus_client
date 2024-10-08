from dataclasses import dataclass
from typing import Optional, Sequence


@dataclass
class AddressRange:
    address: int
    count: int

    @property
    def first_address(self) -> int:
        return self.address

    @property
    def last_address(self) -> int:
        return self.address + self.count - 1


def merge_address_ranges(
    registers: Sequence[AddressRange], allow_holes: bool, max_read_size: int
) -> list[AddressRange]:
    buckets: list[AddressRange] = []
    cur_rng: Optional[AddressRange] = None

    for register in sorted(registers, key=lambda x: (x.address, -x.count)):
        rng = AddressRange(register.address, register.count)

        if (
            cur_rng is not None
            and rng.first_address >= cur_rng.first_address
            and rng.last_address <= cur_rng.last_address
        ):
            continue

        if cur_rng is None:
            cur_rng = rng
        else:
            diff = rng.first_address - cur_rng.last_address
            to_add = rng.last_address - cur_rng.last_address
            if diff > 1:
                if allow_holes:
                    if cur_rng.count + to_add <= max_read_size:
                        cur_rng.count += to_add
                    else:
                        buckets.append(cur_rng)
                        cur_rng = rng
                else:
                    buckets.append(cur_rng)
                    cur_rng = rng
            else:
                cur_rng.count += to_add

    if cur_rng is not None:
        buckets.append(cur_rng)

    return buckets


__all__ = ["AddressRange", "merge_address_ranges"]
