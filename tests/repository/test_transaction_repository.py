import pandas as pd
import pytest

from src.repository.transaction_repository import TransactionRepository

def test_repository_creates_file_if_not_exists(tmp_path):
    file_path = tmp_path / "transactions.csv"

    repo = TransactionRepository(str(file_path))

    assert file_path.exists()

    df = pd.read_csv(file_path)
    assert list(df.columns) == ["transaction_id", "amount", "currency"]
    assert df.empty

def test_save_appends_transactions(tmp_path):
    file_path = tmp_path / "transactions.csv"
    repo = TransactionRepository(str(file_path))

    df1 = pd.DataFrame({
        "transaction_id": ["tx-1"],
        "amount": [100.0],
        "currency": ["USD"]
    })

    df2 = pd.DataFrame({
        "transaction_id": ["tx-2"],
        "amount": [50.0],
        "currency": ["EUR"]
    })

    repo.save(df1)
    repo.save(df2)

    result = pd.read_csv(file_path)

    assert len(result) == 2
    assert result.iloc[0]["transaction_id"] == "tx-1"
    assert result.iloc[1]["transaction_id"] == "tx-2"


def test_find_all_returns_all_transactions(tmp_path):
    file_path = tmp_path / "transactions.csv"
    repo = TransactionRepository(str(file_path))

    df = pd.DataFrame({
        "transaction_id": ["tx-1", "tx-2"],
        "amount": [100.0, 200.0],
        "currency": ["USD", "EUR"]
    })

    repo.save(df)

    result = repo.find_all()

    pd.testing.assert_frame_equal(result, df)

def test_save_empty_dataframe_does_not_change_file(tmp_path):
    file_path = tmp_path / "transactions.csv"
    repo = TransactionRepository(str(file_path))

    empty_df = pd.DataFrame(columns=["transaction_id", "amount", "currency"])
    repo.save(empty_df)

    result = repo.find_all()

    assert result.empty


def test_save_without_schema_validation(tmp_path):
    file_path = tmp_path / "transactions.csv"
    repo = TransactionRepository(str(file_path))

    df = pd.DataFrame({
        "transaction_id": ["tx-1"]
    })

    repo.save(df)

    result = repo.find_all()

    assert "transaction_id" in result.columns
    assert len(result) == 1


def test_save_without_schema_validation(tmp_path):
    file_path = tmp_path / "transactions.csv"
    repo = TransactionRepository(str(file_path))

    df = pd.DataFrame({
        "transaction_id": ["tx-1"]
    })

    repo.save(df)

    result = repo.find_all()

    assert "transaction_id" in result.columns
    assert len(result) == 1


