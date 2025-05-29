from pydantic import BaseModel, Field


class TableAtPostgres(BaseModel):
    table_schema: str = Field(description="Schema which the table belongs to.")
    table_name: str = Field(description="Table name")