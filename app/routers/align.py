from fastapi import APIRouter, File, Request, UploadFile

from app.services.fasta import parse_and_validate
from app.services.reference import get_reference
from app.services.alignment import align_sequences
from app.services.upload import read_single_fasta_upload
from app.schemas import AlignResponse, AlignmentInfoModel, VariantModel

router = APIRouter()


@router.post("/align", response_model=AlignResponse)
async def align_endpoint(request: Request, file: UploadFile = File(...)):
    content = await read_single_fasta_upload(request, file)

    # validasi dulu sebelum diproses
    sequence_id, sequence = parse_and_validate(content)

    # ambil referensi yang sudah di-load waktu startup
    reference_id, ref_seq = get_reference()

    # jalankan alignment dan ekstrak varian
    aln_info, variants = align_sequences(ref_seq, sequence)

    aln_model = AlignmentInfoModel(**aln_info)
    variant_models = [VariantModel(**v) for v in variants]

    return AlignResponse(
        sequence_id=sequence_id,
        reference_id=reference_id,
        alignment=aln_model,
        variants=variant_models
    )
