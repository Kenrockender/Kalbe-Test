from typing import List
from pydantic import BaseModel, Field


# model untuk satu varian (SNV, insertion, atau deletion)
class VariantModel(BaseModel):
    position: int = Field(description="posisi di referensi, 1-based")
    ref: str = Field(description="basa referensi, '-' kalau insertion")
    alt: str = Field(description="basa alternatif, '-' kalau deletion")
    type: str = Field(description="tipe varian: SNV, insertion, atau deletion")


# info hasil alignment
class AlignmentInfoModel(BaseModel):
    score: float = Field(description="skor alignment")
    identity: float = Field(description="proporsi basa yang cocok (0-1)")
    reference_aligned: str = Field(description="referensi dengan gap")
    query_aligned: str = Field(description="query dengan gap")


# response untuk endpoint /api/align
class AlignResponse(BaseModel):
    sequence_id: str
    reference_id: str
    alignment: AlignmentInfoModel
    variants: List[VariantModel]


# hasil translasi DNA ke protein
class TranslationModel(BaseModel):
    protein: str = Field(description="urutan asam amino")
    length: int = Field(description="panjang protein")
    has_stop_codon: bool = Field(description="True kalau ketemu stop codon")


# response untuk endpoint /api/translate
class TranslateResponse(BaseModel):
    sequence_id: str
    frame: int = Field(description="reading frame yang dipakai (1, 2, atau 3)")
    protein: str
    length: int
    has_stop_codon: bool


# format response kalau ada error
class ErrorResponse(BaseModel):
    error: str = Field(description="kode error")
    detail: str = Field(description="pesan error yang bisa dibaca manusia")
