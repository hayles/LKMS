#!/usr/bin/env python3
"""Manage customer shipping SKUs and inventory levels."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

DEFAULT_DB = Path("customer_sku_inventory.json")


def load_db(path: Path) -> dict[str, dict[str, dict[str, int]]]:
    if not path.exists():
        return {"customers": {}}
    data = json.loads(path.read_text(encoding="utf-8"))
    if "customers" not in data:
        data["customers"] = {}
    return data


def save_db(path: Path, data: dict[str, dict[str, dict[str, int]]]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def ensure_customer(data: dict[str, dict[str, dict[str, int]]], customer: str) -> None:
    data.setdefault("customers", {})
    data["customers"].setdefault(customer, {})


def validate_stock(stock: int) -> None:
    if stock < 0:
        raise SystemExit("库存数量不能小于 0")


def add_sku(
    data: dict[str, dict[str, dict[str, int]]],
    customer: str,
    sku: str,
    stock: int,
) -> None:
    validate_stock(stock)
    ensure_customer(data, customer)
    if sku in data["customers"][customer]:
        raise SystemExit(f"SKU 已存在: {sku}")
    data["customers"][customer][sku] = stock


def remove_sku(
    data: dict[str, dict[str, dict[str, int]]], customer: str, sku: str
) -> None:
    ensure_customer(data, customer)
    if sku not in data["customers"][customer]:
        raise SystemExit(f"SKU 不存在: {sku}")
    del data["customers"][customer][sku]


def set_stock(
    data: dict[str, dict[str, dict[str, int]]],
    customer: str,
    sku: str,
    stock: int,
) -> None:
    validate_stock(stock)
    ensure_customer(data, customer)
    if sku not in data["customers"][customer]:
        raise SystemExit(f"SKU 不存在: {sku}")
    data["customers"][customer][sku] = stock


def list_customers(data: dict[str, dict[str, dict[str, int]]]) -> None:
    for customer in sorted(data.get("customers", {})):
        print(customer)


def list_skus(
    data: dict[str, dict[str, dict[str, int]]], customer: str | None
) -> None:
    customers = data.get("customers", {})
    if customer:
        ensure_customer(data, customer)
        skus = customers.get(customer, {})
        print(f"{customer}:")
        for sku, stock in sorted(skus.items()):
            print(f"  {sku}: {stock}")
        return

    for cust_name, skus in sorted(customers.items()):
        print(f"{cust_name}:")
        for sku, stock in sorted(skus.items()):
            print(f"  {sku}: {stock}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage customer SKUs and inventory")
    parser.add_argument(
        "--db",
        type=Path,
        default=DEFAULT_DB,
        help=f"JSON database path (default: {DEFAULT_DB})",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("list-customers", help="List all customers")

    list_parser = sub.add_parser("list", help="List SKUs and stock")
    list_parser.add_argument("--customer", help="Filter by customer name")

    add_parser = sub.add_parser("add-sku", help="Add a SKU for a customer")
    add_parser.add_argument("customer", help="Customer name")
    add_parser.add_argument("sku", help="SKU name")
    add_parser.add_argument("stock", type=int, help="Initial stock (>=0)")

    remove_parser = sub.add_parser("remove-sku", help="Remove a SKU")
    remove_parser.add_argument("customer", help="Customer name")
    remove_parser.add_argument("sku", help="SKU name")

    set_parser = sub.add_parser("set-stock", help="Set stock for a SKU")
    set_parser.add_argument("customer", help="Customer name")
    set_parser.add_argument("sku", help="SKU name")
    set_parser.add_argument("stock", type=int, help="Stock (>=0)")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    data = load_db(args.db)

    if args.command == "list-customers":
        list_customers(data)
        return
    if args.command == "list":
        list_skus(data, args.customer)
        return
    if args.command == "add-sku":
        add_sku(data, args.customer, args.sku, args.stock)
    elif args.command == "remove-sku":
        remove_sku(data, args.customer, args.sku)
    elif args.command == "set-stock":
        set_stock(data, args.customer, args.sku, args.stock)

    save_db(args.db, data)


if __name__ == "__main__":
    main()
