import unittest
from unittest.mock import patch

import pandas as pd
from sqlalchemy import create_engine, inspect, text

from services.data_uploader import DataUploader


class DataUploaderTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite://")

    def tearDown(self):
        self.engine.dispose()

    def test_replaces_existing_table_with_processed_columns_and_data(self):
        pd.DataFrame({"old_column": [1]}).to_sql(
            "violencia", self.engine, index=False
        )

        DataUploader(self.engine).upload_all(
            {"violencia": pd.DataFrame({"fecha": ["2026-01-01"]})}
        )

        self.assertEqual(
            [
                column["name"]
                for column in inspect(self.engine).get_columns("violencia")
            ],
            ["fecha"],
        )
        with self.engine.connect() as connection:
            self.assertEqual(
                connection.execute(
                    text("SELECT fecha FROM violencia")
                ).scalar(),
                "2026-01-01",
            )

    def test_failed_dataset_rolls_back_the_entire_batch(self):
        pd.DataFrame({"value": ["old-first"]}).to_sql(
            "first", self.engine, index=False
        )
        pd.DataFrame({"value": ["old-second"]}).to_sql(
            "second", self.engine, index=False
        )

        def fail_after_writing_second(dataframe, name, *args, **kwargs):
            connection = kwargs["con"]
            connection.execute(text(f"DELETE FROM {name}"))
            connection.execute(
                text(f"INSERT INTO {name} (value) VALUES (:value)"),
                {"value": dataframe.iloc[0]["value"]},
            )
            if name == "second":
                raise RuntimeError("Simulated database error")

        with patch.object(
            pd.DataFrame, "to_sql", new=fail_after_writing_second
        ):
            with self.assertRaisesRegex(RuntimeError, "Simulated database error"):
                DataUploader(self.engine).upload_all(
                    {
                        "first": pd.DataFrame({"value": ["new-first"]}),
                        "second": pd.DataFrame({"value": ["new-second"]}),
                    }
                )

        with self.engine.connect() as connection:
            self.assertEqual(
                connection.execute(text("SELECT value FROM first")).scalar(),
                "old-first",
            )
            self.assertEqual(
                connection.execute(text("SELECT value FROM second")).scalar(),
                "old-second",
            )

    def test_rejects_invalid_table_name_before_opening_transaction(self):
        with self.assertRaisesRegex(ValueError, "Nombre de tabla no válido"):
            DataUploader(self.engine).upload_all(
                {"invalid-name": pd.DataFrame({"value": [1]})}
            )

        self.assertEqual(inspect(self.engine).get_table_names(), [])


if __name__ == "__main__":
    unittest.main()
