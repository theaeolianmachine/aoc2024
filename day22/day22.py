from collections import Counter


def parse_input() -> list[int]:
    with open("day22/day22.txt") as fobj:
        return [int(s) for s in fobj.read().strip().split("\n")]


def calculate_next_secret(secret: int) -> int:
    new_secret = secret

    # Step 1
    calc = new_secret * 64
    new_secret ^= calc
    new_secret = new_secret % 16777216

    # Step 2
    calc = new_secret // 32
    new_secret ^= calc
    new_secret = new_secret % 16777216

    # Step 3
    calc = new_secret * 2048
    new_secret ^= calc
    new_secret = new_secret % 16777216

    return new_secret


def part_one(secrets: list[int]):
    nth_secret: dict[int, int] = {}
    for secret in secrets:
        new_secret = secret
        for i in range(2000):
            new_secret = calculate_next_secret(new_secret)
        nth_secret[secret] = new_secret

    return sum(nth_secret.values())


def gen_secret_prices(secret: int) -> list[int]:
    secret_chain: list[int] = [secret % 10]
    new_secret = secret
    for i in range(2000):
        new_secret = calculate_next_secret(new_secret)
        secret_chain.append((new_secret % 10))
    return secret_chain


def gen_price_changes(secret_chain: list[int]) -> list[int]:
    price_changes: list[int] = []
    for i in range(1, len(secret_chain)):
        price_changes.append(secret_chain[i] - secret_chain[i - 1])

    return price_changes


def part_two(secrets: list[int]):
    secret_chains: dict[int, list[int]] = {}
    secret_price_changes: dict[int, list[int]] = {}
    price_sequences: dict[int, dict[tuple[int, ...], int]] = {}
    for secret in secrets:
        secret_chains[secret] = gen_secret_prices(secret)
        price_changes = gen_price_changes(secret_chains[secret])
        secret_price_changes[secret] = price_changes
        for i in range(0, len(price_changes) - 3):
            sequences = price_sequences.setdefault(secret, {})
            seq = tuple(price_changes[i : i + 4])
            if seq not in sequences:
                sequences[seq] = i + 4  # Index of the end of the price change

    all_sequences = set()
    for ps in price_sequences:
        ps_keys = price_sequences[ps].keys()
        all_sequences.update(ps_keys)

    seq_counts: Counter[tuple[int, ...]] = Counter()
    for seq in all_sequences:
        for ps in price_sequences:
            if seq in price_sequences[ps]:
                seq_counts[seq] = seq_counts.setdefault(seq, 0) + 1

    _, most_common = seq_counts.most_common(1)[0]
    most_common_sequences = {
        seq for seq in seq_counts if seq_counts[seq] == most_common
    }

    bananas: dict[tuple[int, ...], int] = {}
    for seq in most_common_sequences:
        num_bananas = 0
        for secret in price_sequences:
            if seq in price_sequences[secret]:
                index = price_sequences[secret][seq]
                num_bananas += secret_chains[secret][index]
        bananas[seq] = num_bananas
        # print(f"{seq}: {num_bananas}")

    return max(bananas.values())


def main():
    secrets = parse_input()
    print("Part One:")
    print(part_one(secrets))
    print("Part Two:")
    print(part_two(secrets))


if __name__ == "__main__":
    main()
